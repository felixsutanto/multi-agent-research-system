"""Tests for evaluation metrics"""

import pytest


class TestCitationCoverage:
    """Tests for citation coverage metric"""
    
    def test_empty_report_returns_zero(self):
        """Test empty report returns 0 coverage"""
        from src.evaluation.custom_metrics import evaluate_citation_coverage
        
        result = evaluate_citation_coverage("")
        
        assert result["score"] == 0.0
    
    def test_detects_source_citations(self):
        """Test detection of [Source: URL] format"""
        from src.evaluation.custom_metrics import evaluate_citation_coverage
        
        report = """
        This is a factual claim that has proper citation.
        [Source: https://example.com/article]
        
        Another claim with a citation for verification.
        [Source: https://another-source.com]
        """
        
        result = evaluate_citation_coverage(report)
        
        assert result["cited_sentences"] > 0
    
    def test_detects_url_citations(self):
        """Test detection of direct URL citations"""
        from src.evaluation.custom_metrics import evaluate_citation_coverage
        
        report = """
        According to https://example.com, this is a well-documented fact.
        The research shows significant improvements in performance metrics.
        """
        
        result = evaluate_citation_coverage(report)
        
        assert result["cited_sentences"] >= 1


class TestTaskSuccess:
    """Tests for task success evaluation"""
    
    def test_success_with_all_criteria(self):
        """Test success when all criteria are met"""
        from src.evaluation.custom_metrics import evaluate_task_success
        
        state = {
            "final_report": "A" * 600,  # > 500 chars
            "citations": [{"id": 1, "url": "https://example.com"}],
            "approved": True,
            "errors": [],
        }
        
        result = evaluate_task_success(state)
        
        assert result["success"] is True
    
    def test_failure_without_approval(self):
        """Test failure when not approved"""
        from src.evaluation.custom_metrics import evaluate_task_success
        
        state = {
            "final_report": "A" * 600,
            "citations": [{"id": 1}],
            "approved": False,
            "errors": [],
        }
        
        result = evaluate_task_success(state)
        
        assert result["success"] is False


class TestAgentEfficiency:
    """Tests for agent efficiency calculation"""
    
    def test_high_efficiency_single_iteration(self):
        """Test high efficiency with single iteration"""
        from src.evaluation.custom_metrics import calculate_agent_efficiency
        
        state = {
            "iteration_count": 1,
            "approved": True,
            "agent_interactions": [
                {"agent": "planner", "action": "plan"},
                {"agent": "researcher", "action": "search"},
            ],
        }
        
        result = calculate_agent_efficiency(state)
        
        assert result["efficiency_score"] == 1.0
    
    def test_lower_efficiency_multiple_iterations(self):
        """Test lower efficiency with multiple iterations"""
        from src.evaluation.custom_metrics import calculate_agent_efficiency
        
        state = {
            "iteration_count": 3,
            "approved": True,
            "agent_interactions": [],
        }
        
        result = calculate_agent_efficiency(state)
        
        assert result["efficiency_score"] < 1.0
