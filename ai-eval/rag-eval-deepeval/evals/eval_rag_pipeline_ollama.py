"""
evals/eval_rag_pipeline_ollama.py
=================================
Same RAG-triad eval as eval_rag_pipeline.py, but fully Ollama-backed:

  - Pipeline under test: src.rag_pipeline_ollama.RagPipelineOllama
    (nomic-embed-text + cross-encoder rerank + gemma3:4b generate)
  - DeepEval judge: gemma3:4b via Ollama
    (Contextual Relevancy, Faithfulness, Answer Relevancy)

Unlike eval_generator_ollama, context comes from the LIVE retriever/reranker,
not golden ideal_context.

Optional env:
  OLLAMA_JUDGE_MODEL=gemma3:4b
  OLLAMA_BASE_URL=http://localhost:11434
  RAG_MAX_CASES=3

Run:
  python -m evals.eval_rag_pipeline_ollama
  python evals/eval_rag_pipeline_ollama.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "180")
os.environ.setdefault("DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE", "600")

from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
)
from deepeval.models import OllamaModel
from deepeval.evaluate.configs import AsyncConfig

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag_pipeline_ollama import RagPipelineOllama
from evals.harness import load_goldens, summarize_by_metric, print_summary

load_dotenv(ROOT / ".env")

GOLDEN_PATH = str(ROOT / "goldens" / "faithfulness_dataset.json")  # reuse the queries
OLLAMA_MODEL = os.getenv("OLLAMA_JUDGE_MODEL", "gemma3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
THRESHOLD = 0.7
MAX_CASES = os.getenv("RAG_MAX_CASES")


def run(rag):
    print(f"Pipeline: RagPipelineOllama | Judge: {OLLAMA_MODEL} @ {OLLAMA_BASE_URL}")

    goldens = load_goldens(GOLDEN_PATH)
    if MAX_CASES:
        goldens = goldens[: int(MAX_CASES)]
        print(f"Smoke mode: {len(goldens)} case(s)")

    judge = OllamaModel(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )

    # 1–2. LIVE pipeline per query
    test_cases = []
    for g in goldens:
        result = rag.invoke(g["query"])  # retrieve → rerank → generate
        test_cases.append(
            LLMTestCase(
                input=g["query"],
                actual_output=result["answer"],
                retrieval_context=result["context"],
            )
        )

    # 3. RAG triad — local Ollama judge
    metrics = [
        ContextualRelevancyMetric(
            threshold=THRESHOLD,
            model=judge,
            include_reason=True,
            async_mode=False,
        ),
        FaithfulnessMetric(
            threshold=THRESHOLD,
            model=judge,
            include_reason=True,
            async_mode=False,
        ),
        AnswerRelevancyMetric(
            threshold=THRESHOLD,
            model=judge,
            include_reason=True,
            async_mode=False,
        ),
    ]

    # 4. EVALUATE
    result = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        async_config=AsyncConfig(run_async=False, max_concurrent=1),
        hyperparameters={
            "pipeline": "rag_pipeline_ollama",
            "judge_model": OLLAMA_MODEL,
            "judge_provider": "ollama",
            "golden_set": GOLDEN_PATH,
        },
    )
    return summarize_by_metric(result)


def run_local():
    return run(RagPipelineOllama())


if __name__ == "__main__":
    print_summary("rag_pipeline_ollama", run_local())
