"""Web Search Tool using Tavily API

This tool provides web search capabilities for the Research Agent.
"""

from typing import Any

from langchain_core.tools import tool
from tavily import TavilyClient

from ..utils.config import get_tavily_api_key, get_config
from ..utils.logger import AgentLogger

logger = AgentLogger("web_search")


def get_tavily_client() -> TavilyClient:
    """Get or create Tavily client"""
    return TavilyClient(api_key=get_tavily_api_key())


def web_search(
    query: str,
    max_results: int | None = None,
    include_raw_content: bool | None = None,
) -> list[dict[str, Any]]:
    """
    Search the web for information using Tavily API.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        include_raw_content: Whether to include raw HTML content
        
    Returns:
        List of search results with url, title, content, score
    """
    config = get_config()
    
    if max_results is None:
        max_results = config.tools.web_search.max_results
    if include_raw_content is None:
        include_raw_content = config.tools.web_search.include_raw_content
    
    logger.info(f"Searching web for: {query}", {"max_results": max_results})
    
    try:
        client = get_tavily_client()
        response = client.search(
            query=query,
            max_results=max_results,
            include_answer=True,
            include_raw_content=include_raw_content,
        )
        
        results = [
            {
                "url": result.get("url", ""),
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0.0),
                "raw_content": result.get("raw_content") if include_raw_content else None,
            }
            for result in response.get("results", [])
        ]
        
        logger.info(f"Found {len(results)} results", {"query": query})
        return results
        
    except Exception as e:
        logger.error(f"Web search failed: {e}", {"query": query})
        raise


@tool
def create_web_search_tool(query: str) -> str:
    """
    Search the web for current information on a topic.
    
    Use this tool when you need to find up-to-date information from the internet.
    Returns relevant web pages with their content and URLs.
    
    Args:
        query: The search query to find information about
        
    Returns:
        A formatted string of search results with titles, content snippets, and URLs
    """
    results = web_search(query)
    
    if not results:
        return "No results found for the query."
    
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(
            f"**Result {i}:** {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Content: {result['content']}\n"
        )
    
    return "\n---\n".join(formatted)
