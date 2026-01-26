"""
Test response times for the FastAPI RAG integration to ensure they meet performance goals.
According to the spec, 90% of requests should be under 10 seconds.
"""
import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict

async def measure_single_request(session: aiohttp.ClientSession, query: str) -> Dict:
    """Measure response time for a single request."""
    start_time = time.time()
    try:
        response = await session.post(
            "https://mahnoor09-deploy-hack.hf.space/query",
            json={"query": query, "timeout": 30},
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()

        response_time = end_time - start_time
        result = await response.json() if response.status == 200 else None

        return {
            "status": "success" if response.status == 200 else "failed",
            "response_time": response_time,
            "http_status": response.status,
            "query": query
        }
    except Exception as e:
        end_time = time.time()
        return {
            "status": "error",
            "response_time": end_time - start_time,
            "error": str(e),
            "query": query
        }

async def test_response_times(num_requests: int = 20):
    """Test response times for multiple requests to validate performance goals."""
    print(f"Testing response times for {num_requests} requests...")
    print("Note: Using deployed backend at https://mahnoor09-deploy-hack.hf.space")

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
        "Explain the architecture",
        "What are the benefits of RAG?",
        "How do embeddings work?",
        "What is the retrieval process?",
        "Explain the AI agent",
        "What is the book structure?",
        "How to use the API?",
        "What are the components?",
        "Explain the architecture",
        "How does search work?",
        "What are the features?"
    ]

    results = []

    async with aiohttp.ClientSession() as session:
        for i, query in enumerate(queries[:num_requests]):
            print(f"Request {i+1}/{num_requests}: {query[:30]}...")
            result = await measure_single_request(session, query)
            results.append(result)

    # Analyze results
    successful_requests = [r for r in results if r['status'] == 'success']
    failed_requests = [r for r in results if r['status'] == 'failed']
    error_requests = [r for r in results if r['status'] == 'error']

    if successful_requests:
        response_times = [r['response_time'] for r in successful_requests]
        avg_response_time = statistics.mean(response_times)
        median_response_time = statistics.median(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)

        # Calculate 90th percentile
        sorted_times = sorted(response_times)
        p90_index = int(len(sorted_times) * 0.9) - 1
        p90_response_time = sorted_times[p90_index] if p90_index >= 0 else 0

        print(f"\n--- Response Time Analysis ---")
        print(f"Total requests: {len(results)}")
        print(f"Successful: {len(successful_requests)}")
        print(f"Failed: {len(failed_requests)}")
        print(f"Errors: {len(error_requests)}")

        print(f"\nResponse Time Statistics:")
        print(f"Average: {avg_response_time:.2f}s")
        print(f"Median: {median_response_time:.2f}s")
        print(f"Min: {min_response_time:.2f}s")
        print(f"Max: {max_response_time:.2f}s")
        print(f"90th Percentile: {p90_response_time:.2f}s")

        # Check performance goals
        slow_requests = [r for r in successful_requests if r['response_time'] >= 10.0]
        p90_under_10s = len([r for r in successful_requests if r['response_time'] < 10.0]) / len(successful_requests) >= 0.9

        print(f"\nPerformance Analysis:")
        print(f"Requests under 10s: {len(successful_requests) - len(slow_requests)}/{len(successful_requests)} ({(len(successful_requests) - len(slow_requests))/len(successful_requests)*100:.1f}%)")
        print(f"90th percentile under 10s: {'Yes' if p90_under_10s else 'No'}")

        if p90_under_10s:
            print("✅ PASSED: 90% of requests meet the <10s response time requirement")
        else:
            print("❌ FAILED: Less than 90% of requests meet the <10s response time requirement")

        if slow_requests:
            print(f"\nSlow requests (>10s):")
            for req in slow_requests:
                print(f"  - {req['query'][:50]}... : {req['response_time']:.2f}s")

        return {
            "total_requests": len(results),
            "successful": len(successful_requests),
            "failed": len(failed_requests),
            "errors": len(error_requests),
            "avg_response_time": avg_response_time,
            "p90_response_time": p90_response_time,
            "p90_under_10s": p90_under_10s,
            "max_response_time": max_response_time,
            "min_response_time": min_response_time
        }
    else:
        print("❌ No successful requests to analyze")
        return {
            "total_requests": len(results),
            "successful": len(successful_requests),
            "failed": len(failed_requests),
            "errors": len(error_requests),
            "p90_under_10s": False
        }

if __name__ == "__main__":
    try:
        result = asyncio.run(test_response_times(20))
        print(f"\nFinal Result: {result}")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError running response time test: {e}")
        print("Make sure the deployed API server is accessible at https://mahnoor09-deploy-hack.hf.space")