"""Web search capabilities using Tavily API."""
import httpx
from typing import List, Dict, Any
from loguru import logger
from backend.config import settings

class WebSearchMCP:
    """Web search using Tavily API directly."""
    
    def __init__(self):
        """Initialize web search client."""
        self.api_key = settings.tavily_api_key
        self.base_url = "https://api.tavily.com"
        
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform web search for mathematical content.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        logger.info(f"Performing web search for: {query[:100]}...")
        
        if not self.api_key:
            logger.warning("Tavily API key not configured, returning empty results")
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "search_depth": "advanced",
                        "max_results": max_results,
                        "include_answer": True,
                        "include_domains": [
                            "wikipedia.org",
                            "mathworld.wolfram.com",
                            "khanacademy.org",
                            "brilliant.org",
                            "math.stackexchange.com"
                        ]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    logger.info(f"Found {len(results)} web search results")
                    return results
                else:
                    logger.error(f"Web search failed with status {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []

    def format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results for LLM context.
        
        Args:
            results: List of search results
            
        Returns:
            Formatted string
        """
        if not results:
            return "No web search results found."
        
        formatted = "Web Search Results:\n\n"
        for idx, result in enumerate(results, 1):
            formatted += f"{idx}. {result.get('title', 'No title')}\n"
            formatted += f"   URL: {result.get('url', 'No URL')}\n"
            formatted += f"   Content: {result.get('content', 'No content')[:300]}...\n\n"
        
        return formatted
