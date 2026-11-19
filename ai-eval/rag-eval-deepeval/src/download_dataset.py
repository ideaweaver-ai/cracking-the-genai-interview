"""
src/download_dataset.py — download the DevOps (Kubernetes) RAG dataset into data/.

Dataset: https://huggingface.co/datasets/evgenypal/k8s-docs-rag-bench

Writes:
  data/corpus.jsonl          — chunked Kubernetes docs (for Chroma indexing)
  data/qa_train.jsonl        — grounded Q&A (train)
  data/qa_eval.jsonl         — grounded Q&A (eval)
  data/qa_test.jsonl         — grounded Q&A (test)  ← use for class goldens
  data/DATASET_README.txt    — short citation / provenance note

Also clears any previous files under data/ and removes chroma_store/ so the
retriever rebuilds against the new corpus on next run.

Run from the project root (pip):
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m src.download_dataset
"""

from __future__ import annotations

import shutil
from pathlib import Path

from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "chroma_store"

DATASET_ID = "evgenypal/k8s-docs-rag-bench"
DATASET_URL = f"https://huggingface.co/datasets/{DATASET_ID}"

# Files published at the root of the dataset repo (see dataset card configs).
FILES = (
    "corpus.jsonl",
    "qa_train.jsonl",
    "qa_eval.jsonl",
    "qa_test.jsonl",
)


def _clear_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def _count_lines(path: Path) -> int:
    with path.open(encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def download() -> dict[str, int]:
    print(f"Clearing {DATA_DIR} ...")
    _clear_dir(DATA_DIR)

    if DB_DIR.exists():
        print(f"Removing stale vector store {DB_DIR} ...")
        shutil.rmtree(DB_DIR)

    counts: dict[str, int] = {}
    print(f"Downloading from {DATASET_ID} ...")
    for name in FILES:
        cached = hf_hub_download(
            repo_id=DATASET_ID,
            repo_type="dataset",
            filename=name,
        )
        dest = DATA_DIR / name
        shutil.copyfile(cached, dest)
        n = _count_lines(dest)
        counts[name.replace(".jsonl", "")] = n
        print(f"  wrote {n} rows -> data/{name}")

    readme = DATA_DIR / "DATASET_README.txt"
    readme.write_text(
        "\n".join(
            [
                "DevOps RAG corpus for this project",
                "==================================",
                "",
                f"Source dataset: {DATASET_ID}",
                f"URL: {DATASET_URL}",
                "License: CC BY 4.0 (see dataset card)",
                "",
                "Files:",
                "  corpus.jsonl   — Kubernetes documentation chunks (index these)",
                "  qa_train.jsonl — grounded Q&A (train split)",
                "  qa_eval.jsonl  — grounded Q&A (eval split)",
                "  qa_test.jsonl  — grounded Q&A (test split; good for goldens)",
                "",
                "Cite the dataset / paper when using this material in coursework.",
                "Paper: arXiv:2605.28222",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"  wrote {readme.relative_to(ROOT)}")
    return counts


if __name__ == "__main__":
    counts = download()
    print("\nDone.")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print("\nNext: rebuild the vector store with:")
    print("  python -c \"from src.retriever import load_store; load_store()\"")
