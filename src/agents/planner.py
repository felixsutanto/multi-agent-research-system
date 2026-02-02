"""Planner Agent

This agent decomposes complex research queries into structured sub-tasks
and creates an execution plan for other agents.
"""

import json
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..graph.state import AgentState
from ..utils.config import get_config
from ..utils.llm_provider import create_llm
from ..utils.logger import AgentLogger

logger = AgentLogger("planner")


PLANNER_PROMPT = """You are an expert research planning agent. Your task is to decompose 
complex research questions into specific, actionable sub-tasks.

## Research Question
{query}

## Your Task
Create a structured research plan with specific tasks for:
1. **Web Search Tasks** - Queries to search the internet for current information
2. **Data Analysis Tasks** - Quantitative analysis or calculations needed (if applicable)

## Guidelines
- Be specific with search queries - they should be targeted and searchable
- Only include data analysis tasks if the question requires quantitative analysis
- Prioritize tasks (1 = highest priority)
- Keep the total number of tasks manageable (3-6 tasks)

## Output Format
Respond ONLY with a valid JSON object in this exact format:
{{
    "research_summary": "Brief summary of the research approach",
    "tasks": [
        {{
            "type": "web_search",
            "query": "specific search query",
            "priority": 1,
            "agent": "researcher",
            "status": "pending"
        }},
        {{
            "type": "data_analysis",
            "query": "what to analyze and how",
            "priority": 2,
            "agent": "analyst",
            "status": "pending"
        }}
    ]
}}

Important: Return ONLY the JSON object, no additional text or markdown formatting."""


def create_planner_agent():
    """Create the planner agent LLM"""
    return create_llm(temperature=0)  # Deterministic for planning


async def planner_node(state: AgentState) -> dict:
    """
    Planner agent node for the research workflow.
    
    Takes the user query and creates a structured research plan
    with tasks for the researcher and analyst agents.
    """
    logger.info("Creating research plan", {"query": state["query"][:100]})
    
    try:
        llm = create_planner_agent()
        prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
        chain = prompt | llm
        
        response = await chain.ainvoke({"query": state["query"]})
        
        # Parse JSON response
        content = response.content
        # Handle potential markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        plan_data = json.loads(content.strip())
        tasks = plan_data.get("tasks", [])
        
        # Limit tasks to prevent runaway execution
        config = get_config()
        max_tasks = config.agents.max_research_tasks + config.agents.max_analysis_tasks
        tasks = tasks[:max_tasks]
        
        logger.info(f"Created plan with {len(tasks)} tasks")
        
        return {
            "research_plan": tasks,
            "current_agent": "researcher",
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "planner",
                "action": "created_research_plan",
                "timestamp": datetime.now().isoformat(),
                "output": {
                    "summary": plan_data.get("research_summary", ""),
                    "task_count": len(tasks),
                },
            }],
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse planner response: {e}")
        # Return a basic fallback plan
        return {
            "research_plan": [{
                "type": "web_search",
                "query": state["query"],
                "priority": 1,
                "agent": "researcher",
                "status": "pending",
            }],
            "current_agent": "researcher",
            "errors": state.get("errors", []) + [f"Planner JSON parse error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "planner",
                "action": "fallback_plan_created",
                "timestamp": datetime.now().isoformat(),
                "output": None,
            }],
        }
        
    except Exception as e:
        logger.exception(f"Planner agent failed: {e}")
        return {
            "research_plan": [],
            "errors": state.get("errors", []) + [f"Planner error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "planner",
                "action": "error",
                "timestamp": datetime.now().isoformat(),
                "output": {"error": str(e)},
            }],
        }
