"""
src/retriever_ollama.py — Ollama-backed corpus → Chroma retriever.

Same flow as src/retriever.py, but embeddings come from a local Ollama model
(nomic-embed-text) instead of OpenAI. Uses a separate persist dir so it does
not collide with the OpenAI chroma_store/.

Does NOT modify src/retriever.py.

Defaults (override with env):
  OLLAMA_BASE_URL=http://localhost:11434/v1
  OLLAMA_EMBED_MODEL=nomic-embed-text

Run:
  python -m src.retriever_ollama
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.retriever import (  # reuse load + chunk settings
    CORPUS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    load_corpus,
)

load_dotenv(ROOT / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
DB_DIR = str(ROOT / "chroma_store_ollama")


def _embeddings() -> OpenAIEmbeddings:
    # Ollama's OpenAI-compatible /v1 embeddings endpoint expects raw strings.
    # LangChain's default check_embedding_ctx_length=True tokenizes with
    # tiktoken and can send token-id lists → Ollama 400 "invalid input type".
    return OpenAIEmbeddings(
        model=OLLAMA_EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        check_embedding_ctx_length=False,
    )


def load_store():
    """
    Open chroma_store_ollama/ if it has docs; otherwise embed corpus with Ollama.
    """
    embeddings = _embeddings()

    if os.path.exists(DB_DIR):
        store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
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

    print(
        f"Building Ollama Chroma store ({OLLAMA_EMBED_MODEL}) → {DB_DIR} "
        f"({len(chunks)} chunks)…"
    )
    return Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)


def build_retriever():
    return load_store().as_retriever(search_kwargs={"k": 5})


if __name__ == "__main__":
    print(f"embed model: {OLLAMA_EMBED_MODEL} @ {OLLAMA_BASE_URL}")
    retriever = build_retriever()
    results = retriever.invoke("What is a Kubernetes Deployment?")
    if not results:
        print("No results. Is Ollama running? Is nomic-embed-text pulled?")
    for r in results:
        title = r.metadata.get("title", "?")
        print(f"[{title}] {r.page_content[:150]}...\n")
