import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Vector database for storing and retrieving knowledge base documents"""

    def __init__(self):
        self.db_path = Path("data/chroma_db")
        self.db_path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )

        # Initialize LangChain vector store
        self.vector_store = Chroma(
            client=self.client,
            collection_name="knowledge_base",
            embedding_function=self.embeddings
        )

        logger.info(f"Vector store initialized at {self.db_path}")

    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Add documents to the vector store

        Args:
            documents: List of documents with 'content', 'metadata', and 'id' fields

        Returns:
            bool: True if successful
        """
        try:
            texts = [doc['content'] for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            ids = [doc.get('id', f"doc_{i}")
                   for i, doc in enumerate(documents)]

            # Add to vector store
            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids
            )

            logger.info(f"Added {len(documents)} documents to vector store")
            return True

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            return False

    def search_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents with scores
        """
        try:
            # Search the vector store
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k
            )

            # Format results
            documents = []
            for doc, score in results:
                documents.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': float(score)
                })

            logger.info(
                f"Found {len(documents)} relevant documents for query: {query[:50]}...")
            return documents

        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []

    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the vector store

        Args:
            document_id: ID of the document to delete

        Returns:
            bool: True if successful
        """
        try:
            # Get collection
            collection = self.client.get_collection("knowledge_base")
            collection.delete(ids=[document_id])

            logger.info(f"Deleted document with ID: {document_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False

    def update_document(self, document_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """
        Update a document in the vector store

        Args:
            document_id: ID of the document to update
            content: New content
            metadata: New metadata

        Returns:
            bool: True if successful
        """
        try:
            # Delete old document
            self.delete_document(document_id)

            # Add updated document
            self.add_documents([{
                'id': document_id,
                'content': content,
                'metadata': metadata
            }])

            logger.info(f"Updated document with ID: {document_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating document {document_id}: {str(e)}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store

        Returns:
            Dictionary with collection statistics
        """
        try:
            collection = self.client.get_collection("knowledge_base")
            count = collection.count()

            return {
                'total_documents': count,
                'collection_name': 'knowledge_base',
                'embedding_model': 'text-embedding-3-small'
            }

        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {}

    def reset_collection(self) -> bool:
        """
        Reset the entire collection (delete all documents)

        Returns:
            bool: True if successful
        """
        try:
            self.client.delete_collection("knowledge_base")
            self.client.create_collection("knowledge_base")

            logger.info("Reset knowledge base collection")
            return True

        except Exception as e:
            logger.error(f"Error resetting collection: {str(e)}")
            return False


# Global vector store instance
vector_store = VectorStore()
