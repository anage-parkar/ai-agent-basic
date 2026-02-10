# # import httpx
# # from typing import Dict, Any, List
# # from core.config import settings


# # class WebSearchTool:
# #     """Search the web using Azure Bing Search API"""

# #     def __init__(self):
# #         self.name = "web_search"
# #         self.description = """Search the web for current information.
# # Input format: {"query": "your search query", "count": 5}
# # Returns: List of search results with name, snippet, and url"""

# #         self.api_key = settings.azure_bing_search_key
# #         self.endpoint = settings.azure_bing_search_endpoint
# #         self.available = bool(self.api_key)

# #     async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
# #         """Perform web search"""
# #         if not self.available:
# #             return {
# #                 "error": "Web search not configured. Set AZURE_BING_SEARCH_KEY in .env"
# #             }

# #         query = input_data.get("query", "")
# #         count = input_data.get("count", 5)

# #         if not query:
# #             return {"error": "Search query required"}

# #         headers = {
# #             "Ocp-Apim-Subscription-Key": self.api_key
# #         }

# #         params = {
# #             "q": query,
# #             "count": min(count, 10),  # Max 10 results
# #             "textDecorations": False,
# #             "textFormat": "Raw"
# #         }

# #         try:
# #             async with httpx.AsyncClient(timeout=30.0) as client:
# #                 response = await client.get(
# #                     self.endpoint,
# #                     headers=headers,
# #                     params=params
# #                 )
# #                 response.raise_for_status()
# #                 data = response.json()

# #             # Extract relevant information
# #             results = []
# #             for page in data.get("webPages", {}).get("value", []):
# #                 results.append({
# #                     "name": page.get("name", ""),
# #                     "snippet": page.get("snippet", ""),
# #                     "url": page.get("url", "")
# #                 })

# #             return {
# #                 "success": True,
# #                 "query": query,
# #                 "count": len(results),
# #                 "results": results
# #             }

# #         except httpx.HTTPStatusError as e:
# #             return {
# #                 "success": False,
# #                 "error": f"HTTP {e.response.status_code}: {e.response.text}"
# #             }
# #         except Exception as e:
# #             return {
# #                 "success": False,
# #                 "error": f"Search error: {str(e)}"
# #             }


# # # Global instance
# # web_search_tool = WebSearchTool()

# import httpx
# from typing import Dict, Any, List
# from core.config import settings
# from duckduckgo_search import AsyncDDGS  # pip install -U duckduckgo-search


# class WebSearchTool:
#     """🔍 Free Web Search using DuckDuckGo (No API key needed!)"""

#     def __init__(self):
#         self.name = "web_search"
#         self.description = """Search the web for current information.
# Input format: {"query": "your search query", "count": 5}
# Returns: List of search results with title, snippet, and url"""

#         # Always available - no API key!
#         self.available = True

#     async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Perform FREE web search with DuckDuckGo"""
#         query = input_data.get("query", "")
#         count = input_data.get("count", 5)

#         if not query:
#             return {"error": "Search query required"}

#         try:
#             async with AsyncDDGS() as ddgs:
#                 results = []
#                 async for result in ddgs.text(query, max_results=count):
#                     results.append({
#                         "name": result.get("title", ""),
#                         "snippet": result.get("body", ""),
#                         "url": result.get("href", "")
#                     })

