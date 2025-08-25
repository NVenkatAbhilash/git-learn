import { useState, useEffect } from 'react'
import './App.css'
import WelcomePage from './components/WelcomePage'
import ChatIcon from './components/ChatIcon'
import ChatInterface from './components/ChatInterface'
import './components/WelcomePage.css'
import './components/ChatIcon.css'
import './components/ChatInterface.css'

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  // Chat agent name
  const chatAgentName = "IntelliChat";
  
  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };
  
  // Handle click outside chat interface
  const handleOutsideClick = (e) => {
    if (isChatOpen && e.target.className === 'app') {
      closeChat();
    }
  };
  
  return (
    <div className="app" onClick={handleOutsideClick}>
      <WelcomePage />
      <ChatIcon onClick={toggleChat} />
      <ChatInterface 
        isOpen={isChatOpen} 
        onClose={closeChat} 
        agentName={chatAgentName}
      />
    </div>
  )
}

export default App
