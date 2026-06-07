"""FastAPI Application for Multi-Agent Research System

This module provides REST and WebSocket APIs for the research system.
"""

import asyncio
import json
from datetime import datetime
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ..graph.workflow import run_research, run_research_streaming
from ..graph.state import AgentState
from ..evaluation.rag_triad import evaluate_rag_triad
from ..evaluation.custom_metrics import evaluate_all_custom_metrics
from ..utils.config import get_config
from ..utils.logger import setup_logger

logger = setup_logger("api")


# Pydantic models for API
class ResearchRequest(BaseModel):
    """Request model for research endpoint"""
    query: str = Field(..., min_length=10, description="The research question")
    max_iterations: int = Field(default=3, ge=1, le=5, description="Max revision iterations")
    include_evaluation: bool = Field(default=True, description="Include RAG evaluation metrics")


class Citation(BaseModel):
    """Citation model"""
    id: int
    source: str
    title: str
    url: str | None
    accessed_date: str


class QualityMetrics(BaseModel):
    """Quality metrics model"""
    context_relevance: float | None = None
    groundedness: float | None = None
    answer_relevance: float | None = None
    overall_score: float | None = None  # Calculated average of RAG metrics
    citation_coverage: float | None = None
    task_success: bool = False
    latency_seconds: float | None = None


class AgentLog(BaseModel):
    """Agent interaction log"""
    agent: str
    action: str
    timestamp: str
    output: dict[str, Any] | None = None


class ResearchResponse(BaseModel):
    """Response model for research endpoint"""
    query: str
    report: str
    citations: list[Citation]
    metrics: QualityMetrics
    agent_log: list[AgentLog]
    iterations: int
    approved: bool
    errors: list[str]


# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Research System",
    description="AI-powered research system with specialized agents for comprehensive research",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Multi-Agent Research System",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/research": "POST - Conduct research",
            "/ws/research": "WebSocket - Streaming research",
        },
    }


@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Conduct comprehensive research on a query.
    
    This endpoint orchestrates multiple AI agents to:
    1. Plan the research approach
    2. Search the web for relevant information
    3. Analyze data (if applicable)
    4. Synthesize findings into a report
    5. Review and validate the report
    """
    logger.info(f"Research request received: {request.query[:100]}...")
    
    try:
        # Run the research workflow
        final_state = await run_research(request.query)
        
        # Prepare response
        report = final_state.get("final_report", "") or final_state.get("draft_report", "")
        
        # Run evaluation if requested
        metrics_data: dict[str, Any] = {}
        if request.include_evaluation and report:
            # Prepare context from web results
            web_content = "\n".join(
                r.get("content", "") for r in final_state.get("web_results", [])[:5]
            )
            
            if web_content:
                try:
                    rag_metrics = await evaluate_rag_triad(
                        query=request.query,
                        context=web_content,
                        answer=report,
                    )
                    metrics_data["context_relevance"] = rag_metrics["context_relevance"].get("score")
                    metrics_data["groundedness"] = rag_metrics["groundedness"].get("score")
                    metrics_data["answer_relevance"] = rag_metrics["answer_relevance"].get("score")
                except Exception as e:
                    logger.warning(f"RAG evaluation failed: {e}")
            
            # Custom metrics
            custom_metrics = evaluate_all_custom_metrics(final_state)
            metrics_data["citation_coverage"] = custom_metrics["citation_coverage"]["score"]
            metrics_data["task_success"] = custom_metrics["task_success"]["success"]
        
        # Calculate overall_score from available metrics
        rag_scores = [
            metrics_data.get("context_relevance"),
            metrics_data.get("groundedness"),
            metrics_data.get("answer_relevance"),
        ]
        valid_scores = [s for s in rag_scores if s is not None]
        if valid_scores:
            metrics_data["overall_score"] = sum(valid_scores) / len(valid_scores)
        
        # Add latency
        if final_state.get("metrics"):
            metrics_data["latency_seconds"] = final_state["metrics"].get("latency_seconds")
        
        # Format citations
        citations = [
            Citation(
                id=c.get("id", i),
                source=c.get("source", "web"),
                title=c.get("title", ""),
                url=c.get("url"),
                accessed_date=c.get("accessed_date", datetime.now().strftime("%Y-%m-%d")),
            )
            for i, c in enumerate(final_state.get("citations", []), 1)
        ]
        
        # Format agent log
        agent_log = [
            AgentLog(
                agent=i.get("agent", "unknown"),
                action=i.get("action", "unknown"),
                timestamp=i.get("timestamp", ""),
                output=i.get("output"),
            )
            for i in final_state.get("agent_interactions", [])
        ]
        
        return ResearchResponse(
            query=request.query,
            report=report,
            citations=citations,
            metrics=QualityMetrics(**metrics_data),
            agent_log=agent_log,
            iterations=final_state.get("iteration_count", 0),
            approved=final_state.get("approved", False),
            errors=final_state.get("errors", []),
        )
        
    except Exception as e:
        logger.exception(f"Research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/research")
async def research_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for streaming research with real-time updates.
    
    Client sends: {"query": "research question"}
    Server sends: {"type": "agent_update", "agent": "name", "data": {...}}
    Server sends: {"type": "complete", "data": {...}}
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    
    try:
        # Receive initial query
        data = await websocket.receive_json()
        query = data.get("query")
        
        if not query:
            await websocket.send_json({
                "type": "error",
                "message": "Missing 'query' field",
            })
            await websocket.close()
            return
        
        logger.info(f"WebSocket research started: {query[:100]}...")
        
        # Stream updates
        final_state = None
        async for agent_name, state_update in run_research_streaming(query):
            final_state = state_update
            
            # Send update to client
            await websocket.send_json({
                "type": "agent_update",
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "current_agent": state_update.get("current_agent"),
                    "iteration": state_update.get("iteration_count", 0),
                    "approved": state_update.get("approved", False),
                    "has_report": bool(state_update.get("draft_report")),
                },
            })
        
        # Send final result
        if final_state:
            await websocket.send_json({
                "type": "complete",
                "data": {
                    "report": final_state.get("final_report") or final_state.get("draft_report", ""),
                    "approved": final_state.get("approved", False),
                    "iterations": final_state.get("iteration_count", 0),
                    "citations_count": len(final_state.get("citations", [])),
                },
            })
        
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.exception(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e),
            })
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


# Run with: uvicorn src.api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    config = get_config()
    uvicorn.run(
        "src.api.main:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
    )
