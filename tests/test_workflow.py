"""Tests for the agent state and workflow"""

import pytest
from datetime import datetime


class TestAgentState:
    """Tests for AgentState schema"""
    
    def test_create_initial_state(self):
        """Test creating initial state"""
        from src.graph.state import create_initial_state
        
        state = create_initial_state("What is AI?")
        
        assert state["query"] == "What is AI?"
        assert state["messages"] == []
        assert state["research_plan"] == []
        assert state["iteration_count"] == 0
        assert state["approved"] is False
    
    def test_initial_state_has_all_fields(self):
        """Test that initial state contains all required fields"""
        from src.graph.state import create_initial_state
        
        state = create_initial_state("Test query")
        
        required_fields = [
            "query", "messages", "research_plan", "web_results",
            "analysis_results", "draft_report", "final_report",
            "citations", "approved", "iteration_count"
        ]
        
        for field in required_fields:
            assert field in state, f"Missing field: {field}"


class TestWorkflow:
    """Tests for LangGraph workflow"""
    
    def test_create_research_graph(self):
        """Test that research graph can be created"""
        from src.graph.workflow import create_research_graph
        
        graph = create_research_graph()
        
        assert graph is not None
    
    def test_should_revise_approved(self):
        """Test should_revise returns 'end' when approved"""
        from src.graph.workflow import should_revise
        
        state = {"approved": True, "iteration_count": 1, "revision_requests": []}
        
        result = should_revise(state)
        
        assert result == "end"
    
    def test_should_revise_with_requests(self):
        """Test should_revise returns 'synthesizer' when revisions needed"""
        from src.graph.workflow import should_revise
        
        state = {
            "approved": False,
            "iteration_count": 1,
            "revision_requests": ["Fix citation"]
        }
        
        result = should_revise(state)
        
        assert result == "synthesizer"
    
    def test_should_revise_max_iterations(self):
        """Test should_revise returns 'end' at max iterations"""
        from src.graph.workflow import should_revise
        
        state = {
            "approved": False,
            "iteration_count": 5,  # Above default max of 3
            "revision_requests": ["Fix citation"]
        }
        
        result = should_revise(state)
        
        assert result == "end"
