#!/usr/bin/env python3
"""
Start script for the RAG Chatbot API Server
"""
import uvicorn
import argparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Start the RAG Chatbot API Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (development)")

    args = parser.parse_args()

    # Determine if we should enable reload based on DEBUG env var or command line
    reload_enabled = args.reload or os.getenv("DEBUG", "").lower() == "true"

    print(f"Starting RAG Chatbot API Server on {args.host}:{args.port}")
    print(f"Auto-reload: {'enabled' if reload_enabled else 'disabled'}")

    uvicorn.run(
        "api_server:app",  # Import path to the FastAPI app
        host=args.host,
        port=args.port,
        reload=reload_enabled,
        log_level="info"
    )

if __name__ == "__main__":
    main()