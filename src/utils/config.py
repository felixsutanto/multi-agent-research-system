"""Configuration loader for Multi-Agent Research System"""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """LLM configuration settings"""
    model: str = "gpt-4o"
    temperature: float = 0.0
    max_tokens: int = 4096
    timeout: int = 60


class AgentConfig(BaseModel):
    """Agent configuration settings"""
    max_iterations: int = 3
    max_research_tasks: int = 5
    max_analysis_tasks: int = 3


class WebSearchConfig(BaseModel):
    """Web search tool configuration"""
    max_results: int = 5
    include_raw_content: bool = True


class VectorSearchConfig(BaseModel):
    """Vector search tool configuration"""
    top_k: int = 5
    min_score: float = 0.7


class PythonReplConfig(BaseModel):
    """Python REPL tool configuration"""
    timeout: int = 30
    max_output_length: int = 5000


class ToolsConfig(BaseModel):
    """Tools configuration settings"""
    web_search: WebSearchConfig = Field(default_factory=WebSearchConfig)
    vector_search: VectorSearchConfig = Field(default_factory=VectorSearchConfig)
    python_repl: PythonReplConfig = Field(default_factory=PythonReplConfig)


class EvaluationConfig(BaseModel):
    """Evaluation configuration settings"""
    context_relevance_threshold: float = 0.80
    groundedness_threshold: float = 0.90
    answer_relevance_threshold: float = 0.85


class APIConfig(BaseModel):
    """API configuration settings"""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class LoggingConfig(BaseModel):
    """Logging configuration settings"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class Config(BaseModel):
    """Main configuration class"""
    llm: LLMConfig = Field(default_factory=LLMConfig)
    agents: AgentConfig = Field(default_factory=AgentConfig)
    tools: ToolsConfig = Field(default_factory=ToolsConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_config(config_path: str | None = None) -> Config:
    """Load configuration from YAML file and environment variables"""
    # Load environment variables
    load_dotenv()
    
    # Default config path
    if config_path is None:
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "config.yaml"
    
    # Load YAML config if exists
    config_data: dict[str, Any] = {}
    if Path(config_path).exists():
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f) or {}
    
    return Config(**config_data)


def get_openai_api_key() -> str:
    """Get OpenAI API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def get_tavily_api_key() -> str:
    """Get Tavily API key from environment"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is not set")
    return api_key


# Global config instance
_config: Config | None = None


def get_config() -> Config:
    """Get or create global config instance"""
    global _config
    if _config is None:
        _config = load_config()
    return _config
