import json
from typing import List, Dict, Any, Optional
from core.llm import llm
from core.config import settings
from tools.python_tool import python_tool
from tools.mongo_tool import mongo_tool
from tools.web_search import web_search_tool
from tools.visualize import visualize_tool


class DataAgent:
    """ReAct-style agent for data analysis"""
    
    SYSTEM_PROMPT = """You are DataPilot, an expert data analysis agent. You can help users analyze data, create visualizations, query databases, and search the web.

You have access to these tools:

1. **python** - Execute Python code for data analysis
   - Allowed libraries: pandas, numpy, matplotlib, seaborn, datetime, math, statistics, json, collections, re
   - Use for: calculations, data manipulation, creating charts
   - Input: {"code": "python code here"}

2. **mongo** - Query MongoDB database
   - Use for: retrieving data from the analytics database
   - For find: {"collection": "events", "query": {...}, "limit": 100}
   - For aggregate: {"collection": "events", "pipeline": [...]}

3. **web_search** - Search the web for current information
   - Use for: finding recent information, news, facts
   - Input: {"query": "search query", "count": 5}

4. **visualize** - Create quick visualizations
   - Supported types: line, bar, scatter, pie
   - Input: {"type": "line", "data": {"x": [...], "y": [...]}, "title": "...", "xlabel": "...", "ylabel": "..."}

**How to respond:**

When you need to use a tool, respond with JSON in this exact format:
```json
{
  "thought": "I need to query the database to get the revenue data",
  "action": "mongo",
  "input": {"collection": "events", "pipeline": [...]}
}
```

After receiving tool results, provide your final answer in plain text explaining what you found.

**Important guidelines:**
- Think step by step
- Use tools when needed to gather information
- Provide clear, helpful answers
- If you encounter errors, explain them clearly
- Always cite your sources when using web search
"""
    
    def __init__(self):
        self.tools = {
            "python": python_tool,
            "mongo": mongo_tool,
            "web_search": web_search_tool,
            "visualize": visualize_tool
        }
        self.max_iterations = settings.max_iterations
    
    async def run(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Run the agent with ReAct loop"""
        if conversation_history is None:
            conversation_history = []
        
        # Initialize conversation with system prompt
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Storage for artifacts (images)
        artifacts = []
        
        # ReAct loop
        for iteration in range(self.max_iterations):
            # Get LLM response
            try:
                response = await llm.chat(messages)
            except Exception as e:
                return {
                    "messages": messages + [{"role": "assistant", "content": f"Error: {str(e)}"}],
                    "artifacts": artifacts,
                    "error": str(e)
                }
            
            # Check if response contains action (JSON format)
            action_data = self._extract_action(response)
            
            if action_data:
                # Execute tool
                action = action_data.get("action")
                thought = action_data.get("thought", "")
                tool_input = action_data.get("input", {})
                
                if action not in self.tools:
                    error_msg = f"Unknown tool: {action}. Available tools: {', '.join(self.tools.keys())}"
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": f"Error: {error_msg}. Please try again."})
                    continue
                
                # Execute tool
                tool = self.tools[action]
                observation = await tool.execute(tool_input)
                
                # Collect images/artifacts
                if "images" in observation:
                    artifacts.extend(observation["images"])
                elif "image" in observation:
                    artifacts.append(observation["image"])
                
                # Add to conversation
                messages.append({"role": "assistant", "content": response})
                
                # Create observation message
                obs_text = f"Tool '{action}' result:\n{json.dumps(observation, indent=2)}"
                messages.append({"role": "user", "content": obs_text})
                
            else:
                # No action detected - this is the final answer
                messages.append({"role": "assistant", "content": response})
                break
        
        return {
            "messages": messages,
            "artifacts": artifacts
        }
    
    def _extract_action(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract action JSON from LLM response"""
        # Look for JSON blocks
        import re
        
        # Try to find JSON in code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        if matches:
            try:
                return json.loads(matches[0])
            except json.JSONDecodeError:
                pass
        
        # Try to find raw JSON
        try:
            # Find content between first { and last }
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_str = text[start:end+1]
                data = json.loads(json_str)
                # Verify it has required fields
                if "action" in data:
                    return data
        except json.JSONDecodeError:
            pass
        
        return None


# Global agent instance
agent = DataAgent()
