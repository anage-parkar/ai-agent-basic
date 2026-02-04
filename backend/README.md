# DataPilot Backend

FastAPI-based backend for the DataPilot AI agent.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn app:app --reload --port 8000
```

## API Endpoints

### GET /
Root endpoint with API info

### GET /health
Health check - returns status of all services

**Response:**
```json
{
  "status": "healthy",
  "llm_provider": "openai",
  "mongo_connected": true,
  "web_search_available": true
}
```

### GET /tools
List all available tools

**Response:**
```json
{
  "tools": [
    {
      "name": "python",
      "description": "Execute Python code..."
    },
    ...
  ]
}
```

### POST /agent/chat
Chat with the agent

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "user_message": "Calculate fibonacci numbers"
}
```

**Response:**
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Calculate fibonacci numbers"},
    {"role": "assistant", "content": "..."}
  ],
  "artifacts": ["base64_image_1", "base64_image_2"],
  "error": null
}
```

## Environment Variables

See `.env.example` for all configuration options.

### Required
- `LLM_PROVIDER`: openai, hf, or ollama
- Provider-specific API key (OPENAI_API_KEY, HUGGINGFACE_API_KEY, etc.)

### Optional
- `MONGO_URI`: MongoDB connection string
- `AZURE_BING_SEARCH_KEY`: For web search functionality
- `ALLOW_ORIGINS`: CORS allowed origins

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
black .
flake8
```

## Production Deployment

1. Set environment variables
2. Use production ASGI server (gunicorn with uvicorn workers):
   ```bash
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
3. Set up reverse proxy (nginx)
4. Enable HTTPS
5. Configure rate limiting
6. Set up monitoring

## Architecture

### ReAct Agent Loop

The agent follows this loop:
1. Receive user message
2. LLM reasons about what to do (Thought)
3. LLM chooses an action (Action + Input)
4. Execute tool and get observation
5. LLM uses observation to form final answer
6. Return response with any artifacts

### Tools

Each tool implements:
- `name`: Tool identifier
- `description`: What the tool does
- `execute(input_data)`: Async method that runs the tool

## Security

- Python execution is sandboxed
- Dangerous operations are blocked
- API keys are never exposed
- CORS is configurable
- Input validation on all endpoints
