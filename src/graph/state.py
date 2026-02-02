"""Agent State Schema for Multi-Agent Research System

This module defines the shared state that flows through all agents
in the research workflow.
"""

from typing import Annotated, Any
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class ResearchTask(TypedDict):
    """A single research task"""
    type: str  # "web_search", "data_analysis", "document_retrieval"
    query: str  # The search query or task description
    priority: int  # 1 = highest priority
    agent: str  # "researcher", "analyst"
    status: str  # "pending", "in_progress", "completed", "failed"


class WebSearchResult(TypedDict):
    """Result from web search"""
    url: str
    title: str
    content: str
    score: float
    raw_content: str | None


class DocumentResult(TypedDict):
    """Result from vector search"""
    id: str
    content: str
    metadata: dict[str, Any]
    score: float


class AnalysisResult(TypedDict):
    """Result from data analysis"""
    task: str
    method: str
    code: str
    result: str
    interpretation: str


class QualityAssessment(TypedDict):
    """Quality assessment from critic agent"""
    approved: bool
    groundedness_score: float
    citation_coverage: float
    issues: list[dict[str, Any]]
    revision_requests: list[str]


class AgentInteraction(TypedDict):
    """Log of a single agent interaction"""
    agent: str
    action: str
    timestamp: str
    output: dict[str, Any] | None


class Citation(TypedDict):
    """A citation reference"""
    id: int
    source: str
    title: str
    url: str | None
    accessed_date: str


class EvaluationMetrics(TypedDict):
    """Evaluation metrics for the research output"""
    context_relevance: float
    groundedness: float
    answer_relevance: float
    citation_coverage: float
    task_success: bool
    token_usage: dict[str, int]
    latency_seconds: float


class AgentState(TypedDict):
    """
    Shared state across all agents in the research workflow.
    
    This state is passed through the LangGraph workflow and updated
    by each agent as they perform their tasks.
    """
    
    # User input
    query: str
    
    # Messages for LangGraph compatibility (agent scratchpad)
    messages: Annotated[list, add_messages]
    
    # Planner outputs
    research_plan: list[ResearchTask]
    
    # Research Agent outputs
    web_results: list[WebSearchResult]
    documents: list[DocumentResult]
    scraped_content: list[dict[str, str]]
    
    # Analyst outputs
    analysis_results: list[AnalysisResult]
    code_snippets: list[str]
    
    # Synthesis outputs
    draft_report: str
    
    # Critic outputs
    quality_assessment: QualityAssessment | None
    revision_requests: list[str]
    approved: bool
    
    # Workflow control
    iteration_count: int
    current_agent: str
    
    # Tracking and logging
    agent_interactions: list[AgentInteraction]
    
    # Final outputs
    final_report: str
    citations: list[Citation]
    metrics: EvaluationMetrics | None
    
    # Error handling
    errors: list[str]


def create_initial_state(query: str) -> AgentState:
    """Create an initial state for a new research query"""
    return AgentState(
        query=query,
        messages=[],
        research_plan=[],
        web_results=[],
        documents=[],
        scraped_content=[],
        analysis_results=[],
        code_snippets=[],
        draft_report="",
        quality_assessment=None,
        revision_requests=[],
        approved=False,
        iteration_count=0,
        current_agent="planner",
        agent_interactions=[],
        final_report="",
        citations=[],
        metrics=None,
        errors=[],
    )
