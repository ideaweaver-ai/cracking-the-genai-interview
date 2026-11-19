"""
Generate DRAFT retriever goldens from the local Kubernetes corpus.

Uses data/corpus.jsonl (demo or full). Review every golden before trusting it.

Run from project root:
    python goldens/generate_goldens.py
"""

import json
import random
from pathlib import Path

from dotenv import load_dotenv
from deepeval.synthesizer import Synthesizer

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "data" / "corpus.jsonl"
OUT_PATH = ROOT / "goldens" / "retriever_deepeval_goldens.json"


def load_chunks():
    """Load chunk texts from data/corpus.jsonl (same store the retriever uses)."""
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(
            f"Missing {CORPUS_PATH}. Run: python -m src.download_dataset "
            f"&& python -m src.prepare_demo_data"
        )
    chunks = []
    with CORPUS_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            text = (row.get("text") or "").strip()
            if text:
                chunks.append(text)
    return chunks


chunks = load_chunks()
sample = random.sample(chunks, min(15, len(chunks)))
contexts = [[c] for c in sample]

synthesizer = Synthesizer(model="gpt-4.1-mini")
goldens = synthesizer.generate_goldens_from_contexts(
    contexts=contexts,
    include_expected_output=True,
    max_goldens_per_context=1,
)

rows = []
for i, g in enumerate(goldens, 1):
    rows.append(
        {
            "id": f"g{i:03d}",
            "query": g.input,
            "ideal_answer": g.expected_output,
            "source": "TODO-verify",
        }
    )

OUT_PATH.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(rows)} DRAFT goldens -> {OUT_PATH}")
print("!! REVIEW EVERY ONE before using: check grounding, trim padding, fix leading questions.")
