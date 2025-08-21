import React, { useState, useEffect, useRef } from 'react';
import './ChatIcon.css';

const ChatIcon = ({ onClick }) => {
  const [position, setPosition] = useState({ x: window.innerWidth - 80, y: window.innerHeight - 80 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const iconRef = useRef(null);

  // Handle mouse down event to start dragging
  const handleMouseDown = (e) => {
    if (iconRef.current) {
      const rect = iconRef.current.getBoundingClientRect();
      setDragOffset({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      });
      setIsDragging(true);
      setHasMoved(false);
    }
  };

  // Handle mouse move event during dragging
  const handleMouseMove = (e) => {
    if (isDragging) {
      setHasMoved(true);
      let newX = e.clientX - dragOffset.x;
      let newY = e.clientY - dragOffset.y;
      
      // Constrain to window boundaries
      const iconSize = 60; // Size of the icon
      const maxX = window.innerWidth - iconSize;
      const maxY = window.innerHeight - iconSize;
      
      newX = Math.max(0, Math.min(newX, maxX));
      newY = Math.max(0, Math.min(newY, maxY));
      
      // Determine which edge or corner is closest
      const leftDist = newX;
      const rightDist = maxX - newX;
      const topDist = newY;
      const bottomDist = maxY - newY;
      
      const minHorizDist = Math.min(leftDist, rightDist);
      const minVertDist = Math.min(topDist, bottomDist);
      
      // Snap to sides or corners only
      if (minHorizDist <= minVertDist) {
        // Snap horizontally first (left or right)
        newX = leftDist < rightDist ? 0 : maxX;
        
        // Then check if we should snap to a corner
        if (topDist < 50) newY = 0;
        else if (bottomDist < 50) newY = maxY;
      } else {
        // Snap vertically first (top or bottom)
        newY = topDist < bottomDist ? 0 : maxY;
        
        // Then check if we should snap to a corner
        if (leftDist < 50) newX = 0;
        else if (rightDist < 50) newX = maxX;
      }
      
      setPosition({ x: newX, y: newY });
    }
  };

  // Handle mouse up event to stop dragging
  const handleMouseUp = () => {
    setIsDragging(false);
  };
  
  // Track if we've moved during this drag session
  const [hasMoved, setHasMoved] = useState(false);

  // Add and remove event listeners
  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    } else {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    }
    
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      setPosition(prevPosition => {
        const iconSize = 60;
        const maxX = window.innerWidth - iconSize;
        const maxY = window.innerHeight - iconSize;
        
        return {
          x: Math.min(prevPosition.x, maxX),
          y: Math.min(prevPosition.y, maxY)
        };
      });
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div
      ref={iconRef}
      className={`chat-icon ${isDragging ? 'dragging' : ''}`}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`
      }}
      onMouseDown={handleMouseDown}
      onClick={(e) => {
        if (!hasMoved && !isDragging) {
          onClick(e);
        }
      }}
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
      </svg>
    </div>
  );
};

export default ChatIcon;