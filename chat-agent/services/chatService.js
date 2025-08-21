// Mock API service for chat functionality

// Maximum number of messages to store in cache
const MAX_STORED_MESSAGES = 20;

// Cache key
const CACHE_KEY = 'chat_agent_messages';

// Cache expiration time (24 hours in milliseconds)
const CACHE_EXPIRATION = 24 * 60 * 60 * 1000;

/**
 * Get all messages from cache
 * @returns {Array} Array of message objects
 */
export const getStoredMessages = () => {
  try {
    const cachedData = sessionStorage.getItem(CACHE_KEY);
    if (!cachedData) return [];
    
    const { messages, timestamp } = JSON.parse(cachedData);
    
    // Check if cache has expired (24 hours)
    if (Date.now() - timestamp > CACHE_EXPIRATION) {
      sessionStorage.removeItem(CACHE_KEY);
      return [];
    }
    
    return messages;
  } catch (error) {
    console.error('Error retrieving messages from cache:', error);
    return [];
  }
};

/**
 * Save messages to cache, keeping only the most recent MAX_STORED_MESSAGES
 * @param {Array} messages Array of message objects to store
 */
export const saveMessages = (messages) => {
  try {
    // Only keep the most recent MAX_STORED_MESSAGES
    const messagesToStore = messages.slice(-MAX_STORED_MESSAGES);
    
    // Store messages with timestamp for expiration check
    const cacheData = {
      messages: messagesToStore,
      timestamp: Date.now()
    };
    
    sessionStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
  } catch (error) {
    console.error('Error saving messages to cache:', error);
  }
};

/**
 * Add a new message to storage
 * @param {Object} message Message object to add
 */
export const addMessage = (message) => {
  const messages = getStoredMessages();
  const updatedMessages = [...messages, message];
  saveMessages(updatedMessages);
  return updatedMessages;
};

/**
 * Clear all stored messages
 */
export const clearMessages = () => {
  try {
    sessionStorage.removeItem(CACHE_KEY);
  } catch (error) {
    console.error('Error clearing messages from cache:', error);
  }
};

/**
 * Mock API call to get a response from the chat agent
 * @param {string} userMessage The message sent by the user
 * @returns {Promise} Promise that resolves with a response message
 */
export const getChatResponse = (userMessage) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const responses = [
        "I'm here to help! What else would you like to know?",
        "That's an interesting question. Let me think about that.",
        "I understand your query. Here's what I can tell you...",
        "Thanks for sharing that with me. Can you tell me more?",
        "I'm processing your request. Is there anything specific you're looking for?"
      ];
      
      // For demo purposes, just return a random response
      const responseText = responses[Math.floor(Math.random() * responses.length)];
      
      resolve({
        id: Date.now(),
        text: responseText,
        sender: 'bot',
        timestamp: new Date().toISOString()
      });
    }, 1000); // 1 second delay to simulate API call
  });
};