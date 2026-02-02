"""Custom Evaluation Metrics

This module implements custom metrics for evaluating research output quality.
"""

import re
from typing import Any

from ..graph.state import AgentState
from ..utils.logger import setup_logger

logger = setup_logger("evaluation.custom")


def evaluate_citation_coverage(report: str) -> dict[str, Any]:
    """
    Calculate what percentage of the report has proper citations.
    
    Args:
        report: The generated research report
        
    Returns:
        Dict with coverage score and details
    """
    if not report:
        return {"score": 0.0, "total_sentences": 0, "cited_sentences": 0}
    
    # Split into sentences
    sentence_pattern = r'[.!?]+(?:\s|$)'
    sentences = [s.strip() for s in re.split(sentence_pattern, report) if s.strip()]
    
    # Filter to only factual sentences (skip headers, short fragments)
    factual_sentences = [
        s for s in sentences 
        if len(s) > 30 and not s.startswith('#')
    ]
    
    if not factual_sentences:
        return {"score": 0.0, "total_sentences": 0, "cited_sentences": 0}
    
    # Count sentences with citations
    citation_patterns = [
        r'\[Source:\s*[^\]]+\]',
        r'\[URL:\s*[^\]]+\]',
        r'\[Document:\s*[^\]]+\]',
        r'\[\d+\]',  # Numbered references
        r'https?://[^\s\]]+',  # Direct URLs
    ]
    
    cited_count = 0
    for sentence in factual_sentences:
        for pattern in citation_patterns:
            if re.search(pattern, sentence):
                cited_count += 1
                break
    
    coverage = cited_count / len(factual_sentences) if factual_sentences else 0
    
    return {
        "score": round(coverage, 3),
        "total_sentences": len(factual_sentences),
        "cited_sentences": cited_count,
        "uncited_percentage": round(1 - coverage, 3),
    }


def evaluate_task_success(state: AgentState) -> dict[str, Any]:
    """
    Determine if the research task completed successfully.
    
    Args:
        state: The final agent state
        
    Returns:
        Dict with success status and details
    """
    # Check for required outputs
    has_report = len(state.get("final_report", "")) > 500
    has_citations = len(state.get("citations", [])) > 0
    is_approved = state.get("approved", False)
    no_critical_errors = not any(
        "critical" in str(e).lower() or "fatal" in str(e).lower()
        for e in state.get("errors", [])
    )
    
    # Calculate success
    success = has_report and is_approved and no_critical_errors
    
    return {
        "success": success,
        "criteria": {
            "has_report": has_report,
            "has_citations": has_citations,
            "is_approved": is_approved,
            "no_critical_errors": no_critical_errors,
        },
        "report_length": len(state.get("final_report", "")),
        "citation_count": len(state.get("citations", [])),
        "error_count": len(state.get("errors", [])),
    }


def calculate_agent_efficiency(state: AgentState) -> dict[str, Any]:
    """
    Measure the efficiency of agent collaboration.
    
    Args:
        state: The final agent state
        
    Returns:
        Dict with efficiency metrics
    """
    interactions = state.get("agent_interactions", [])
    
    # Count by agent
    agent_counts = {}
    for interaction in interactions:
        agent = interaction.get("agent", "unknown")
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    # Count by action type
    action_counts = {}
    for interaction in interactions:
        action = interaction.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1
    
    # Calculate efficiency score
    # Lower iterations with successful completion = more efficient
    iteration_count = state.get("iteration_count", 0)
    success = state.get("approved", False)
    
    # Base efficiency on iteration count (fewer is better)
    if success:
        if iteration_count <= 1:
            efficiency_score = 1.0
        elif iteration_count == 2:
            efficiency_score = 0.8
        else:
            efficiency_score = max(0.5, 1.0 - (iteration_count * 0.15))
    else:
        efficiency_score = 0.3  # Penalize failed tasks
    
    return {
        "efficiency_score": round(efficiency_score, 2),
        "total_interactions": len(interactions),
        "iterations": iteration_count,
        "agent_calls": agent_counts,
        "action_breakdown": action_counts,
    }


def calculate_token_usage(state: AgentState) -> dict[str, Any]:
    """
    Estimate token usage and cost for the research task.
    
    Note: This is an estimation. Actual usage should be tracked
    via LLM provider callbacks for accuracy.
    
    Args:
        state: The final agent state
        
    Returns:
        Dict with token estimates and cost
    """
    # Rough token estimation based on content length
    # Average ~4 characters per token for English text
    
    query_tokens = len(state.get("query", "")) // 4
    
    # Web results
    web_content = "".join(
        r.get("content", "") for r in state.get("web_results", [])
    )
    web_tokens = len(web_content) // 4
    
    # Report
    report_tokens = len(state.get("final_report", "")) // 4
    
    # Estimate total based on multi-turn conversation
    # Each agent call roughly processes input + generates output
    agent_calls = len(state.get("agent_interactions", []))
    estimated_input = query_tokens + web_tokens
    estimated_output = report_tokens + (agent_calls * 500)  # ~500 tokens per agent response
    
    # GPT-4o pricing estimates (as of 2024)
    # Input: $5/1M tokens, Output: $15/1M tokens
    input_cost = (estimated_input / 1_000_000) * 5
    output_cost = (estimated_output / 1_000_000) * 15
    total_cost = input_cost + output_cost
    
    return {
        "estimated_input_tokens": estimated_input,
        "estimated_output_tokens": estimated_output,
        "estimated_total_tokens": estimated_input + estimated_output,
        "estimated_cost_usd": round(total_cost, 4),
        "note": "These are estimates. Actual usage may vary.",
    }


def evaluate_all_custom_metrics(state: AgentState) -> dict[str, Any]:
    """
    Run all custom evaluation metrics.
    
    Args:
        state: The final agent state
        
    Returns:
        Complete custom metrics evaluation
    """
    report = state.get("final_report", "")
    
    citation_coverage = evaluate_citation_coverage(report)
    task_success = evaluate_task_success(state)
    agent_efficiency = calculate_agent_efficiency(state)
    token_usage = calculate_token_usage(state)
    
    return {
        "citation_coverage": citation_coverage,
        "task_success": task_success,
        "agent_efficiency": agent_efficiency,
        "token_usage": token_usage,
        "summary": {
            "success": task_success["success"],
            "citation_score": citation_coverage["score"],
            "efficiency_score": agent_efficiency["efficiency_score"],
            "estimated_cost": token_usage["estimated_cost_usd"],
        },
    }
