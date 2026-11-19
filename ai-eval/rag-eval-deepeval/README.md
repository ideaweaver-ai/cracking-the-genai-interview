# RAG Eval with DeepEval

Hands-on RAG evaluation for a **Kubernetes / DevOps teaching assistant**.

Build a retrieve → rerank → generate pipeline, score it with [DeepEval](https://github.com/confident-ai/deepeval) (RAG triad, safety, leakage, ops), and compare **OpenAI** vs local **Ollama** stacks.

## What you get

| Area | What it covers |
|------|----------------|
| **Retriever** | Contextual recall & precision over golden queries |
| **Generator** | Faithfulness + answer relevancy |
| **Full pipeline** | RAG triad (contextual relevancy, faithfulness, answer relevancy) |
| **Safety** | Scope (stay on-domain), toxicity, PII / prompt leakage |
| **Ops** | Latency, cost, reliability (+ regression suite) |
| **Leak demo** | Separate intentional-leak path for teaching PII failures |

## Layout

```text
rag-eval-deepeval/
├── data/demo/          # small corpus for demos & evals
├── goldens/            # fixed questions + trusted answers
├── src/                # pipeline (OpenAI, Ollama, leak-demo)
├── evals/              # DeepEval scripts (*_ollama twins where useful)
├── requirements.txt
└── .env.example
```

### Core pipeline (`src/`)

| File | Role |
|------|------|
| `retriever.py` / `retriever_ollama.py` | Chunk → embed → Chroma |
| `reranker.py` / `reranker_ollama.py` | Over-fetch + cross-encoder rerank |
| `generator.py` / `generator_ollama.py` | Grounded answer from context |
| `rag_pipeline.py` / `rag_pipeline_ollama.py` | End-to-end `invoke(query)` |
| `app.py` / `app_leak_demo.py` | Streamlit UIs |
| `*_leak_demo.py` | Teaching-only leaky generator (does not change the safe path) |

### Evals (`evals/`)

Run from the project root. OpenAI judges default to `gpt-4o-mini`; Ollama twins use `gemma3:4b`.

| Script | Measures |
|--------|----------|
| `eval_retriever.py` | Contextual recall / precision |
| `eval_generator.py` (+ `_ollama`) | Faithfulness, answer relevancy |
| `eval_rag_pipeline.py` (+ `_ollama`) | Full RAG triad |
| `eval_toxicity.py` (+ `_ollama`) | Toxicity |
| `eval_scope_safety.py` (+ `_ollama`) | Stays in DevOps/K8s scope |
| `eval_leakage.py` (+ `_ollama`) | PII / secret leakage |
| `eval_application.py` | Correctness (GEval) |
| `eval_ops.py` / `eval_safety.py` | Ops + safety snapshots |
| `run_suite.py` + `compare.py` | Baseline vs candidate regression |

## Setup

```bash
cd rag-eval-deepeval
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# put OPENAI_API_KEY in .env for the OpenAI stack
```

### OpenAI stack

```bash
# first run builds chroma_store/ from data/demo (or data/corpus.jsonl)
python src/rag_pipeline.py
python evals/eval_retriever.py
python evals/eval_rag_pipeline.py
streamlit run src/app.py
```

### Ollama stack (local)

```bash
# pull once
ollama pull nomic-embed-text
ollama pull gemma3:4b

# builds chroma_store_ollama/
python src/rag_pipeline_ollama.py

# smoke a few cases, then full run
RAG_MAX_CASES=3 python evals/eval_rag_pipeline_ollama.py
python evals/eval_generator_ollama.py
python evals/eval_toxicity_ollama.py
```

Ollama notes:

- Embeddings go through Ollama’s OpenAI-compatible `/v1` API (`nomic-embed-text`).
- Chat + DeepEval judges use `gemma3:4b`.
- Prefer non-thinking small models for judges to avoid local timeouts.

## Golden datasets

Under `goldens/`:

- `retriever_goldens.json` — retrieval quality
- `faithfulness_dataset.json` / `correctness_goldens.json` — generation quality
- `toxicity_goldens.json`, `scope_goldens.json`, `leakage_goldens.json` — safety

Goldens are the fixed truth. Swap models/prompts/retrievers and re-run the same evals to compare fairly.

## Leak demo (teaching only)

Safe pipeline stays in `generator.py` / `app.py`.

To show a PII failure on purpose:

```bash
streamlit run src/app_leak_demo.py
# or
python evals/eval_leakage.py   # against the leak-demo path where configured
```

## Requirements

- Python 3.11+
- OpenAI API key **or** Ollama with the models above
- Optional: LangSmith for tracing / online triad (`evals/eval_online.py`)
