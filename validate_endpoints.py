"""
Simple test to validate FastAPI endpoints are working correctly
"""
import requests
import json

def test_endpoints():
    print("Testing FastAPI endpoints...")

    # Test the root endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/")
        print(f"[OK] Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"[FAIL] Root endpoint failed: {e}")

    # Test the health endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/health")
        print(f"[OK] Health endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"[FAIL] Health endpoint failed: {e}")

    # Test the stats endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/stats")
        print(f"[OK] Stats endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"[FAIL] Stats endpoint failed: {e}")

    # Test the categories endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/documents/categories")
        print(f"[OK] Categories endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"[FAIL] Categories endpoint failed: {e}")

    # Test the query endpoint with a simple request
    try:
        query_data = {
            "query": "What is this book about?",
            "top_k": 3
        }
        response = requests.post(
            "https://mahnoor09-deploy-hack.hf.space/query",
            headers={"Content-Type": "application/json"},
            json=query_data
        )
        print(f"[OK] Query endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Response keys: {list(result.keys())}")
            print(f"  Total documents: {result.get('total_documents', 'N/A')}")
            print(f"  Query: {result.get('query', 'N/A')}")
            if result.get('results'):
                print(f"  First result preview: {result['results'][0].get('content', 'N/A')[:100]}...")
        else:
            print(f"  Error response: {response.text}")
    except Exception as e:
        print(f"[FAIL] Query endpoint failed: {e}")

    # Test the chat endpoint with a simple request
    try:
        chat_data = {
            "messages": [
                {"role": "user", "content": "Hello, what can you tell me about this book?"}
            ]
        }
        response = requests.post(
            "https://mahnoor09-deploy-hack.hf.space/chat",
            headers={"Content-Type": "application/json"},
            json=chat_data
        )
        print(f"[OK] Chat endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Response keys: {list(result.keys())}")
            print(f"  Response preview: {result.get('response', 'N/A')[:100]}...")
            print(f"  Retrieved documents: {len(result.get('retrieved_documents', []))}")
        else:
            print(f"  Error response: {response.text}")
    except Exception as e:
        print(f"[FAIL] Chat endpoint failed: {e}")

if __name__ == "__main__":
    test_endpoints()