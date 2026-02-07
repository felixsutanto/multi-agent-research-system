"""
End-to-end tests with real-world scenarios.

Tests the system with diverse, production-like queries.
"""
import pytest
from src.graph.workflow import create_research_graph


# Test Suite: Real User Queries
E2E_TEST_CASES = [
    {
        "name": "Simple Factual",
        "query": "What are the main features of Python 3.12?",
        "expected_content": ["python"],
        "min_length": 300,
    },
    {
        "name": "Comparative Analysis",
        "query": "Compare PostgreSQL vs MongoDB for web applications",
        "expected_content": ["postgresql", "mongodb"],
        "min_length": 400,
    },
    {
        "name": "Technical Explanation",
        "query": "How does Docker containerization work?",
        "expected_content": ["docker", "container"],
        "min_length": 300,
    },
]


@pytest.mark.parametrize("test_case", E2E_TEST_CASES)
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.slow
async def test_e2e_query(test_case):
    """Run end-to-end test for each test case"""
    
    graph = create_research_graph()
    
    print(f"\n🧪 Testing: {test_case['name']}")
    print(f"Query: {test_case['query']}")
    
    initial_state = {
        "query": test_case["query"],
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
    
    report = final_state.get("final_report") or final_state.get("draft_report", "")
    
    # Test 1: Completion
    assert report, "Report should be generated"
    print(f"✓ Report generated ({len(report)} chars)")
    
    # Test 2: Length
    assert len(report) >= test_case["min_length"], \
        f"Report too short: {len(report)} < {test_case['min_length']}"
    print(f"✓ Length requirement met")
    
    # Test 3: Content relevance
    report_lower = report.lower()
    for keyword in test_case["expected_content"]:
        assert keyword.lower() in report_lower, \
            f"Missing expected keyword: {keyword}"
    print(f"✓ Content keywords present")
    
    # Test 4: Agents ran
    agent_names = {log["agent"] for log in final_state.get("agent_interactions", [])}
    assert len(agent_names) >= 2, "Multiple agents should participate"
    print(f"✓ {len(agent_names)} agents participated")
    
    print(f"✅ {test_case['name']} - ALL CHECKS PASSED\n")


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_produces_citations():
    """Test that E2E workflow produces citations"""
    
    graph = create_research_graph()
    
    initial_state = {
        "query": "What is FastAPI framework?",
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
    
    # Should have web results (which become citations)
    web_results = final_state.get("web_results", [])
    assert len(web_results) > 0, "Should find web sources"
    
    print(f"✅ E2E Citations Test Passed - Found {len(web_results)} sources")


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_e2e_handles_error_gracefully():
    """Test E2E handles unusual queries gracefully"""
    
    graph = create_research_graph()
    
    # A challenging query
    initial_state = {
        "query": "Explain something very obscure and specific",
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
        
        # Should complete without crashing
        assert final_state is not None
        assert len(final_state.get("agent_interactions", [])) > 0
        
        print("✅ E2E Error Handling Test Passed")
    except Exception as e:
        pytest.fail(f"E2E should handle unusual queries: {e}")
