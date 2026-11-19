# AI Eval Book — Beginner Guide

**What this folder is:** a hands-on path for learning how to **evaluate AI systems**, not just build them.

We worked through two big teaching examples:

1. **Text-to-SQL** — turn English questions into SQL and check if the answers are correct  
2. **RAG (Retrieval-Augmented Generation)** — answer questions from documents and check if retrieval + answers are good  

This guide walks through **everything we did**, in plain language, from the start.

---

## Big idea (read this first)

Public leaderboards tell you which model is “best” in general.  
**Custom evals** tell you which model / pipeline is good **for your product**.

| Idea | Simple meaning |
|------|----------------|
| **Golden dataset** | A fixed list of questions + trusted correct answers |
| **Eval** | Run your system on those questions and score it |
| **Metric** | The scoring rule (e.g. “did SQL return the same rows?”, “did we retrieve the right docs?”) |

You build goldens once. Then you can swap models, prompts, or retrievers and compare fairly.

---

# Part 1 — Text-to-SQL evaluation

## 1.1 Starting point: cricket / IPL project

We began by looking at a teaching-style SQL eval project: **`llm-sql-eval`**.

**What it does**

- Stores IPL cricket data in a SQLite database  
- Asks natural-language questions like “Who scored the most runs…?”  
- An LLM writes SQL  
- The eval runs that SQL and compares the **result rows** to a golden answer  

**Why result comparison matters**

Two different SQL queries can both be “right” if they return the same answer.  
So we usually score **execution accuracy** (same results), not exact SQL string match.

Key files in `llm-sql-eval/`:

| File | Role |
|------|------|
| `db.py` | Builds the SQLite DB from CSV data |
| `golden_dataset.csv` | Questions + gold SQL + expected results |
| `evaluator.py` | Runs model SQL vs gold results |
| `main.py` | End-to-end eval flow |

---

## 1.2 Same idea, housing domain: Redfin

Cricket is fun, but many teams care about **business / product data**.  
So we built a parallel project: **`redfin-sql-eval`**.

**Teaching story**

Imagine a housing analytics app (Redfin / Zillow style). Users ask:

- Which metro had the highest median sale price in December 2024?  
- Which state had the lowest days on market?  

The app must turn that into correct SQL over market data.

### Important ethics / data note

We use **public research downloads** only:

