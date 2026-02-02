"""Lightweight Gradio Interface for Multi-Agent Research System

Optimized for Hugging Face Spaces 2GB memory limit.
"""

import gradio as gr
import os


def conduct_research_simple(query: str):
    """
    Simple research interface that checks environment first.
    """
    if not query or len(query) < 10:
        return "❌ Please enter a research question (at least 10 characters)", "", ""
    
    # Check API keys
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if not groq_key or not tavily_key:
        return """❌ **API Keys Missing**
        
Please add these secrets in Space Settings → Repository secrets:
- `GROQ_API_KEY` 
- `TAVILY_API_KEY`

Then restart the Space.""", "", ""
    
    try:
        # Lazy import to save memory
        import asyncio
        from src.graph.workflow import run_research
        
        # Run research
        result = asyncio.run(run_research(query, use_checkpointer=False))
        
        # Format output
        report = result.get("final_report", "No report generated")
        
        metrics = f"""## Metrics
- **Iterations**: {result.get('iteration_count', 0)}
- **Approved**: {'✅' if result.get('approved') else '❌'}
- **Citations**: {len(result.get('citations', []))}
"""
        
        logs = f"**Status**: Research completed successfully"
        
        return report, metrics, logs
        
    except Exception as e:
        return f"❌ Error: {str(e)}", "", f"**Error Details**: {type(e).__name__}"


# Simple Gradio interface
demo = gr.Interface(
    fn=conduct_research_simple,
    inputs=gr.Textbox(
        label="Research Question",
        placeholder="What are the latest developments in AI?",
        lines=3
    ),
    outputs=[
        gr.Markdown(label="Research Report"),
        gr.Markdown(label="Metrics"),
        gr.Markdown(label="Status")
    ],
    title="🔬 Multi-Agent Research System",
    description="""
    Ask any research question and get a comprehensive report with citations.
    
    **Powered by**: Groq Llama 3.3 70B (free) + Tavily Search (free)
    
    ⏱️ Takes 2-3 minutes to complete
    """,
    examples=[
        ["What are the benefits of renewable energy?"],
        ["How does quantum computing work?"],
        ["Explain the impact of climate change"],
    ],
    theme=gr.themes.Soft(),
    allow_flagging="never"
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
