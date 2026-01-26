import time
import requests

def run_tests_after_server_starts():
    """Function to run tests against the deployed backend"""
    # Check if deployed backend is accessible
    print("Checking if deployed backend is accessible...")
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/health", timeout=10)
        if response.status_code == 200:
            print("Deployed backend is accessible!")
        else:
            print(f"Deployed backend returned status code: {response.status_code}")
    except Exception as e:
        print(f"Deployed backend is not accessible: {e}")
        return

    # Now run the tests
    print("Running tests...")

    # Test 1: Health check
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Test 2: Root endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")

    # Test 3: Stats endpoint
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/stats")
        print(f"Stats endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Stats endpoint failed: {e}")

    print("Tests completed.")

if __name__ == "__main__":
    # Run tests against deployed backend
    print("Running tests against deployed backend at https://mahnoor09-deploy-hack.hf.space...")

    # Run tests
    run_tests_after_server_starts()

    print("Tests completed.")