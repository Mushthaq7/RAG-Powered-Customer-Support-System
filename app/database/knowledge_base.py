import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from app.database.vector_store import vector_store

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Knowledge base management for support documents and FAQs"""

    def __init__(self):
        self.data_path = Path("data/knowledge_base")
        self.data_path.mkdir(parents=True, exist_ok=True)

        # Initialize with sample data if empty
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Initialize knowledge base with sample support documents"""
        try:
            stats = vector_store.get_collection_stats()
            if stats.get('total_documents', 0) == 0:
                logger.info("Initializing knowledge base with sample data...")
                self._add_sample_documents()
        except Exception as e:
            logger.error(f"Error initializing sample data: {str(e)}")

    def _add_sample_documents(self):
        """Add sample support documents to the knowledge base"""
        sample_documents = [
            {
                'id': 'password_reset',
                'content': """
                How to Reset Your Password:
                
                1. Go to the login page
                2. Click "Forgot Password" link
                3. Enter your email address
                4. Check your email for reset instructions
                5. Click the reset link in the email
                6. Enter your new password
                7. Confirm your new password
                
                If you don't receive the email, check your spam folder.
                """,
                'metadata': {
                    'category': 'account',
                    'topic': 'password_reset',
                    'priority': 'high',
                    'created_at': datetime.now().isoformat()
                }
            },
            {
                'id': 'account_creation',
                'content': """
                Creating a New Account:
                
                1. Visit our website homepage
                2. Click "Sign Up" or "Create Account"
                3. Fill in your personal information:
                   - Full name
                   - Email address
                   - Password (minimum 8 characters)
                4. Accept terms and conditions
                5. Click "Create Account"
                6. Verify your email address
                
                You'll receive a confirmation email to activate your account.
                """,
                'metadata': {
                    'category': 'account',
                    'topic': 'account_creation',
                    'priority': 'high',
                    'created_at': datetime.now().isoformat()
                }
            },
            {
                'id': 'billing_help',
                'content': """
                Billing and Payment Information:
                
                Payment Methods Accepted:
                - Credit cards (Visa, MasterCard, American Express)
                - PayPal
                - Bank transfers (for annual plans)
                
                Billing Cycle:
                - Monthly plans: Charged on the same date each month
                - Annual plans: Charged once per year with 2 months free
                
                To update payment information:
                1. Log into your account
                2. Go to Settings > Billing
                3. Click "Update Payment Method"
                4. Enter new payment details
                
                For billing questions, contact our support team.
                """,
                'metadata': {
                    'category': 'billing',
                    'topic': 'payment_methods',
                    'priority': 'medium',
                    'created_at': datetime.now().isoformat()
                }
            },
            {
                'id': 'refund_policy',
                'content': """
                Refund Policy:
                
                We offer a 30-day money-back guarantee for all new subscriptions.
                
                Refund Eligibility:
                - Must be within 30 days of initial purchase
                - Account must be in good standing
                - No refunds for partial months
                
                To request a refund:
                1. Contact customer support
                2. Provide your account details
                3. Explain the reason for refund
                4. Allow 3-5 business days for processing
                
                Refunds are processed to the original payment method.
                """,
                'metadata': {
                    'category': 'billing',
                    'topic': 'refunds',
                    'priority': 'medium',
                    'created_at': datetime.now().isoformat()
                }
            },
            {
                'id': 'technical_support',
                'content': """
                Technical Support:
                
                Common Issues and Solutions:
                
                1. Can't log in:
                   - Clear browser cache and cookies
                   - Try incognito/private browsing mode
                   - Reset your password
                
                2. Slow performance:
                   - Check your internet connection
                   - Close unnecessary browser tabs
                   - Try a different browser
                
                3. Features not working:
                   - Update your browser to the latest version
                   - Disable browser extensions temporarily
                   - Contact support with specific error messages
                
                For urgent technical issues, contact our 24/7 support team.
                """,
                'metadata': {
                    'category': 'technical',
                    'topic': 'troubleshooting',
                    'priority': 'high',
                    'created_at': datetime.now().isoformat()
                }
            }
        ]

        success = vector_store.add_documents(sample_documents)
        if success:
            logger.info(
                f"Added {len(sample_documents)} sample documents to knowledge base")
        else:
            logger.error("Failed to add sample documents")

    def add_document(self, content: str, metadata: Dict[str, Any], document_id: Optional[str] = None) -> bool:
        """
        Add a new document to the knowledge base

        Args:
            content: Document content
            metadata: Document metadata
            document_id: Optional document ID

        Returns:
            bool: True if successful
        """
        try:
            if not document_id:
                document_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Add creation timestamp if not present
            if 'created_at' not in metadata:
                metadata['created_at'] = datetime.now().isoformat()

            document = {
                'id': document_id,
                'content': content,
                'metadata': metadata
            }

            success = vector_store.add_documents([document])
            if success:
                logger.info(f"Added document {document_id} to knowledge base")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            return False

    def search_knowledge_base(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant information

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        try:
            documents = vector_store.search_documents(query, k)
            return documents
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return []

    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific document by ID

        Args:
            document_id: Document ID

        Returns:
            Document data or None if not found
        """
        try:
            # Search for the specific document
            documents = vector_store.search_documents(f"id:{document_id}", k=1)
            if documents:
                return documents[0]
            return None
        except Exception as e:
            logger.error(f"Error getting document {document_id}: {str(e)}")
            return None

    def update_document(self, document_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """
        Update an existing document

        Args:
            document_id: Document ID
            content: New content
            metadata: Updated metadata

        Returns:
            bool: True if successful
        """
        try:
            # Add update timestamp
            metadata['updated_at'] = datetime.now().isoformat()

            success = vector_store.update_document(
                document_id, content, metadata)
            if success:
                logger.info(f"Updated document {document_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error updating document {document_id}: {str(e)}")
            return False

    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the knowledge base

        Args:
            document_id: Document ID to delete

        Returns:
            bool: True if successful
        """
        try:
            success = vector_store.delete_document(document_id)
            if success:
                logger.info(f"Deleted document {document_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False

    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics

        Returns:
            Dictionary with knowledge base statistics
        """
        try:
            stats = vector_store.get_collection_stats()
            return {
                'total_documents': stats.get('total_documents', 0),
                'collection_name': stats.get('collection_name', 'knowledge_base'),
                'embedding_model': stats.get('embedding_model', 'text-embedding-3-small'),
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting knowledge base stats: {str(e)}")
            return {}

    def export_knowledge_base(self, file_path: str) -> bool:
        """
        Export knowledge base to JSON file

        Args:
            file_path: Path to export file

        Returns:
            bool: True if successful
        """
        try:
            # Get all documents (search with empty query to get all)
            documents = vector_store.search_documents("", k=1000)

            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_documents': len(documents),
                'documents': documents
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Exported knowledge base to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting knowledge base: {str(e)}")
            return False


# Global knowledge base instance
knowledge_base = KnowledgeBase()
