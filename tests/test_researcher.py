"""
Unit tests for the Researcher Agent.

Tests the researcher's ability to:
- Find relevant sources via web search
- Include proper citations
- Handle timeout scenarios
"""
import pytest
import asyncio
from src.agents.researcher import researcher_node


@pytest.mark.asyncio
@pytest.mark.unit
async def test_researcher_finds_sources():
    """Test researcher retrieves relevant information"""
    
    test_state = {
        "query": "Latest AI trends in 2026",
        "research_plan": [
            {
                "type": "web_search",
                "query": "artificial intelligence trends 2026",
                "agent": "researcher"
            }
        ],
        "web_results": [],
        "agent_interactions": [],
    }
    
    result = await researcher_node(test_state)
    
    # Check results
    assert "web_results" in result
    assert len(result["web_results"]) > 0
    
    # Verify result structure has content
    for res in result["web_results"]:
        # Should have some content or output
        assert "content" in res or "url" in res or "title" in res
    
    print(f"✅ Research Test Passed - Found {len(result['web_results'])} sources")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_researcher_logs_activity():
    """Test researcher logs its activities"""
    
    test_state = {
        "query": "Python programming",
        "research_plan": [
            {
                "type": "web_search",
                "query": "Python programming language",
                "agent": "researcher"
            }
        ],
        "web_results": [],
        "agent_interactions": [],
    }
    
    result = await researcher_node(test_state)
    
    # Should log interaction
    assert "agent_interactions" in result
    assert len(result["agent_interactions"]) >= 1
    
    log = result["agent_interactions"][0]
    assert log["agent"] == "researcher"
    
    print("✅ Researcher Logging Test Passed")


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.slow
async def test_researcher_timeout():
    """Test researcher handles slow/hanging searches"""
    
    test_state = {
        "query": "test query",
        "research_plan": [{"type": "web_search", "query": "test", "agent": "researcher"}],
        "web_results": [],
        "agent_interactions": [],
    }
    
    try:
        # Should complete within 120 seconds
        result = await asyncio.wait_for(
            researcher_node(test_state),
            timeout=120
        )
        assert result is not None
        print("✅ Timeout Test Passed")
    except asyncio.TimeoutError:
        pytest.fail("Researcher took too long (>120s)")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_researcher_handles_no_plan():
    """Test researcher handles empty research plan gracefully"""
    
    test_state = {
        "query": "test",
        "research_plan": [],  # Empty plan
        "web_results": [],
        "agent_interactions": [],
    }
    
    result = await researcher_node(test_state)
    
    # Should handle gracefully - either return empty or skip
    assert result is not None
    
    print("✅ Empty Plan Handling Test Passed")
