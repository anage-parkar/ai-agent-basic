import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import ChartPreview from './ChartPreview';
import { chatWithAgent } from '../api';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [artifacts, setArtifacts] = useState([]);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, artifacts]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || loading) {
      return;
    }

    const userMessage = input.trim();
    setInput('');
    setError(null);
    setLoading(true);

    // Add user message to UI immediately
    const newMessages = [...messages, { role: 'user', content: userMessage }];
    setMessages(newMessages);

    try {
      // Call API
      const response = await chatWithAgent(messages, userMessage);
      
      // Update messages with full conversation
      setMessages(response.messages);
      
      // Update artifacts (charts/images)
      if (response.artifacts && response.artifacts.length > 0) {
        setArtifacts(response.artifacts);
      }
      
      // Handle errors from agent
      if (response.error) {
        setError(response.error);
      }
      
    } catch (err) {
      console.error('Chat error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to get response from agent');
      
      // Add error message to chat
      setMessages([
        ...newMessages,
        { 
          role: 'assistant', 
          content: `Sorry, I encountered an error: ${err.response?.data?.detail || err.message}` 
        }
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleClear = () => {
    setMessages([]);
    setArtifacts([]);
    setError(null);
    setInput('');
  };

  const exampleQueries = [
    "Show me a simple line chart with dates and values",
    "Execute Python code to calculate fibonacci numbers",
    "Search the web for latest AI trends",
    "Query MongoDB for sample data"
  ];

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🤖 DataPilot Agent</h1>
        <p>Your AI assistant for data analysis</p>
        {messages.length > 0 && (
          <button onClick={handleClear} className="clear-button">
            Clear Chat
          </button>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <h2>Welcome to DataPilot! 👋</h2>
            <p>I can help you with:</p>
            <ul>
              <li>📊 Data analysis with Python (pandas, numpy, matplotlib)</li>
              <li>🗄️ MongoDB queries and aggregations</li>
              <li>🔍 Web search for current information</li>
              <li>📈 Creating visualizations and charts</li>
            </ul>
            <div className="example-queries">
              <p><strong>Try asking:</strong></p>
              {exampleQueries.map((query, idx) => (
                <button
                  key={idx}
                  className="example-button"
                  onClick={() => setInput(query)}
                >
                  {query}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <MessageBubble key={idx} message={msg} />
            ))}
            
            {artifacts.length > 0 && (
              <div className="artifacts-section">
                <h3>📊 Generated Charts</h3>
                <ChartPreview images={artifacts} />
              </div>
            )}
            
            {loading && (
              <div className="loading-indicator">
                <div className="spinner"></div>
                <span>DataPilot is thinking...</span>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="error-banner">
          <strong>⚠️ Error:</strong> {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask DataPilot anything..."
          disabled={loading}
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={loading || !input.trim()}
          className="send-button"
        >
          {loading ? '⏳' : '📤'} Send
        </button>
      </form>
    </div>
  );
};

export default Chat;
