# Implementation Plan: RAG Retrieval Validation

**Feature**: RAG Retrieval Validation
**Branch**: 003-rag-retrieval-validation
**Created**: 2026-01-14
**Status**: Draft

## Technical Context

### System Overview
The RAG retrieval validation system is designed to validate the accuracy and reliability of the RAG (Retrieval-Augmented Generation) pipeline by connecting to the Qdrant vector database and testing query-response functionality. The system will be implemented as a single Python script (`retrieve.py`) in the backend folder that connects to Qdrant, performs similarity searches, and validates the retrieved content.

### Architecture Components
- **Backend Script**: `retrieve.py` - Main entry point for validation
- **Qdrant Client**: Connection layer to vector database
- **Embedding Processor**: Converts queries to embeddings for similarity search
- **Validation Engine**: Verifies retrieved content matches source metadata

### Technology Stack
- **Language**: Python
- **Vector Database**: Qdrant
- **Embedding Model**: Cohere (as specified in constraints)
- **Dependencies**: qdrant-client, cohere

### External Dependencies
- **Qdrant Service**: Hosted vector database containing book content embeddings
- **Cohere API**: For embedding generation and similarity computation
- **Existing Collections**: Vector collections from Spec-1 ingestion

### Known Unknowns
- Qdrant connection parameters (host, port, API key) - RESOLVED: Will use same config as main.py (QDRANT_URL, QDRANT_API_KEY from environment)
- Collection name for book content embeddings - RESOLVED: Will use same config as main.py (QDRANT_COLLECTION_NAME from environment, default "docs_embeddings")
- Specific embedding dimension used during ingestion - RESOLVED: 1024 (from main.py: vector_dimension = 1024 for Cohere v3 models)
- Top-k value for similarity search - RESOLVED: Default to 5, configurable via command line
- Expected metadata structure for validation - RESOLVED: From main.py, metadata includes content, source_url, chunk_id, and other payload fields

## Constitution Check

### Principle 1: Library-First Approach
- ✅ The validation functionality will be implemented as a reusable module within the `retrieve.py` script
- ✅ Functions will be organized to allow potential reuse in other validation contexts

### Principle 2: CLI Interface
- ✅ The `retrieve.py` script will accept command-line arguments for queries and configuration
- ✅ Will follow text-in/text-out protocol with structured JSON output

### Principle 3: Test-First (NON-NEGOTIABLE)
- ✅ Unit tests will be developed alongside the implementation
- ✅ Integration tests will validate the full retrieval pipeline

### Principle 4: Integration Testing
- ✅ Focus on integration testing between Python script and Qdrant service
- ✅ Contract testing for expected data structures

### Principle 5: Observability
- ✅ Structured logging for debugging and monitoring
- ✅ Clear error messages for troubleshooting

### Potential Violations
- None identified

### Post-Design Review
- ✅ All design decisions align with constitution principles
- ✅ Implementation follows established patterns from main.py
- ✅ Dependencies match those already used in the codebase

## Phase 0: Research & Resolution

### Research Tasks
Based on the analysis of existing backend code (`main.py`), the following information has been discovered:

1. Qdrant connection parameters: Use environment variables QDRANT_URL and QDRANT_API_KEY as configured in main.py
2. Collection name: Use QDRANT_COLLECTION_NAME environment variable (defaults to "docs_embeddings") from main.py
3. Embedding dimensions: 1024-dimensional vectors from Cohere v3 models (as specified in main.py)
4. Metadata structure: Contains content, source_url, chunk_id, and additional payload fields as implemented in main.py
5. Top-k value: Will default to 5 but be configurable via command line argument

### Success Criteria for Research
- ✅ All "NEEDS CLARIFICATION" items resolved using existing codebase
- ✅ Understanding of existing vector database schema from main.py
- ✅ Confirmation of embedding model compatibility (Cohere embed-multilingual-v3.0 with 1024 dimensions)

## Phase 1: Design & Contracts

### Data Model Design

#### Text Chunk Entity (from main.py DocumentChunk)
- **id**: String - Unique identifier for the document chunk
- **content**: String - The actual text content retrieved from the source
- **source_url**: String - URL where the content originated
- **position**: Integer - Position of the chunk within the document
- **length**: Integer - Length of the content in characters
- **created_at**: DateTime - Timestamp when the chunk was created
- **metadata**: Object - Additional metadata about the chunk

#### Query Entity
- **text**: String - The input query text
- **top_k**: Integer - Number of results to return (default: 5)
- **filters**: Object - Optional filters for refined search

