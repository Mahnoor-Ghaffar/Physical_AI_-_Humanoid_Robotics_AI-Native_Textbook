import React, { useState, useEffect, useRef } from 'react';

const FloatingChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, role: 'assistant', content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Note: We can't use useLocation hook here since this component is rendered outside router context
  // Navigation-based chat closing functionality has been removed to avoid router dependency

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
    <>
      {/* Floating Chat Icon */}
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: '99999', // Increased z-index to ensure it's always on top
          pointerEvents: 'auto', // Ensure the button receives click events
        }}
      >
        {!isOpen ? (
          <button
            onClick={() => setIsOpen(true)}
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              backgroundColor: '#3498db',
              color: 'white',
              border: '2px solid white',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '24px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.25), 0 0 0 2px rgba(255, 255, 255, 0.5)', // Added border effect for better visibility
              transition: 'all 0.3s ease',
              outline: 'none',
            }}
            aria-label="Open chat"
          >
            💬
          </button>
        ) : null}
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '350px',
            height: '500px',
            backgroundColor: 'white',
            borderRadius: '12px',
            boxShadow: '0 8px 30px rgba(0, 0, 0, 0.2)',
            display: 'flex',
            flexDirection: 'column',
            zIndex: '9999',
            border: '1px solid #e0e0e0',
            fontFamily: 'sans-serif',
          }}
        >
          {/* Header */}
          <div
            style={{
              backgroundColor: '#3498db',
              color: 'white',
              padding: '15px',
              borderTopLeftRadius: '12px',
              borderTopRightRadius: '12px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <h3 style={{ margin: 0, fontSize: '16px' }}>AI Assistant</h3>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: 'none',
                border: 'none',
                color: 'white',
                fontSize: '18px',
                cursor: 'pointer',
                padding: '0',
                width: '24px',
                height: '24px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div
            className="chat-messages"
            style={{
              flex: 1,
              padding: '15px',
              overflowY: 'auto',
              backgroundColor: '#f9f9f9',
            }}
          >
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role}`}
                style={{
                  padding: '10px 12px',
                  margin: '8px 0',
                  borderRadius: '18px',
                  maxWidth: '80%',
                  alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
                  backgroundColor: message.role === 'user' ? '#3498db' : '#e9ecef',
                  color: message.role === 'user' ? 'white' : '#2c3e50',
                  marginLeft: message.role === 'user' ? 'auto' : '0',
                  marginRight: message.role === 'user' ? '0' : '0',
                  wordWrap: 'break-word',
                  fontSize: '14px',
                }}
              >
                <strong style={{ display: 'block', marginBottom: '4px', fontSize: '12px' }}>
                  {message.role === 'user' ? 'You:' : 'Assistant:'}
                </strong>
                <div>{message.content}</div>
              </div>
            ))}
            {isLoading && (
              <div
                className="message assistant"
                style={{
                  padding: '10px 12px',
                  margin: '8px 0',
                  borderRadius: '18px',
                  maxWidth: '80%',
                  alignSelf: 'flex-start',
                  backgroundColor: '#e9ecef',
                  color: '#2c3e50',
                  fontSize: '14px',
                }}
              >
                <strong style={{ display: 'block', marginBottom: '4px', fontSize: '12px' }}>Assistant:</strong>
                <div>Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form
            onSubmit={handleSubmit}
            style={{
              padding: '12px',
              backgroundColor: 'white',
              borderBottomLeftRadius: '12px',
              borderBottomRightRadius: '12px',
              borderTop: '1px solid #eee',
            }}
          >
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask about the textbook..."
                disabled={isLoading}
                style={{
                  flex: 1,
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '20px',
                  fontSize: '14px',
                  outline: 'none',
                }}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                style={{
                  padding: '12px 16px',
                  backgroundColor: '#3498db',
                  color: 'white',
                  border: 'none',
                  borderRadius: '20px',
                  cursor: (isLoading || !inputValue.trim()) ? 'not-allowed' : 'pointer',
                  opacity: (isLoading || !inputValue.trim()) ? 0.6 : 1,
                  fontSize: '14px',
                }}
              >
                Send
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
};

export default FloatingChatWidget;