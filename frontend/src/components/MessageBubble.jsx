// import React from 'react';

// const MessageBubble = ({ message }) => {
//   const isUser = message.role === 'user';
//   const isSystem = message.role === 'system';
  
//   if (isSystem) {
//     return null; // Don't display system messages
//   }
  
//   return (
//     <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
//       <div className="message-header">
//         <span className="role">{isUser ? 'You' : '🤖 DataPilot'}</span>
//       </div>
//       <div className="message-content">
//         {message.content}
//       </div>
//     </div>
//   );
// };

// export default MessageBubble;

import React from 'react';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  
  // Don't display system messages
  if (isSystem) {
    return null;
  }
  
  // Filter out tool execution messages (JSON responses and tool results)
  if (isUser) {
    // Hide user messages that are tool results
    const content = message.content.toLowerCase();
    if (content.includes("tool '") && content.includes("result:")) {
      return null;
    }
    if (content.includes("now provide a natural language response")) {
      return null;
    }
  }
  
  // Filter out assistant messages that are JSON (tool calls)
  if (!isUser) {
    const content = message.content.trim();
    // Check if it's a JSON object with "thought" and "action"
    if (content.startsWith('{') && content.includes('"thought"') && content.includes('"action"')) {
      return null;
    }
    // Also hide if it's wrapped in code blocks
    if (content.includes('```json') || (content.includes('"thought"') && content.includes('"input"'))) {
      return null;
    }
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