#### Validation Result Entity
- **query**: String - Original query text
- **results**: Array - List of retrieved text chunks with metadata
- **validation_status**: Enum - PASS/FAIL status of the validation
- **errors**: Array - List of validation errors if any
- **metrics**: Object - Performance metrics (response time, accuracy, etc.)

#### Qdrant Point Structure (from main.py)
- **id**: String - UUID for the point in Qdrant
- **vector**: Array[Float] - 1024-dimensional embedding vector (Cohere v3)
- **payload**: Object - Contains:
  - **content**: String - The actual text content
  - **source_url**: String - URL of the source document
  - **position**: Integer - Position in original document
  - **length**: Integer - Length of content in characters
  - **created_at**: String - ISO timestamp
  - **chunk_id**: String - Original chunk ID
  - **meta_*: Mixed - Additional metadata fields

### API Contract

#### Command-Line Interface
Since this is a validation script rather than a service, the interface will be a command-line interface:

```
python retrieve.py --query "What is the main concept?" --top-k 5 --collection-name "book-content"
```

Parameters:
- `--query`: The search query text (required)
- `--top-k`: Number of results to retrieve (default: 5)
- `--collection-name`: Name of the Qdrant collection (default: from environment QDRANT_COLLECTION_NAME)
- `--config`: Path to configuration file (optional, will use environment variables by default)
- `--validate-metadata`: Flag to enable metadata validation (default: true)
- `--expected-source`: Expected source URL for validation (optional)

#### Output Format
The script will output validation results in JSON format:

```json
{
  "query": "What is the main concept?",
  "results": [
    {
      "content": "The main concept is...",
      "source_url": "https://example.com/page",
      "similarity_score": 0.85,
      "chunk_id": "abc123_0",
      "metadata": {...}
    }
  ],
  "validation_status": "PASS",
  "metrics": {
    "response_time_ms": 1250,
    "top_k_requested": 5,
    "results_returned": 5,
    "semantic_accuracy": 0.87
  },
  "errors": []
}
```

#### Environment Variables (from main.py)
- `QDRANT_URL`: URL for Qdrant service
- `QDRANT_API_KEY`: API key for Qdrant authentication
- `QDRANT_COLLECTION_NAME`: Name of the collection (default: "docs_embeddings")
- `COHERE_API_KEY`: API key for Cohere service
- `COHERE_MODEL`: Model name for embeddings (default: "embed-multilingual-v3.0")

### Quickstart Guide

1. **Setup**: Copy backend/requirements.txt dependencies and install: `pip install -r requirements.txt`
2. **Configuration**: Set environment variables (QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, COHERE_API_KEY)
3. **Execution**: Run validation with sample queries: `python retrieve.py --query "your query here"`
4. **Validation**: Verify results match expected content and metadata

## Phase 2: Implementation Plan

### Task Breakdown
1. **Configuration Setup**: Create Config class similar to main.py to handle environment variables
2. **Qdrant Client Initialization**: Connect to Qdrant using the same parameters as main.py
3. **Query Embedding**: Convert input query to 1024-dimensional embedding using Cohere API
4. **Similarity Search**: Implement search in Qdrant collection using cosine distance (same as main.py)
5. **Result Processing**: Extract content, metadata, and similarity scores from search results
6. **Validation Engine**: Compare retrieved content/metadata against expected values
7. **Output Formatting**: Generate structured JSON output with validation results and metrics
8. **Error Handling**: Handle network errors, API limits, and invalid responses
9. **Logging**: Implement structured logging similar to main.py for debugging
10. **Command-Line Interface**: Parse arguments and provide user-friendly output

### Risk Assessment
- **High Risk**: Qdrant connectivity issues could prevent validation - Mitigation: Implement retry logic and health checks from main.py
- **Medium Risk**: Cohere API rate limits could slow validation - Mitigation: Implement exponential backoff as in main.py
- **Medium Risk**: Collection name mismatches could cause failures - Mitigation: Validate collection exists before searching
- **Low Risk**: Metadata structure differences could affect validation accuracy - Mitigation: Flexible validation that checks for required fields only

### Success Metrics
- Successful connection to Qdrant 100% of the time during validation runs
- Query response time under 2 seconds for 95% of requests
- Validation accuracy above 85% for relevant results (measured by semantic relevance)
- Proper metadata validation ensuring retrieved content matches source URLs
- Zero crashes during validation runs