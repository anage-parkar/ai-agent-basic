import React, { useState, useEffect } from 'react';
import Chat from './components/Chat';
import { getHealth } from './api';
import './App.css';

function App() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const healthData = await getHealth();
      setHealth(healthData);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealth({ status: 'error', error: error.message });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="spinner-large"></div>
        <p>Connecting to DataPilot...</p>
      </div>
    );
  }

  if (health?.status === 'error') {
    return (
      <div className="app-error">
        <h1>⚠️ Connection Error</h1>
        <p>Unable to connect to the DataPilot backend.</p>
        <p className="error-detail">{health.error}</p>
        <button onClick={checkHealth} className="retry-button">
          Retry Connection
        </button>
        <div className="help-text">
          <p>Make sure the backend is running:</p>
          <code>cd backend && uvicorn app:app --reload</code>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Chat />
      
      {health && (
        <div className="status-bar">
          <span className={`status-indicator ${health.status === 'healthy' ? 'healthy' : 'error'}`}>
            ● {health.status}
          </span>
          <span className="provider-info">
            LLM: {health.llm_provider}
          </span>
          <span className="mongo-info">
            MongoDB: {health.mongo_connected ? '✓' : '✗'}
          </span>
          <span className="search-info">
            Web Search: {health.web_search_available ? '✓' : '✗'}
          </span>
        </div>
      )}
    </div>
  );
}

export default App;
