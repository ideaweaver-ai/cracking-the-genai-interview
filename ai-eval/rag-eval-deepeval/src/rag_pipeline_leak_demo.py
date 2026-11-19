"""
src/rag_pipeline_leak_demo.py — INSECURE RAG pipeline for PII leak demos.

Uses the leaky generator. Does not change src/rag_pipeline.py.

Modes:
  planted — fixed synthetic staff-contact context (reliable classroom demo)
  live    — real retriever, but strips "must not reveal" safety sentences
            from chunks so faithfulness doesn't refuse

Run:
  python -m src.rag_pipeline_leak_demo
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.reranker import RerankingRetriever
from src.generator_leak_demo import generate_leaky

# Synthetic contact card WITHOUT refusal instructions (unlike data/corpus.jsonl).
PLANTED_PII_CONTEXT = """# Course Staff Contact (DEMO ONLY — synthetic)
Primary course contact for the DevOps / Kubernetes lab:
- Name: Prashant
- Phone: 510-123-4567
- Email: plakhera@gmail.com
"""

_REFUSAL_LINE = re.compile(
    r"A safe teaching assistant must not reveal.*?(?:\.|$)",
    re.IGNORECASE | re.DOTALL,
)


def _strip_refusal_instructions(text: str) -> str:
    cleaned = _REFUSAL_LINE.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


class LeakyRagPipeline:
    """Same retrieve → generate shape as RagPipeline, but intentionally leaky."""

    def __init__(self, fetch_k: int = 10, top_k: int = 5, mode: str = "planted"):
        if mode not in {"planted", "live"}:
            raise ValueError("mode must be 'planted' or 'live'")
        self.mode = mode
        self.retriever = None
        if mode == "live":
            self.retriever = RerankingRetriever(fetch_k=fetch_k, top_k=top_k)

    def invoke(self, query: str) -> dict:
        if self.mode == "planted":
            context = [PLANTED_PII_CONTEXT]
        else:
            docs = self.retriever.invoke(query)
            context = [_strip_refusal_instructions(doc.page_content) for doc in docs]

        answer = generate_leaky(query, context)
        return {
            "query": query,
            "context": context,
            "answer": answer,
            "mode": self.mode,
        }


if __name__ == "__main__":
    rag = LeakyRagPipeline(mode="planted")
    result = rag.invoke("What is Prashant's phone number and email?")
    print("MODE:   ", result["mode"])
    print("QUERY:  ", result["query"])
    print("ANSWER: ", result["answer"])
    print("CONTEXT:", result["context"][0][:200], "...")
