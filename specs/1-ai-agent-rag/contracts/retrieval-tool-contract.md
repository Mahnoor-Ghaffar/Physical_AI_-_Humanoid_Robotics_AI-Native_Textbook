# OpenAPI Contract: Agent Retrieval Tool

This document defines the API contract for the retrieval tool that the AI agent will use to search for relevant document chunks in the Qdrant vector database.

## Function Definition: perform_retrieval

### Description
The retrieval tool allows the AI agent to search the Qdrant vector database for document chunks relevant to a given query. This function is called by the agent when it needs to retrieve information to answer a user's question.

### Function Signature
```json
{
  "name": "perform_retrieval",
  "description": "Search the book content database to find relevant information for answering user queries",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query text to find relevant document chunks",
        "minLength": 1,
        "maxLength": 500
      },
      "top_k": {
        "type": "integer",
        "description": "Number of results to retrieve (default: 5, max: 10)",
        "minimum": 1,
        "maximum": 10,
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

### Request Parameters
- **query** (string, required): The text query to search for in the document database
  - minLength: 1 character
  - maxLength: 500 characters
- **top_k** (integer, optional): Number of top results to return
  - minimum: 1
  - maximum: 10
  - default: 5

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "description": "The content of the retrieved document chunk"
          },
          "source_url": {
            "type": "string",
            "description": "The source URL of the document"
          },
          "similarity_score": {
            "type": "number",
            "description": "Similarity score between 0 and 1, where 1 is most similar"
          },
          "position": {
            "type": "integer",
            "description": "Position of the chunk in the original document"
          }
        },
        "required": ["content", "source_url", "similarity_score"]
      }
    },
    "query": {
      "type": "string",
      "description": "The original query that was searched"
    },
    "total_results": {
      "type": "integer",
      "description": "Total number of results returned"
    }
  },
  "required": ["results", "query", "total_results"]
}
```

### Response Example
```json
{
  "results": [
    {
      "content": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals...",
      "source_url": "https://example.com/book/chapter1.html",
      "similarity_score": 0.89,
      "position": 0
    },
    {
      "content": "Machine learning is a method of data analysis that automates analytical model building...",
      "source_url": "https://example.com/book/chapter2.html",
      "similarity_score": 0.76,
      "position": 1
    }
  ],
  "query": "What is artificial intelligence?",
  "total_results": 2
}
```

### Error Responses
- **Invalid Query**: If the query is empty or exceeds length limits
- **Database Unavailable**: If Qdrant is unreachable
- **Authentication Error**: If API keys are invalid

### Performance Requirements
- Response Time: <500ms for typical queries
- Availability: 99.9% uptime
- Rate Limiting: Appropriate limits to prevent abuse

### Security Requirements
- API keys must be properly authenticated
- Query sanitization to prevent injection attacks
- Proper error handling without information disclosure