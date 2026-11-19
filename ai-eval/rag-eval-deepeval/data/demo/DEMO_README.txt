Demo slice of evgenypal/k8s-docs-rag-bench
==========================================

chunks     : 200
questions  : 20
pages      : 25
seed       : 42

Use this for class demos. Full data stays in data/full/.
Active retriever corpus is data/corpus.jsonl when --activate is used
(default).

Rebuild the vector store after activating:
  python -c "from src.retriever import load_store; load_store()"
