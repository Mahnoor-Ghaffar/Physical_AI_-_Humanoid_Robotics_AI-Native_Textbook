#!/usr/bin/env python3
"""
Test script to verify that the deployed backend at https://mahnoor09-deploy-hack.hf.space is accessible.
"""

import requests
import json

def test_deployed_backend():
    """Test the deployed backend API endpoints."""
    base_url = "https://mahnoor09-deploy-hack.hf.space"

    print(f"Testing deployed backend at: {base_url}")
    print("-" * 50)

    # Test health endpoint
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health endpoint: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"  Health data: {health_data}")
        else:
            print(f"  Health error: {health_response.text}")
    except Exception as e:
        print(f"Health endpoint failed: {e}")

    print()

    # Test root endpoint
    try:
        root_response = requests.get(f"{base_url}/", timeout=10)
        print(f"Root endpoint: {root_response.status_code}")
        if root_response.status_code == 200:
            root_data = root_response.json()
            print(f"  Root data: {root_data}")
        else:
            print(f"  Root error: {root_response.text}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")

    print()

    # Test query endpoint with a simple query
    try:
        query_data = {
            "query": "What is this service about?",
            "timeout": 30
        }
        query_response = requests.post(
            f"{base_url}/query",
            json=query_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Query endpoint: {query_response.status_code}")
        if query_response.status_code == 200:
            query_result = query_response.json()
            print(f"  Query result keys: {list(query_result.keys()) if isinstance(query_result, dict) else 'Non-dict response'}")
        else:
            print(f"  Query error: {query_response.text}")
    except Exception as e:
        print(f"Query endpoint failed: {e}")

    print()
    print("-" * 50)
    print("Test completed. If you see 200 status codes, the deployed backend is accessible!")

if __name__ == "__main__":
    test_deployed_backend()