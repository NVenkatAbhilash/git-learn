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
  
  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };
  
  return (
    <div className="app">
      <WelcomePage />
      <ChatIcon onClick={toggleChat} />
      <ChatInterface isOpen={isChatOpen} onClose={closeChat} />
    </div>
  )
}

export default App
