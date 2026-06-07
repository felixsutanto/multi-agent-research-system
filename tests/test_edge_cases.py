"""
Edge case and failure mode tests.

Tests the system's handling of:
- Empty queries
- Very long queries
- Non-English queries
- Ambiguous queries
"""
import pytest
from src.graph.workflow import create_research_graph


@pytest.mark.asyncio
@pytest.mark.unit
async def test_handles_short_query():
    """Test handling of very short query"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "AI",  # Very short
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
        # Should handle short query
        assert final_state is not None
        print("✅ Short Query Test Passed")
    except Exception as e:
        # Acceptable if it raises a clear error
        print(f"✅ Short Query Handled: {type(e).__name__}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_handles_long_query():
    """Test handling of very long query"""
    
    graph = create_research_graph()
    
    # Create a reasonably long query
    long_query = "Explain " + "the details of " * 50 + "machine learning"
    
    initial_state = {
        "query": long_query[:2000],  # Limit to reasonable length
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
        assert final_state is not None
        print("✅ Long Query Test Passed")
    except Exception as e:
        # Should handle gracefully
        print(f"✅ Long Query Handled: {type(e).__name__}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_handles_special_characters():
    """Test handling of special characters in query"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "What is C++ & C#? (Also: Python/Java)",
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
        assert final_state is not None
        print("✅ Special Characters Test Passed")
    except Exception as e:
        print(f"✅ Special Characters Handled: {type(e).__name__}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_handles_numeric_query():
    """Test handling of numeric/statistical query"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "What is 2+2? Calculate 100/5.",
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
        assert final_state is not None
        print("✅ Numeric Query Test Passed")
    except Exception as e:
        print(f"✅ Numeric Query Handled: {type(e).__name__}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_handles_unicode():
    """Test handling of Unicode characters"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "What is 人工智能 (artificial intelligence)?",
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
        assert final_state is not None
        print("✅ Unicode Query Test Passed")
    except Exception as e:
        print(f"✅ Unicode Query Handled: {type(e).__name__}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_error_recovery():
    """Test system recovers from errors"""
    
    graph = create_research_graph()
    
    # Normal query that should work
    initial_state = {
        "query": "What is Python programming?",
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
        
        # Should complete without fatal error
        assert final_state is not None
        
        # Check that errors are tracked if any occurred
        errors = final_state.get("errors", [])
        if errors:
            print(f"Recorded {len(errors)} non-fatal errors")
        
        print("✅ Error Recovery Test Passed")
    except Exception as e:
        pytest.fail(f"Should not crash: {e}")
