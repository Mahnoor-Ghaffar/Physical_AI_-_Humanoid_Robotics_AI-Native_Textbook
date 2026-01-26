# Quickstart Guide: RAG Content Ingestion Pipeline

**Feature**: RAG Content Ingestion Pipeline
**Date**: 2026-01-12

## Prerequisites

- Python 3.11+
- UV package manager installed
- Cohere API key
- Qdrant Cloud account and API key
- Target Docusaurus/Vercel documentation site URL

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Backend Directory and Initialize UV Environment
```bash
mkdir backend
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install cohere qdrant-client requests beautifulsoup4 langchain-text-splitters
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory with the following:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
DOCUSAURUS_BASE_URL=https://your-docs-site.vercel.app
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
COHERE_MODEL=embed-multilingual-v3.0
QDRANT_COLLECTION_NAME=docs_embeddings
```

## Usage

### 1. Run the Ingestion Pipeline
```bash
cd backend
python main.py
```

### 2. Verify Ingestion
The script will:
- Crawl all pages from the specified Docusaurus site
- Extract and clean text content
- Chunk the text appropriately
- Generate embeddings using Cohere
- Store embeddings in Qdrant
- Run validation tests

### 3. Check Results
After execution, verify that:
- Documents are stored in your Qdrant collection
- Test searches return relevant results
- Logs indicate successful processing

## Troubleshooting

### Common Issues

#### API Rate Limits
- If you encounter rate limiting, add delays between API calls or upgrade your Cohere/Qdrant tier

#### Connection Issues
- Verify that your QDRANT_URL and API keys are correct
- Check that your network allows outbound connections

#### Empty Results
- Ensure the DOCUSAURUS_BASE_URL is accessible
- Verify that the site structure follows Docusaurus conventions

### Logging
The pipeline logs all activities to help diagnose issues:
- Successful URL crawls
- Failed URL requests
- Embedding generation status
- Qdrant upload results

## Validation Tests

The script performs the following validation tests:
1. Confirms that content was extracted from the target site
2. Verifies that embeddings were generated successfully
3. Checks that vectors were stored in Qdrant
4. Performs a sample search to validate retrieval functionality