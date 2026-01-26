"""
API Server for the RAG Chatbot
Handles API endpoints and integrates with the retrieval system
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import logging
import sys
import os
sys.path.append(os.path.dirname(__file__))
from document_retriever import get_document_retriever
from embedding_generator import get_embedding_generator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Native Book RAG API",
    description="API for the RAG chatbot backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class ChatResponse(BaseModel):
    response: str
    context: Optional[List[Dict]] = []
    retrieved_documents: Optional[List[Dict]] = []

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    results: List[Dict]
    query: str
    total_documents: int

class Document(BaseModel):
    id: int
    content: str
    source: str
    category: Optional[str] = None

class AddDocumentRequest(BaseModel):
    document: Document

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler
    """
    logger.info("Starting up RAG API server...")
    # Initialize components
    get_document_retriever()
    get_embedding_generator()
    logger.info("RAG API server started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler
    """
    logger.info("Shutting down RAG API server...")

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "AI Native Book RAG API", "status": "running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for the RAG chatbot
    """
    try:
        logger.info(f"Received chat request with {len(request.messages)} messages")

        # Get the last user message as the query
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found in the conversation")

        query = user_messages[-1].content

        # Retrieve relevant documents
        retriever = get_document_retriever()
        retrieved_docs = retriever.retrieve(query, top_k=request.max_tokens // 100)  # Adjust top_k based on max_tokens

        # Prepare context for the response
        context = []
        retrieved_documents = []

        for doc, similarity in retrieved_docs:
            context.append({
                "content": doc["content"],
                "source": doc["source"],
                "similarity": similarity
            })
            retrieved_documents.append({
                "id": doc["id"],
                "content": doc["content"],
                "source": doc["source"],
                "category": doc.get("category"),
                "similarity": similarity
            })

        # Generate response based on context
        if context:
            context_snippets = [item["content"] for item in context[:2]]  # Use top 2 most relevant
            context_str = " ".join(context_snippets)

            response = (
                f"Based on the knowledge base: {context_str}\n\n"
                f"Regarding your question '{query}', here's what I found: "
                f"The information suggests that this topic relates to concepts covered in the AI Native Book project."
            )
        else:
            response = (
                f"I received your message: '{query}'. I'm a RAG chatbot for the AI Native Book project. "
                f"Could you ask about digital twins, Isaac Sim, ROS2, AI native applications, or related topics?"
            )

        return ChatResponse(
            response=response,
            context=context,
            retrieved_documents=retrieved_documents
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Query endpoint to search the knowledge base directly
    """
    try:
        logger.info(f"Received query: {request.query}")

        # Retrieve relevant documents
        retriever = get_document_retriever()
        retrieved_docs = retriever.retrieve(request.query, top_k=request.top_k)

        # Format results
        results = []
        for doc, similarity in retrieved_docs:
            results.append({
                "id": doc["id"],
                "content": doc["content"],
                "source": doc["source"],
                "category": doc.get("category"),
                "similarity": similarity
            })

        return QueryResponse(
            results=results,
            query=request.query,
            total_documents=len(retrieved_docs)
        )

    except Exception as e:
        logger.error(f"Error in query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/documents/categories", response_model=List[str])
async def get_categories():
    """
    Get all document categories
    """
    try:
        retriever = get_document_retriever()
        categories = retriever.get_all_categories()
        return categories
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@app.post("/documents", status_code=201)
async def add_document(request: AddDocumentRequest):
    """
    Add a document to the knowledge base
    """
    try:
        retriever = get_document_retriever()
        retriever.add_document(request.document.dict())
        logger.info(f"Added document with ID: {request.document.id}")
        return {"message": "Document added successfully", "id": request.document.id}
    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding document: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    import datetime
    return HealthResponse(
        status="healthy",
        service="rag-api-server",
        timestamp=datetime.datetime.now().isoformat()
    )

@app.get("/stats")
async def get_stats():
    """
    Get statistics about the knowledge base
    """
    try:
        retriever = get_document_retriever()
        total_docs = len(retriever.documents)
        categories = retriever.get_all_categories()

        return {
            "total_documents": total_docs,
            "categories": categories,
            "total_categories": len(categories)
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)