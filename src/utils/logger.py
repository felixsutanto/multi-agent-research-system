"""Logging utilities for Multi-Agent Research System"""

import logging
import sys
from typing import Any

from .config import get_config


def setup_logger(name: str = "research_system") -> logging.Logger:
    """Setup and return a configured logger"""
    config = get_config()
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.logging.level))
    
    # Avoid adding handlers multiple times
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, config.logging.level))
        
        # Formatter
        formatter = logging.Formatter(config.logging.format)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


def get_agent_logger(agent_name: str) -> logging.Logger:
    """Get a logger for a specific agent"""
    return setup_logger(f"research_system.agents.{agent_name}")


class AgentLogger:
    """Context-aware logger for agents"""
    
    def __init__(self, agent_name: str):
        self.logger = get_agent_logger(agent_name)
        self.agent_name = agent_name
    
    def _format_message(self, message: str, context: dict[str, Any] | None = None) -> str:
        """Format message with agent context"""
        prefix = f"[{self.agent_name}]"
        if context:
            context_str = " ".join(f"{k}={v}" for k, v in context.items())
            return f"{prefix} {message} | {context_str}"
        return f"{prefix} {message}"
    
    def info(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Log info message"""
        self.logger.info(self._format_message(message, context))
    
    def debug(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Log debug message"""
        self.logger.debug(self._format_message(message, context))
    
    def warning(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Log warning message"""
        self.logger.warning(self._format_message(message, context))
    
    def error(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Log error message"""
        self.logger.error(self._format_message(message, context))
    
    def exception(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Log exception with traceback"""
        self.logger.exception(self._format_message(message, context))
