"""FastAPI-only Application for Hugging Face Spaces

This replaces the Gradio interface with a pure FastAPI backend.
The frontend will connect to these endpoints directly.
"""

import uvicorn
from src.api.main import app

# The FastAPI app is imported from src.api.main
# All endpoints are already configured there:
# - GET  /              - API info
# - GET  /health        - Health check  
# - POST /research      - Conduct research
# - WS   /ws/research   - WebSocket streaming

if __name__ == "__main__":
    # Run on Hugging Face Spaces port
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,
        log_level="info"
    )
