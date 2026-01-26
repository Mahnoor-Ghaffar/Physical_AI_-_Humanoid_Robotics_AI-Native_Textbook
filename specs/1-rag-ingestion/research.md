# Research: RAG Content Ingestion Pipeline

**Feature**: RAG Content Ingestion Pipeline
**Date**: 2026-01-12

## Overview
Research document to resolve technical unknowns and establish best practices for the RAG ingestion pipeline implementation.

## Technical Decisions

### 1. Web Scraping Approach for Docusaurus Sites
**Decision**: Use requests + BeautifulSoup4 for scraping Docusaurus sites
**Rationale**: Docusaurus sites are typically static-rendered, making them well-suited for traditional web scraping. Requests handles HTTP operations while BeautifulSoup4 provides robust HTML parsing.
**Alternatives considered**:
- Selenium/Puppeteer (overkill for static content, adds complexity)
- Specialized documentation scrapers (less flexible for customization)

### 2. Text Extraction and Cleaning
**Decision**: Target main content areas of Docusaurus sites using CSS selectors
**Rationale**: Docusaurus follows predictable DOM structures with main content in specific containers (e.g., `.main-wrapper`, `article`, `.markdown`). This allows precise extraction while avoiding navigation and footer content.
**Alternatives considered**:
- Generic text extraction (would include unwanted boilerplate)
- Machine learning-based content detection (unnecessary complexity)

### 3. Text Chunking Strategy
**Decision**: Use LangChain's RecursiveCharacterTextSplitter with semantic boundaries
**Rationale**: LangChain's splitter provides intelligent chunking that respects sentence and paragraph boundaries, which is crucial for maintaining context in embeddings.
**Parameters**:
- Chunk size: 1000 characters (configurable)
- Chunk overlap: 200 characters (configurable)
- Separators: ["\n\n", "\n", " ", ""]

### 4. Embedding Model Selection
**Decision**: Use Cohere's embed-multilingual-v3.0 model
**Rationale**: Cohere embeddings consistently perform well across various content types and languages. The multilingual model handles diverse documentation content effectively.
**Alternatives considered**:
- OpenAI embeddings (costlier, vendor lock-in)
- Self-hosted models (more complex infrastructure)

### 5. Qdrant Collection Design
**Decision**: Create collection with 1024-dimensional vectors (matching Cohere embedding size)
**Rationale**: Cohere's v3 models produce 1024-dimensional vectors. Qdrant will be configured with cosine distance metric for semantic similarity.
**Collection schema**:
- Payload: {content: str, source_url: str, chunk_metadata: dict}
- Vector size: 1024
- Distance: Cosine

### 6. Error Handling and Resilience
**Decision**: Implement retry mechanisms and graceful degradation
**Rationale**: Web scraping and API calls are inherently unreliable. The system must handle timeouts, rate limits, and transient failures gracefully.
**Approach**:
- Exponential backoff for API calls
- Skip failed URLs with logging
- Batch processing with checkpointing capability

### 7. Configuration Management
**Decision**: Use environment variables with a .env template
**Rationale**: Environment variables provide secure and flexible configuration across different deployment environments.
**Required variables**:
- COHERE_API_KEY
- QDRANT_URL
- QDRANT_API_KEY
- DOCUSAURUS_BASE_URL
- CHUNK_SIZE
- CHUNK_OVERLAP

## Best Practices Applied

1. **Rate Limiting**: Respectful scraping with delays between requests
2. **User-Agent Identification**: Proper identification when making requests
3. **Session Management**: Reuse connections for efficiency
4. **Memory Management**: Process content in batches to avoid memory issues
5. **Logging**: Comprehensive logging for debugging and monitoring
6. **Validation**: Test searches to verify ingestion quality