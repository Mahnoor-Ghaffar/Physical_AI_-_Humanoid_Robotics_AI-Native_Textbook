import React from 'react';
import ReactDOM from 'react-dom/client';
import FloatingChatWidget from '../../components/FloatingChatWidget';

// Create the root element if it doesn't exist
if (typeof document !== 'undefined') {
  const initFloatingChat = () => {
    console.log('Initializing floating chat...');

    // Find or create the chat root element
    let chatRoot = document.getElementById('floating-chat-root');

    // If the element doesn't exist, create it and append to body
    if (!chatRoot) {
      chatRoot = document.createElement('div');
      chatRoot.id = 'floating-chat-root';
      document.body.appendChild(chatRoot);
      console.log('Floating chat root element created and appended to body');
    }

    // Small delay to ensure DOM element is properly attached
    requestAnimationFrame(() => {
      try {
        if (chatRoot && document.body.contains(chatRoot)) {
          const root = ReactDOM.createRoot(chatRoot);
          root.render(<FloatingChatWidget />);
          console.log('Floating chat widget rendered successfully');
        } else {
          console.error('Failed to render floating chat widget: root element not attached to DOM');
        }
      } catch (error) {
        console.error('Error rendering floating chat widget:', error);
      }
    });
  };

  // Initialize the floating chat widget when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFloatingChat);
  } else {
    // Use requestAnimationFrame to ensure DOM is ready
    requestAnimationFrame(initFloatingChat);
  }
}