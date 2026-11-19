"""
src/retriever.py — load the Kubernetes docs corpus, chunk it, and build Chroma.

Teaching flow for the Kubernetes / DevOps docs RAG:
  1. LOAD documents
  2. CHUNK with RecursiveCharacterTextSplitter
  3. EMBED once into chroma_store/

Corpus file:
    data/corpus.jsonl
  (from: python -m src.download_dataset && python -m src.prepare_demo_data)
"""

import json
import os
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()  # loads OPENAI_API_KEY from .env

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CORPUS_PATH = DATA_DIR / "corpus.jsonl"
DB_DIR = str(ROOT / "chroma_store")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_corpus() -> list[Document]:
    """
    LOAD step.

    Reads data/corpus.jsonl and rebuilds one Document per Kubernetes page
    (all chunk pieces for a page_id joined), then we split ourselves.
    """
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(
            f"Missing {CORPUS_PATH}. Run:\n"
            f"  python -m src.download_dataset\n"
            f"  python -m src.prepare_demo_data"
        )

    pages: dict[str, list[dict]] = defaultdict(list)
    with CORPUS_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            text = (row.get("text") or "").strip()
            if not text:
                continue
            page_id = str(row.get("page_id") or row.get("id") or "unknown")
            pages[page_id].append(row)

    docs: list[Document] = []
    for page_id, rows in pages.items():
        rows.sort(key=lambda r: int(r.get("chunk_index") or 0))
        text = "\n\n".join((r.get("text") or "").strip() for r in rows if (r.get("text") or "").strip())
        if not text:
            continue
        first = rows[0]
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "page_id": page_id,
                    "title": str(first.get("title", "")),
                    "section": str(first.get("section", "")),
                    "url": str(first.get("url", "")),
                    "page_kind": str(first.get("page_kind", "")),
                },
            )
        )
    return docs



def load_store():
    """
    BUILD step.

    Open an existing Chroma store if it has documents, otherwise:
      load docs -> RecursiveCharacterTextSplitter -> embed -> persist
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if os.path.exists(DB_DIR):
        store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        # An empty chroma_store/ directory still "exists" — rebuild if vacant.
        try:
            n = store._collection.count()
        except Exception:
            n = 0
        if n > 0:
            return store

    docs = load_corpus()
    if not docs:
        raise RuntimeError(f"No documents found in {CORPUS_PATH}")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    ).split_documents(docs)

    return Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)


def build_retriever():
    return load_store().as_retriever(search_kwargs={"k": 5})


if __name__ == "__main__":
    retriever = build_retriever()
    results = retriever.invoke("What is a Kubernetes Deployment?")
    if not results:
        print("No results. Check that data/corpus.jsonl exists and chroma_store was built.")
    for r in results:
        title = r.metadata.get("title", "?")
        print(f"[{title}] {r.page_content[:150]}...\n")
