# 🧪 Testing Guide for DataPilot

This guide will help you test all the features of DataPilot.

## Prerequisites

1. Backend is running on `http://localhost:8000`
2. Frontend is running on `http://localhost:5173`
3. You have configured at least one LLM provider in `.env`
4. (Optional) MongoDB is running for database tests

## Quick Health Check

### 1. Check API Status
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "llm_provider": "openai",
  "mongo_connected": true,
  "web_search_available": true
}
```

### 2. List Available Tools
```bash
curl http://localhost:8000/tools
```

## Test Queries

### Level 1: Basic Python Execution

#### Test 1: Simple Calculation
```
Calculate the first 10 Fibonacci numbers
```

Expected: Agent will execute Python code and return the numbers.

#### Test 2: Data Analysis
```
Create a dataset with 50 random numbers and calculate the mean, median, and standard deviation
```

Expected: Statistical summary of the generated data.

#### Test 3: Visualization
```
Generate 20 random points and create a scatter plot
```

Expected: Python code execution + base64 image of scatter plot.

### Level 2: Visualization Tool

#### Test 4: Line Chart
```
Create a line chart showing temperature over a week:
Monday: 72°F, Tuesday: 75°F, Wednesday: 71°F, Thursday: 68°F, Friday: 73°F, Saturday: 76°F, Sunday: 74°F
```

Expected: Line chart with days of week on x-axis and temperatures on y-axis.

#### Test 5: Bar Chart
```
Create a bar chart comparing sales by region:
North: $45000, South: $62000, East: $38000, West: $51000
```

Expected: Bar chart showing regional sales comparison.

#### Test 6: Pie Chart
```
Show me a pie chart of market share:
Company A: 35%, Company B: 28%, Company C: 22%, Company D: 15%
```

Expected: Pie chart with proper percentage labels.

### Level 3: Web Search (if configured)

#### Test 7: Current Information
```
What are the latest developments in AI technology this week?
```

Expected: Agent searches the web and summarizes recent AI news.

#### Test 8: Fact Checking
```
Search for information about the current price of Bitcoin
```

Expected: Current Bitcoin price from web search results.

### Level 4: MongoDB Queries (if configured)

#### Test 9: Simple Query
First, seed the database:
```bash
cd backend
python seed_mongodb.py
```

Then ask:
```
Query MongoDB to show me all events from January 2025
```

Expected: Results from MongoDB events collection.

#### Test 10: Aggregation
```
Query MongoDB and show me total revenue by region for 2025
```

Expected: Aggregated results grouped by region.

#### Test 11: Complex Analysis
```
Query MongoDB for 2025 data, calculate monthly revenue, and create a line chart
```

Expected: MongoDB aggregation → data → visualization.

### Level 5: Multi-Tool Workflows

#### Test 12: Data Pipeline
```
1. Query MongoDB for all electronics sales in Q1 2025
2. Calculate the average sale amount
3. Create a bar chart showing sales by month
```

Expected: Agent uses MongoDB tool → Python tool → Visualization.

#### Test 13: Research + Analysis
```
Search for current trends in renewable energy, then create a summary with key statistics
```

Expected: Web search → Python processing → formatted output.

## Testing with cURL

### Basic Chat Request
```bash
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "Calculate 15 factorial"
  }'
```

### Chat with History
```bash
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello"},
      {"role": "assistant", "content": "Hi! How can I help?"}
    ],
    "user_message": "Calculate fibonacci numbers"
  }'
```

## Frontend Testing

### 1. Open the Application
Navigate to `http://localhost:5173`

### 2. Check Status Bar
Bottom of screen should show:
- ● healthy (green)
- LLM provider name
- MongoDB connection status
- Web search availability

### 3. Try Example Queries
Click any of the example query buttons in the welcome screen.

### 4. Test Error Handling
Try an invalid query:
```
This query has no clear intent or action needed
```

The agent should respond naturally without crashing.

### 5. Test Chart Generation
Ask for any visualization - verify images appear below the chat.

### 6. Test Conversation Flow
Have a multi-turn conversation:
1. "Generate some sample data"
2. "Now create a chart from that data"
3. "What's the average value?"

## Performance Testing

### Measure Response Time
```bash
time curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Calculate 100 fibonacci numbers"}'
```

### Concurrent Requests
Use Apache Bench:
```bash
ab -n 100 -c 10 -p test.json -T application/json \
  http://localhost:8000/agent/chat
```

Where `test.json` contains:
```json
{"user_message": "Hello"}
```

## Troubleshooting Tests

### Test Fails: "LLM Error"
- Check API key is valid
- Verify you have credits/quota
- Check internet connection

### Test Fails: "MongoDB not connected"
- Start MongoDB: `brew services start mongodb-community`
- Check MONGO_URI in `.env`
- Run seed script to populate data

### Test Fails: "Web search not available"
- Set AZURE_BING_SEARCH_KEY in `.env`
- Or skip web search tests

### Charts Don't Appear
- Check browser console for errors
- Verify base64 images are in API response
- Check CORS settings

### Frontend Can't Connect
- Verify backend is running on port 8000
- Check VITE_API_BASE in frontend/.env
- Check browser network tab for CORS errors

## Expected Agent Behavior

### Good Response Patterns
✅ Uses appropriate tool for the task
✅ Provides clear explanations
✅ Handles errors gracefully
✅ Returns visualizations when appropriate
✅ Cites sources when using web search

### Red Flags
❌ Infinite loops (should stop after MAX_ITERATIONS)
❌ Wrong tool selection
❌ Crashes on invalid input
❌ No error messages
❌ Exposing sensitive data

## Success Criteria

- [ ] All Level 1 tests pass (Python execution)
- [ ] All Level 2 tests pass (Visualizations)
- [ ] Level 3 tests pass (if web search configured)
- [ ] Level 4 tests pass (if MongoDB configured)
- [ ] Level 5 tests pass (Multi-tool workflows)
- [ ] Frontend loads without errors
- [ ] Charts display correctly
- [ ] Error messages are helpful
- [ ] Response time < 10 seconds for simple queries
- [ ] No crashes or unhandled exceptions

## Automated Testing (Future)

Create `tests/test_agent.py`:
```python
import pytest
from core.agent import agent

@pytest.mark.asyncio
async def test_python_execution():
    result = await agent.run("Calculate 5 factorial")
    assert "120" in result["messages"][-1]["content"]

@pytest.mark.asyncio
async def test_visualization():
    result = await agent.run("Create a simple line chart")
    assert len(result["artifacts"]) > 0
```

Run with:
```bash
pytest tests/
```

## Reporting Issues

When reporting bugs, include:
1. The exact query that failed
2. Full error message
3. Backend logs
4. Browser console errors (for frontend issues)
5. Environment details (OS, Python version, Node version)
6. Contents of `.env` (without sensitive keys)
