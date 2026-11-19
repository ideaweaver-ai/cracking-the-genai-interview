"""
src/reranker_ollama.py — cross-encoder rerank on top of the Ollama Chroma store.

Same as src/reranker.py, but pulls candidates from chroma_store_ollama/.
"""

from __future__ import annotations

import sys
from pathlib import Path

from sentence_transformers import CrossEncoder
from langsmith import traceable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.retriever_ollama import load_store

CROSS_ENCODER = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class RerankingRetrieverOllama:
    def __init__(self, fetch_k: int = 10, top_k: int = 5):
        self.store = load_store()
        self.reranker = CrossEncoder(CROSS_ENCODER)
        self.fetch_k = fetch_k
        self.top_k = top_k

    @traceable(run_type="retriever", name="RerankingRetrieverOllama")
    def invoke(self, query: str):
        candidates = self.store.similarity_search(query, k=self.fetch_k)
        pairs = [(query, doc.page_content) for doc in candidates]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked[: self.top_k]]
