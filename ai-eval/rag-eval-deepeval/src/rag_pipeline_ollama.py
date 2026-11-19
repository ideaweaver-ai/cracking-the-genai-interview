"""
src/rag_pipeline_ollama.py — full RAG path with local Ollama embed + chat.

Does not change src/rag_pipeline.py.

Run:
  python -m src.rag_pipeline_ollama
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.reranker_ollama import RerankingRetrieverOllama
from src.generator_ollama import generate


class RagPipelineOllama:
    def __init__(self, fetch_k: int = 10, top_k: int = 5):
        self.retriever = RerankingRetrieverOllama(fetch_k=fetch_k, top_k=top_k)

    def invoke(self, query: str) -> dict:
        docs = self.retriever.invoke(query)
        context = [doc.page_content for doc in docs]
        answer = generate(query, context)
        return {
            "query": query,
            "context": context,
            "answer": answer,
        }


if __name__ == "__main__":
    rag = RagPipelineOllama()
    result = rag.invoke("What is a Kubernetes Deployment?")
    print("QUERY:  ", result["query"])
    print("ANSWER: ", result["answer"])
    print("\nCONTEXT CHUNKS:")
    for i, chunk in enumerate(result["context"]):
        print(f"  [{i}] {chunk[:120]}...")
