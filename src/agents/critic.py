"""Critic Agent

This agent reviews reports for quality, accuracy, and hallucinations.
"""

import json
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from ..graph.state import AgentState
from ..utils.config import get_config
from ..utils.llm_provider import create_llm
from ..utils.logger import AgentLogger

logger = AgentLogger("critic")


CRITIC_PROMPT = """You are a critical quality reviewer for research reports.
Your job is to identify issues and ensure the report meets high quality standards.

## Original Research Question
{query}

## Draft Report to Review
{draft_report}

## Source Materials (Web Search Results)
{web_results}

## Review Criteria
Evaluate the report on:

1. **Groundedness** (0.0-1.0): Are ALL claims supported by the provided sources?
   - Every factual statement should have a citation
   - Claims should accurately reflect what sources say
   - No speculation presented as fact

2. **Citation Coverage** (0.0-1.0): What percentage of claims have proper citations?
   - Look for [Source: URL] format
   - Verify citations exist in source materials

3. **Answer Relevance**: Does the report actually answer the research question?

4. **Logical Consistency**: Are there any contradictions or logical errors?

5. **Completeness**: Are there major gaps in the research?

## Output Format
Respond ONLY with a valid JSON object:
{{
    "approved": true/false,
    "groundedness_score": 0.0-1.0,
    "citation_coverage": 0.0-1.0,
    "answer_relevance_score": 0.0-1.0,
    "issues": [
        {{
            "type": "hallucination|missing_citation|logic_error|incomplete",
            "description": "specific issue description",
            "location": "section or paragraph where issue occurs",
            "severity": "high|medium|low"
        }}
    ],
    "revision_requests": [
        "Specific request 1: What to fix and how",
        "Specific request 2: Another fix needed"
    ],
    "summary": "Brief overall assessment"
}}

## Approval Criteria
- Approve if groundedness >= 0.85 AND citation_coverage >= 0.70
- Do NOT approve if there are any HIGH severity issues
- Do NOT approve if there are clear hallucinations

Important: Return ONLY the JSON object, no additional text."""


def create_critic_agent():
    """Create the critic agent LLM"""
    return create_llm(temperature=0)  # Strict evaluation


def format_web_results_for_review(results: list) -> str:
    """Format web results for review comparison"""
    if not results:
        return "No source materials available."
    
    formatted = []
    for result in results[:10]:
        formatted.append(
            f"URL: {result.get('url', 'N/A')}\n"
            f"Title: {result.get('title', 'Untitled')}\n"
            f"Content: {result.get('content', '')[:300]}...\n"
        )
    
    return "\n---\n".join(formatted)


async def critic_node(state: AgentState) -> dict:
    """
    Critic agent node for the research workflow.
    
    Reviews the draft report for quality and decides whether to approve
    or send back for revision.
    """
    logger.info("Starting quality review", {"iteration": state.get("iteration_count", 0)})
    
    draft_report = state.get("draft_report", "")
    
    if not draft_report:
        logger.warning("No draft report to review")
        return {
            "approved": False,
            "quality_assessment": None,
            "revision_requests": ["No draft report was generated. Please create a report."],
            "current_agent": "synthesizer",
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "critic",
                "action": "no_draft",
                "timestamp": datetime.now().isoformat(),
                "output": None,
            }],
        }
    
    try:
        llm = create_critic_agent()
        prompt = ChatPromptTemplate.from_template(CRITIC_PROMPT)
        
        web_results_text = format_web_results_for_review(state.get("web_results", []))
        
        response = await (prompt | llm).ainvoke({
            "query": state["query"],
            "draft_report": draft_report,
            "web_results": web_results_text,
        })
        
        # Parse JSON response
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        assessment = json.loads(content.strip())
        
        approved = assessment.get("approved", False)
        revision_requests = assessment.get("revision_requests", [])
        
        # Check iteration limit
        config = get_config()
        iteration_count = state.get("iteration_count", 0)
        if iteration_count >= config.agents.max_iterations:
            logger.warning(f"Max iterations ({config.agents.max_iterations}) reached, forcing approval")
            approved = True
            revision_requests = []
        
        quality_assessment = {
            "approved": approved,
            "groundedness_score": assessment.get("groundedness_score", 0.0),
            "citation_coverage": assessment.get("citation_coverage", 0.0),
            "issues": assessment.get("issues", []),
            "revision_requests": revision_requests,
        }
        
        logger.info(
            f"Review complete: {'APPROVED' if approved else 'REVISIONS NEEDED'}",
            {
                "groundedness": quality_assessment["groundedness_score"],
                "citation_coverage": quality_assessment["citation_coverage"],
                "issues_found": len(quality_assessment["issues"]),
            }
        )
        
        # If approved, finalize the report
        final_report = draft_report if approved else ""
        
        return {
            "approved": approved,
            "quality_assessment": quality_assessment,
            "revision_requests": revision_requests,
            "final_report": final_report,
            "current_agent": "end" if approved else "synthesizer",
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "critic",
                "action": "review_complete",
                "timestamp": datetime.now().isoformat(),
                "output": {
                    "approved": approved,
                    "groundedness": quality_assessment["groundedness_score"],
                    "issues_count": len(quality_assessment["issues"]),
                },
            }],
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse critic response: {e}")
        # Default to approval to prevent infinite loops
        return {
            "approved": True,
            "quality_assessment": None,
            "final_report": draft_report,
            "current_agent": "end",
            "errors": state.get("errors", []) + [f"Critic JSON parse error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "critic",
                "action": "parse_error_approval",
                "timestamp": datetime.now().isoformat(),
                "output": {"error": str(e)},
            }],
        }
        
    except Exception as e:
        logger.exception(f"Critic agent failed: {e}")
        return {
            "approved": True,  # Default approve to prevent blocking
            "quality_assessment": None,
            "final_report": draft_report,
            "current_agent": "end",
            "errors": state.get("errors", []) + [f"Critic error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "critic",
                "action": "error",
                "timestamp": datetime.now().isoformat(),
                "output": {"error": str(e)},
            }],
        }
