"""Synthesis Agent

This agent combines findings from research and analysis into a coherent report.
"""

from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from ..graph.state import AgentState
from ..utils.config import get_config
from ..utils.llm_provider import create_llm
from ..utils.logger import AgentLogger

logger = AgentLogger("synthesizer")


SYNTHESIS_PROMPT = """You are an expert research writer. Your task is to synthesize 
research findings into a comprehensive, well-structured report using IEEE citation style.

## Original Research Question
{query}

## Web Research Findings
{web_results}

## Data Analysis Results
{analysis_results}

{revision_context}

## Your Task
Create a comprehensive research report that:
1. Addresses the original research question thoroughly
2. Synthesizes all findings into a coherent narrative
3. USES IEEE CITATION FORMAT: [1], [2], etc. for all claims
4. Includes data analysis insights where applicable
5. Draws meaningful conclusions

## Citation Guidelines (IEEE Style)
- Use numbered citations in square brackets: [1], [2], [3]
- Multiple citations: [1], [2] or [1]-[3]
- Each source should have a unique number
- References section lists all sources by number

## Report Structure
Use this markdown structure:

# [Research Question Rephrased as Title]

## Executive Summary
[2-3 sentence summary of key findings with citations]

## Methodology
- Sources consulted: [N web sources]
- Analysis performed: [Types of analysis]

## Findings

### [Topic 1]
[Detailed findings with IEEE citations like [1], [2]]

### [Topic 2]
[More findings with citations]

## Data Analysis
[If applicable: analysis results and interpretations]

## Conclusions
[Key takeaways and implications]

## References
Format each reference as:
[1] "Title", URL, Accessed: Date.
[2] "Title", URL, Accessed: Date.

## Important Guidelines
- Every factual claim MUST have an IEEE citation [N]
- Use professional, objective language
- Be thorough but concise
- If information is uncertain, acknowledge it
- Make the report actionable and insightful"""


REVISION_PROMPT = """
## Revision Requested
The previous draft was reviewed and the following issues were identified:
{revision_requests}

Please address these issues in your revised report. Pay special attention to:
- Adding missing IEEE citations [N]
- Removing any unsupported claims
- Improving factual accuracy
"""


def create_synthesizer_agent():
    """Create the synthesizer agent LLM"""
    config = get_config()
    return create_llm(temperature=0.3, max_tokens=config.llm.max_tokens)


def format_web_results(results: list) -> str:
    """Format web results for the prompt with numbered references"""
    if not results:
        return "No web research results available."
    
    formatted = []
    for i, result in enumerate(results[:10], 1):  # Limit to top 10
        formatted.append(
            f"**[{i}] Source:** {result.get('title', 'Untitled')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'No content')[:500]}...\n"
            f"(Use citation [A{i}] to reference this source)"
        )
    
    return "\n---\n".join(formatted)


def format_analysis_results(results: list) -> str:
    """Format analysis results for the prompt"""
    if not results:
        return "No data analysis was performed."
    
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(
            f"**Analysis {i}:** {result.get('task', 'Unnamed analysis')}\n"
            f"Method: {result.get('method', 'N/A')}\n"
            f"Result: {result.get('result', 'No result')[:300]}\n"
            f"Interpretation: {result.get('interpretation', 'N/A')[:500]}...\n"
        )
    
    return "\n---\n".join(formatted)



async def synthesizer_node(state: AgentState) -> dict:
    """
    Synthesis agent node for the research workflow.
    
    Combines all research and analysis findings into a coherent report.
    """
    logger.info("Starting synthesis phase", {"iteration": state.get("iteration_count", 0)})
    
    # Check for revision requests
    revision_requests = state.get("revision_requests", [])
    revision_context = ""
    if revision_requests:
        revision_context = REVISION_PROMPT.format(
            revision_requests="\n".join(f"- {r}" for r in revision_requests)
        )
        logger.info(f"Addressing {len(revision_requests)} revision requests")
    
    try:
        llm = create_synthesizer_agent()
        prompt = ChatPromptTemplate.from_template(SYNTHESIS_PROMPT)
        
        # Format inputs
        web_results_text = format_web_results(state.get("web_results", []))
        analysis_results_text = format_analysis_results(state.get("analysis_results", []))
        
        response = await (prompt | llm).ainvoke({
            "query": state["query"],
            "web_results": web_results_text,
            "analysis_results": analysis_results_text,
            "revision_context": revision_context,
        })
        
        draft_report = response.content
        
        # Build citations from web_results (for IEEE format)
        # The LLM should have used [1], [2], etc. based on our numbered sources
        citations = []
        web_results = state.get("web_results", [])
        
        for i, result in enumerate(web_results[:10], 1):
            citations.append({
                "id": i,
                "source": "web",
                "title": result.get("title", "Unknown Title"),
                "url": result.get("url", ""),
                "accessed_date": datetime.now().strftime("%Y-%m-%d"),
            })

        
        logger.info(f"Draft report created: {len(draft_report)} chars, {len(citations)} citations")
        
        return {
            "draft_report": draft_report,
            "citations": citations,
            "revision_requests": [],  # Clear revision requests after addressing
            "current_agent": "critic",
            "iteration_count": state.get("iteration_count", 0) + 1,
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "synthesizer",
                "action": "draft_created",
                "timestamp": datetime.now().isoformat(),
                "output": {
                    "report_length": len(draft_report),
                    "citations_found": len(citations),
                    "is_revision": len(revision_requests) > 0,
                },
            }],
        }
        
    except Exception as e:
        logger.exception(f"Synthesizer agent failed: {e}")
        return {
            "draft_report": state.get("draft_report", ""),
            "current_agent": "critic",
            "errors": state.get("errors", []) + [f"Synthesizer error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "synthesizer",
                "action": "error",
                "timestamp": datetime.now().isoformat(),
                "output": {"error": str(e)},
            }],
        }
