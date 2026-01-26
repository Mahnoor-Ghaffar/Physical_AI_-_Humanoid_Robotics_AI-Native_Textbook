"""
Mock module to bypass dependency issues for testing
"""
from typing import List, Dict, Optional
import os
from datetime import datetime

class Config:
    def __init__(self):
        # Mock config that doesn't require actual API keys
        self.cohere_api_key = os.getenv("COHERE_API_KEY", "mock-key")
        self.qdrant_url = os.getenv("QDRANT_URL", "mock-url")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY", "mock-key")
        self.qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "mock-collection")

def retrieve_content(query: str, top_k: int = 5):
    """
    Mock function to retrieve content from the database
    """
    # Return mock results
    mock_results = []
    for i in range(min(top_k, 3)):  # Return max 3 mock results
        mock_results.append({
            'content': f'This is mock content related to your query: {query}',
            'source_url': f'mock://source-{i+1}',
            'chunk_id': f'mock-chunk-{i+1}',
            'similarity_score': 0.8 - (i * 0.1),  # Decreasing similarity
            'position': i,
            'length': len(query) * 10,
            'created_at': datetime.now().isoformat(),
            'metadata': {'category': 'mock-category'}
        })
    return mock_results