#             return {
#                 "success": True,
#                 "query": query,
#                 "count": len(results),
#                 "results": results[:count]  # Ensure exact count
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
import urllib.parse


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
            # Try the duckduckgo_search library first
            try:
                from duckduckgo_search import DDGS

                results = []
                ddgs = DDGS()
                search_results = list(
                    ddgs.text(query, max_results=count * 2)
                )  # Get more to filter

                for result in search_results[:count]:
                    # Clean up the URL (decode if needed)
                    url = result.get("href", "")
                    url = self._clean_url(url)

                    # Get a better snippet
                    snippet = result.get("body", "")
                    if not snippet or len(snippet.strip()) < 10:
                        snippet = "No description available"

                    results.append(
                        {
                            "name": result.get("title", ""),
                            "snippet": snippet,
                            "url": url,
                        }
                    )

                if len(results) > 0:
                    return {
                        "success": True,
                        "query": query,
                        "count": len(results),
                        "results": results,
                    }
                else:
                    # If no results, try the API fallback
                    return await self._api_search(query, count)

            except ImportError:
                # If library not installed, use API method
                return await self._api_search(query, count)
            except Exception as e:
                print(f"DuckDuckGo library error: {e}, trying API fallback...")
                return await self._api_search(query, count)

        except Exception as e:
            return {"success": False, "error": f"Search error: {str(e)}"}

    def _clean_url(self, url: str) -> str:
        """Clean and decode URLs"""
        try:
            # Remove HTML entities
            url = url.replace("&amp;", "&")

            # If URL starts with http encoded, decode it
            if "http%3A" in url or "https%3A" in url:
                url = urllib.parse.unquote(url)

            # Extract actual URL if it's a redirect
            if "uddg=" in url:
                start = url.find("uddg=") + 5
                end = url.find("&", start)
                if end == -1:
                    decoded_url = url[start:]
                else:
                    decoded_url = url[start:end]
                url = urllib.parse.unquote(decoded_url)

            return url
        except:
            return url

    async def _api_search(self, query: str, count: int) -> Dict[str, Any]:
        """Use DuckDuckGo Instant Answer API as fallback"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # DuckDuckGo Instant Answer API
                params = {
                    "q": query,
                    "format": "json",
                    "no_html": "1",
                    "skip_disambig": "1",
                }

                response = await client.get(
                    "https://api.duckduckgo.com/", params=params, follow_redirects=True
                )

                if response.status_code == 200:
                    data = response.json()
                    results = []

                    # Get abstract if available
                    if data.get("Abstract"):
                        results.append(
                            {
                                "name": data.get("Heading", "DuckDuckGo Result"),
                                "snippet": data.get("Abstract", ""),
                                "url": self._clean_url(data.get("AbstractURL", "")),
                            }
                        )

                    # Get related topics
                    for topic in data.get("RelatedTopics", [])[:count]:
                        if isinstance(topic, dict) and "Text" in topic:
                            results.append(
                                {
                                    "name": topic.get("Text", "").split(" - ")[0]
                                    if " - " in topic.get("Text", "")
                                    else "Related",
                                    "snippet": topic.get("Text", ""),
                                    "url": self._clean_url(topic.get("FirstURL", "")),
                                }
                            )

                    if results:
                        return {
                            "success": True,
                            "query": query,
                            "count": len(results),
                            "results": results[:count],
                        }

                # If API didn't work, try web scraping method
                return await self._scrape_search(query, count)

        except Exception as e:
            print(f"API search error: {e}, trying scraping fallback...")
            return await self._scrape_search(query, count)

    async def _scrape_search(self, query: str, count: int) -> Dict[str, Any]:
        """Fallback: Scrape DuckDuckGo lite HTML"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Use DuckDuckGo Lite (simpler HTML)
                params = {"q": query, "kl": "us-en"}
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }

                response = await client.get(
                    "https://lite.duckduckgo.com/lite/",
                    params=params,
                    headers=headers,
                    follow_redirects=True,
                )

                if response.status_code == 200:
                    results = self._parse_lite_html(response.text, count)

                    return {
                        "success": True,
                        "query": query,
                        "count": len(results),
                        "results": results,
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Search returned status code {response.status_code}",
                    }

        except Exception as e:
            return {
                "success": False,
                "error": f"Scraping error: {str(e)}. Try: pip install -U duckduckgo-search --break-system-packages",
            }

    def _parse_lite_html(self, html: str, max_results: int) -> List[Dict]:
        """Parse DuckDuckGo Lite HTML results"""
        results = []

        try:
            import re

            # Split by result blocks
            parts = html.split("<tr>")

            for part in parts[1 : max_results * 3]:  # Get more to ensure we have enough
                try:
                    # Extract title and URL
                    if "uddg=" in part and "<a rel=" in part:
                        # Find the URL (encoded in uddg parameter)
                        url_match = re.search(r'uddg=([^"\'&]+)', part)
                        if url_match:
                            url = urllib.parse.unquote(url_match.group(1))
                        else:
                            continue

                        # Find the title
                        title_match = re.search(r"<a rel=[^>]+>([^<]+)</a>", part)
                        if title_match:
                            title = title_match.group(1).strip()
                            # Remove extra spaces
                            title = re.sub(r"\s+", " ", title)
                        else:
                            continue

                        # Find the snippet
                        snippet = ""
                        snippet_match = re.search(
                            r'<td class="result-snippet">([^<]+)', part
                        )
                        if snippet_match:
                            snippet = snippet_match.group(1).strip()
                            snippet = re.sub(r"\s+", " ", snippet)

                        if title and url and len(results) < max_results:
                            results.append(
                                {
                                    "name": title[:200],  # Limit length
                                    "snippet": snippet[:300]
                                    if snippet
                                    else "No description available",
                                    "url": url,
                                }
                            )
                except:
                    continue

            # If no results found, provide helpful message
            if not results:
                results = [
                    {
                        "name": "Search completed but no results found",
                        "snippet": "Try a different search query or install: pip install -U duckduckgo-search --break-system-packages",
                        "url": "https://pypi.org/project/duckduckgo-search/",
                    }
                ]

        except Exception as e:
            results = [
                {"name": "Parsing error", "snippet": f"Error: {str(e)}", "url": ""}
            ]

        return results


# Global instance
web_search_tool = WebSearchTool()
