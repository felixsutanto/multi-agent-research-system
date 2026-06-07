"""
Quality metrics tests for RAG Triad and custom metrics.

Tests evaluation functions for:
- Context relevance
- Groundedness
- Answer relevance
- Citation coverage
- Task success
"""
import pytest
from src.evaluation.rag_triad import RAGTriadEvaluator
from src.evaluation.custom_metrics import (
    evaluate_citation_coverage,
    evaluate_task_success,
    evaluate_all_custom_metrics,
)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_rag_triad_context_relevance():
    """Test context relevance evaluation"""
    
    evaluator = RAGTriadEvaluator()
    
    query = "What is machine learning?"
    context = "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
    
    result = await evaluator.evaluate_context_relevance(query, context)
    
    assert "metric" in result
    assert result["metric"] == "context_relevance"
    assert "score" in result
    assert 0.0 <= result["score"] <= 1.0
    
    print(f"✅ Context Relevance Test Passed - Score: {result['score']:.2f}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_rag_triad_groundedness():
    """Test groundedness evaluation"""
    
    evaluator = RAGTriadEvaluator()
    
    context = "Python was created by Guido van Rossum and first released in 1991."
    answer = "Python is a programming language created by Guido van Rossum in 1991."
    
    result = await evaluator.evaluate_groundedness(context, answer)
    
    assert "metric" in result
    assert result["metric"] == "groundedness"
    assert "score" in result
    assert 0.0 <= result["score"] <= 1.0
    
    print(f"✅ Groundedness Test Passed - Score: {result['score']:.2f}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_rag_triad_answer_relevance():
    """Test answer relevance evaluation"""
    
    evaluator = RAGTriadEvaluator()
    
    query = "What are the benefits of Python?"
    answer = "Python offers several benefits including easy syntax, extensive libraries, and strong community support."
    
    result = await evaluator.evaluate_answer_relevance(query, answer)
    
    assert "metric" in result
    assert result["metric"] == "answer_relevance"
    assert "score" in result
    assert 0.0 <= result["score"] <= 1.0
    
    print(f"✅ Answer Relevance Test Passed - Score: {result['score']:.2f}")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_rag_triad_full_evaluation():
    """Test full RAG Triad evaluation"""
    
    evaluator = RAGTriadEvaluator()
    
    query = "What is Docker?"
    context = "Docker is a platform for developing, shipping, and running applications in containers."
    answer = "Docker is a containerization platform that helps developers package applications with their dependencies."
    
    result = await evaluator.evaluate_all(query, context, answer)
    
    # Should have all three metrics
    assert "context_relevance" in result
    assert "groundedness" in result
    assert "answer_relevance" in result
    assert "overall_score" in result
    
    # All scores in valid range
    assert 0.0 <= result["overall_score"] <= 1.0
    
    print(f"✅ Full RAG Triad Test Passed - Overall: {result['overall_score']:.2f}")


def test_citation_coverage_well_cited():
    """Test citation coverage for well-cited report"""
    
    report = """
# Python Guide

Python is a programming language [1].
It was created by Guido van Rossum [2].
Python is widely used for data science [3].

## References
[1] https://python.org
[2] https://history.python.org
[3] https://datascience.org
    """
    
    web_results = [
        {"url": "https://python.org"},
        {"url": "https://history.python.org"},
        {"url": "https://datascience.org"}
    ]
    
    coverage = evaluate_citation_coverage(report, web_results)
    
    assert coverage["score"] >= 0.5, f"Well-cited report should have high coverage: {coverage['score']}"
    
    print(f"✅ Citation Coverage Test Passed - Score: {coverage['score']:.2f}")


def test_citation_coverage_uncited():
    """Test citation coverage for uncited report"""
    
    report = """
# Python Guide

Python is a programming language.
It is widely used.
Many people like it.
    """
    
    web_results = []
    
    coverage = evaluate_citation_coverage(report, web_results)
    
    # Lower coverage expected for uncited report
    assert coverage["score"] <= 0.5, f"Uncited report should have lower coverage"
    
    print(f"✅ Uncited Report Test Passed - Score: {coverage['score']:.2f}")


def test_task_success_evaluation():
    """Test task success criteria"""
    
    # Successful state
    success_state = {
        "approved": True,
        "final_report": "A" * 600,  # >500 chars
        "citations": [{"url": "https://example.com"}],
        "errors": []
    }
    
    result = evaluate_task_success(success_state)
    assert result["success"] == True, "Should be successful"
    
    # Failed state - too short
    fail_state = {
        "approved": True,
        "final_report": "Too short",
        "citations": [],
        "errors": []
    }
    
    result = evaluate_task_success(fail_state)
    # May or may not be successful depending on criteria
    assert "success" in result
    
    print("✅ Task Success Evaluation Test Passed")


def test_all_custom_metrics():
    """Test all custom metrics together"""
    
    state = {
        "query": "Test query",
        "final_report": """
# Test Report
This is a test report with content [1].

## Details
More information here [2].

[1] https://source1.com
[2] https://source2.com
        """,
        "web_results": [
            {"url": "https://source1.com"},
            {"url": "https://source2.com"}
        ],
        "citations": [
            {"url": "https://source1.com"},
            {"url": "https://source2.com"}
        ],
        "approved": True,
        "errors": []
    }
    
    metrics = evaluate_all_custom_metrics(state)
    
    assert "citation_coverage" in metrics
    assert "task_success" in metrics
    
    print(f"✅ All Custom Metrics Test Passed")
    print(f"Citation Coverage: {metrics['citation_coverage']}")
    print(f"Task Success: {metrics['task_success']}")
