"""
src/prepare_demo_data.py — build a small demo slice of the K8s RAG dataset.

Why: the full corpus (~7.9k chunks) is overkill for class demos (slow/expensive
to embed and judge). This script keeps a curated ~200-chunk subset plus ~20
grounded test questions.

Writes:
  data/demo/corpus.jsonl
  data/demo/qa_test.jsonl
  data/demo/DEMO_README.txt

Also:
  - archives the full download under data/full/ (once)
  - copies the demo corpus to data/corpus.jsonl so the retriever uses it by default
  - removes chroma_store/ so the next load rebuilds against the demo corpus

Run from the project root (after download_dataset):
    python -m src.prepare_demo_data
    python -m src.prepare_demo_data --chunks 200 --questions 20
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
FULL_DIR = DATA_DIR / "full"
DEMO_DIR = DATA_DIR / "demo"
DB_DIR = ROOT / "chroma_store"

CORPUS_SRC = DATA_DIR / "corpus.jsonl"
QA_TEST_SRC = DATA_DIR / "qa_test.jsonl"

# Prefer teaching-friendly concept/task pages over huge API reference dumps.
PREFERRED_PAGE_IDS = [
    "concepts_workloads_pods",
    "concepts_workloads_pods_pod-lifecycle",
    "concepts_workloads_controllers_deployment",
    "concepts_workloads_controllers_replicaset",
    "concepts_workloads_controllers_statefulset",
    "concepts_workloads_controllers_daemonset",
    "concepts_workloads_controllers_job",
    "concepts_workloads_controllers_cron-jobs",
    "concepts_services-networking_service",
    "concepts_services-networking_ingress",
    "concepts_services-networking_network-policies",
    "concepts_services-networking_dns-pod-service",
    "concepts_configuration_secret",
    "concepts_configuration_manage-resources-containers",
    "concepts_workloads_autoscaling_horizontal-pod-autoscale",
    "concepts_security_service-accounts",
    "tasks_configure-pod-container_configure-liveness-readiness-startup-probes",
    "tasks_configure-pod-container_configure-pod-configmap",
    "tasks_configure-pod-container_security-context",
    "tasks_debug_debug-application_debug-running-pod",
    "tasks_debug_debug-application_debug-service",
    "reference_access-authn-authz_rbac",
    "tutorials_services_connect-applications-service",
]

TITLE_KEYWORDS = (
    "pod",
    "deployment",
    "service",
    "ingress",
    "configmap",
    "secret",
    "probe",
    "rbac",
    "network polic",
    "statefulset",
    "daemonset",
    "cronjob",
    "job",
    "replicaset",
    "autoscal",
    "debug",
    "troubleshoot",
)


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _archive_full_if_needed() -> None:
    """Keep one copy of the full download under data/full/."""
    FULL_DIR.mkdir(parents=True, exist_ok=True)
    for name in ("corpus.jsonl", "qa_train.jsonl", "qa_eval.jsonl", "qa_test.jsonl"):
        src = DATA_DIR / name
        dest = FULL_DIR / name
        if src.exists() and not dest.exists():
            shutil.copyfile(src, dest)
            print(f"  archived {src.name} -> data/full/{name}")


def _page_groups(corpus: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in corpus:
        groups[str(row.get("page_id", ""))].append(row)
    return groups


def _score_page(page_id: str, rows: list[dict]) -> tuple[int, str]:
    title = str(rows[0].get("title", ""))
    kind = str(rows[0].get("page_kind", ""))
    blob = f"{page_id} {title}".lower()

    score = 0
    if page_id in PREFERRED_PAGE_IDS:
        score += 100
    if kind in {"concept", "task", "tutorial"}:
        score += 20
    if kind == "reference":
        score -= 10  # keep some refs, but prefer concepts/tasks
    if any(k in blob for k in TITLE_KEYWORDS):
        score += 15
    # Prefer medium pages (enough content, not huge API dumps)
    n = len(rows)
    if 8 <= n <= 40:
        score += 10
    elif n > 60:
        score -= 20
    return score, title


def _take_page_chunks(rows: list[dict], per_page_cap: int) -> list[dict]:
    # Prefer earlier chunks (usually definitions / overview) within a page.
    ordered = sorted(rows, key=lambda r: int(r.get("chunk_index") or 0))
    return ordered[:per_page_cap]


def select_corpus(corpus: list[dict], target_chunks: int, seed: int) -> list[dict]:
    groups = _page_groups(corpus)

    selected: list[dict] = []
    selected_pages: list[str] = []
    selected_page_set: set[str] = set()

    def add_page(page_id: str, cap: int) -> None:
        if page_id in selected_page_set or page_id not in groups:
            return
        remaining = target_chunks - len(selected)
        if remaining <= 0:
            return
        take = _take_page_chunks(groups[page_id], min(cap, remaining))
        if not take:
            return
        selected.extend(take)
        selected_pages.append(page_id)
        selected_page_set.add(page_id)

    # 1) Force-include teaching pages, sharing the budget so later pages are not starved.
    present_preferred = [pid for pid in PREFERRED_PAGE_IDS if pid in groups]
    if present_preferred:
        per_preferred = max(6, target_chunks // max(len(present_preferred), 1))
        per_preferred = min(per_preferred, 15)
        for page_id in present_preferred:
            add_page(page_id, per_preferred)

    # 2) Fill remaining budget with other high-scoring related pages.
    ranked = sorted(
        groups.items(),
        key=lambda item: (_score_page(item[0], item[1])[0], -len(item[1]), item[0]),
        reverse=True,
    )
    for page_id, _rows in ranked:
        if len(selected) >= target_chunks:
            break
        add_page(page_id, cap=12)

    selected.sort(
        key=lambda r: (
            str(r.get("page_id", "")),
            int(r.get("chunk_index") or 0),
            str(r.get("id", "")),
        )
    )
    print(
        f"  selected {len(selected)} chunks from {len(selected_pages)} pages "
        f"({len(present_preferred)} preferred pages included)"
    )
    return selected


def _load_all_qa() -> list[dict]:
    """Load train+eval+test so demo goldens can cover concept pages, not only qa_test pages."""
    rows: list[dict] = []
    for name in ("qa_train.jsonl", "qa_eval.jsonl", "qa_test.jsonl"):
        for base in (FULL_DIR, DATA_DIR):
            path = base / name
            if path.exists():
                part = _read_jsonl(path)
                for r in part:
                    r = dict(r)
                    r["_split"] = name.replace(".jsonl", "")
                    rows.append(r)
                break
    return rows


def select_questions(
    qa_rows: list[dict],
    selected_corpus: list[dict],
    n_questions: int,
    seed: int,
) -> list[dict]:
    """
    Spread questions across many source pages.

    Strategy:
      1. Keep only questions grounded in the demo corpus pages.
      2. Take at most one question per page first (round-robin diversity).
      3. If we still need more, allow a second question from larger pages.
    """
    page_ids = {str(r.get("page_id", "")) for r in selected_corpus}
    chunk_ids = {str(r.get("id", "")) for r in selected_corpus}

    grounded = [
        q
        for q in qa_rows
        if str(q.get("source_page", "")) in page_ids
        or str(q.get("source_chunk", "")) in chunk_ids
    ]
    if not grounded:
        grounded = list(qa_rows)

    rng = random.Random(seed)
    by_page: dict[str, list[dict]] = defaultdict(list)
    for q in grounded:
        by_page[str(q.get("source_page") or "unknown")].append(q)

    # Shuffle each page's questions for variety, then pick round-robin.
    page_order = sorted(by_page.keys())
    rng.shuffle(page_order)
    for pid in page_order:
        rng.shuffle(by_page[pid])

    chosen: list[dict] = []
    chosen_ids: set[str] = set()

    def take_one(pid: str) -> bool:
        bucket = by_page.get(pid) or []
        while bucket:
            q = bucket.pop()
            qid = str(q.get("id", ""))
            if qid in chosen_ids:
                continue
            chosen.append(q)
            chosen_ids.add(qid)
            return True
        return False

    # Pass 1: one question per page.
    for pid in page_order:
        if len(chosen) >= n_questions:
            break
        take_one(pid)

    # Pass 2: fill remaining from pages that still have leftovers.
    guard = 0
    while len(chosen) < n_questions and guard < n_questions * 5:
        guard += 1
        progressed = False
        for pid in page_order:
            if len(chosen) >= n_questions:
                break
            if take_one(pid):
                progressed = True
        if not progressed:
            break

    chosen.sort(key=lambda q: str(q.get("id", "")))
    src_counts = Counter(str(q.get("source_page", "")) for q in chosen)
    print(
        f"  selected {len(chosen)} questions across {len(src_counts)} source pages "
        f"(grounded pool={len(grounded)})"
    )
    for pid, n in src_counts.most_common():
        print(f"    {n:2}  {pid}")
    return chosen


def prepare(target_chunks: int, n_questions: int, seed: int, activate: bool) -> None:
    if not CORPUS_SRC.exists() and not (FULL_DIR / "corpus.jsonl").exists():
        raise FileNotFoundError(
            "Missing data/corpus.jsonl. Run: python -m src.download_dataset"
        )

    print("Archiving full dataset under data/full/ (if needed)...")
    _archive_full_if_needed()

    # Prefer reading from full/ so re-running demo prep doesn't shrink further.
    corpus_path = FULL_DIR / "corpus.jsonl"
    if not corpus_path.exists():
        corpus_path = CORPUS_SRC

    print(f"Loading {corpus_path} ...")
    corpus = _read_jsonl(corpus_path)
    print("Loading QA from train+eval+test ...")
    qa_rows = _load_all_qa()
    if not qa_rows:
        raise FileNotFoundError(
            "Missing QA jsonl files under data/ or data/full/. "
            "Run: python -m src.download_dataset"
        )

    print(f"Selecting demo corpus (~{target_chunks} chunks)...")
    demo_corpus = select_corpus(corpus, target_chunks=target_chunks, seed=seed)

    print(f"Selecting demo questions (~{n_questions})...")
    demo_qa = select_questions(qa_rows, demo_corpus, n_questions=n_questions, seed=seed)

    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    _write_jsonl(DEMO_DIR / "corpus.jsonl", demo_corpus)
    _write_jsonl(DEMO_DIR / "qa_test.jsonl", demo_qa)

    pages = sorted({str(r.get("page_id", "")) for r in demo_corpus})
    (DEMO_DIR / "DEMO_README.txt").write_text(
        "\n".join(
            [
                "Demo slice of evgenypal/k8s-docs-rag-bench",
                "==========================================",
                "",
                f"chunks     : {len(demo_corpus)}",
                f"questions  : {len(demo_qa)}",
                f"pages      : {len(pages)}",
                f"seed       : {seed}",
                "",
                "Use this for class demos. Full data stays in data/full/.",
                "Active retriever corpus is data/corpus.jsonl when --activate is used",
                "(default).",
                "",
                "Rebuild the vector store after activating:",
                '  python -c "from src.retriever import load_store; load_store()"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Wrote data/demo/corpus.jsonl ({len(demo_corpus)} rows)")
    print(f"Wrote data/demo/qa_test.jsonl ({len(demo_qa)} rows)")

    if activate:
        shutil.copyfile(DEMO_DIR / "corpus.jsonl", DATA_DIR / "corpus.jsonl")
        print("Activated demo corpus -> data/corpus.jsonl")
        if DB_DIR.exists():
            shutil.rmtree(DB_DIR)
            print("Removed stale chroma_store/")

    print("\nDone. Demo data is ready.")


def main():
    parser = argparse.ArgumentParser(description="Prepare a small demo subset of the K8s RAG dataset.")
    parser.add_argument("--chunks", type=int, default=200, help="target number of corpus chunks (default: 200)")
    parser.add_argument("--questions", type=int, default=20, help="number of test questions (default: 20)")
    parser.add_argument("--seed", type=int, default=42, help="sampling seed")
    parser.add_argument(
        "--no-activate",
        action="store_true",
        help="only write data/demo/; do not replace data/corpus.jsonl",
    )
    args = parser.parse_args()
    prepare(
        target_chunks=args.chunks,
        n_questions=args.questions,
        seed=args.seed,
        activate=not args.no_activate,
    )


if __name__ == "__main__":
    main()
