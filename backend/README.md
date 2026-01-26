# RAG Content Ingestion Pipeline

This script implements a complete RAG content ingestion pipeline that:
- Crawls deployed Docusaurus/Vercel URLs
- Extracts and cleans text content
- Chunks the text optimally
- Generates Cohere embeddings
- Stores them in Qdrant vector database

## Configuration

The pipeline is configured through environment variables. Create a `.env` file in the backend directory with the following variables:

### Required Environment Variables

- `COHERE_API_KEY`: Your Cohere API key for generating embeddings
- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `DOCUSAURUS_BASE_URL`: The base URL of the Docusaurus site to crawl (e.g., `https://my-docs-site.vercel.app`)

### Optional Environment Variables

- `CHUNK_SIZE`: Size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between text chunks (default: 200 characters)
- `COHERE_MODEL`: Cohere model to use for embeddings (default: `embed-multilingual-v3.0`)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: `docs_embeddings`)
- `REQUEST_DELAY`: Delay between requests in seconds (default: 1 second)
- `MAX_RETRIES`: Maximum number of retries for failed requests (default: 3)

## Command Line Arguments

The script accepts the following command line arguments:

```bash
python main.py [OPTIONS]
```

### Options

- `--base-url TEXT`: Base URL of the Docusaurus site to crawl (overrides environment variable)
- `--chunk-size INTEGER`: Size of text chunks (overrides environment variable)
- `--chunk-overlap INTEGER`: Overlap between text chunks (overrides environment variable)
- `--cohere-model TEXT`: Cohere model to use for embeddings (overrides environment variable)
- `--collection-name TEXT`: Qdrant collection name (overrides environment variable)
- `--request-delay FLOAT`: Delay between requests in seconds (overrides environment variable)
- `--max-retries INTEGER`: Maximum number of retries for failed requests (overrides environment variable)
- `--verbose`: Enable verbose logging
- `--health-check`: Run health check and exit

### Example Usage

```bash
# Run with default configuration
python main.py

# Run with custom base URL
python main.py --base-url https://example-docs.com

# Run with custom chunk size and verbose logging
python main.py --chunk-size 2000 --chunk-overlap 300 --verbose

# Run health check only
python main.py --health-check
```

## Health Check

The pipeline includes a health check feature that validates connectivity to all required services:

- Cohere API connectivity
- Qdrant database connectivity
- Base URL accessibility

Run the health check with the `--health-check` flag.

## Services

The pipeline integrates with the following services:

### Cohere
Used for generating text embeddings. The pipeline uses Cohere's embedding models to convert text chunks into vector representations.

### Qdrant
Used as the vector database for storing embeddings with metadata. The pipeline creates collections with proper schema and indexes for efficient similarity search.

### Web Scraping
The pipeline respectfully scrapes Docusaurus sites, following robots.txt guidelines and implementing rate limiting to avoid overloading the target servers.


# RAG Retrieval Validation Script

The `retrieve.py` script validates the accuracy and reliability of the RAG (Retrieval-Augmented Generation) pipeline by connecting to the Qdrant vector database and testing query-response functionality.

## Purpose

This script connects to Qdrant, performs similarity searches, and validates the retrieved content to ensure the RAG pipeline is functioning correctly.

## Prerequisites

Before running the script, ensure you have the following environment variables set:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL for your Qdrant service
- `QDRANT_API_KEY`: API key for your Qdrant service
- `QDRANT_COLLECTION_NAME`: Name of the collection to search (optional, defaults to "docs_embeddings")

## Installation

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python retrieve.py --query "Your search query here" --top-k 5
```

### Command Line Arguments

- `--query` (required): The search query text
- `--top-k` (optional): Number of results to retrieve (default: 5)
- `--collection-name` (optional): Qdrant collection name (default: from environment)
- `--config` (optional): Path to configuration file (optional, will use environment variables by default)
- `--validate-metadata` (optional): Enable metadata validation (default: true)
- `--expected-source` (optional): Expected source URL for validation
- `--health-check` (optional): Run health check and exit

### Examples

Perform a basic search:
```bash
python retrieve.py --query "What is artificial intelligence?" --top-k 3
```

Validate results with specific source expectation:
```bash
python retrieve.py --query "Machine learning algorithms" --expected-source "https://example.com/ml-guide"
```

Run a health check on services:
```bash
python retrieve.py --health-check
```

## Output Format

The script outputs results in JSON format:

```json
{
  "query": "What is artificial intelligence?",
  "results": [
    {
      "content": "Artificial intelligence is the simulation of human intelligence processes...",
      "source_url": "https://example.com/ai-intro",
      "chunk_id": "abc123_0",
      "similarity_score": 0.85,
      "position": 0,
      "length": 120,
      "created_at": "2023-01-01T00:00:00",
      "metadata": {}
    }
  ],
  "validation_status": "PASS",
  "metrics": {
    "response_time_ms": 1250,
    "top_k_requested": 5,
    "results_returned": 5,
    "high_similarity_results": 3,
    "avg_similarity_score": 0.78,
    "max_similarity_score": 0.92,
    "semantic_accuracy_estimate": 0.6,
    "timestamp": "2026-01-14T10:30:00"
  },
  "errors": []
}
```

## Features

- **Connectivity Validation**: Validates connections to both Cohere and Qdrant services
- **Content Retrieval**: Performs similarity search in Qdrant collections
- **Metadata Validation**: Ensures retrieved content matches source URLs and metadata
- **Performance Metrics**: Measures response time and result quality
- **Health Checking**: Verifies service connectivity before running validation
- **Error Reporting**: Provides detailed error information for troubleshooting

## Troubleshooting

If you encounter issues:

1. Verify all required environment variables are set
2. Check that the Qdrant service is accessible
3. Ensure the Cohere API key is valid and has sufficient quota
4. Confirm the specified collection exists in Qdrant