"""Vector Search Tool using ChromaDB

This tool provides document retrieval capabilities from a vector database.
"""

from typing import Any
from pathlib import Path

from langchain_core.tools import tool

from ..utils.config import get_config
from ..utils.logger import AgentLogger

logger = AgentLogger("vector_search")

# Lazy initialization of ChromaDB
_chroma_client = None
_collection = None


def get_chroma_collection():
    """Get or create ChromaDB collection"""
    global _chroma_client, _collection
    
    if _collection is None:
        import chromadb
        from chromadb.config import Settings
        
        # Create persistent storage directory
        persist_dir = Path(__file__).parent.parent.parent / "data" / "chroma"
        persist_dir.mkdir(parents=True, exist_ok=True)
        
        _chroma_client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        
        # Get or create the research documents collection
        _collection = _chroma_client.get_or_create_collection(
            name="research_documents",
            metadata={"description": "Research documents for the multi-agent system"},
        )
        
        logger.info(f"ChromaDB collection initialized with {_collection.count()} documents")
    
    return _collection


def add_documents(
    documents: list[str],
    metadatas: list[dict[str, Any]] | None = None,
    ids: list[str] | None = None,
) -> None:
    """
    Add documents to the vector database.
    
    Args:
        documents: List of document texts
        metadatas: Optional metadata for each document
        ids: Optional IDs for each document
    """
    collection = get_chroma_collection()
    
    if ids is None:
        # Generate IDs based on current count
        start_id = collection.count()
        ids = [f"doc_{start_id + i}" for i in range(len(documents))]
    
    if metadatas is None:
        metadatas = [{}] * len(documents)
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )
    
    logger.info(f"Added {len(documents)} documents to vector store")


def vector_search(
    query: str,
    top_k: int | None = None,
    min_score: float | None = None,
) -> list[dict[str, Any]]:
    """
    Search the vector database for relevant documents.
    
    Args:
        query: The search query
        top_k: Maximum number of results to return
        min_score: Minimum similarity score threshold
        
    Returns:
        List of matching documents with content, metadata, and scores
    """
    config = get_config()
    
    if top_k is None:
        top_k = config.tools.vector_search.top_k
    if min_score is None:
        min_score = config.tools.vector_search.min_score
    
    logger.info(f"Vector search for: {query}", {"top_k": top_k})
    
    try:
        collection = get_chroma_collection()
        
        if collection.count() == 0:
            logger.warning("Vector database is empty")
            return []
        
        results = collection.query(
            query_texts=[query],
            n_results=min(top_k, collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        
        # Convert distances to similarity scores (ChromaDB uses L2 distance)
        documents = []
        for i, doc in enumerate(results["documents"][0]):
            distance = results["distances"][0][i]
            # Convert L2 distance to similarity score (rough approximation)
            score = 1 / (1 + distance)
            
            if score >= min_score:
                documents.append({
                    "id": results["ids"][0][i],
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": round(score, 4),
                })
        
        logger.info(f"Found {len(documents)} matching documents")
        return documents
        
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []


@tool
def create_vector_search_tool(query: str) -> str:
    """
    Search the internal knowledge base for relevant documents.
    
    Use this tool when you need to find information from previously indexed
    documents and research materials.
    
    Args:
        query: The search query to find relevant documents
        
    Returns:
        A formatted string of matching documents with their content
    """
    results = vector_search(query)
    
    if not results:
        return "No relevant documents found in the knowledge base."
    
    formatted = []
    for i, doc in enumerate(results, 1):
        metadata_str = ", ".join(f"{k}: {v}" for k, v in doc["metadata"].items()) if doc["metadata"] else "None"
        formatted.append(
            f"**Document {i}** (Score: {doc['score']:.2f})\n"
            f"Metadata: {metadata_str}\n"
            f"Content: {doc['content']}\n"
        )
    
    return "\n---\n".join(formatted)
