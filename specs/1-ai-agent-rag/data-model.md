# Data Model: AI Agent with Retrieval-Augmented Capabilities

## Overview
This document defines the key data structures and entities for the AI agent with retrieval capabilities.

## Core Entities

### 1. AI Agent
- **Description**: The intelligent system that orchestrates tool-based retrieval and generates responses based on retrieved content
- **Fields**:
  - `id`: Unique identifier for the agent instance
  - `name`: Name of the agent
  - `instructions`: System prompt that defines agent behavior and content restrictions
  - `model`: OpenAI model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
  - `tools`: List of available tools/functions the agent can use
  - `created_at`: Timestamp when the agent was created
  - `updated_at`: Timestamp when the agent was last updated

### 2. Retrieval Tool
- **Description**: The component that interfaces with the vector database to find relevant document chunks
- **Fields**:
  - `name`: Function name ("perform_retrieval")
  - `description`: Description of what the tool does
  - `parameters`: Schema defining input parameters
    - `query`: The search query text
    - `top_k`: Number of results to retrieve (default: 5)
  - `function`: The actual function implementation that calls Qdrant

### 3. Document Chunk
- **Description**: Segments of book content stored in the vector database for retrieval
- **Fields**:
  - `id`: Unique identifier for the chunk
  - `content`: The actual text content of the chunk
  - `source_url`: URL or identifier of the original source
  - `position`: Position of the chunk in the original document
  - `length`: Length of the chunk in characters
  - `created_at`: Timestamp when the chunk was created
  - `metadata`: Additional metadata about the chunk

### 4. Query Context
- **Description**: Information maintained between follow-up queries to preserve conversation state
- **Fields**:
  - `thread_id`: Unique identifier for the conversation thread
  - `messages`: List of messages in the conversation
  - `last_retrieved_chunks`: Cache of recently retrieved document chunks
  - `created_at`: Timestamp when the context was created
  - `updated_at`: Timestamp when the context was last updated

## Relationships

### AI Agent → Retrieval Tool
- One-to-many relationship: An agent can have multiple tools
- The retrieval tool is registered with the agent to enable RAG capabilities

### Retrieval Tool → Document Chunk
- One-to-many relationship: A retrieval operation can return multiple document chunks
- The tool performs similarity search and returns relevant chunks

### AI Agent → Query Context
- One-to-many relationship: An agent can manage multiple conversation threads
- Each conversation thread maintains its own context

## State Transitions

### Agent States
1. **Initialization**: Agent is created with configuration
2. **Ready**: Agent is ready to accept queries
3. **Processing**: Agent is currently processing a query
4. **Response Ready**: Agent has generated a response and is ready for next query

### Query Context States
1. **Active**: Conversation thread is ongoing
2. **Idle**: Conversation thread is waiting for user input
3. **Expired**: Conversation thread has timed out and should be cleaned up

## Validation Rules

### Agent Validation
- Instructions must contain a restriction to use only retrieved content
- Model must be a valid OpenAI model identifier
- Tools must be properly configured with required parameters

### Retrieval Tool Validation
- Query must not be empty
- top_k must be between 1 and 10
- Query must be properly formatted for semantic search

### Document Chunk Validation
- Content must not be empty
- Content must meet minimum quality thresholds
- Source URL must be valid

## Data Flow

### Query Processing Flow
1. User submits query to AI Agent
2. Agent calls Retrieval Tool with the query
3. Retrieval Tool performs similarity search in Qdrant
4. Retrieved Document Chunks are returned to the agent
5. Agent generates response based only on retrieved content
6. Response and context are stored in Query Context
7. Response is returned to user