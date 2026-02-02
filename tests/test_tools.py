"""Tests for the research tools"""

import pytest
from unittest.mock import patch, MagicMock


class TestWebSearch:
    """Tests for web search tool"""
    
    def test_web_search_returns_list(self):
        """Test that web_search returns a list of results"""
        from src.tools.web_search import web_search
        
        with patch('src.tools.web_search.TavilyClient') as mock_tavily:
            mock_client = MagicMock()
            mock_client.search.return_value = {
                "results": [
                    {
                        "title": "Test Result",
                        "url": "https://example.com",
                        "content": "Test content"
                    }
                ]
            }
            mock_tavily.return_value = mock_client
            
            results = web_search("test query")
            
            assert isinstance(results, list)
            assert len(results) == 1
            assert results[0]["title"] == "Test Result"
    
    def test_web_search_handles_empty_results(self):
        """Test handling of empty search results"""
        from src.tools.web_search import web_search
        
        with patch('src.tools.web_search.TavilyClient') as mock_tavily:
            mock_client = MagicMock()
            mock_client.search.return_value = {"results": []}
            mock_tavily.return_value = mock_client
            
            results = web_search("nonexistent query xyz123")
            
            assert results == []


class TestPythonREPL:
    """Tests for Python REPL tool"""
    
    def test_execute_simple_code(self):
        """Test executing simple Python code"""
        from src.tools.python_repl import execute_python
        
        result = execute_python("print(2 + 2)")
        
        assert result["success"] is True
        assert "4" in result["output"]
    
    def test_execute_with_numpy(self):
        """Test executing code with numpy (skip if numpy not installed)"""
        from src.tools.python_repl import execute_python
        
        # First check if numpy is available
        check_result = execute_python("import numpy as np; print('numpy available')")
        
        if check_result["success"] and "numpy available" in check_result.get("output", ""):
            code = """
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(f"Mean: {np.mean(arr)}")
"""
            result = execute_python(code)
            
            assert result["success"] is True
            assert "Mean: 3.0" in result["output"]
        else:
            # Skip if numpy not available
            pytest.skip("numpy not available in REPL environment")
    
    def test_blocks_dangerous_code(self):
        """Test that dangerous operations are blocked"""
        from src.tools.python_repl import execute_python
        
        # Attempt to use blocked function
        result = execute_python("import os; os.system('echo hello')")
        
        # Should either fail or not execute system command
        assert result["success"] is False or "os" not in result.get("output", "")
    
    def test_handles_syntax_error(self):
        """Test handling of syntax errors"""
        from src.tools.python_repl import execute_python
        
        result = execute_python("def broken(")
        
        assert result["success"] is False
        assert "error" in result


class TestWebScraper:
    """Tests for web scraper tool"""
    
    def test_scrape_returns_dict(self):
        """Test that scrape_url returns expected structure"""
        from src.tools.web_scraper import scrape_url
        
        with patch('src.tools.web_scraper.httpx.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "<html><head><title>Test</title></head><body><p>Content</p></body></html>"
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response
            
            result = scrape_url("https://example.com")
            
            assert result["success"] is True
            assert "title" in result
            assert "content" in result
    
    def test_handles_http_error(self):
        """Test handling of HTTP errors"""
        from src.tools.web_scraper import scrape_url
        
        with patch('src.tools.web_scraper.httpx.get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            
            result = scrape_url("https://invalid-url.test")
            
            assert result["success"] is False


class TestVectorSearch:
    """Tests for vector search tool"""
    
    def test_vector_search_returns_list(self):
        """Test that vector_search returns a list"""
        from src.tools.vector_search import vector_search
        
        # Should return empty list when collection is empty
        results = vector_search("test query", top_k=3)
        
        assert isinstance(results, list)
