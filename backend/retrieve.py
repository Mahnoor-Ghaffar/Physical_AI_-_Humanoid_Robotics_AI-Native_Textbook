"""
Retrieval module for the RAG chatbot
Handles retrieval of relevant documents from the knowledge base
"""
from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .embedding_generator import embedding_generator
import json
import os


class DocumentRetriever:
    """
    Retrieves relevant documents based on semantic similarity
    """
    def __init__(self, knowledge_base_path: str = None):
        """
        Initialize the document retriever

        Args:
            knowledge_base_path: Path to the knowledge base file (optional)
        """
        self.documents = []
        self.embeddings = []

        if knowledge_base_path and os.path.exists(knowledge_base_path):
            self.load_knowledge_base(knowledge_base_path)
        else:
            # Initialize with default knowledge base
            self._initialize_default_knowledge_base()

    def _initialize_default_knowledge_base(self):
        """
        Initialize with default knowledge base content
        """
        default_docs = [
            {
                "id": 1,
                "content": "AI Native applications leverage artificial intelligence as a core component of their architecture, integrating ML models directly into the application lifecycle.",
                "source": "Module 1",
                "category": "ai-native"
            },
            {
                "id": 2,
                "content": "Digital twins are virtual replicas of physical systems that enable real-time monitoring, simulation, and optimization of real-world assets.",
                "source": "Module 2",
                "category": "digital-twin"
            },
            {
                "id": 3,
                "content": "Isaac Sim is NVIDIA's robotics simulation platform that provides high-fidelity physics simulation for robot development and testing.",
                "source": "Module 3",
                "category": "simulation"
            },
            {
                "id": 4,
                "content": "ROS2 (Robot Operating System 2) provides a flexible framework for writing robot software with distributed computation and real-time control.",
                "source": "Module 4",
                "category": "ros2"
            },
            {
                "id": 5,
                "content": "Large Language Models (LLMs) are transformer-based neural networks trained on vast amounts of text data to understand and generate human-like language.",
                "source": "Module 5",
                "category": "llm"
            },
            {
                "id": 6,
                "content": "Retrieval Augmented Generation (RAG) combines information retrieval with text generation to produce more accurate and context-aware responses.",
                "source": "Module 6",
                "category": "rag"
            },
            {
                "id": 7,
                "content": "Vector databases store and index high-dimensional vectors for efficient similarity search, crucial for RAG systems.",
                "source": "Module 7",
                "category": "vector-db"
            },
            {
                "id": 8,
                "content": "Prompt engineering is the practice of crafting effective prompts to guide large language models to produce desired outputs.",
                "source": "Module 8",
                "category": "prompt-engineering"
            }
        ]

        self.documents = default_docs
        self._generate_embeddings()

    def load_knowledge_base(self, knowledge_base_path: str):
        """
        Load knowledge base from file

        Args:
            knowledge_base_path: Path to the knowledge base JSON file
        """
        with open(knowledge_base_path, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
        self._generate_embeddings()

    def save_knowledge_base(self, knowledge_base_path: str):
        """
        Save knowledge base to file

        Args:
            knowledge_base_path: Path to save the knowledge base JSON file
        """
        with open(knowledge_base_path, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=2)

    def _generate_embeddings(self):
        """
        Generate embeddings for all documents
        """
        contents = [doc["content"] for doc in self.documents]
        self.embeddings = embedding_generator.encode(contents)

    def add_document(self, doc: Dict):
        """
        Add a document to the knowledge base

        Args:
            doc: Document dictionary with id, content, source, and category
        """
        self.documents.append(doc)
        embedding = embedding_generator.encode_single(doc["content"])
        self.embeddings.append(embedding)

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Retrieve relevant documents for a query

        Args:
            query: Query string
            top_k: Number of top results to return

        Returns:
            List of tuples containing (document, similarity_score)
        """
        query_embedding = embedding_generator.encode_single(query)

        # Calculate cosine similarity
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]

        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Only return documents with reasonable similarity
                results.append((self.documents[idx], float(similarities[idx])))

        return results

    def get_all_categories(self) -> List[str]:
        """
        Get all categories in the knowledge base

        Returns:
            List of unique categories
        """
        categories = set()
        for doc in self.documents:
            if "category" in doc:
                categories.add(doc["category"])
        return list(categories)


# Global instance
document_retriever = DocumentRetriever()


def get_document_retriever() -> DocumentRetriever:
    """
    Get the global document retriever instance
    """
    return document_retriever