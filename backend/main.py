from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Dict, Optional
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Native Book RAG Chatbot API",
    description="Retrieval Augmented Generation API for AI Native Book project",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    context: Optional[List[Dict]] = []

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    results: List[Dict]
    query: str

# Mock data for demonstration
mock_knowledge_base = [
    {"id": 1, "content": "AI Native applications leverage artificial intelligence as a core component of their architecture, integrating ML models directly into the application lifecycle.", "source": "Module 1"},
    {"id": 2, "content": "Digital twins are virtual replicas of physical systems that enable real-time monitoring, simulation, and optimization of real-world assets.", "source": "Module 2"},
    {"id": 3, "content": "Isaac Sim is NVIDIA's robotics simulation platform that provides high-fidelity physics simulation for robot development and testing.", "source": "Module 3"},
    {"id": 4, "content": "ROS2 (Robot Operating System 2) provides a flexible framework for writing robot software with distributed computation and real-time control.", "source": "Module 4"},
    {"id": 5, "content": "Large Language Models (LLMs) are transformer-based neural networks trained on vast amounts of text data to understand and generate human-like language.", "source": "Module 5"}
]

@app.get("/")
def read_root():
    return {"message": "AI Native Book RAG Chatbot API", "status": "running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for the RAG chatbot
    """
    try:
        # In a real implementation, this would:
        # 1. Retrieve relevant context from vector database based on conversation history
        # 2. Format the context with the user's query
        # 3. Call the LLM with the augmented prompt
        # 4. Return the response with context information

        # For demo purposes, we'll return a mock response
        last_user_message = request.messages[-1].content if request.messages else "Hello"

        # Simple mock RAG implementation
        relevant_docs = []
        for doc in mock_knowledge_base:
            if last_user_message.lower() in doc["content"].lower():
                relevant_docs.append(doc)

        if not relevant_docs:
            # If no direct match, return a generic response
            response = f"I received your message: '{last_user_message}'. I'm a RAG chatbot for the AI Native Book project. I can answer questions about digital twins, Isaac Sim, ROS2, and AI native applications."
        else:
            # Use the relevant document in the response
            context_str = " ".join([doc["content"] for doc in relevant_docs])
            response = f"Based on the knowledge base: {context_str}"

        return ChatResponse(response=response, context=relevant_docs[:2])  # Return top 2 contexts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query endpoint to search the knowledge base directly
    """
    try:
        # In a real implementation, this would query a vector database
        # For demo, we'll do a simple text search

        results = []
        query_lower = request.query.lower()

        for doc in mock_knowledge_base:
            if query_lower in doc["content"].lower():
                results.append({
                    "id": doc["id"],
                    "content": doc["content"],
                    "source": doc["source"],
                    "score": 1.0  # Mock score
                })

        # If no exact matches, return closest matches
        if not results:
            for doc in mock_knowledge_base:
                content_words = set(doc["content"].lower().split())
                query_words = set(query_lower.split())
                overlap = len(content_words.intersection(query_words))
                if overlap > 0:
                    results.append({
                        "id": doc["id"],
                        "content": doc["content"],
                        "source": doc["source"],
                        "score": overlap / max(len(content_words), len(query_words))  # Simple similarity score
                    })

        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:request.top_k]

        return QueryResponse(results=results, query=request.query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "rag-chatbot-api"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)