# 🤖 DataPilot - AI Data Analysis Agent

A full-stack AI agent application built with **Python FastAPI** (backend) and **React** (frontend). DataPilot can execute Python code, query MongoDB, search the web, and create visualizations—all through a conversational interface powered by LLMs.

![DataPilot Banner](https://img.shields.io/badge/AI-Agent-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green) ![React](https://img.shields.io/badge/React-18.2-blue)

## ✨ Features

- 🧠 **ReAct Agent Loop**: Reason → Act → Observe loop for intelligent decision-making
- 🐍 **Python Code Execution**: Run pandas, numpy, matplotlib code safely
- 🗄️ **MongoDB Integration**: Query and aggregate data from your database
- 🔍 **Web Search**: Search the web using Azure Bing Search API
- 📊 **Visualizations**: Auto-generate charts and graphs
- 🎨 **Beautiful UI**: Modern, responsive React interface
- 🔄 **Multiple LLM Support**: OpenAI, Hugging Face, or local Ollama

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │────────▶│   FastAPI    │────────▶│     LLM     │
│  Frontend   │  HTTP   │   Backend    │   API   │  (OpenAI/   │
│             │◀────────│              │◀────────│  HF/Ollama) │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ├──▶ Python Execution
                              ├──▶ MongoDB Queries
                              ├──▶ Web Search
                              └──▶ Visualizations
```

## 📁 Project Structure

```
ai-agent-starter/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend Docker config
│   ├── .env.example          # Environment variables template
│   ├── core/
│   │   ├── agent.py          # ReAct agent implementation
│   │   ├── config.py         # Configuration management
│   │   └── llm.py            # LLM abstraction layer
│   └── tools/
│       ├── python_tool.py    # Python code execution
│       ├── mongo_tool.py     # MongoDB queries
│       ├── web_search.py     # Web search
│       └── visualize.py      # Chart generation
└── frontend/
    ├── src/
    │   ├── App.jsx           # Main React component
    │   ├── main.jsx          # Entry point
    │   ├── api.js            # API client
    │   ├── App.css           # Styles
    │   └── components/
    │       ├── Chat.jsx      # Chat interface
    │       ├── MessageBubble.jsx
    │       └── ChartPreview.jsx
    ├── package.json          # Node dependencies
    ├── vite.config.js        # Vite configuration
    └── Dockerfile            # Frontend Docker config
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (optional, for database features)
- An LLM API key (OpenAI, Hugging Face, or Ollama locally)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

   The UI will be available at `http://localhost:5173`

## ⚙️ Configuration

### Backend (.env)

```env
# LLM Provider (openai, hf, ollama)
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4

# Hugging Face Configuration
HUGGINGFACE_API_KEY=hf_your-key-here
HUGGINGFACE_MODEL=meta-llama/Llama-2-70b-chat-hf

# Ollama Configuration (for local LLMs)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=analytics

# Azure Bing Search (Optional)
AZURE_BING_SEARCH_KEY=your-bing-key
AZURE_BING_SEARCH_ENDPOINT=https://api.bing.microsoft.com/v7.0/search

# CORS
ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_BASE=http://localhost:8000
```

## 🛠️ Available Tools

### 1. Python Tool
Execute Python code with access to data science libraries:
- pandas, numpy, matplotlib, seaborn
- datetime, math, statistics, json
- Safely sandboxed execution
- Automatic chart capture

**Example:**
```python
import pandas as pd
import matplotlib.pyplot as plt

data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]}
df = pd.DataFrame(data)

plt.plot(df['x'], df['y'])
plt.title('Sample Plot')
plt.show()
```

### 2. MongoDB Tool
Query your MongoDB database:
- **Find queries**: Simple document retrieval
- **Aggregation pipelines**: Complex data transformations

**Example:**
```json
{
  "collection": "events",
  "pipeline": [
    {"$match": {"date": {"$gte": "2026-01-01"}}},
    {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}}
  ]
}
```

### 3. Web Search Tool
Search the web for current information using Azure Bing Search.

**Example:**
```json
{
  "query": "latest developments in AI",
  "count": 5
}
```

### 4. Visualize Tool
Quickly create charts without writing code:
- Line, bar, scatter, and pie charts
- Automatic styling

**Example:**
```json
{
  "type": "bar",
  "data": {"x": ["Q1", "Q2", "Q3", "Q4"], "y": [100, 150, 200, 180]},
  "title": "Quarterly Revenue",
  "xlabel": "Quarter",
  "ylabel": "Revenue ($K)"
}
```

## 💬 Example Queries

Try asking DataPilot:

1. **"Calculate the first 10 Fibonacci numbers and plot them"**
   - Uses Python tool to compute and visualize

2. **"Query MongoDB for all events in January 2026 and show revenue by region"**
   - Uses MongoDB aggregation + visualization

3. **"Search for recent AI breakthroughs and summarize the top 3"**
   - Uses web search to get current information

4. **"Create a bar chart showing sales by product category"**
   - Uses visualize tool for quick charts

## 🐳 Docker Deployment

### Using Docker Compose

1. **Create docker-compose.yml:**
   ```yaml
   version: '3.8'
   
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       env_file:
         - ./backend/.env
       depends_on:
         - mongo
     
     frontend:
       build: ./frontend
       ports:
         - "5173:5173"
       environment:
         - VITE_API_BASE=http://localhost:8000
     
     mongo:
       image: mongo:7
       ports:
         - "27017:27017"
       volumes:
         - mongo-data:/data/db
   
   volumes:
     mongo-data:
   ```

2. **Run:**
   ```bash
   docker-compose up -d
   ```

### Individual Containers

**Backend:**
```bash
cd backend
docker build -t datapilot-api .
docker run -p 8000:8000 --env-file .env datapilot-api
```

**Frontend:**
```bash
cd frontend
docker build -t datapilot-web .
docker run -p 5173:5173 -e VITE_API_BASE=http://localhost:8000 datapilot-web
```

## 🧪 Testing the Agent

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. List Available Tools
```bash
curl http://localhost:8000/tools
```

### 3. Chat with Agent
```bash
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "Calculate fibonacci numbers up to 10"
  }'
```

## 📊 Sample MongoDB Data

To test MongoDB features, seed some sample data:

```python
from pymongo import MongoClient
from datetime import datetime
import random

client = MongoClient("mongodb://localhost:27017")
db = client.analytics
events = db.events

# Clear existing data
events.delete_many({})

# Insert sample events
for i in range(100):
    events.insert_one({
        "date": datetime(2026, 1, random.randint(1, 31)),
        "amount": round(random.uniform(10, 500), 2),
        "region": random.choice(["North", "South", "East", "West"]),
        "category": random.choice(["Electronics", "Clothing", "Food", "Books"])
    })

print(f"Inserted {events.count_documents({})} documents")
```

## 🔒 Security Considerations

- **Python Execution**: Sandboxed with restricted imports
- **API Keys**: Never expose in frontend, use environment variables
- **MongoDB**: Use authentication in production
- **CORS**: Restrict origins in production
- **Rate Limiting**: Implement for production use

## 🎯 Roadmap

- [ ] Add streaming responses (Server-Sent Events)
- [ ] SQL database support (PostgreSQL)
- [ ] File upload and CSV analysis
- [ ] Vector database integration for memory
- [ ] Multi-turn conversation context
- [ ] User authentication (JWT/OAuth)
- [ ] Advanced visualizations (Plotly, Altair)
- [ ] Export reports (PDF/DOCX)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🆘 Troubleshooting

### Backend won't start
- Check that all required environment variables are set
- Verify Python version is 3.11+
- Ensure MongoDB is running (if using mongo tool)

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check VITE_API_BASE in frontend/.env
- Ensure CORS is configured correctly

### LLM errors
- Verify API key is valid
- Check you have sufficient credits/quota
- For Ollama, ensure the model is downloaded

### MongoDB connection fails
- Check MONGO_URI is correct
- Ensure MongoDB is running
- Verify database name exists

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Ollama](https://ollama.ai/)

---

Built with ❤️ by the DataPilot team
#   a i - a g e n t - b a s i c  
 