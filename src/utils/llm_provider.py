"""LLM Provider abstraction for Multi-Agent Research System

Supports multiple LLM providers:
- OpenAI (GPT-4o)
- Groq (Llama 3 - FREE)
"""

import os
from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel

from .config import get_config
from .logger import setup_logger

logger = setup_logger("llm_provider")

LLMProvider = Literal["openai", "groq"]


def get_llm_provider() -> LLMProvider:
    """Detect which LLM provider to use based on available API keys"""
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    elif os.getenv("OPENAI_API_KEY"):
        return "openai"
    else:
        # Default to Groq as it's free
        return "groq"


def get_groq_api_key() -> str:
    """Get Groq API key from environment"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set. "
            "Get a free API key at https://console.groq.com"
        )
    return api_key


def create_llm(
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> BaseChatModel:
    """
    Create an LLM instance based on available API keys.
    
    Priority: Groq (free) > OpenAI
    
    Args:
        temperature: LLM temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        A LangChain chat model instance
    """
    config = get_config()
    provider = get_llm_provider()
    
    if temperature is None:
        temperature = config.llm.temperature
    if max_tokens is None:
        max_tokens = config.llm.max_tokens
    
    if provider == "groq":
        from langchain_groq import ChatGroq
        
        logger.info("Using Groq (Llama 3) - FREE tier")
        return ChatGroq(
            model="llama-3.3-70b-versatile",  # Free, fast, powerful
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=get_groq_api_key(),
        )
    
    else:  # openai
        from langchain_openai import ChatOpenAI
        from .config import get_openai_api_key
        
        logger.info("Using OpenAI (GPT-4o)")
        return ChatOpenAI(
            model=config.llm.model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=get_openai_api_key(),
            timeout=config.llm.timeout,
        )
