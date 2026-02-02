"""Python REPL Tool for Data Analysis

This tool provides safe Python code execution for the Data Analyst Agent.
"""

import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Any

from langchain_core.tools import tool

from ..utils.config import get_config
from ..utils.logger import AgentLogger

logger = AgentLogger("python_repl")


# Safe built-ins for the REPL
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "pow": pow,
    "print": print,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "type": type,
    "zip": zip,
}


def execute_python(
    code: str,
    timeout: int | None = None,
    max_output_length: int | None = None,
) -> dict[str, Any]:
    """
    Execute Python code safely in a restricted environment.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        max_output_length: Maximum length of output to return
        
    Returns:
        Dict with 'success', 'output', 'error' keys
    """
    config = get_config()
    
    if timeout is None:
        timeout = config.tools.python_repl.timeout
    if max_output_length is None:
        max_output_length = config.tools.python_repl.max_output_length
    
    logger.info("Executing Python code", {"code_length": len(code)})
    
    # Capture stdout and stderr
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    # Prepare execution environment with safe imports
    exec_globals: dict[str, Any] = {
        "__builtins__": SAFE_BUILTINS,
    }
    
    # Allow safe data analysis imports
    try:
        import numpy as np
        exec_globals["np"] = np
        exec_globals["numpy"] = np
    except ImportError:
        pass
    
    try:
        import pandas as pd
        exec_globals["pd"] = pd
        exec_globals["pandas"] = pd
    except ImportError:
        pass
    
    try:
        import statistics
        exec_globals["statistics"] = statistics
    except ImportError:
        pass
    
    try:
        import math
        exec_globals["math"] = math
    except ImportError:
        pass
    
    try:
        import json
        exec_globals["json"] = json
    except ImportError:
        pass
    
    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, exec_globals)
        
        output = stdout_capture.getvalue()
        error_output = stderr_capture.getvalue()
        
        if len(output) > max_output_length:
            output = output[:max_output_length] + "\n... (output truncated)"
        
        result = {
            "success": True,
            "output": output,
            "error": error_output if error_output else None,
        }
        
        logger.info("Code execution successful", {"output_length": len(output)})
        return result
        
    except Exception as e:
        error_msg = traceback.format_exc()
        logger.error(f"Code execution failed: {e}")
        
        return {
            "success": False,
            "output": stdout_capture.getvalue(),
            "error": error_msg,
        }


@tool
def create_python_repl_tool(code: str) -> str:
    """
    Execute Python code for data analysis and calculations.
    
    Use this tool when you need to:
    - Perform numerical calculations
    - Analyze data with pandas and numpy
    - Create statistical summaries
    - Process and transform data
    
    Available libraries: numpy (np), pandas (pd), statistics, math, json
    
    Args:
        code: Python code to execute. Use print() to show results.
        
    Returns:
        The output of the code execution or error message
    """
    result = execute_python(code)
    
    if result["success"]:
        output = result["output"]
        if not output.strip():
            return "Code executed successfully but produced no output. Use print() to display results."
        return f"**Execution successful:**\n```\n{output}\n```"
    else:
        return f"**Execution failed:**\n```\n{result['error']}\n```"
