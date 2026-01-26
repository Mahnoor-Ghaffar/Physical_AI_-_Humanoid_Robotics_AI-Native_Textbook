import requests
import time

def test_api():
    """Test the API endpoints to verify the server is running."""
    try:
        # Wait a moment for server to start
        time.sleep(3)

        # Test the root endpoint
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/")
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")

        # Test the health endpoint
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/health")
        print(f"Health endpoint status: {response.status_code}")
        print(f"Health endpoint response: {response.json()}")

        print("API server is running and responding correctly!")

    except requests.exceptions.ConnectionError:
        print("API server is not running or not accessible at https://mahnoor09-deploy-hack.hf.space")
        print("Please make sure the server is started with 'python run_server.py'")
    except Exception as e:
        print(f"Error testing API: {str(e)}")

if __name__ == "__main__":
    test_api()