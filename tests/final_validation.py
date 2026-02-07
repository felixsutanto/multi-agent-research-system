"""
Final comprehensive validation for portfolio deployment.

Runs a complete validation across multiple diverse queries
and reports overall quality metrics.
"""
import pytest
import asyncio
from src.graph.workflow import create_research_graph
from src.evaluation.rag_triad import RAGTriadEvaluator
from src.evaluation.custom_metrics import evaluate_citation_coverage


FINAL_TEST_QUERIES = [
    "What is LangGraph and how does it work?",
    "Explain the benefits of microservices architecture",
    "What are the key features of Python 3.12?",
]


@pytest.mark.asyncio
@pytest.mark.slow
async def test_final_validation():
    """Comprehensive final validation"""
    
    print("\n" + "="*60)
    print("🎯 FINAL PROJECT VALIDATION")
    print("="*60 + "\n")
    
    graph = create_research_graph()
    evaluator = RAGTriadEvaluator()
    
    results = []
    
    for i, query in enumerate(FINAL_TEST_QUERIES, 1):
        print(f"\n📝 Test Query {i}/{len(FINAL_TEST_QUERIES)}")
        print(f"Query: {query}\n")
        
        try:
            # Run research
            final_state = await graph.ainvoke({
                "query": query,
                "messages": [],
                "iteration_count": 0,
                "agent_interactions": [],
                "approved": False,
                "research_plan": [],
                "web_results": [],
                "analysis_results": {},
                "draft_report": "",
                "final_report": "",
                "citations": [],
                "errors": [],
            })
            
            report = final_state.get("final_report") or final_state.get("draft_report", "")
            web_results = final_state.get("web_results", [])
            
            # Get web content for evaluation
            web_content = "\n".join(
                r.get("content", "") for r in web_results[:5]
            )
            
            # Evaluate if we have content
            metrics = {"context_relevance": 0, "groundedness": 0, "answer_relevance": 0}
            if report and web_content:
                try:
                    eval_result = await evaluator.evaluate_all(query, web_content, report)
                    metrics = {
                        "context_relevance": eval_result.get("context_relevance", {}).get("score", 0),
                        "groundedness": eval_result.get("groundedness", {}).get("score", 0),
                        "answer_relevance": eval_result.get("answer_relevance", {}).get("score", 0),
                    }
                except Exception as e:
                    print(f"Warning: Evaluation failed: {e}")
            
            # Citation coverage
            citation_result = evaluate_citation_coverage(report, web_results)
            citation_coverage = citation_result.get("score", 0)
            
            # Collect results
            result = {
                "query": query,
                "length": len(report),
                "agents_used": len(set(log["agent"] for log in final_state.get("agent_interactions", []))),
                "context_relevance": metrics.get("context_relevance", 0),
                "groundedness": metrics.get("groundedness", 0),
                "answer_relevance": metrics.get("answer_relevance", 0),
                "citation_coverage": citation_coverage,
                "approved": final_state.get("approved", False),
                "success": len(report) > 200,
            }
            
            results.append(result)
            
            # Print results
            print(f"✓ Length: {result['length']} chars")
            print(f"✓ Agents: {result['agents_used']}")
            print(f"✓ Approved: {result['approved']}")
            print(f"✓ Success: {result['success']}")
            
        except Exception as e:
            print(f"✗ Query failed: {e}")
            results.append({
                "query": query,
                "length": 0,
                "success": False,
            })
    
    # Summary
    print("\n" + "="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60 + "\n")
    
    successful = [r for r in results if r.get("success")]
    success_rate = len(successful) / len(results) if results else 0
    
    print(f"Total Queries: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Success Rate: {success_rate * 100:.1f}%")
    
    if successful:
        avg_length = sum(r["length"] for r in successful) / len(successful)
        print(f"Average Report Length: {avg_length:.0f} chars")
    
    # Pass/Fail
    print("\n" + "="*60)
    if success_rate >= 0.6:
        print("✅ PROJECT VALIDATION PASSED")
    else:
        print("❌ PROJECT VALIDATION NEEDS IMPROVEMENT")
    print("="*60 + "\n")
    
    assert success_rate >= 0.5, f"At least 50% of queries should succeed: {success_rate}"


@pytest.mark.asyncio
async def test_quick_validation():
    """Quick validation with single query"""
    
    graph = create_research_graph()
    
    final_state = await graph.ainvoke({
        "query": "What is Python?",
        "messages": [],
        "iteration_count": 0,
        "agent_interactions": [],
        "approved": False,
        "research_plan": [],
        "web_results": [],
        "analysis_results": {},
        "draft_report": "",
        "final_report": "",
        "citations": [],
        "errors": [],
    })
    
    report = final_state.get("final_report") or final_state.get("draft_report", "")
    
    assert len(report) > 100, "Should produce substantial report"
    assert len(final_state.get("agent_interactions", [])) > 0, "Agents should run"
    
    print("✅ Quick Validation Passed")


if __name__ == "__main__":
    asyncio.run(test_final_validation())
