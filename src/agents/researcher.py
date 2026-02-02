"""Research Agent

This agent conducts web searches and gathers information from various sources.
"""

from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from ..graph.state import AgentState
from ..tools.web_search import web_search
from ..tools.web_scraper import scrape_url
from ..utils.config import get_config
from ..utils.llm_provider import create_llm
from ..utils.logger import AgentLogger

logger = AgentLogger("researcher")


RESEARCHER_PROMPT = """You are an expert research agent. Based on the search results provided,
extract and synthesize the most relevant information.

## Research Task
{task_query}

## Search Results
{search_results}

## Your Task
Analyze the search results and extract:
1. Key facts and findings relevant to the research question
2. Important data points, statistics, or quotes
3. Source attribution for each piece of information

## Output Format
Provide a structured summary of findings with clear source citations.
Use [Source: URL] format for citations.
Be thorough but concise - focus on the most relevant information."""


def create_researcher_agent():
    """Create the researcher agent LLM"""
    return create_llm(temperature=0.1)  # Slightly creative for better synthesis


async def researcher_node(state: AgentState) -> dict:
    """
    Research agent node for the research workflow.
    
    Executes web search tasks from the research plan and
    synthesizes the findings.
    """
    logger.info("Starting research phase")
    
    # Get web search tasks from the plan
    research_tasks = [
        task for task in state.get("research_plan", [])
        if task.get("type") == "web_search"
    ]
    
    if not research_tasks:
        logger.warning("No web search tasks in plan")
        return {
            "web_results": [],
            "current_agent": "analyst",
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "researcher",
                "action": "no_tasks",
                "timestamp": datetime.now().isoformat(),
                "output": None,
            }],
        }
    
    # Limit tasks to prevent excessive API calls
    config = get_config()
    research_tasks = research_tasks[:config.agents.max_research_tasks]
    
    all_results = []
    scraped_content = []
    errors = []
    
    try:
        llm = create_researcher_agent()
        prompt = ChatPromptTemplate.from_template(RESEARCHER_PROMPT)
        
        for task in research_tasks:
            query = task.get("query", "")
            logger.info(f"Executing search: {query[:50]}...")
            
            try:
                # Perform web search
                search_results = web_search(query)
                
                if not search_results:
                    logger.warning(f"No results for query: {query}")
                    continue
                
                # Store raw results
                all_results.extend(search_results)
                
                # Optionally scrape top result for more content
                top_result = search_results[0]
                if top_result.get("url"):
                    scraped = scrape_url(top_result["url"])
                    if scraped.get("success"):
                        scraped_content.append({
                            "url": top_result["url"],
                            "title": scraped.get("title", ""),
                            "content": scraped.get("content", "")[:3000],  # Limit content
                        })
                
            except Exception as e:
                logger.error(f"Search failed for query '{query}': {e}")
                errors.append(f"Search error for '{query}': {e}")
        
        logger.info(f"Research complete: {len(all_results)} results from {len(research_tasks)} queries")
        
        return {
            "web_results": all_results,
            "scraped_content": scraped_content,
            "current_agent": "analyst",
            "errors": state.get("errors", []) + errors,
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "researcher",
                "action": "web_search_complete",
                "timestamp": datetime.now().isoformat(),
                "output": {
                    "queries_executed": len(research_tasks),
                    "results_found": len(all_results),
                    "pages_scraped": len(scraped_content),
                },
            }],
        }
        
    except Exception as e:
        logger.exception(f"Researcher agent failed: {e}")
        return {
            "web_results": all_results,
            "scraped_content": scraped_content,
            "current_agent": "analyst",
            "errors": state.get("errors", []) + [f"Researcher error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "researcher",
                "action": "error",
                "timestamp": datetime.now().isoformat(),
                "output": {"error": str(e)},
            }],
        }
