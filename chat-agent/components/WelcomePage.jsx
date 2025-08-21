import React from 'react';

const WelcomePage = () => {
  return (
    <div className="welcome-page">
      <div className="welcome-content">
        <h1>Welcome to Chat Agent</h1>
        <p>Your intelligent conversation assistant</p>
        <p className="welcome-description">
          This application features a draggable chat icon that you can position anywhere on the screen.
          Click on the icon to start a conversation with our AI assistant.
        </p>
        <div className="welcome-instructions">
          <h2>How to use:</h2>
          <ul>
            <li>Drag the chat icon to your preferred position</li>
            <li>Click the icon to open the chat interface</li>
            <li>Type your message and press Enter</li>
            <li>View the AI's response in the conversation</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default WelcomePage;