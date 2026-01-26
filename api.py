"""
FastAPI server for RAG system integration.

This API serves as an interface between the frontend and the RAG agent system,
exposing endpoints that allow the frontend to send user queries and receive
responses from the RAG agent with retrieval capabilities.
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime
from typing import AsyncGenerator, Dict, Any, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import sys
import json

# Add backend directory to path to import the agent and retrieval modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import required functions from agent.py and retrieve.py
try:
    from retrieve import retrieve_content
    from agent import create_agent, run_agent_interaction, execute_retrieve_content
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are available")
    raise

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG System API",
    description="API for interacting with the RAG (Retrieval-Augmented Generation) system",
    version="1.0.0"
)

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    """Model for query requests."""
    query: str = Field(..., min_length=1, max_length=10000, description="The user's question or query text")
    timeout: int = Field(30, ge=1, le=300, description="Timeout in seconds for query processing")
    stream: bool = Field(False, description="Whether to stream the response")

    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v

class StreamChunk(BaseModel):
    """Model for stream response chunks."""
    id: str
    content: str
    index: int
    is_final: bool
    timestamp: str

class QueryResponse(BaseModel):
    """Model for query responses."""
    id: str
    query: str
    answer: str
    sources: Optional[list] = []
    confidence: Optional[float] = None
    processing_time: Optional[float] = None
    timestamp: str
    status: str

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str

@app.get("/")
async def root():
    """Root endpoint for basic health check."""
    return {"message": "RAG System API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Test that we can access the required systems
    try:
        # Try to access environment variables
        required_envs = ['OPENAI_API_KEY', 'COHERE_API_KEY', 'QDRANT_URL']
        missing_envs = [env for env in required_envs if not os.getenv(env)]

        if missing_envs:
            return {
                "status": "unhealthy",
                "missing_envs": missing_envs,
                "timestamp": datetime.now().isoformat()
            }

        # Try a simple operation with the RAG system
        # Just check if the functions exist (we won't actually call them to avoid resource usage)
        if not callable(retrieve_content):
            return {"status": "unhealthy", "reason": "retrieve_content function not available", "timestamp": datetime.now().isoformat()}

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "api": "available",
                "rag_system": "available"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/query", response_model=QueryResponse, responses={
    200: {"description": "Successful response from RAG agent"},
    400: {"model": ErrorResponse, "description": "Invalid request parameters"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def query_endpoint(request: QueryRequest):
    """
    Process a user query through the RAG agent system.

    This endpoint accepts a query from the frontend, processes it through the
    RAG agent with retrieval capabilities, and returns a structured response.
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.now()

    try:
        logger.info(f"Processing query {request_id}: {request.query[:50]}...")

        if request.stream:
            # For streaming, we return an async generator
            return query_stream_endpoint(request)

        # Process the query through the RAG agent
        # For now, we'll simulate this by using the retrieve_content function directly
        # In a real implementation, this would integrate with the agent more completely

        # Retrieve content based on the query
        results = retrieve_content(request.query, top_k=5)

        # Create a simulated answer based on the retrieved content
        if results:
            # Combine content from the retrieved results
            answer_parts = []
            sources = []

            for result in results:
                content = result.get('content', '')
                if content:
                    answer_parts.append(content[:500])  # Limit content length

                # Add source information
                source_url = result.get('source_url', '')
                if source_url:
                    sources.append({"title": f"Source {len(sources)+1}", "url": source_url})

            answer = "\n\n".join(answer_parts)[:2000]  # Limit total answer length

            # Calculate confidence based on similarity scores
            if results and 'similarity_score' in results[0]:
                avg_confidence = sum(r.get('similarity_score', 0) for r in results) / len(results)
            else:
                avg_confidence = 0.5  # Default confidence
        else:
            answer = "No relevant content found for your query."
            sources = []
            avg_confidence = 0.0

        processing_time = (datetime.now() - start_time).total_seconds()

        response = QueryResponse(
            id=request_id,
            query=request.query,
            answer=answer,
            sources=sources,
            confidence=round(avg_confidence, 2),
            processing_time=round(processing_time, 2),
            timestamp=datetime.now().isoformat(),
            status="success"
        )

        logger.info(f"Query {request_id} completed in {processing_time:.2f}s")
        return response

    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()

        error_details = ErrorResponse(
            error=f"Error processing query: {str(e)}",
            code="AGENT_ERROR",
            details={"processing_time": round(processing_time, 2)},
            timestamp=datetime.now().isoformat()
        )

        logger.error(f"Query {request_id} failed after {processing_time:.2f}s: {str(e)}")
        raise HTTPException(status_code=500, detail=error_details.dict())

async def query_stream_endpoint(request: QueryRequest) -> AsyncGenerator[str, None]:
    """
    Stream response chunks for the query.
    Note: This is a simplified streaming implementation.
    In a full implementation, this would connect to the agent's streaming capabilities.
    """
    request_id = str(uuid.uuid4())

    try:
        # For demonstration, we'll simulate streaming by yielding chunks of the response
        # First, get the content to simulate what would be streamed
        results = retrieve_content(request.query, top_k=3)

        if results:
            combined_content = ""
            for result in results:
                content = result.get('content', '')
                if content:
                    combined_content += content + "\n\n"

            # Split content into chunks to simulate streaming
            words = combined_content.split()
            chunk_size = max(10, len(words) // 5)  # Create about 5 chunks

            for i in range(0, len(words), chunk_size):
                chunk_words = words[i:i + chunk_size]
                content_chunk = " ".join(chunk_words)

                chunk = StreamChunk(
                    id=f"{request_id}-chunk-{i//chunk_size}",
                    content=content_chunk,
                    index=i // chunk_size,
                    is_final=(i + chunk_size >= len(words)),
                    timestamp=datetime.now().isoformat()
                )

                yield f"data: {chunk.json()}\n\n"

                # Small delay to simulate real streaming
                await asyncio.sleep(0.1)
        else:
            chunk = StreamChunk(
                id=f"{request_id}-chunk-0",
                content="No relevant content found for your query.",
                index=0,
                is_final=True,
                timestamp=datetime.now().isoformat()
            )

            yield f"data: {chunk.json()}\n\n"

    except Exception as e:
        error_chunk = StreamChunk(
            id=f"{request_id}-error",
            content=f"Error: {str(e)}",
            index=-1,
            is_final=True,
            timestamp=datetime.now().isoformat()
        )

        yield f"data: {error_chunk.json()}\n\n"

# Add CORS middleware for frontend integration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)