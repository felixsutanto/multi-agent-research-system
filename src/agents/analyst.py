"""Data Analyst Agent

This agent processes data and performs quantitative analysis using Python.
"""

from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from ..graph.state import AgentState
from ..tools.python_repl import execute_python
from ..utils.config import get_config
from ..utils.llm_provider import create_llm
from ..utils.logger import AgentLogger

logger = AgentLogger("analyst")


ANALYST_PROMPT = """You are an expert data analyst. Your task is to analyze data
and perform calculations based on the research findings and analysis request.

## Analysis Request
{analysis_task}

## Available Data from Research
{research_data}

## Your Task
1. Identify what calculations or analysis can be performed
2. Write Python code to perform the analysis
3. Interpret the results

## Guidelines
- Use numpy (np) and pandas (pd) for data processing
- Use statistics module for statistical calculations
- Use print() statements to show results
- Include comments explaining your approach
- If the data is insufficient, explain what's missing

## Output Format
Provide your analysis with:
1. **Approach**: What analysis you're performing and why
2. **Code**: Python code to execute (will be run automatically)
3. **Interpretation**: What the results mean

Format your Python code in a ```python code block."""


CODE_EXTRACTION_PROMPT = """Extract ONLY the Python code from the following text.
Return ONLY the code, no explanations or markdown formatting.

Text:
{text}

Python code:"""


def create_analyst_agent():
    """Create the analyst agent LLM"""
    return create_llm(temperature=0)  # Deterministic for code generation


def extract_python_code(text: str) -> str | None:
    """Extract Python code from markdown code blocks"""
    if "```python" in text:
        parts = text.split("```python")
        if len(parts) > 1:
            code = parts[1].split("```")[0]
            return code.strip()
    elif "```" in text:
        parts = text.split("```")
        if len(parts) > 1:
            code = parts[1]
            # Skip language identifier if present
            lines = code.split("\n")
            if lines[0].strip() in ["python", "py", ""]:
                code = "\n".join(lines[1:])
            return code.strip()
    return None


async def analyst_node(state: AgentState) -> dict:
    """
    Data analyst agent node for the research workflow.
    
    Executes data analysis tasks using Python code execution.
    """
    logger.info("Starting analysis phase")
    
    # Get analysis tasks from the plan
    analysis_tasks = [
        task for task in state.get("research_plan", [])
        if task.get("type") == "data_analysis"
    ]
    
    if not analysis_tasks:
        logger.info("No analysis tasks in plan - skipping")
        return {
            "analysis_results": [],
            "code_snippets": [],
            "current_agent": "synthesizer",
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "analyst",
                "action": "no_tasks",
                "timestamp": datetime.now().isoformat(),
                "output": None,
            }],
        }
    
    # Limit tasks
    config = get_config()
    analysis_tasks = analysis_tasks[:config.agents.max_analysis_tasks]
    
    # Prepare research data summary for the LLM
    web_results = state.get("web_results", [])
    research_summary = "\n".join([
        f"- {r.get('title', 'Untitled')}: {r.get('content', '')[:200]}..."
        for r in web_results[:5]
    ])
    
    analysis_results = []
    code_snippets = []
    errors = []
    
    try:
        llm = create_analyst_agent()
        prompt = ChatPromptTemplate.from_template(ANALYST_PROMPT)
        
        for task in analysis_tasks:
            task_query = task.get("query", "")
            logger.info(f"Analyzing: {task_query[:50]}...")
            
            try:
                # Get analysis plan from LLM
                response = await (prompt | llm).ainvoke({
                    "analysis_task": task_query,
                    "research_data": research_summary or "No research data available yet.",
                })
                
                # Extract and execute Python code
                code = extract_python_code(response.content)
                
                if code:
                    code_snippets.append(code)
                    result = execute_python(code)
                    
                    analysis_results.append({
                        "task": task_query,
                        "method": "Python analysis",
                        "code": code,
                        "result": result.get("output", ""),
                        "interpretation": response.content,
                    })
                    
                    if not result.get("success"):
                        errors.append(f"Code execution error: {result.get('error')}")
                else:
                    # No code generated - store the analysis as interpretation only
                    analysis_results.append({
                        "task": task_query,
                        "method": "Qualitative analysis",
                        "code": "",
                        "result": "",
                        "interpretation": response.content,
                    })
                
            except Exception as e:
                logger.error(f"Analysis failed for task '{task_query}': {e}")
                errors.append(f"Analysis error: {e}")
        
        logger.info(f"Analysis complete: {len(analysis_results)} analyses performed")
        
        return {
            "analysis_results": analysis_results,
            "code_snippets": code_snippets,
            "current_agent": "synthesizer",
            "errors": state.get("errors", []) + errors,
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "analyst",
                "action": "analysis_complete",
                "timestamp": datetime.now().isoformat(),
                "output": {
                    "tasks_completed": len(analysis_results),
                    "code_executed": len(code_snippets),
                },
            }],
        }
        
    except Exception as e:
        logger.exception(f"Analyst agent failed: {e}")
        return {
            "analysis_results": analysis_results,
            "code_snippets": code_snippets,
            "current_agent": "synthesizer",
            "errors": state.get("errors", []) + [f"Analyst error: {e}"],
            "agent_interactions": state.get("agent_interactions", []) + [{
                "agent": "analyst",
                "action": "error",
                "timestamp": datetime.now().isoformat(),
                "output": {"error": str(e)},
            }],
        }
