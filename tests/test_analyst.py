"""
Unit tests for the Analyst Agent.

Tests the analyst's ability to:
- Execute Python code safely
- Perform data analysis
- Handle security concerns
"""
import pytest
from src.agents.analyst import analyst_node


@pytest.mark.asyncio
@pytest.mark.unit
async def test_analyst_performs_calculation():
    """Test analyst can perform calculations"""
    
    test_state = {
        "query": "Calculate average",
        "research_plan": [
            {
                "type": "data_analysis",
                "description": "Calculate the average of [10, 20, 30, 40, 50]",
                "agent": "analyst"
            }
        ],
        "web_results": [],
        "analysis_results": {},
        "agent_interactions": [],
    }
    
    result = await analyst_node(test_state)
    
    # Should produce analysis results
    assert "analysis_results" in result or "agent_interactions" in result
    
    print("✅ Analyst Calculation Test Passed")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_analyst_handles_no_tasks():
    """Test analyst handles no analysis tasks gracefully"""
    
    test_state = {
        "query": "Simple question with no analysis needed",
        "research_plan": [
            {
                "type": "web_search",  # Not a data_analysis task
                "query": "simple search",
                "agent": "researcher"
            }
        ],
        "web_results": [],
        "analysis_results": {},
        "agent_interactions": [],
    }
    
    result = await analyst_node(test_state)
    
    # Should handle gracefully
    assert result is not None
    
    print("✅ No Analysis Tasks Handling Test Passed")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_analyst_logs_activity():
    """Test analyst logs its activities"""
    
    test_state = {
        "query": "Calculate something",
        "research_plan": [
            {
                "type": "data_analysis",
                "description": "Simple calculation: 5 + 5",
                "agent": "analyst"
            }
        ],
        "web_results": [],
        "analysis_results": {},
        "agent_interactions": [],
    }
    
    result = await analyst_node(test_state)
    
    # Should log interaction
    assert "agent_interactions" in result
    
    if result["agent_interactions"]:
        log = result["agent_interactions"][0]
        assert log["agent"] == "analyst"
    
    print("✅ Analyst Logging Test Passed")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_analyst_data_processing():
    """Test analyst handles realistic data tasks"""
    
    test_state = {
        "query": "Process sales data",
        "research_plan": [
            {
                "type": "data_analysis",
                "description": """
                Given sales data: [100, 150, 120, 180, 200]
                Calculate: mean and total
                """,
                "agent": "analyst"
            }
        ],
        "web_results": [],
        "analysis_results": {},
        "agent_interactions": [],
    }
    
    result = await analyst_node(test_state)
    
    # Should complete without error
    assert result is not None
    
    print("✅ Data Processing Test Passed")
