"""
Test script to verify the FastAPI RAG integration works correctly.
"""

import asyncio
import json
import requests

def test_api():
    print("Testing FastAPI RAG Integration...")

    # Test the health endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        print("Make sure the API server is running with: uvicorn api:app --reload --port 8000")
        return

    # Test the chat endpoint used by the floating chat widget
    try:
        chat_data = {
            "messages": [
                {"role": "user", "content": "What is this book about?"}
            ],
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(
            "https://mahnoor09-deploy-hack.hf.space/chat",
            headers={"Content-Type": "application/json"},
            json=chat_data
        )

        print(f"Chat response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Chat Response: {result}")
        else:
            print(f"Chat Error: {response.text}")

    except Exception as e:
        print(f"Chat test failed: {e}")

    # Test the query endpoint
    try:
        query_data = {
            "query": "What is this book about?",
            "timeout": 30
        }

        response = requests.post(
            "https://mahnoor09-deploy-hack.hf.space/query",
            headers={"Content-Type": "application/json"},
            json=query_data
        )

        print(f"Query response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Query Response: {result}")
        else:
            print(f"Query Error: {response.text}")

    except Exception as e:
        print(f"Query test failed: {e}")

if __name__ == "__main__":
    test_api()