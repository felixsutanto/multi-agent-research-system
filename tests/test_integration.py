"""
Integration tests for Multi-Agent Workflow.

Tests the complete workflow with all agents collaborating.
"""
import pytest
import asyncio
from src.graph.workflow import create_research_graph


@pytest.mark.asyncio
@pytest.mark.integration
async def test_full_workflow_simple_query():
    """Test complete workflow with simple query"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "What is FastAPI?",
        "messages": [],
        "iteration_count": 0,
        "agent_interactions": [],
        "approved": False,
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "errors": [],
    }
    
    # Run workflow
    final_state = await graph.ainvoke(initial_state)
    
    # Verify agents ran
    agent_names = {log["agent"] for log in final_state.get("agent_interactions", [])}
    
    assert "planner" in agent_names, "Planner should run"
    assert "researcher" in agent_names, "Researcher should run"
    assert "synthesizer" in agent_names, "Synthesizer should run"
    
    # Verify output exists
    report = final_state.get("final_report") or final_state.get("draft_report", "")
    assert len(report) > 100, "Should produce substantial report"
    
    print("✅ Full Workflow Test Passed")
    print(f"Agents involved: {agent_names}")
    print(f"Total interactions: {len(final_state.get('agent_interactions', []))}")


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.slow
async def test_workflow_with_analysis():
    """Test workflow requiring data analysis"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "What are the key statistics about Python programming language usage in 2025?",
        "messages": [],
        "iteration_count": 0,
        "agent_interactions": [],
        "approved": False,
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "errors": [],
    }
    
    final_state = await graph.ainvoke(initial_state)
    
    # Should produce output
    report = final_state.get("final_report") or final_state.get("draft_report", "")
    assert len(report) > 100
    
    print("✅ Analysis Workflow Test Passed")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_workflow_iteration_limit():
    """Test workflow respects iteration limits"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "Complex topic requiring multiple revisions",
        "messages": [],
        "iteration_count": 0,
        "max_iterations": 2,  # Low limit for testing
        "agent_interactions": [],
        "approved": False,
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "errors": [],
    }
    
    final_state = await graph.ainvoke(initial_state)
    
    # Should not exceed max iterations
    assert final_state.get("iteration_count", 0) <= 3, "Should respect max iterations"
    
    print("✅ Iteration Limit Test Passed")


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.slow
async def test_workflow_timeout_protection():
    """Test that workflow doesn't hang indefinitely"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "Explain quantum computing basics",
        "messages": [],
        "iteration_count": 0,
        "agent_interactions": [],
        "approved": False,
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "errors": [],
    }
    
    try:
        # Should complete within 5 minutes
        final_state = await asyncio.wait_for(
            graph.ainvoke(initial_state),
            timeout=300
        )
        assert final_state is not None
        print("✅ Timeout Protection Test Passed")
    except asyncio.TimeoutError:
        pytest.fail("Workflow exceeded 5 minute timeout")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_workflow_error_recovery():
    """Test workflow handles errors gracefully"""
    
    graph = create_research_graph()
    
    # Query that should still work
    initial_state = {
        "query": "What is Python?",
        "messages": [],
        "iteration_count": 0,
        "agent_interactions": [],
        "approved": False,
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "errors": [],
    }
    
    try:
        final_state = await graph.ainvoke(initial_state)
        
        # Should complete and produce output
        assert final_state is not None
        assert len(final_state.get("agent_interactions", [])) > 0
        
        print("✅ Error Recovery Test Passed")
    except Exception as e:
        # Should not crash catastrophically
        pytest.fail(f"Workflow crashed: {e}")
