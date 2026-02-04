# 🚀 DataPilot Quick Start Guide

## What You Have

A complete, production-ready AI agent system with:

✅ **Backend (Python/FastAPI)**
- ReAct agent loop implementation
- 4 powerful tools (Python, MongoDB, Web Search, Visualize)
- Support for OpenAI, Hugging Face, and Ollama LLMs
- Clean, modular architecture

✅ **Frontend (React/Vite)**
- Beautiful, modern chat interface  
- Real-time chart display
- Responsive design
- Health monitoring

✅ **Complete Documentation**
- Main README with full details
- Testing guide with example queries
- MongoDB seed script
- Docker setup

## 🏃 Quick Start (5 Minutes)

### Option 1: Manual Setup

```bash
# 1. Run the setup script
./setup.sh

# 2. Edit backend/.env with your API key
#    At minimum, add your OPENAI_API_KEY or other LLM provider

# 3. Start backend (Terminal 1)
cd backend
uvicorn app:app --reload --port 8000

# 4. Start frontend (Terminal 2)
cd frontend
npm run dev

# 5. Open http://localhost:5173
```

### Option 2: Docker Setup

```bash
# 1. Copy and edit environment file
cp .env.example .env
# Edit .env with your API keys

# 2. Start everything
docker-compose up -d

# 3. Open http://localhost:5173
```

## 📝 Configuration

**Minimum Required:**
Just add ONE of these to `backend/.env`:

```env
# Option A: OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# Option B: Hugging Face
LLM_PROVIDER=hf
HUGGINGFACE_API_KEY=hf_your-key-here

# Option C: Ollama (local, free)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

**Optional:**
- `MONGO_URI` - For database features
- `AZURE_BING_SEARCH_KEY` - For web search

## 🎯 Try These First

Open the web interface and try:

1. **"Calculate the first 10 Fibonacci numbers"**
   → Tests Python execution

2. **"Create a bar chart showing sales: Jan $100k, Feb $150k, Mar $200k"**
   → Tests visualization

3. **"Search for latest AI developments"** (if web search configured)
   → Tests web search

4. **"Query MongoDB for sample data"** (if MongoDB configured)
   → Tests database

## 📊 Optional: Add Sample Data

If you want to test MongoDB features:

```bash
cd backend
python seed_mongodb.py
```

Then ask: "Query MongoDB and show me revenue by region"

## 🔍 Health Check

Backend health check:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "llm_provider": "openai",
  "mongo_connected": true,
  "web_search_available": true
}
```

## 📁 Project Structure

```
ai-agent-starter/
├── backend/              # Python FastAPI server
│   ├── app.py           # Main API
│   ├── core/            # Agent & LLM logic
│   ├── tools/           # Python, Mongo, Search, Visualize
│   └── seed_mongodb.py  # Sample data generator
├── frontend/            # React UI
│   └── src/
│       ├── components/  # Chat, Messages, Charts
│       └── App.jsx      # Main component
├── README.md            # Full documentation
├── TESTING.md          # Test cases & examples
├── docker-compose.yml  # Docker setup
└── setup.sh           # Auto-setup script
```

## 🛠️ What Each Tool Does

| Tool | Purpose | Example |
|------|---------|---------|
| **python** | Execute data analysis code | "Calculate statistics for this data" |
| **mongo** | Query your database | "Show me all orders from January" |
| **web_search** | Get current information | "What's the latest news on AI?" |
| **visualize** | Create quick charts | "Plot this data as a line chart" |

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.11+)
- Check .env exists and has API key
- Run: `pip install -r requirements.txt`

**Frontend won't connect:**
- Check backend is running: `curl http://localhost:8000/health`
- Check VITE_API_BASE in frontend/.env
- Clear browser cache

**"LLM Error":**
- Verify API key is correct
- Check you have credits/quota
- Try a different model/provider

**"MongoDB not connected":**
- Start MongoDB: `brew services start mongodb-community`
- Or skip MongoDB features (Python/viz still work)

## 📚 Next Steps

1. ✅ Get the basic setup working
2. ✅ Try the example queries
3. 📖 Read the full [README.md](README.md)
4. 🧪 Explore [TESTING.md](TESTING.md) for more examples
5. 🔧 Customize the agent for your use case
6. 🚀 Deploy to production

## 🤔 How It Works

The agent follows a **ReAct loop**:

1. **Reason**: LLM thinks about what to do
2. **Act**: Chooses a tool and provides input
3. **Observe**: Gets the tool result
4. **Answer**: Forms final response

Example conversation flow:
```
User: "Calculate fibonacci and plot it"
  ↓
Agent: [Thinks: Need Python tool]
  ↓
Tool: [Executes Python code]
  ↓
Agent: [Observes: Got numbers and chart]
  ↓
Agent: "Here are the Fibonacci numbers: [1,1,2,3,5...] and here's the chart"
```

## 💡 Pro Tips

1. **Be specific**: "Create a bar chart" is better than "visualize this"
2. **Chain tasks**: "Query MongoDB, calculate average, and plot"
3. **Use Python for complex logic**: The Python tool is very powerful
4. **Check the status bar**: Shows what's connected/working

## 🆘 Need Help?

- Full docs: See [README.md](README.md)
- Test cases: See [TESTING.md](TESTING.md)
- API docs: Visit `http://localhost:8000/docs` (when backend running)
- Check backend logs for detailed error messages

## 🎉 You're Ready!

Your AI agent is ready to:
- Analyze data with Python
- Query databases
- Search the web
- Create visualizations
- Answer complex questions

Just start the servers and begin chatting! 🚀
