# How to Run the AI Native Book with Floating Chat Widget

## Prerequisites
- Node.js v18+
- Python 3.8+
- Access to OpenAI API (for backend RAG system)

## Steps

### 1. Set Up Environment Variables
Make sure your `.env` file contains:
```
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=docs_embeddings
OPENAI_MODEL=gpt-4o-mini
COHERE_MODEL=embed-multilingual-v3.0
DOCUSAURUS_BASE_URL=https://your-docs-site.com
REACT_APP_BACKEND_URL=https://mahnoor09-deploy-hack.hf.space
```
Note: The backend is already deployed at https://mahnoor09-deploy-hack.hf.space, so no need to start a local backend server.

### 2. Start the Frontend
```bash
# From project root
npm install
npm start
```


## Expected Behavior
- Visit http://localhost:3000
- You should see a chat bubble 💬 on the bottom-right corner of every page
- Clicking the bubble opens the AI assistant chat interface
- The chat connects to the backend RAG system to answer questions about the textbook

## Troubleshooting
- If the chat widget doesn't appear, check browser console for errors
- Make sure both frontend and backend servers are running
- Verify that REACT_APP_BACKEND_URL is set correctly
- Clear browser cache and Docusaurus cache (`npm run clear`)