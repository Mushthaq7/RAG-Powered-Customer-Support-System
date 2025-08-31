import hashlib
import hmac
import json
import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def validate_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """
    Validate Intercom webhook signature

    Args:
        payload: Raw request body
        signature: X-Hub-Signature header value
        secret: Webhook secret from Intercom

    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        if not signature or not secret:
            logger.warning(
                "Missing signature or secret for webhook validation")
            return False

        # Extract the signature value (format: sha256=hash)
        if signature.startswith('sha256='):
            signature = signature[7:]

        # Calculate expected signature
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Compare signatures
        return hmac.compare_digest(signature, expected_signature)

    except Exception as e:
        logger.error(f"Error validating webhook signature: {str(e)}")
        return False


def sanitize_message(message: str) -> str:
    """
    Sanitize user message for safe processing

    Args:
        message: Raw user message

    Returns:
        str: Sanitized message
    """
    if not message:
        return ""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', message)

    # Limit length
    if len(sanitized) > 10000:
        sanitized = sanitized[:10000] + "..."

    return sanitized.strip()


def extract_user_info_from_webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract user information from Intercom webhook data

    Args:
        data: Webhook payload data

    Returns:
        Dict containing user information
    """
    user_info = {}

    try:
        # Extract from conversation data
        if 'conversation' in data:
            conversation = data['conversation']
            if 'user' in conversation:
                user = conversation['user']
                user_info.update({
                    'user_id': user.get('id'),
                    'email': user.get('email'),
                    'name': user.get('name'),
                    'created_at': user.get('created_at')
                })

        # Extract from conversation message data
        if 'conversation_message' in data:
            message = data['conversation_message']
            if 'user' in message:
                user = message['user']
                user_info.update({
                    'user_id': user.get('id'),
                    'email': user.get('email'),
                    'name': user.get('name')
                })

        # Extract from user data directly
        if 'user' in data:
            user = data['user']
            user_info.update({
                'user_id': user.get('id'),
                'email': user.get('email'),
                'name': user.get('name'),
                'created_at': user.get('created_at')
            })

    except Exception as e:
        logger.error(f"Error extracting user info: {str(e)}")

    return user_info


def format_timestamp(timestamp: int) -> str:
    """
    Format Unix timestamp to readable string

    Args:
        timestamp: Unix timestamp

    Returns:
        str: Formatted timestamp
    """
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception as e:
        logger.error(f"Error formatting timestamp {timestamp}: {str(e)}")
        return str(timestamp)


def categorize_urgency(message: str) -> str:
    """
    Simple urgency categorization based on keywords

    Args:
        message: User message

    Returns:
        str: Urgency level (low, medium, high, critical)
    """
    message_lower = message.lower()

    # Critical keywords
    critical_keywords = ['emergency', 'urgent',
                         'broken', 'down', 'not working', 'error']
    if any(keyword in message_lower for keyword in critical_keywords):
        return 'critical'

    # High urgency keywords
    high_keywords = ['help', 'issue', 'problem',
                     'frustrated', 'angry', 'unhappy']
    if any(keyword in message_lower for keyword in high_keywords):
        return 'high'

    # Medium urgency keywords
    medium_keywords = ['question', 'how', 'what', 'when', 'where', 'why']
    if any(keyword in message_lower for keyword in medium_keywords):
        return 'medium'

    return 'low'


def extract_contact_info(message: str) -> Dict[str, str]:
    """
    Extract contact information from message

    Args:
        message: User message

    Returns:
        Dict containing extracted contact info
    """
    contact_info = {}

    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, message)
    if emails:
        contact_info['email'] = emails[0]

    # Phone pattern (basic)
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    phones = re.findall(phone_pattern, message)
    if phones:
        contact_info['phone'] = phones[0]

    return contact_info


def truncate_message(message: str, max_length: int = 500) -> str:
    """
    Truncate message to specified length

    Args:
        message: Original message
        max_length: Maximum allowed length

    Returns:
        str: Truncated message
    """
    if len(message) <= max_length:
        return message

    # Try to truncate at word boundary
    truncated = message[:max_length]
    last_space = truncated.rfind(' ')

    if last_space > max_length * 0.8:  # If we can find a space in the last 20%
        return truncated[:last_space] + "..."

    return truncated + "..."


def is_business_hours() -> bool:
    """
    Check if current time is within business hours (9 AM - 6 PM UTC)

    Returns:
        bool: True if within business hours
    """
    now = datetime.now(timezone.utc)
    hour = now.hour

    # Business hours: 9 AM - 6 PM UTC
    return 9 <= hour < 18


def should_auto_escalate(message: str, user_info: Dict[str, Any]) -> bool:
    """
    Determine if conversation should be auto-escalated

    Args:
        message: User message
        user_info: User information

    Returns:
        bool: True if should escalate
    """
    # Check for escalation keywords
    escalation_keywords = [
        'speak to someone', 'human', 'agent', 'representative', 'manager',
        'supervisor', 'escalate', 'urgent', 'emergency', 'complaint'
    ]

    message_lower = message.lower()
    if any(keyword in message_lower for keyword in escalation_keywords):
        return True

    # Check urgency
    urgency = categorize_urgency(message)
    if urgency in ['critical', 'high']:
        return True

    # Check if outside business hours
    if not is_business_hours():
        return True

    return False


def format_response_for_intercom(response: str) -> str:
    """
    Format AI response for Intercom

    Args:
        response: Raw AI response

    Returns:
        str: Formatted response
    """
    # Ensure response is not too long
    if len(response) > 4000:
        response = truncate_message(response, 4000)

    # Add signature if response is from AI
    if response and not response.endswith("(AI Assistant)"):
        response += "\n\n---\n*This response was generated by our AI assistant. If you need further assistance, please let us know!*"

    return response


def log_conversation_event(event_type: str, data: Dict[str, Any]):
    """
    Log conversation events for monitoring

    Args:
        event_type: Type of event
        data: Event data
    """
    log_data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'event_type': event_type,
        'data': data
    }

    logger.info(f"Conversation Event: {json.dumps(log_data)}")


def validate_intercom_webhook_url(url: str) -> bool:
    """
    Validate Intercom webhook URL format

    Args:
        url: Webhook URL

    Returns:
        bool: True if valid format
    """
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            parsed.netloc and
            parsed.path
        )
    except Exception:
        return False
