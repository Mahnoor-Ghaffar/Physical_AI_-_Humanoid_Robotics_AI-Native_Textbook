import React from 'react';
import Layout from '@theme/Layout';
import ChatInterface from '../components/ChatInterface';

const ChatPage = () => {
  return (
    <Layout title="AI Assistant" description="Chat with the AI assistant for the Physical AI & Humanoid Robotics textbook">
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh',
        padding: '20px',
        backgroundColor: '#f5f5f5'
      }}>
        <div style={{
          width: '100%',
          maxWidth: '800px',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          padding: '20px'
        }}>
          <h1 style={{ textAlign: 'center', marginBottom: '20px', color: '#2c3e50' }}>AI Assistant for Physical AI & Humanoid Robotics</h1>
          <ChatInterface />
        </div>
      </div>
    </Layout>
  );
};

export default ChatPage;