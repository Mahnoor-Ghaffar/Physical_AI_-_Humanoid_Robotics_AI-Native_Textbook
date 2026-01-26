"""
Embedding generator for the RAG chatbot
Handles text embedding generation for retrieval-augmented generation
"""
from typing import List
import numpy as np
import hashlib


class EmbeddingGenerator:
    """
    Generates mock embeddings for text (for testing purposes)
    In a real implementation, this would use a proper embedding model
    """
    def __init__(self, model_name: str = "mock-embedding-model"):
        """
        Initialize the embedding generator

        Args:
            model_name: Name of the model (just for identification)
        """
        self.model_name = model_name
        print(f"Initialized mock embedding generator: {model_name}")

    def encode(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate mock embeddings for a list of texts

        Args:
            texts: List of texts to encode

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            # Create a deterministic mock embedding based on the text hash
            text_hash = hashlib.sha256(text.encode()).hexdigest()

            # Convert hex to numbers and create a vector
            vector = []
            for i in range(0, len(text_hash), 2):
                byte_val = int(text_hash[i:i+2], 16)
                normalized_val = (byte_val / 255.0) * 2 - 1  # Normalize to [-1, 1]
                vector.append(normalized_val)

            # Ensure consistent size (truncate or pad to 384 dimensions)
            if len(vector) > 384:
                vector = vector[:384]
            else:
                vector.extend([0.0] * (384 - len(vector)))

            embeddings.append(np.array(vector, dtype=np.float32))

        return embeddings

    def encode_single(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text

        Args:
            text: Text to encode

        Returns:
            Embedding vector
        """
        return self.encode([text])[0]


# Global instance
embedding_generator = EmbeddingGenerator()


def get_embedding_generator() -> EmbeddingGenerator:
    """
    Get the global embedding generator instance
    """
    return embedding_generator