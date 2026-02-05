# import httpx
# from typing import Dict, Any, List
# from core.config import settings


# class WebSearchTool:
#     """Search the web using Azure Bing Search API"""
    
#     def __init__(self):
#         self.name = "web_search"
#         self.description = """Search the web for current information.
# Input format: {"query": "your search query", "count": 5}
# Returns: List of search results with name, snippet, and url"""
        
#         self.api_key = settings.azure_bing_search_key
#         self.endpoint = settings.azure_bing_search_endpoint
#         self.available = bool(self.api_key)
    
#     async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Perform web search"""
#         if not self.available:
#             return {
#                 "error": "Web search not configured. Set AZURE_BING_SEARCH_KEY in .env"
#             }
        
#         query = input_data.get("query", "")
#         count = input_data.get("count", 5)
        
#         if not query:
#             return {"error": "Search query required"}
        
#         headers = {
#             "Ocp-Apim-Subscription-Key": self.api_key
#         }
        
#         params = {
#             "q": query,
#             "count": min(count, 10),  # Max 10 results
#             "textDecorations": False,
#             "textFormat": "Raw"
#         }
        
#         try:
#             async with httpx.AsyncClient(timeout=30.0) as client:
#                 response = await client.get(
#                     self.endpoint,
#                     headers=headers,
#                     params=params
#                 )
#                 response.raise_for_status()
#                 data = response.json()
            
#             # Extract relevant information
#             results = []
#             for page in data.get("webPages", {}).get("value", []):
#                 results.append({
#                     "name": page.get("name", ""),
#                     "snippet": page.get("snippet", ""),
#                     "url": page.get("url", "")
#                 })
            
#             return {
#                 "success": True,
#                 "query": query,
#                 "count": len(results),
#                 "results": results
#             }
            
#         except httpx.HTTPStatusError as e:
#             return {
#                 "success": False,
#                 "error": f"HTTP {e.response.status_code}: {e.response.text}"
#             }
#         except Exception as e:
#             return {
#                 "success": False,
#                 "error": f"Search error: {str(e)}"
#             }


# # Global instance
# web_search_tool = WebSearchTool()

import httpx
from typing import Dict, Any, List
from core.config import settings
from duckduckgo_search import AsyncDDGS  # pip install -U duckduckgo-search


class WebSearchTool:
    """🔍 Free Web Search using DuckDuckGo (No API key needed!)"""
    
    def __init__(self):
        self.name = "web_search"
        self.description = """Search the web for current information.
Input format: {"query": "your search query", "count": 5}
Returns: List of search results with title, snippet, and url"""
        
        # Always available - no API key!
        self.available = True
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform FREE web search with DuckDuckGo"""
        query = input_data.get("query", "")
        count = input_data.get("count", 5)
        
        if not query:
            return {"error": "Search query required"}
        
        try:
            async with AsyncDDGS() as ddgs:
                results = []
                async for result in ddgs.text(query, max_results=count):
                    results.append({
                        "name": result.get("title", ""),
                        "snippet": result.get("body", ""),
                        "url": result.get("href", "")
                    })
            
            return {
                "success": True,
                "query": query,
                "count": len(results),
                "results": results[:count]  # Ensure exact count
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Search error: {str(e)}"
            }


# Global instance
web_search_tool = WebSearchTool()
