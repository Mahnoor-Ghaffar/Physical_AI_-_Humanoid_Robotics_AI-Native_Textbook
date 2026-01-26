"""
Minimal API test to validate FastAPI endpoints without full backend dependencies
"""
import requests
import time

def test_minimal_endpoints():
    print("Testing FastAPI endpoints...")

    # Test the root endpoint
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Error'}")
    except Exception as e:
        print(f"Root endpoint failed (expected if server not running): {e}")

    # Test the health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Error'}")
    except Exception as e:
        print(f"Health endpoint failed (expected if server not running): {e}")

    # Test the stats endpoint
    try:
        response = requests.get("http://localhost:8000/stats")
        print(f"Stats endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Error'}")
    except Exception as e:
        print(f"Stats endpoint failed (expected if server not running): {e}")

if __name__ == "__main__":
    test_minimal_endpoints()