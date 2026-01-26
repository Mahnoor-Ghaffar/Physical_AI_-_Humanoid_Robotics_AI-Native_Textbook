"""
Document Retriever for the RAG chatbot
Provides a consistent interface for retrieving documents from the vector database
"""
from typing import List, Dict, Tuple
import sys
import os
sys.path.append(os.path.dirname(__file__))
from retrieve import retrieve_content, Config


class DocumentRetriever:
    """
    A wrapper class for document retrieval functionality
    """
    def __init__(self):
        # Initialize the config to ensure we can connect to the database
        try:
            self.config = Config()
            self.documents = []  # Placeholder - in a real implementation this would come from the database
        except Exception as e:
            print(f"Warning: Could not initialize DocumentRetriever: {e}")
            self.config = None
            self.documents = []

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Retrieve documents based on a query

        Args:
            query: The search query text
            top_k: Number of results to return

        Returns:
            List of tuples containing (document_dict, similarity_score)
        """
        if self.config is None:
            # Return mock results if config failed to initialize
            return [({"id": 1, "content": f"Mock content for query: {query}", "source": "mock_source"}, 0.8)]

        # Use the retrieve_content function from retrieve.py
        results = retrieve_content(query, top_k)

        # Convert results to the expected format (document_dict, similarity_score)
        formatted_results = []
        for result in results:
            doc_dict = {
                "id": result.get('chunk_id', 'unknown'),
                "content": result.get('content', ''),
                "source": result.get('source_url', ''),
                "category": result.get('metadata', {}).get('category')
            }
            similarity_score = result.get('similarity_score', 0.0)
            formatted_results.append((doc_dict, similarity_score))

        return formatted_results

    def get_all_categories(self) -> List[str]:
        """
        Get all document categories

        Returns:
            List of category names
        """
        # This would normally query the database for all categories
        # For now, return an empty list or mock data
        return []

    def add_document(self, document: Dict):
        """
        Add a document to the knowledge base

        Args:
            document: Document dictionary with id, content, source, etc.
        """
        # This would normally add the document to the vector database
        # For now, just store in memory
        self.documents.append(document)


# Global instance
_document_retriever = None


def get_document_retriever() -> DocumentRetriever:
    """
    Get the global document retriever instance

    Returns:
        DocumentRetriever: The global instance
    """
    global _document_retriever
    if _document_retriever is None:
        _document_retriever = DocumentRetriever()
    return _document_retriever