import logging
from typing import List, Dict, Any, Optional
from app.database.knowledge_base import knowledge_base
from app.utils import sanitize_message

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieval-Augmented Generation retriever for enhanced AI responses"""

    def __init__(self):
        self.knowledge_base = knowledge_base
        self.default_k = 3  # Default number of documents to retrieve

    def retrieve_context(self, query: str, k: Optional[int] = None) -> Dict[str, Any]:
        """
        Retrieve relevant context for a user query

        Args:
            query: User's question or message
            k: Number of documents to retrieve (default: 3)

        Returns:
            Dictionary containing retrieved context and metadata
        """
        try:
            if k is None:
                k = self.default_k

            # Sanitize the query
            sanitized_query = sanitize_message(query)

            # Search knowledge base for relevant documents
            documents = self.knowledge_base.search_knowledge_base(
                sanitized_query, k)

            # Build context from retrieved documents
            context = self._build_context(documents, query)

            logger.info(
                f"Retrieved {len(documents)} documents for query: {query[:50]}...")

            return {
                'context': context,
                'documents': documents,
                'query': sanitized_query,
                'retrieved_count': len(documents)
            }

        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return {
                'context': "",
                'documents': [],
                'query': query,
                'retrieved_count': 0,
                'error': str(e)
            }

    def _build_context(self, documents: List[Dict[str, Any]], query: str) -> str:
        """
        Build context string from retrieved documents

        Args:
            documents: List of retrieved documents
            query: Original user query

        Returns:
            Formatted context string
        """
        if not documents:
            return ""

        context_parts = []
        context_parts.append(
            "Based on our knowledge base, here is relevant information:")

        for i, doc in enumerate(documents, 1):
            content = doc.get('content', '').strip()
            metadata = doc.get('metadata', {})
            score = doc.get('score', 0)

            # Only include documents with good relevance scores
            if score < 0.8:  # Adjust threshold as needed
                continue

            # Add document content
            context_parts.append(f"\n{i}. {content}")

            # Add metadata if available
            if metadata.get('category'):
                context_parts.append(f"   Category: {metadata['category']}")
            if metadata.get('topic'):
                context_parts.append(f"   Topic: {metadata['topic']}")

        context_parts.append(f"\nUser Question: {query}")
        context_parts.append(
            "\nPlease provide a helpful response based on the information above.")

        return "\n".join(context_parts)

    def get_relevant_categories(self, query: str) -> List[str]:
        """
        Get relevant categories for a query

        Args:
            query: User query

        Returns:
            List of relevant categories
        """
        try:
            documents = self.knowledge_base.search_knowledge_base(query, k=5)
            categories = set()

            for doc in documents:
                metadata = doc.get('metadata', {})
                if 'category' in metadata:
                    categories.add(metadata['category'])

            return list(categories)

        except Exception as e:
            logger.error(f"Error getting relevant categories: {str(e)}")
            return []

    def get_similar_questions(self, query: str, k: int = 3) -> List[str]:
        """
        Get similar questions from the knowledge base

        Args:
            query: User query
            k: Number of similar questions to return

        Returns:
            List of similar questions
        """
        try:
            documents = self.knowledge_base.search_knowledge_base(query, k=k)
            questions = []

            for doc in documents:
                content = doc.get('content', '')
                # Extract potential questions from content
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.endswith('?') and len(line) > 10:
                        questions.append(line)

            return questions[:k]

        except Exception as e:
            logger.error(f"Error getting similar questions: {str(e)}")
            return []

    def should_use_rag(self, query: str) -> bool:
        """
        Determine if RAG should be used for this query

        Args:
            query: User query

        Returns:
            bool: True if RAG should be used
        """
        # Keywords that suggest the user needs specific information
        rag_keywords = [
            'how', 'what', 'when', 'where', 'why', 'which',
            'password', 'reset', 'account', 'billing', 'payment',
            'refund', 'cancel', 'delete', 'update', 'change',
            'problem', 'issue', 'error', 'help', 'support',
            'policy', 'terms', 'privacy', 'security'
        ]

        query_lower = query.lower()

        # Check if query contains RAG keywords
        for keyword in rag_keywords:
            if keyword in query_lower:
                return True

        # Check if query is a question
        if query.strip().endswith('?'):
            return True

        return False

    def enhance_query(self, query: str) -> str:
        """
        Enhance the query for better retrieval

        Args:
            query: Original query

        Returns:
            Enhanced query
        """
        # Add context words to improve retrieval
        enhanced_parts = [query]

        # Add category hints based on query content
        query_lower = query.lower()

        if any(word in query_lower for word in ['password', 'login', 'account']):
            enhanced_parts.append("account management")

        if any(word in query_lower for word in ['billing', 'payment', 'refund', 'money']):
            enhanced_parts.append("billing payment")

        if any(word in query_lower for word in ['error', 'problem', 'issue', 'broken']):
            enhanced_parts.append("technical support")

        return " ".join(enhanced_parts)


# Global RAG retriever instance
rag_retriever = RAGRetriever()
