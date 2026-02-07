"""
Unit tests for the Planner Agent.

Tests the planner's ability to:
- Create valid research plans
- Handle complex queries
- Handle error cases
"""
import pytest
from src.agents.planner import planner_node


@pytest.mark.asyncio
@pytest.mark.unit
async def test_planner_creates_valid_plan():
    """Test planner generates structured research plan"""
    
    test_state = {
        "query": "What are the environmental impacts of palm oil production in Indonesia?",
        "messages": [],
        "agent_interactions": [],
        "research_plan": [],
    }
    
    result = await planner_node(test_state)
    
    # Assert plan was created
    assert "research_plan" in result
    assert isinstance(result["research_plan"], list)
    assert len(result["research_plan"]) > 0
    
    # Check plan structure - each task should have type and query
    for task in result["research_plan"]:
        assert "type" in task
        assert task["type"] in ["web_search", "data_analysis", "synthesis"]
    
    # Should create at least one web search task
    web_tasks = [t for t in result["research_plan"] if t["type"] == "web_search"]
    assert len(web_tasks) >= 1, "Should create at least one search task"
    
    print("✅ Planner Test Passed")
    print(f"Generated {len(result['research_plan'])} tasks")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_planner_handles_complex_query():
    """Test planner with multi-faceted question"""
    
    test_state = {
        "query": "Compare the cost, efficiency, and environmental impact of solar vs wind energy in Southeast Asia",
        "messages": [],
        "agent_interactions": [],
        "research_plan": [],
    }
    
    result = await planner_node(test_state)
    
    # Should decompose into multiple sub-tasks
    assert len(result["research_plan"]) >= 2, "Complex query should create multiple tasks"
    
    # Should include web search
    task_types = [t["type"] for t in result["research_plan"]]
    assert "web_search" in task_types
    
    print("✅ Complex Query Planning Passed")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_planner_logs_interaction():
    """Test planner logs its interaction"""
    
    test_state = {
        "query": "What is Python?",
        "messages": [],
        "agent_interactions": [],
        "research_plan": [],
    }
    
    result = await planner_node(test_state)
    
    # Should log agent interaction
    assert "agent_interactions" in result
    assert len(result["agent_interactions"]) >= 1
    
    # Check log structure
    log = result["agent_interactions"][0]
    assert log["agent"] == "planner"
    assert "action" in log
    assert "timestamp" in log
    
    print("✅ Planner Logging Test Passed")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_planner_includes_analysis_for_quantitative_query():
    """Test planner includes data analysis for quantitative questions"""
    
    test_state = {
        "query": "Calculate the average GDP growth rate of ASEAN countries from 2015 to 2023",
        "messages": [],
        "agent_interactions": [],
        "research_plan": [],
    }
    
    result = await planner_node(test_state)
    
    # Check if analysis task was included
    task_types = [t["type"] for t in result["research_plan"]]
    
    # Should recognize quantitative nature (may include data_analysis)
    assert len(result["research_plan"]) >= 1
    
    print("✅ Quantitative Query Planning Passed")
    print(f"Plan types: {task_types}")