- [Redfin Data Center](https://www.redfin.com/news/data-center/)  
- [Zillow Research Data](https://www.zillow.com/research/data/)  

**Do not scrape** live listing pages on Redfin or Zillow.

### What we built in `redfin-sql-eval/`

| File | What it is |
|------|------------|
| `data/housing_market_tracker_monthly.csv` | Public Redfin monthly market tracker |
| `db.py` | Loads CSV → `redfin_2021_2024.db` |
| `schema.sql` | Schema text the LLM sees in the prompt |
| `golden_dataset_generator.py` | 20 hard questions + gold SQL |
| `make_golden_dataset.py` | Runs gold SQL → writes `golden_dataset.csv` |
| `golden_dataset.csv` | Ready-to-use golden set |
| `prompt_example.txt` | Example SYSTEM/USER prompt |
| `Selecting_the_Right_LLM_Custom_Model_Evals.*` | Student handout (MD / HTML / PDF) with figures |

### Golden CSV columns (same shape as the IPL project)

```text
id, difficulty, question, gold_sql, gold_result_json, n_rows, order_sensitive
```

Example question from the Redfin golden set:

> What is the average median sale price across all metro areas in December 2024?

Gold SQL runs against the DB; the JSON result becomes the trusted answer for scoring.

### Student handout

We also prepared a beginner-facing handout:

**`redfin-sql-eval/Selecting_the_Right_LLM_Custom_Model_Evals.pdf`**

It covers:

- Product problem (housing Q&A)  
- Cost / latency / correctness requirements  
- How to shortlist models  
- How custom evals beat “just trust the leaderboard”  
- Figures kept in place for class use  

---

## 1.3 Text-to-SQL flow (beginner picture)

```text
User question (English)
        │
        ▼
   LLM writes SQL
        │
        ▼
  Run SQL on SQLite
        │
        ▼
Compare result rows to golden_dataset.csv
        │
        ▼
   Pass / Fail (+ accuracy over the set)
```

---

# Part 2 — RAG evaluation with DeepEval

## 2.1 Starting point: RAG + DeepEval repo

Next we cloned / reviewed **`rag-eval-deepeval`**.

**What RAG means (simple)**

1. **Retrieve** relevant chunks from your documents  
2. **Generate** an answer with an LLM using those chunks  

**What DeepEval is**

A Python library for evaluating LLM apps with metrics like:

- Did we retrieve the right context? (**Contextual Recall / Precision**)  
- Did the answer stick to the context? (**Faithfulness**)  
- Is the answer correct? (**Correctness / Answer Relevancy**)  
- Safety / toxicity / leakage checks  

The teaching materials originally used video transcripts (VTT).  
We replaced that domain with **public Kubernetes / DevOps docs**.

---

## 2.2 New dataset: Kubernetes docs on Hugging Face

**Dataset:** [evgenypal/k8s-docs-rag-bench](https://huggingface.co/datasets/evgenypal/k8s-docs-rag-bench)  
**License:** CC BY 4.0 (cite when teaching)

| File | Meaning |
|------|---------|
| `corpus.jsonl` | Documentation chunks to index |
| `qa_train.jsonl` / `qa_eval.jsonl` / `qa_test.jsonl` | Grounded Q&A pairs |

### Why we made a demo slice

The full corpus is large for a classroom laptop.  
So we prepared a small demo:

| Demo size | Count |
|-----------|-------|
| Chunks | ~200 |
| Questions | ~20 |
| Pages | ~25 |

- Full download lives under `rag-eval-deepeval/data/full/`  
- Demo slice under `rag-eval-deepeval/data/demo/`  
- Active file the retriever uses: `rag-eval-deepeval/data/corpus.jsonl`

Scripts that do this:

| Script | Job |
|--------|-----|
| `src/download_dataset.py` | Download public JSONL files into `data/full/` |
| `src/prepare_demo_data.py` | Build the ~200/20 demo slice |
| `src/build_demo_goldens.py` | Help turn demo QAs into golden JSON |

---

## 2.3 How the RAG pipeline works here

### Step A — Load + chunk documents

`src/retriever.py`:

1. Load `data/corpus.jsonl`  
2. Join chunks back into pages (one Document per Kubernetes page)  
3. Split again with **`RecursiveCharacterTextSplitter`**  
   - `chunk_size = 1000`  
   - `chunk_overlap = 150`  
4. Embed with **`text-embedding-3-large`**  
5. Store vectors in **Chroma** (`chroma_store/`)

> Why chunk? Models and retrievers work better on smaller pieces. Overlap helps avoid cutting important sentences in half.

### Step B — Retrieve + rerank

`src/reranker.py` (`RerankingRetriever`):

1. Fetch more candidates first (`fetch_k`, default 10)  
2. Rerank with a cross-encoder  
3. Keep the best (`top_k`, default **5**)

### Step C — Generate

`src/generator.py` + `src/rag_pipeline.py` turn retrieved context into an answer (DevOps / Kubernetes domain).

Optional UI: `src/app.py` (Streamlit).

---

## 2.4 What is a “golden dataset” in RAG?

Same idea as SQL goldens, different shape.

For **retriever** eval (`goldens/retriever_goldens.json`), each item looks like:

```json
{
  "id": "...",
  "query": "What is a service account in Kubernetes?",
  "ideal_answer": "A service account is a type of non-human account...",
  "source": "concepts_security_service-accounts"
}
```

| Field | Meaning |
|-------|---------|
| `query` | Question we ask the system |
| `ideal_answer` | Trusted good answer (used by judge metrics) |
| `source` | Which doc/page the answer should come from |

We rebuilt **20 retriever goldens** and spread them across **many different pages** (so the eval is not stuck on only a few “debug” docs).

Other golden files in `goldens/` cover faithfulness, correctness, toxicity, scope, leakage, etc.

---

## 2.5 Retriever eval script

File: `evals/eval_retriever.py`

**What it does**

1. Load `goldens/retriever_goldens.json`  
2. For each question, call `RerankingRetriever`  
3. Score with DeepEval metrics:  
   - **Contextual Recall** — did we miss needed info?  
   - **Contextual Precision** — are useful chunks ranked well?  
4. Tag the run with hyperparameters so reports stay honest  

**Hyperparameters we aligned to the real pipeline**

| Setting | Value |
|---------|-------|
| Embedding model | `text-embedding-3-large` |
| Chunk size / overlap | `1000` / `150` |
| `top_k` | `5` |
| Judge model | `gpt-4o-mini` |

Run (from `rag-eval-deepeval/`, with venv + `.env` set):

```bash
python -m evals.eval_retriever
```

---

## 2.6 RAG flow (beginner picture)

```text
Question
   │
   ▼
Embed question → search Chroma → get candidate chunks
   │
   ▼
Rerank → keep top_k chunks
   │
   ▼
LLM answers using those chunks
   │
   ▼
DeepEval metrics vs golden questions / ideal answers
```

---

# Part 3 — Setup cheat sheet

## Shared tools

- **Python 3** + a virtual environment  
- Prefer **`pip` + `requirements.txt`** for this workspace (simpler for class demos than `uv`)  
- OpenAI API key in `.env` for embeddings / judges / generation  

## Redfin SQL project

```bash
cd redfin-sql-eval
python3 db.py
python3 golden_dataset_generator.py
python3 make_golden_dataset.py
```

Read the handout PDF for the teaching narrative.

## RAG + DeepEval project

```bash
cd rag-eval-deepeval
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# put OPENAI_API_KEY in .env

# if you need to rebuild data:
python -m src.download_dataset
python -m src.prepare_demo_data

# build / open vector store
python -c "from src.retriever import load_store; load_store()"

# run retriever eval
python -m evals.eval_retriever
```

---

# Part 4 — Folder map (whole workspace)

```text
ai-eval-book/
├── BEGINNER_GUIDE.md          ← this file
│
├── llm-sql-eval/              ← original IPL cricket text-to-SQL example
│   ├── golden_dataset.csv
│   ├── evaluator.py
│   └── ...
│
├── redfin-sql-eval/           ← housing parallel + student handout
│   ├── golden_dataset.csv
│   ├── db.py
│   └── Selecting_the_Right_LLM_Custom_Model_Evals.pdf
│
└── rag-eval-deepeval/         ← RAG + DeepEval on Kubernetes docs
    ├── data/
    │   ├── full/              ← full HF download
    │   ├── demo/              ← small class slice
    │   └── corpus.jsonl       ← active corpus for retriever
    ├── src/
    │   ├── download_dataset.py
    │   ├── prepare_demo_data.py
    │   ├── retriever.py
    │   ├── reranker.py
    │   ├── generator.py
    │   └── ...
    ├── goldens/
    │   └── retriever_goldens.json
    └── evals/
        └── eval_retriever.py
```

---

# Part 5 — What we learned (takeaways for beginners)

1. **Evals need a fixed truth set** — without goldens, you are guessing.  
2. **Match the domain to the lesson** — cricket → housing SQL; video transcripts → Kubernetes RAG.  
3. **Use public, citable data** — Redfin/Zillow research downloads; Hugging Face K8s docs bench.  
4. **Keep demos small** — ~20 goldens / ~200 chunks is enough to teach the loop.  
5. **Don’t drop important pipeline pieces** — chunking, embeddings, and reranking all matter.  
6. **Keep eval metadata honest** — if the retriever uses `top_k=5` and `text-embedding-3-large`, the eval report should say the same.  
7. **Spread goldens across sources** — one page dominating the set makes the eval look better (or worse) than reality.

---

# Part 6 — Suggested sharing order for a new person

1. Skim this guide (10–15 min)  
2. Open `redfin-sql-eval/Selecting_the_Right_LLM_Custom_Model_Evals.pdf`  
3. Look at `redfin-sql-eval/golden_dataset.csv` (one row = one test)  
4. Skim `rag-eval-deepeval/data/DATASET_README.txt` and `data/demo/DEMO_README.txt`  
5. Read `rag-eval-deepeval/src/retriever.py` then `evals/eval_retriever.py`  
6. Peek at `goldens/retriever_goldens.json`  

That path goes: **why evals → SQL goldens → RAG goldens → run an eval**.

---

## Credits / sources to cite in class

- Original SQL and DeepEval teaching starter repos  
- Redfin public Housing Market Tracker data  
- Hugging Face dataset: `evgenypal/k8s-docs-rag-bench` (CC BY 4.0; paper arXiv:2605.28222)  
- Tools: SQLite, OpenAI embeddings, Chroma, LangChain text splitters, DeepEval  

---

*Last updated for the `ai-eval-book` workspace after the Redfin SQL + Kubernetes RAG demo work.*
