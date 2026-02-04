import React from 'react';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  
  if (isSystem) {
    return null; // Don't display system messages
  }
  
  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-header">
        <span className="role">{isUser ? 'You' : '🤖 DataPilot'}</span>
      </div>
      <div className="message-content">
        {message.content}
      </div>
    </div>
  );
};

export default MessageBubble;
