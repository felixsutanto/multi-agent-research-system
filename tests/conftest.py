"""
Pytest configuration and shared fixtures for Multi-Agent Research System tests.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import Any


# =============================================
# Fixtures for State Management
# =============================================

@pytest.fixture
def base_state() -> dict[str, Any]:
    """Base state for testing agents"""
    return {
        "query": "",
        "messages": [],
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "agent_interactions": [],
        "iteration_count": 0,
        "max_iterations": 3,
        "approved": False,
        "errors": [],
        "metrics": {},
    }


@pytest.fixture
def simple_query_state(base_state) -> dict[str, Any]:
    """State with a simple factual query"""
    base_state["query"] = "What is Python programming language?"
    return base_state


@pytest.fixture
def complex_query_state(base_state) -> dict[str, Any]:
    """State with a complex multi-faceted query"""
    base_state["query"] = "Compare PostgreSQL vs MongoDB for e-commerce applications in terms of performance, scalability, and cost"
    return base_state


@pytest.fixture
def research_state_with_results(base_state) -> dict[str, Any]:
    """State with web research results"""
    base_state["query"] = "What is LangGraph?"
    base_state["web_results"] = [
        {
            "url": "https://langchain.com/langgraph",
            "title": "LangGraph Documentation",
            "content": "LangGraph is a framework for building stateful multi-agent applications using LangChain."
        },
        {
            "url": "https://github.com/langchain-ai/langgraph",
            "title": "LangGraph GitHub",
            "content": "LangGraph enables building complex LLM workflows with state management and cycles."
        }
    ]
    return base_state


@pytest.fixture
def synthesis_state_with_draft(research_state_with_results) -> dict[str, Any]:
    """State with a draft report for critic review"""
    research_state_with_results["draft_report"] = """
# LangGraph Overview

LangGraph is a framework for building stateful multi-agent applications [1].
It enables complex LLM workflows with state management and cycles [2].

## Key Features

- **State Management**: Maintains state across agent interactions
- **Cyclic Workflows**: Supports loops and conditional branching
- **Built on LangChain**: Integrates seamlessly with LangChain ecosystem

## References

[1] https://langchain.com/langgraph
[2] https://github.com/langchain-ai/langgraph
"""
    return research_state_with_results


# =============================================
# Mock Fixtures
# =============================================

@pytest.fixture
def mock_llm():
    """Mock LLM that returns predictable responses"""
    mock = AsyncMock()
    mock.ainvoke = AsyncMock(return_value=MagicMock(
        content='{"tasks": [{"type": "web_search", "query": "test", "agent": "researcher"}]}'
    ))
    return mock


@pytest.fixture
def mock_tavily_client():
    """Mock Tavily search client"""
    mock = MagicMock()
    mock.search = MagicMock(return_value={
        "results": [
            {
                "url": "https://example.com",
                "title": "Test Result",
                "content": "Test content for the search query."
            }
        ]
    })
    return mock


# =============================================
# Event Loop Configuration
# =============================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# =============================================
# Test Categories (Markers)
# =============================================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "api: marks tests as API tests")
