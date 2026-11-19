"""
Build eval golden JSON files from data/demo/qa_test.jsonl + data/corpus.jsonl.

Builds Kubernetes demo Q&A goldens so retriever / faithfulness /
correctness evals match the current corpus.

Run:
    python -m src.build_demo_goldens
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO_QA = ROOT / "data" / "demo" / "qa_test.jsonl"
CORPUS = ROOT / "data" / "corpus.jsonl"
GOLDENS = ROOT / "goldens"


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    if not DEMO_QA.exists():
        raise FileNotFoundError(f"Missing {DEMO_QA}. Run: python -m src.prepare_demo_data")
    if not CORPUS.exists():
        raise FileNotFoundError(f"Missing {CORPUS}")

    qa = _read_jsonl(DEMO_QA)
    corpus_by_id = {}
    for row in _read_jsonl(CORPUS):
        corpus_by_id[str(row.get("id", ""))] = row

    retriever_rows = []
    faithfulness_rows = []
    correctness_rows = []

    for i, g in enumerate(qa, 1):
        qid = str(g.get("id") or f"k8s-{i:03d}")
        question = g["question"]
        answer = g["answer"]
        source_page = str(g.get("source_page", ""))
        source_chunk = str(g.get("source_chunk", ""))

        retriever_rows.append(
            {
                "id": qid,
                "query": question,
                "ideal_answer": answer,
                "source": source_page or "k8s-docs",
            }
        )

        correctness_rows.append(
            {
                "id": qid,
                "question": question,
                "ideal_answer": answer,
                "source_session": source_page or "k8s-docs",
            }
        )

        chunk = corpus_by_id.get(source_chunk)
        # Fall back to any chunk from the same page if exact id isn't in the demo corpus.
        if chunk is None:
            chunk = next(
                (r for r in corpus_by_id.values() if str(r.get("page_id", "")) == source_page),
                None,
            )
        ideal_context = [chunk["text"]] if chunk and chunk.get("text") else [answer]

        faithfulness_rows.append(
            {
                "id": qid,
                "query": question,
                "ideal_context": ideal_context,
                "source_sessions": [source_page or "k8s-docs"],
            }
        )

    (GOLDENS / "retriever_goldens.json").write_text(
        json.dumps(retriever_rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (GOLDENS / "faithfulness_dataset.json").write_text(
        json.dumps(faithfulness_rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (GOLDENS / "correctness_goldens.json").write_text(
        json.dumps(correctness_rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"wrote {len(retriever_rows)} retriever goldens")
    print(f"wrote {len(faithfulness_rows)} faithfulness goldens")
    print(f"wrote {len(correctness_rows)} correctness goldens")


if __name__ == "__main__":
    main()
