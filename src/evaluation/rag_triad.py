"""RAG Triad Evaluation Metrics

This module implements the RAG Triad evaluation framework:
- Context Relevance: How relevant are retrieved documents to the query?
- Groundedness: Is the answer supported by the context?
- Answer Relevance: Does the answer address the question?
"""

from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from ..utils.config import get_config
from ..utils.llm_provider import create_llm
from ..utils.logger import setup_logger

logger = setup_logger("evaluation.rag_triad")


CONTEXT_RELEVANCE_PROMPT = """You are evaluating the relevance of search results to a query.

## Query
{query}

## Retrieved Context
{context}

## Task
Rate how relevant the retrieved context is to answering the query.
Consider:
- Does the context contain information needed to answer the query?
- Is the information directly related or tangential?
- Would this context help in formulating a good answer?

Provide a score from 0.0 to 1.0:
- 0.0-0.3: Not relevant - context doesn't relate to query
- 0.4-0.6: Partially relevant - some useful information
- 0.7-0.8: Relevant - good information for answering
- 0.9-1.0: Highly relevant - excellent, comprehensive context

Respond with ONLY a JSON object:
{{"score": 0.85, "reasoning": "Brief explanation of the score"}}"""


GROUNDEDNESS_PROMPT = """You are evaluating whether an answer is grounded in the provided context.

## Context (Source Material)
{context}

## Answer to Evaluate
{answer}

## Task
Evaluate what percentage of claims in the answer are supported by the context.

For each claim in the answer, check if it can be verified from the context.
Unsupported claims or hallucinations should reduce the score.

Provide a score from 0.0 to 1.0:
- 0.0-0.3: Mostly unsupported - significant hallucinations
- 0.4-0.6: Partially supported - some claims not in context
- 0.7-0.8: Well supported - minor unsupported details
- 0.9-1.0: Fully grounded - all claims verified in context

Respond with ONLY a JSON object:
{{"score": 0.92, "reasoning": "Brief explanation", "unsupported_claims": ["list of unsupported claims if any"]}}"""


ANSWER_RELEVANCE_PROMPT = """You are evaluating whether an answer actually addresses the question asked.

## Original Question
{query}

## Answer
{answer}

## Task
Evaluate how well the answer addresses the specific question asked.

Consider:
- Does the answer directly address what was asked?
- Is the answer complete or does it miss key aspects?
- Is there irrelevant information that doesn't help?

Provide a score from 0.0 to 1.0:
- 0.0-0.3: Off-topic - doesn't address the question
- 0.4-0.6: Partially answers - missing key aspects
- 0.7-0.8: Good answer - addresses main points
- 0.9-1.0: Excellent - comprehensive, directly addresses question

Respond with ONLY a JSON object:
{{"score": 0.88, "reasoning": "Brief explanation"}}"""


class RAGTriadEvaluator:
    """Evaluator for RAG Triad metrics using LLM-as-judge"""
    
    def __init__(self):
        self.llm = create_llm(temperature=0)
    
    async def evaluate_context_relevance(
        self,
        query: str,
        context: str,
    ) -> dict[str, Any]:
        """
        Evaluate how relevant the retrieved context is to the query.
        
        Args:
            query: The original research question
            context: The retrieved context/documents
            
        Returns:
            Dict with score and reasoning
        """
        prompt = ChatPromptTemplate.from_template(CONTEXT_RELEVANCE_PROMPT)
        
        try:
            response = await (prompt | self.llm).ainvoke({
                "query": query,
                "context": context[:5000],  # Limit context length
            })
            
            import json
            result = json.loads(response.content)
            return {
                "metric": "context_relevance",
                "score": result.get("score", 0.0),
                "reasoning": result.get("reasoning", ""),
            }
        except Exception as e:
            logger.error(f"Context relevance evaluation failed: {e}")
            return {"metric": "context_relevance", "score": 0.0, "error": str(e)}
    
    async def evaluate_groundedness(
        self,
        context: str,
        answer: str,
    ) -> dict[str, Any]:
        """
        Evaluate how well the answer is grounded in the context.
        
        Args:
            context: The source context/documents
            answer: The generated answer/report
            
        Returns:
            Dict with score, reasoning, and unsupported claims
        """
        prompt = ChatPromptTemplate.from_template(GROUNDEDNESS_PROMPT)
        
        try:
            response = await (prompt | self.llm).ainvoke({
                "context": context[:5000],
                "answer": answer[:3000],
            })
            
            import json
            result = json.loads(response.content)
            return {
                "metric": "groundedness",
                "score": result.get("score", 0.0),
                "reasoning": result.get("reasoning", ""),
                "unsupported_claims": result.get("unsupported_claims", []),
            }
        except Exception as e:
            logger.error(f"Groundedness evaluation failed: {e}")
            return {"metric": "groundedness", "score": 0.0, "error": str(e)}
    
    async def evaluate_answer_relevance(
        self,
        query: str,
        answer: str,
    ) -> dict[str, Any]:
        """
        Evaluate how well the answer addresses the question.
        
        Args:
            query: The original research question
            answer: The generated answer/report
            
        Returns:
            Dict with score and reasoning
        """
        prompt = ChatPromptTemplate.from_template(ANSWER_RELEVANCE_PROMPT)
        
        try:
            response = await (prompt | self.llm).ainvoke({
                "query": query,
                "answer": answer[:3000],
            })
            
            import json
            result = json.loads(response.content)
            return {
                "metric": "answer_relevance",
                "score": result.get("score", 0.0),
                "reasoning": result.get("reasoning", ""),
            }
        except Exception as e:
            logger.error(f"Answer relevance evaluation failed: {e}")
            return {"metric": "answer_relevance", "score": 0.0, "error": str(e)}
    
    async def evaluate_all(
        self,
        query: str,
        context: str,
        answer: str,
    ) -> dict[str, Any]:
        """
        Run all three RAG Triad evaluations.
        
        Args:
            query: The original research question
            context: The retrieved context/documents
            answer: The generated answer/report
            
        Returns:
            Dict with all three scores and overall assessment
        """
        import asyncio
        
        # Run all evaluations concurrently
        results = await asyncio.gather(
            self.evaluate_context_relevance(query, context),
            self.evaluate_groundedness(context, answer),
            self.evaluate_answer_relevance(query, answer),
        )
        
        context_relevance = results[0]
        groundedness = results[1]
        answer_relevance = results[2]
        
        # Calculate overall score (weighted average)
        overall_score = (
            context_relevance.get("score", 0) * 0.25 +
            groundedness.get("score", 0) * 0.50 +  # Weight groundedness higher
            answer_relevance.get("score", 0) * 0.25
        )
        
        config = get_config()
        
        return {
            "context_relevance": context_relevance,
            "groundedness": groundedness,
            "answer_relevance": answer_relevance,
            "overall_score": round(overall_score, 3),
            "thresholds_met": {
                "context_relevance": context_relevance.get("score", 0) >= config.evaluation.context_relevance_threshold,
                "groundedness": groundedness.get("score", 0) >= config.evaluation.groundedness_threshold,
                "answer_relevance": answer_relevance.get("score", 0) >= config.evaluation.answer_relevance_threshold,
            },
        }


async def evaluate_rag_triad(
    query: str,
    context: str,
    answer: str,
) -> dict[str, Any]:
    """
    Convenience function to evaluate RAG Triad metrics.
    
    Args:
        query: The research question
        context: The retrieved context
        answer: The generated answer
        
    Returns:
        Complete evaluation results
    """
    evaluator = RAGTriadEvaluator()
    return await evaluator.evaluate_all(query, context, answer)
