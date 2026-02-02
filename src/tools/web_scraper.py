"""Web Scraper Tool

This tool provides URL content extraction capabilities.
"""

from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import tool

from ..utils.logger import AgentLogger

logger = AgentLogger("web_scraper")


def scrape_url(
    url: str,
    timeout: int = 30,
    max_content_length: int = 10000,
) -> dict[str, Any]:
    """
    Scrape content from a URL.
    
    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds
        max_content_length: Maximum content length to return
        
    Returns:
        Dict with 'success', 'title', 'content', 'url', 'error' keys
    """
    logger.info(f"Scraping URL: {url}")
    
    # Validate URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {
                "success": False,
                "url": url,
                "title": None,
                "content": None,
                "error": "Invalid URL format",
            }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "title": None,
            "content": None,
            "error": f"URL parsing error: {e}",
        }
    
    try:
        # Fetch the page
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title
        title = None
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
        
        # Get text content
        text = soup.get_text(separator="\n", strip=True)
        
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)
        
        # Truncate if too long
        if len(content) > max_content_length:
            content = content[:max_content_length] + "\n... (content truncated)"
        
        logger.info(f"Successfully scraped {url}", {"content_length": len(content)})
        
        return {
            "success": True,
            "url": url,
            "title": title,
            "content": content,
            "error": None,
        }
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error scraping {url}: {e}")
        return {
            "success": False,
            "url": url,
            "title": None,
            "content": None,
            "error": f"HTTP {e.response.status_code}: {e.response.reason_phrase}",
        }
        
    except httpx.TimeoutException:
        logger.error(f"Timeout scraping {url}")
        return {
            "success": False,
            "url": url,
            "title": None,
            "content": None,
            "error": "Request timed out",
        }
        
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return {
            "success": False,
            "url": url,
            "title": None,
            "content": None,
            "error": str(e),
        }


@tool
def create_web_scraper_tool(url: str) -> str:
    """
    Extract content from a web page URL.
    
    Use this tool when you need to get the full text content from a specific
    web page that was found in search results.
    
    Args:
        url: The URL to scrape content from
        
    Returns:
        The extracted text content from the page or an error message
    """
    result = scrape_url(url)
    
    if result["success"]:
        title = result["title"] or "No title"
        return f"**Page Title:** {title}\n\n**Content:**\n{result['content']}"
    else:
        return f"**Failed to scrape URL:** {result['error']}"
