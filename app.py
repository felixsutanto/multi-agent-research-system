"""Gradio Web Interface for Multi-Agent Research System"""

import asyncio
import gradio as gr
from src.graph.workflow import run_research
from src.utils.logger import setup_logger

logger = setup_logger("gradio_app")


async def conduct_research(query: str, progress=gr.Progress()):
    """
    Conduct research using the multi-agent system.
    
    Args:
        query: Research question from user
        progress: Gradio progress tracker
    
    Returns:
        tuple: (report, metrics, logs)
    """
    if not query or len(query) < 10:
        return "❌ Please enter a research question (at least 10 characters)", "", ""
    
    try:
        progress(0, desc="Starting research...")
        
        # Run the research workflow
        progress(0.2, desc="Planning research tasks...")
        result = await run_research(query, use_checkpointer=False)
        
        progress(0.9, desc="Finalizing report...")
        
        # Format the report
        report = result.get("final_report", "No report generated")
        
        # Format metrics
        metrics = f"""## Research Metrics
        
- **Iterations**: {result.get('iteration_count', 0)}
- **Approved**: {'✅ Yes' if result.get('approved') else '❌ No'}
- **Web Results**: {len(result.get('web_results', []))}
- **Citations**: {len(result.get('citations', []))}
- **Errors**: {len(result.get('errors', []))}
"""
        
        # Format agent logs
        interactions = result.get('agent_interactions', [])
        logs = "## Agent Activity\n\n"
        for i, interaction in enumerate(interactions[-10:], 1):  # Last 10 interactions
            agent = interaction.get('agent', 'unknown')
            action = interaction.get('action', 'unknown')
            logs += f"{i}. **{agent.title()}**: {action}\n"
        
        progress(1.0, desc="Complete!")
        return report, metrics, logs
        
    except Exception as e:
        logger.exception(f"Research failed: {e}")
        return f"❌ Error: {str(e)}", "", ""


def sync_research(query: str, progress=gr.Progress()):
    """Synchronous wrapper for Gradio"""
    return asyncio.run(conduct_research(query, progress))


# Create Gradio interface
with gr.Blocks(title="Multi-Agent Research System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔬 Multi-Agent Research System
    
    > Powered by **5 AI Agents** working together: Planner → Researcher → Analyst → Synthesizer → Critic
    
    Ask any research question and get a comprehensive, cited report!
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            query_input = gr.Textbox(
                label="Research Question",
                placeholder="e.g., What are the latest developments in artificial intelligence?",
                lines=3,
                max_lines=5
            )
            
            with gr.Row():
                submit_btn = gr.Button("🚀 Start Research", variant="primary", size="lg")
                clear_btn = gr.ClearButton(components=[query_input], value="Clear")
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### Examples:
            - What are the benefits of renewable energy?
            - How does quantum computing work?
            - What are the latest trends in web development?
            - Explain the impact of climate change on biodiversity
            """)
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=2):
            report_output = gr.Markdown(
                label="Research Report",
                value="*Your research report will appear here...*"
            )
        
        with gr.Column(scale=1):
            metrics_output = gr.Markdown(
                label="Metrics",
                value=""
            )
            logs_output = gr.Markdown(
                label="Agent Logs",
                value=""
            )
    
    # Event handlers
    submit_btn.click(
        fn=sync_research,
        inputs=[query_input],
        outputs=[report_output, metrics_output, logs_output]
    )
    
    gr.Markdown("""
    ---
    ### 🌟 Features
    - **Free APIs**: Groq Llama 3.3 70B + Tavily Search
    - **Quality Control**: Automatic revision loops
    - **Citations**: All claims backed by sources
    - **Evaluation**: RAG Triad metrics
    
    **GitHub**: [felixsutanto/multi-agent-research-system](https://github.com/felixsutanto/multi-agent-research-system)
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
