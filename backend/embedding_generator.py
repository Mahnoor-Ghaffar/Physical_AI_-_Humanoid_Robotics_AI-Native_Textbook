"""
Embedding generator for the RAG chatbot
Handles text embedding generation for retrieval-augmented generation
"""
from typing import List
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch


class EmbeddingGenerator:
    """
    Generates embeddings for text using pre-trained models
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator

        Args:
            model_name: Name of the pre-trained model to use
        """
        self.model_name = model_name
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
        except Exception as e:
            print(f"Warning: Could not load {model_name}. Using mock embeddings.")
            print(f"Error: {e}")
            self.tokenizer = None
            self.model = None

    def encode(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for a list of texts

        Args:
            texts: List of texts to encode

        Returns:
            List of embedding vectors
        """
        if self.model is None or self.tokenizer is None:
            # Return mock embeddings if model couldn't be loaded
            return [np.random.rand(384).astype(np.float32) for _ in texts]

        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use mean pooling to get sentence embedding
                embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
                embeddings.append(embedding.numpy().astype(np.float32))

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