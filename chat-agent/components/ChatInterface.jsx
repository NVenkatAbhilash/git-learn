import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';
import { getStoredMessages, addMessage, getChatResponse } from '../services/chatService';

const ChatInterface = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Load messages from local storage when component mounts
  useEffect(() => {
    if (isOpen) {
      const storedMessages = getStoredMessages();
      if (storedMessages.length > 0) {
        setMessages(storedMessages);
      }
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle input change
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (inputValue.trim() === '' || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    // Add to state and local storage
    addMessage(userMessage);
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get response from mock API
      const botMessage = await getChatResponse(inputValue);
      
      // Add bot response to state and local storage
      addMessage(botMessage);
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error getting chat response:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I couldn't process your request. Please try again.",
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      
      addMessage(errorMessage);
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>Chat Assistant</h3>
        <button className="close-button" onClick={onClose}>
          &times;
        </button>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>👋 Hi there! How can I help you today?</p>
          </div>
        ) : (
          messages.map(message => (
            <div 
              key={message.id} 
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-content">{message.text}</div>
              <div className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Type your message here..."
          className="chat-input"
          disabled={isLoading}
        />
        <button type="submit" className="send-button" disabled={isLoading || inputValue.trim() === ''}>
          {isLoading ? (
            <div className="loading-indicator"></div>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;