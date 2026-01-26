# Data Model: FastAPI RAG System Integration

## Overview
Data structures for the FastAPI RAG integration API, defining request/response schemas and data validation rules.

## Entity: QueryRequest
**Description**: Represents a user's input query sent to the RAG system

**Fields**:
- `query`: string (required) - The user's question or query text
- `timeout`: integer (optional, default: 30) - Timeout in seconds for the query processing
- `stream`: boolean (optional, default: false) - Whether to stream the response

**Validation Rules**:
- `query` must be between 1 and 10000 characters
- `timeout` must be between 1 and 300 seconds
- `query` cannot be empty or whitespace-only

**State Transitions**: N/A (immutable request object)

## Entity: QueryResponse
**Description**: Contains the RAG agent's response to the query

**Fields**:
- `id`: string (required) - Unique identifier for the response
- `query`: string (required) - The original query text
- `answer`: string (required) - The agent's answer to the query
- `sources`: array of objects (optional) - List of sources used in the response
- `confidence`: number (optional) - Confidence score between 0 and 1
- `processing_time`: number (optional) - Time taken to process the query in seconds
- `timestamp`: string (required) - ISO 8601 timestamp of response creation
- `status`: string (required) - Status of the response (success, error)

**Validation Rules**:
- `id` must be a valid UUID
- `answer` cannot be empty when status is "success"
- `confidence` must be between 0 and 1 when provided
- `processing_time` must be a positive number when provided

**State Transitions**: N/A (immutable response object)

## Entity: StreamChunk
**Description**: Represents a portion of the response when using streaming

**Fields**:
- `id`: string (required) - Unique identifier for the chunk
- `content`: string (required) - The content of this chunk
- `index`: integer (required) - The sequence number of this chunk
- `is_final`: boolean (required) - Whether this is the final chunk
- `timestamp`: string (required) - ISO 8601 timestamp of chunk creation

**Validation Rules**:
- `index` must be non-negative
- `content` can be empty for final chunks
- Exactly one chunk per stream should have `is_final` set to true

**State Transitions**: N/A (immutable chunk object)

## Entity: ErrorResponse
**Description**: Standardized error response format

**Fields**:
- `error`: string (required) - Error message
- `code`: string (required) - Error code
- `details`: object (optional) - Additional error details
- `timestamp`: string (required) - ISO 8601 timestamp of error

**Validation Rules**:
- `error` and `code` must not be empty
- `code` should follow standard HTTP status code format or custom error codes

**State Transitions**: N/A (immutable error object)

## Relationships
- `QueryRequest` → `QueryResponse` (1:1) - Each query request generates one response
- `QueryRequest` → `StreamChunk` (1:many) - Each query request can generate multiple stream chunks (when streaming is enabled)
- `QueryRequest` → `ErrorResponse` (1:1) - Each query request generates one error response when an error occurs

## Validation Rules Summary
- All string fields must be properly sanitized to prevent injection attacks
- All numeric fields must be validated for appropriate ranges
- All timestamp fields must follow ISO 8601 format
- All ID fields must follow UUID format or appropriate identifier format