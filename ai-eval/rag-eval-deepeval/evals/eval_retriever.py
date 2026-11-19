# eval_retriever.py
#
# Run either way from the project root:
#   python -m evals.eval_retriever
#   python evals/eval_retriever.py
import sys
from pathlib import Path

from dotenv import load_dotenv

# Running as a file (python evals/eval_retriever.py) puts evals/ on sys.path,
# not the project root — so `from src...` / `from evals...` would fail without this.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualRecallMetric, ContextualPrecisionMetric

from src.reranker import RerankingRetriever
from evals.harness import load_goldens, summarize_by_metric, print_summary

load_dotenv(ROOT / ".env")

GOLDEN_PATH = str(ROOT / "goldens" / "retriever_goldens.json")
JUDGE_MODEL = "gpt-5-mini"   # NOTE: differs from the other evals (gpt-4o-mini)
THRESHOLD = 0.7


def run(retriever):
    # 1. LOAD the golden set --- the fixed, human-authored truth
    goldens = load_goldens(GOLDEN_PATH)

    # 2. RUN THE INJECTED RETRIEVER on each question to fill retrieval_context,
    #    then build one test case per golden.
    test_cases = []
    for g in goldens:
        retrieved = retriever.invoke(g["query"])
        retrieval_context = [doc.page_content for doc in retrieved]

        test_cases.append(
            LLMTestCase(
                input=g["query"],
                expected_output=g["ideal_answer"],
                retrieval_context=retrieval_context,
                actual_output="(generator not evaluated in this run)",
            )
        )

    # 3. THE METRICS --- recall (did we miss?) and precision (ranked well?)
    metrics = [
        ContextualRecallMetric(threshold=THRESHOLD, model=JUDGE_MODEL, include_reason=True),
        ContextualPrecisionMetric(threshold=THRESHOLD, model=JUDGE_MODEL, include_reason=True),
    ]

    # 4. EVALUATE --- every metric on every case, batched + parallel, printed report.
    #    hyperparameters travel with the run so the report is tagged with the config.
    result = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        hyperparameters={
            # Matches RerankingRetriever() defaults in src/reranker.py.
            # Tag "base" only if you inject build_retriever() (no cross-encoder).
            "retriever": "reranked",
            "cross_encoder": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "embedding_model": "text-embedding-3-large",
            "chunk_size": 1000,
            "chunk_overlap": 150,
            "fetch_k": 10,
            "top_k": 5,
            "judge_model": JUDGE_MODEL,
            "golden_set": GOLDEN_PATH,
        },
    )
    return summarize_by_metric(result)


def run_local():
    """Standalone convenience: build the retriever, then run."""
    return run(RerankingRetriever())


if __name__ == "__main__":
    print_summary("retriever", run_local())