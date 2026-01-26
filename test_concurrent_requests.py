"""
Test concurrent request handling for the FastAPI RAG integration.
"""
import asyncio
import aiohttp
import time
from typing import List

async def make_request(session: aiohttp.ClientSession, query: str, idx: int) -> dict:
    """Make a single request to the API."""
    start_time = time.time()
    try:
        response = await session.post(
            "https://mahnoor09-deploy-hack.hf.space/query",
            json={"query": query, "timeout": 30},
            headers={"Content-Type": "application/json"}
        )
        response_time = time.time() - start_time
        result = await response.json()
        status = "success" if response.status in [200] else "failed"

        return {
            "idx": idx,
            "status": status,
            "response_time": response_time,
            "http_status": response.status,
            "result_length": len(str(result)) if result else 0
        }
    except Exception as e:
        response_time = time.time() - start_time
        return {
            "idx": idx,
            "status": "error",
            "response_time": response_time,
            "error": str(e)
        }

async def test_concurrent_requests(num_requests: int = 10):
    """Test concurrent request handling."""
    print(f"Testing {num_requests} concurrent requests...")

    # Sample queries for testing
    queries = [
        "What is this book about?",
        "Explain AI native applications",
        "What are the key concepts?",
        "Tell me about RAG systems",
        "How does retrieval work?",
        "What is vector search?",
        "Explain embeddings",
        "What is semantic search?",
        "How does this relate to AI?",
        "Explain the architecture"
    ]

    # Trim or extend the queries list to match num_requests
    test_queries = queries[:num_requests] if num_requests <= len(queries) else queries + [queries[-1]] * (num_requests - len(queries))

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        # Create tasks for concurrent requests
        tasks = [
            make_request(session, test_queries[i], i)
            for i in range(num_requests)
        ]

        # Execute all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

    total_time = time.time() - start_time

    # Analyze results
    successful_requests = [r for r in results if isinstance(r, dict) and r.get('status') == 'success']
    failed_requests = [r for r in results if isinstance(r, dict) and r.get('status') != 'success']
    error_requests = [r for r in results if not isinstance(r, dict)]  # Exceptions

    print(f"\n--- Test Results ---")
    print(f"Total requests: {num_requests}")
    print(f"Successful: {len(successful_requests)}")
    print(f"Failed: {len(failed_requests)}")
    print(f"Errors: {len(error_requests)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per request: {total_time/num_requests:.2f}s")

    if successful_requests:
        response_times = [r['response_time'] for r in successful_requests]
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)

        print(f"\nResponse Time Statistics:")
        print(f"Average: {avg_response_time:.2f}s")
        print(f"Min: {min_response_time:.2f}s")
        print(f"Max: {max_response_time:.2f}s")

    # Check if we met the requirement of handling at least 10 concurrent requests
    success_rate = len(successful_requests) / num_requests if num_requests > 0 else 0
    print(f"\nSuccess rate: {success_rate:.2%}")

    if len(successful_requests) >= 10:
        print("✅ Passed: System can handle at least 10 concurrent requests")
    else:
        print("❌ Failed: System could not handle at least 10 concurrent requests")

    return {
        "total_requests": num_requests,
        "successful": len(successful_requests),
        "failed": len(failed_requests),
        "errors": len(error_requests),
        "total_time": total_time,
        "success_rate": success_rate
    }

if __name__ == "__main__":
    print("Testing concurrent request handling for FastAPI RAG integration...")
    print("Note: Using deployed backend at https://mahnoor09-deploy-hack.hf.space")

    try:
        result = asyncio.run(test_concurrent_requests(10))
        print(f"\nFinal Result: {result}")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError running concurrent test: {e}")
        print("Make sure the deployed API server is accessible at https://mahnoor09-deploy-hack.hf.space")