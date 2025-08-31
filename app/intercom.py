import aiohttp
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)


class IntercomClient:
    """Client for interacting with Intercom API"""

    def __init__(self):
        self.base_url = "https://api.intercom.io"
        self.access_token = settings.INTERCOM_ACCESS_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a conversation by ID"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/conversations/{conversation_id}"
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(
                            f"Failed to get conversation {conversation_id}: {response.status}")
                        return None
        except Exception as e:
            logger.error(
                f"Error getting conversation {conversation_id}: {str(e)}")
            return None

    async def reply_to_conversation(self, conversation_id: str, message: str, message_type: str = "comment") -> bool:
        """Reply to a conversation with a message"""
        try:
            payload = {
                "message_type": message_type,
                "body": message
            }

            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/conversations/{conversation_id}/reply"
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status in [200, 201]:
                        logger.info(
                            f"Successfully replied to conversation {conversation_id}")
                        return True
                    else:
                        logger.error(
                            f"Failed to reply to conversation {conversation_id}: {response.status}")
                        return False
        except Exception as e:
            logger.error(
                f"Error replying to conversation {conversation_id}: {str(e)}")
            return False

    async def assign_conversation(self, conversation_id: str, admin_id: str) -> bool:
        """Assign a conversation to a specific admin"""
        try:
            payload = {
                "admin_id": admin_id
            }

            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/conversations/{conversation_id}/reply"
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status in [200, 201]:
                        logger.info(
                            f"Successfully assigned conversation {conversation_id} to admin {admin_id}")
                        return True
                    else:
                        logger.error(
                            f"Failed to assign conversation {conversation_id}: {response.status}")
                        return False
        except Exception as e:
            logger.error(
                f"Error assigning conversation {conversation_id}: {str(e)}")
            return False

    async def close_conversation(self, conversation_id: str) -> bool:
        """Close a conversation"""
        try:
            payload = {
                "conversation_id": conversation_id
            }

            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/conversations/{conversation_id}/reply"
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status in [200, 201]:
                        logger.info(
                            f"Successfully closed conversation {conversation_id}")
                        return True
                    else:
                        logger.error(
                            f"Failed to close conversation {conversation_id}: {response.status}")
                        return False
        except Exception as e:
            logger.error(
                f"Error closing conversation {conversation_id}: {str(e)}")
            return False

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information by ID"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/users/{user_id}"
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(
                            f"Failed to get user {user_id}: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {str(e)}")
            return None

    async def update_user(self, user_id: str, attributes: Dict[str, Any]) -> bool:
        """Update user attributes"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/users/{user_id}"
                async with session.put(url, headers=self.headers, json=attributes) as response:
                    if response.status in [200, 201]:
                        logger.info(f"Successfully updated user {user_id}")
                        return True
                    else:
                        logger.error(
                            f"Failed to update user {user_id}: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return False
