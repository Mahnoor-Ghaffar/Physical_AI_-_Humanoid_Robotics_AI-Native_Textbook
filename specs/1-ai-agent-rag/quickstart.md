# Quickstart Guide: AI Agent with Retrieval-Augmented Capabilities

## Overview
This guide will help you quickly set up and run the AI agent that can retrieve information from book content using a vector database.

## Prerequisites
- Python 3.11+
- OpenAI API key
- Access to Qdrant vector database with book content
- Cohere API key
- Pip package manager

## Setup

### 1. Install Dependencies
```bash
pip install openai cohere qdrant-client python-dotenv
```

### 2. Configure Environment Variables
Create a `.env` file in your project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=docs_embeddings
```

### 3. Verify Qdrant Connection
Make sure your Qdrant database has book content ingested. You can use the existing ingestion script if needed:

```bash
cd backend
python main.py --base-url "your_book_url_here"
```

## Running the Agent

### 1. Initialize the Agent
```bash
python agent.py --init
```

### 2. Query the Agent
```bash
python agent.py --query "What does the book say about artificial intelligence?"
```

### 3. Interactive Mode
Run the agent in interactive mode to have a conversation:

```bash
python agent.py --interactive
```

## Configuration Options

### Command Line Arguments
- `--query`: Direct query to the agent
- `--interactive`: Start interactive conversation mode
- `--init`: Initialize the agent with proper tools
- `--collection-name`: Specify Qdrant collection name (defaults to environment variable)
- `--top-k`: Number of results to retrieve (default: 5)

### Environment Variables
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4)
- `TOP_K_RESULTS`: Number of results to retrieve (default: 5)
- `RESPONSE_TIMEOUT`: Timeout for agent responses in seconds (default: 30)

## Example Usage

### Simple Query
```bash
python agent.py --query "Explain the concept of neural networks"
```

### Interactive Session
```bash
python agent.py --interactive
# Output: Agent initialized. Type your questions (type 'exit' to quit):
# User: What is deep learning?
# Agent: According to the book content, deep learning is...
# User: How is it different from machine learning?
# Agent: The book explains that the main difference is...
```

## Troubleshooting

### Common Issues

#### Issue: "API key not found"
**Solution**: Verify that your `.env` file contains the required API keys and that the file is in the correct location.

#### Issue: "Qdrant connection failed"
**Solution**: Check that your Qdrant URL and API key are correct, and that the Qdrant service is running.

#### Issue: "No results returned"
**Solution**: Verify that your Qdrant collection contains book content and that the collection name is correctly specified.

### Debug Mode
Run with the `--debug` flag to get more detailed logs:

```bash
python agent.py --query "your query" --debug
```

## Next Steps
- Customize the agent's personality by modifying the system prompt
- Adjust the number of results retrieved with the `--top-k` option
- Integrate the agent into your application using the provided API