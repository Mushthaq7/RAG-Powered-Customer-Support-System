import os
import logging
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from app.config import settings
from app.rag.retriever import rag_retriever

logger = logging.getLogger(__name__)


class AIService:
    """Service for handling AI-powered responses using OpenAI"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE

        # System prompt for customer support
        self.system_prompt = """You are a helpful and professional customer support AI assistant. Your role is to:

1. Provide accurate, helpful, and friendly responses to customer inquiries
2. Understand customer issues and provide relevant solutions
3. Escalate complex issues when necessary
4. Maintain a professional and empathetic tone
5. Ask clarifying questions when needed
6. Provide step-by-step instructions when appropriate
7. Acknowledge customer concerns and show understanding

Key guidelines:
- Always be polite and professional
- Provide specific, actionable advice
- If you don't know something, say so and offer to connect them with a human agent
- Keep responses concise but comprehensive
- Use clear, simple language
- Show empathy for customer frustrations
- If the issue requires human intervention, clearly state this

Remember: You're here to help customers feel heard and supported while providing practical solutions to their problems."""

    async def generate_response(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate an AI response to a user message with RAG enhancement"""
        try:
            # Build the conversation context
            messages = [{"role": "system", "content": self.system_prompt}]

            # Add context if provided
            if context:
                context_message = self._build_context_message(context)
                messages.append({"role": "system", "content": context_message})

            # Use RAG to retrieve relevant information
            rag_context = await self._get_rag_context(user_message)
            if rag_context:
                messages.append({"role": "system", "content": rag_context})

            # Add user message
            messages.append({"role": "user", "content": user_message})

            # Generate response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            ai_response = response.choices[0].message.content
            logger.info(
                f"Generated AI response for message: {user_message[:100]}...")

            return ai_response

        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return "I apologize, but I'm experiencing technical difficulties right now. Please try again in a moment or contact our human support team for immediate assistance."

    async def analyze_sentiment(self, message: str) -> Dict[str, Any]:
        """Analyze the sentiment of a customer message"""
        try:
            prompt = f"""Analyze the sentiment of this customer message and provide insights:

Message: "{message}"

Please provide:
1. Sentiment (positive, negative, neutral)
2. Urgency level (low, medium, high)
3. Key emotions detected
4. Whether human escalation is recommended (true/false)
5. Brief reasoning

Format as JSON."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )

            # Parse the response (in production, you'd want proper JSON parsing)
            return {"analysis": response.choices[0].message.content}

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"error": "Failed to analyze sentiment"}

    async def categorize_issue(self, message: str) -> str:
        """Categorize the type of customer issue"""
        try:
            prompt = f"""Categorize this customer support issue into one of these categories:

- Technical Support
- Billing/Account
- Product Questions
- Feature Requests
- Bug Reports
- General Inquiry
- Complaints
- Other

Message: "{message}"

Respond with only the category name."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a customer support issue categorizer. Respond with only the category name."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.1
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error categorizing issue: {str(e)}")
            return "General Inquiry"

    async def generate_follow_up_questions(self, message: str) -> list:
        """Generate follow-up questions to better understand the customer's issue"""
        try:
            prompt = f"""Based on this customer message, generate 2-3 follow-up questions that would help clarify their issue:

Message: "{message}"

Generate questions that are:
- Specific and relevant
- Helpful for understanding the problem
- Professional and friendly

Respond with a JSON array of questions."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a customer support specialist. Respond with a JSON array of follow-up questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )

            # In production, you'd parse this as JSON
            return [response.choices[0].message.content]

        except Exception as e:
            logger.error(f"Error generating follow-up questions: {str(e)}")
            return []

    def _build_context_message(self, context: Dict[str, Any]) -> str:
        """Build a context message from conversation history and user info"""
        context_parts = []

        if context.get("user_info"):
            user_info = context["user_info"]
            context_parts.append(
                f"Customer Info: {user_info.get('name', 'Unknown')} - {user_info.get('email', 'No email')}")

        if context.get("conversation_history"):
            history = context["conversation_history"]
            context_parts.append(
                f"Previous messages in this conversation: {len(history)}")

        if context.get("issue_category"):
            context_parts.append(
                f"Issue Category: {context['issue_category']}")

        if context.get("sentiment"):
            context_parts.append(f"Sentiment: {context['sentiment']}")

        return "Context: " + " | ".join(context_parts) if context_parts else ""

    async def should_escalate_to_human(self, message: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Determine if the conversation should be escalated to a human agent"""
        try:
            escalation_keywords = [
                "speak to someone", "human", "agent", "representative", "manager",
                "supervisor", "escalate", "urgent", "emergency", "complaint",
                "unhappy", "frustrated", "angry", "disappointed", "not working",
                "broken", "refund", "cancel", "delete account"
            ]

            message_lower = message.lower()

            # Check for escalation keywords
            if any(keyword in message_lower for keyword in escalation_keywords):
                return True

            # Use AI to analyze if escalation is needed
            prompt = f"""Should this customer support conversation be escalated to a human agent?

Message: "{message}"

Consider:
- Complexity of the issue
- Customer's emotional state
- Whether the issue requires human intervention
- Urgency of the situation

Respond with only 'YES' or 'NO'."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a customer support escalation specialist. Respond with only 'YES' or 'NO'."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )

            return response.choices[0].message.content.strip().upper() == "YES"

        except Exception as e:
            logger.error(f"Error determining escalation: {str(e)}")
            return False

    async def _get_rag_context(self, user_message: str) -> Optional[str]:
        """
        Get RAG context for enhanced responses

        Args:
            user_message: User's message

        Returns:
            RAG context string or None
        """
        try:
            # Check if RAG should be used for this query
            if not rag_retriever.should_use_rag(user_message):
                return None

            # Enhance the query for better retrieval
            enhanced_query = rag_retriever.enhance_query(user_message)

            # Retrieve relevant context
            rag_result = rag_retriever.retrieve_context(enhanced_query)

            if rag_result.get('context') and rag_result.get('retrieved_count', 0) > 0:
                logger.info(
                    f"Retrieved {rag_result['retrieved_count']} documents for RAG context")
                return rag_result['context']

            return None

        except Exception as e:
            logger.error(f"Error getting RAG context: {str(e)}")
            return None
