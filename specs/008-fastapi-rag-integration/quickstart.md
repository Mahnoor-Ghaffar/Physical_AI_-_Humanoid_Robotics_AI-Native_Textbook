# Quickstart Guide: FastAPI RAG System Integration

## Prerequisites
- Python 3.11+
- pip package manager
- Access to OpenAI API key
- Access to Cohere API key
- Access to Qdrant vector database

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-native-book
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv openai cohere qdrant-client
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=your_collection_name
```

### 4. Verify RAG System
Ensure the existing RAG system is working:
```bash
python backend/retrieve.py --query "test" --top-k 1
```

## Using the Deployed API

### 1. The API is already deployed
The API is already deployed and available at `https://mahnoor09-deploy-hack.hf.space`

API documentation is available at:
- `https://mahnoor09-deploy-hack.hf.space/docs` (Swagger UI)
- `https://mahnoor09-deploy-hack.hf.space/redoc` (ReDoc)

### 1. Test the API
```bash
curl -X POST https://mahnoor09-deploy-hack.hf.space/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic of chapter 1?"}'
```

## API Usage Examples

### Basic Query
```bash
curl -X POST https://mahnoor09-deploy-hack.hf.space/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key concepts in chapter 1?",
    "timeout": 30
  }'
```

### Streaming Query
```bash
curl -X POST https://mahnoor09-deploy-hack.hf.space/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Summarize chapter 1",
    "stream": true
  }'
```

## Integration with Frontend

The API is designed to work seamlessly with the existing Docusaurus frontend:

1. The frontend can make AJAX requests to the `/query` endpoint
2. For real-time experience, use the streaming option
3. Handle errors appropriately with the standardized error responses

## Troubleshooting

### Common Issues

**Issue**: Connection timeout to Qdrant
**Solution**: Verify QDRANT_URL and QDRANT_API_KEY in your .env file

**Issue**: OpenAI API errors
**Solution**: Check OPENAI_API_KEY in your .env file and ensure you have sufficient quota

**Issue**: 422 Validation Error
**Solution**: Verify that your request body matches the expected schema in the API documentation

### Checking Service Status
```bash
# Check if the API server is running
curl https://mahnoor09-deploy-hack.hf.space/health

# Check if the RAG system is accessible
curl -X POST https://mahnoor09-deploy-hack.hf.space/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "timeout": 10}'
```

## Next Steps
1. Integrate the API endpoints into your frontend application
2. Add error handling for various response scenarios
3. Implement streaming response handling for better user experience
4. Add loading indicators during query processing