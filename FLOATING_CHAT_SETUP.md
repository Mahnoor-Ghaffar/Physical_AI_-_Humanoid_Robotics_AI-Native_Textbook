# Floating Chat Widget Setup

## Overview
The AI Native Book website includes a floating chat widget that appears as a chat bubble on the bottom-right corner of every page. When clicked, it opens a chat interface that connects to the backend RAG system.

## How it Works
1. The floating chat widget is implemented as a React component (`src/components/FloatingChatWidget.jsx`)
2. It's injected into every page via a Docusaurus plugin (`src/plugins/floating-chat-plugin/`)
3. The widget communicates with the backend API server running on port 8000

## Prerequisites
- Node.js (v18 or higher)
- Python (3.8 or higher)
- Backend API server dependencies (see backend/requirements.txt)

## Setup Instructions

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Make sure your `.env` file contains the required API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
CLIENT_BACKEND_URL=https://mahnoor09-deploy-hack.hf.space
```


### 3. Start the Frontend (in a new terminal)
```bash
# From the project root
npm install
npm start
```

## Troubleshooting

### Chat Widget Not Appearing
- Verify that the backend server is accessible at https://mahnoor09-deploy-hack.hf.space
- Check browser console for JavaScript errors
- Ensure the Docusaurus build completed successfully

### API Connection Issues
- Make sure all required environment variables are set
- Verify that the backend API server is accessible
- Check the network tab in browser dev tools for failed requests

### Build Issues
- Clean the Docusaurus cache: `npm run clear`
- Reinstall node modules: `rm -rf node_modules && npm install`

## Configuration
The chat widget uses the following API endpoint:
- Backend URL: `https://mahnoor09-deploy-hack.hf.space/chat` (configurable via CLIENT_BACKEND_URL environment variable)
- Request format: JSON with messages array, model, temperature, and max_tokens
- Response format: JSON with response field containing the AI-generated text

## Files Structure
- `src/components/FloatingChatWidget.jsx` - Main chat widget component
- `src/plugins/floating-chat-plugin/` - Docusaurus plugin to inject widget on all pages
- `src/components/ChatInterface.jsx` - Core chat interface component
- `backend/api_server.py` - Backend API server with chat endpoint
- `.env` - Environment variables including CLIENT_BACKEND_URL