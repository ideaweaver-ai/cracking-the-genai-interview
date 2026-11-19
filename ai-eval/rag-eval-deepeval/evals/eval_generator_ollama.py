"""
evals/eval_generator_ollama.py
==============================
Same generator isolation eval as eval_generator.py, but fully Ollama-backed:

  - Component under test: src.generator_ollama.generate
  - DeepEval judge: gemma3:4b via Ollama (Faithfulness + Answer Relevancy)

ISOLATION: feeds GOLDEN context from faithfulness_dataset.json (not the
retriever), so a low score is the generator's fault.

Optional env:
  OLLAMA_JUDGE_MODEL=gemma3:4b
  OLLAMA_BASE_URL=http://localhost:11434
  GENERATOR_MAX_CASES=3

Run:
  python -m evals.eval_generator_ollama
  python evals/eval_generator_ollama.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "180")
os.environ.setdefault("DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE", "600")

from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.models import OllamaModel
from deepeval.evaluate.configs import AsyncConfig

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.generator_ollama import generate
from evals.harness import load_goldens, summarize_by_metric, print_summary

load_dotenv(ROOT / ".env")

GOLDEN_PATH = str(ROOT / "goldens" / "faithfulness_dataset.json")
OLLAMA_MODEL = os.getenv("OLLAMA_JUDGE_MODEL", "gemma3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
THRESHOLD = 0.7
MAX_CASES = os.getenv("GENERATOR_MAX_CASES")


def run():
    print(f"Generator: src.generator_ollama | Judge: {OLLAMA_MODEL} @ {OLLAMA_BASE_URL}")

    goldens = load_goldens(GOLDEN_PATH)
    if MAX_CASES:
        goldens = goldens[: int(MAX_CASES)]
        print(f"Smoke mode: {len(goldens)} case(s)")

    judge = OllamaModel(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )

    # 1–2. RUN Ollama generator on GOLDEN context (isolation)
    test_cases = []
    for g in goldens:
        context = g["ideal_context"]
        answer = generate(g["query"], context)

        test_cases.append(
            LLMTestCase(
                input=g["query"],
                actual_output=answer,
                retrieval_context=context,
            )
        )

    # 3. Metrics — local Ollama judge
    metrics = [
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

    # 4. EVALUATE (sync — local Ollama)
    result = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        async_config=AsyncConfig(run_async=False, max_concurrent=1),
        hyperparameters={
            "generator": "generator_ollama",
            "judge_model": OLLAMA_MODEL,
            "judge_provider": "ollama",
            "golden_set": GOLDEN_PATH,
        },
    )
    return summarize_by_metric(result)


if __name__ == "__main__":
    print_summary("generator_ollama", run())
