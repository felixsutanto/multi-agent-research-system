"""LangGraph Workflow for Multi-Agent Research System

This module defines the research workflow graph that orchestrates
all agents to work together on research tasks.
"""

import asyncio
import time
from typing import Literal

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import AgentState, create_initial_state
from ..agents.planner import planner_node
from ..agents.researcher import researcher_node
from ..agents.analyst import analyst_node
from ..agents.synthesizer import synthesizer_node
from ..agents.critic import critic_node
from ..utils.config import get_config
from ..utils.logger import setup_logger

logger = setup_logger("workflow")


def should_revise(state: AgentState) -> Literal["synthesizer", "end"]:
    """
    Conditional edge function to determine if revision is needed.
    
    Returns:
        "synthesizer" if revisions are needed
        "end" if the report is approved or max iterations reached
    """
    config = get_config()
    
    # Check if approved
    if state.get("approved", False):
        logger.info("Report approved - ending workflow")
        return "end"
    
    # Check iteration limit
    iteration_count = state.get("iteration_count", 0)
    if iteration_count >= config.agents.max_iterations:
        logger.warning(f"Max iterations ({config.agents.max_iterations}) reached - forcing end")
        return "end"
    
    # Check if there are revision requests
    revision_requests = state.get("revision_requests", [])
    if revision_requests:
        logger.info(f"Revision needed - {len(revision_requests)} requests")
        return "synthesizer"
    
    return "end"


def create_research_graph(checkpointer=None) -> StateGraph:
    """
    Create the multi-agent research workflow graph.
    
    The workflow follows this pattern:
    1. Planner → Creates research plan
    2. Researcher → Executes web searches
    3. Analyst → Performs data analysis
    4. Synthesizer → Creates draft report
    5. Critic → Reviews and approves or requests revisions
    6. (Loop back to Synthesizer if revisions needed)
    
    Args:
        checkpointer: Optional LangGraph checkpointer for state persistence
        
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize graph with state schema
    workflow = StateGraph(AgentState)
    
    # Add all agent nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("critic", critic_node)
    
    # Define the main flow
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "synthesizer")
    workflow.add_edge("synthesizer", "critic")
    
    # Conditional edge from critic (approve or revise)
    workflow.add_conditional_edges(
        "critic",
        should_revise,
        {
            "synthesizer": "synthesizer",
            "end": END,
        }
    )
    
    # Compile with optional checkpointer
    if checkpointer:
        return workflow.compile(checkpointer=checkpointer)
    else:
        return workflow.compile()


def get_memory_checkpointer() -> MemorySaver:
    """
    Create a memory-based checkpointer for state persistence.
    
    Returns:
        MemorySaver instance
    """
    return MemorySaver()


async def run_research(
    query: str,
    thread_id: str | None = None,
    use_checkpointer: bool = False,
) -> AgentState:
    """
    Run the complete research workflow for a query.
    
    Args:
        query: The research question to investigate
        thread_id: Optional thread ID for checkpointing
        use_checkpointer: Whether to use SQLite checkpointing
        
    Returns:
        Final AgentState with all results
    """
    logger.info(f"Starting research workflow for: {query[:100]}...")
    start_time = time.time()
    
    # Create checkpointer if requested
    checkpointer = None
    if use_checkpointer:
        checkpointer = get_memory_checkpointer()
    
    # Create the graph
    graph = create_research_graph(checkpointer=checkpointer)
    
    # Create initial state
    initial_state = create_initial_state(query)
    
    # Prepare config
    config = {}
    if thread_id:
        config["configurable"] = {"thread_id": thread_id}
    
    try:
        # Run the workflow
        final_state = await graph.ainvoke(initial_state, config=config)
        
        # Calculate metrics
        elapsed_time = time.time() - start_time
        
        # Add timing to metrics
        if final_state.get("metrics") is None:
            final_state["metrics"] = {}
        final_state["metrics"]["latency_seconds"] = round(elapsed_time, 2)
        
        logger.info(
            f"Research workflow completed in {elapsed_time:.1f}s",
            {
                "approved": final_state.get("approved"),
                "iterations": final_state.get("iteration_count"),
                "report_length": len(final_state.get("final_report", "")),
            }
        )
        
        return final_state
        
    except Exception as e:
        logger.exception(f"Research workflow failed: {e}")
        raise


async def run_research_streaming(
    query: str,
    thread_id: str | None = None,
):
    """
    Run research workflow with streaming updates.
    
    Yields intermediate states as each agent completes.
    
    Args:
        query: The research question
        thread_id: Optional thread ID
        
    Yields:
        Tuple of (agent_name, state_update) for each step
    """
    logger.info(f"Starting streaming research for: {query[:100]}...")
    
    graph = create_research_graph()
    initial_state = create_initial_state(query)
    
    config = {}
    if thread_id:
        config["configurable"] = {"thread_id": thread_id}
    
    async for event in graph.astream(initial_state, config=config):
        # Event contains the node name and output
        for node_name, node_output in event.items():
            logger.debug(f"Stream event from {node_name}")
            yield node_name, node_output


def run_research_sync(query: str, **kwargs) -> AgentState:
    """
    Synchronous wrapper for run_research.
    
    Args:
        query: The research question
        **kwargs: Additional arguments for run_research
        
    Returns:
        Final AgentState
    """
    return asyncio.run(run_research(query, **kwargs))
