import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { id: 1, role: 'assistant', content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue.trim()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API - using the backend server URL
      // In Docusaurus, environment variables with REACT_APP_ prefix are available in process.env
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${backendUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage.content,
          top_k: 5
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Format response from query endpoint
      let responseText = '';
      if (data.response) {
        // Use the response field from the deployed backend
        responseText = data.response;
      } else if (data.results && data.results.length > 0) {
        // Fallback to original format if needed
        responseText = `Based on the knowledge base: ${data.results[0].content.substring(0, 300)}...`;
      } else {
        responseText = 'I couldn\'t find relevant information in the knowledge base.';
      }

      // Add assistant message
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: responseText
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I\'m having trouble connecting to the API. Please try again later.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container" style={{
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '20px',
      height: '500px',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#f9f9f9'
    }}>
      <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>AI Assistant for Physical AI & Humanoid Robotics</h3>

      <div className="chat-messages" style={{
        flex: 1,
        overflowY: 'auto',
        marginBottom: '15px',
        padding: '10px',
        backgroundColor: 'white',
        borderRadius: '4px',
        maxHeight: '70%'
      }}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
            style={{
              padding: '10px 15px',
              margin: '10px 0',
              borderRadius: '8px',
              maxWidth: '80%',
              alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: message.role === 'user' ? '#3498db' : '#ecf0f1',
              color: message.role === 'user' ? 'white' : '#2c3e50',
              marginLeft: message.role === 'user' ? 'auto' : '0',
              marginRight: message.role === 'user' ? '0' : 'auto',
              wordWrap: 'break-word'
            }}
          >
            <strong style={{ display: 'block', marginBottom: '5px', fontSize: '0.9em' }}>
              {message.role === 'user' ? 'You:' : 'Assistant:'}
            </strong>
            <div style={{ fontSize: '0.95em' }}>{message.content}</div>
          </div>
        ))}
        {isLoading && (
          <div
            className="message assistant"
            style={{
              padding: '10px 15px',
              margin: '10px 0',
              borderRadius: '8px',
              maxWidth: '80%',
              alignSelf: 'flex-start',
              backgroundColor: '#ecf0f1',
              color: '#2c3e50'
            }}
          >
            <strong style={{ display: 'block', marginBottom: '5px', fontSize: '0.9em' }}>Assistant:</strong>
            <div style={{ fontSize: '0.95em' }}>Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form" style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook..."
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '12px 15px',
            border: '1px solid #ddd',
            borderRadius: '25px',
            fontSize: '16px',
            outline: 'none'
          }}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          style={{
            padding: '12px 25px',
            backgroundColor: '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '25px',
            cursor: (isLoading || !inputValue.trim()) ? 'not-allowed' : 'pointer',
            opacity: (isLoading || !inputValue.trim()) ? 0.6 : 1
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;