# RAG Pipeline

Simple LangChain RAG examples: load documents → split → embed → retrieve → answer.

Each notebook is meant to be opened in Google Colab. Runtime → Run all.

## Colab notebooks

| Notebook | What it does | Open in Colab |
| --- | --- | --- |
| `rag_pipeline_colab.ipynb` | OpenAI embeddings + in-memory vector store. Rebuilds the index on every run. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ePHjjpq_JFCOZc8QgUr3muAVf2Drqbfa?usp=sharing) |
| `rag_pipeline_chroma_colab.ipynb` | Same RAG flow with persistent Chroma. Re-embeds only files whose content hash changed. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/148qSax0ZYES7W7GHoWoCT_8Sb034TxVz?usp=sharing) |
| `rag_pipeline_opensource_colab.ipynb` | Open-source embeddings (`all-MiniLM-L6-v2`) and an open-weight Qwen2.5 Instruct LLM. No OpenAI key. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ZhjD96FgMvccWXkXKi6aCRbBNNesU8M2?usp=sharing) |
| `rag_qwen_streamlit_colab.ipynb` | Streamlit UI over Qwen3-Embedding-0.6B + Qwen2.5 Instruct, with the same persistent Chroma index. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1my1xvKxtHgsCKHPBL8ogSqR4Y0NQ93Rc?usp=sharing) |

## Setup

The first two notebooks need `OPENAI_API_KEY` in Colab Secrets (key icon on the left). The last two run locally on the Colab runtime and do not need an OpenAI key.

For the MiniLM, Qwen embedding, and Streamlit notebooks: Runtime → Change runtime type → T4 GPU. First run downloads the models.

Sample docs are in [`docs/`](docs):

| File | Topic |
| --- | --- |
| `docs/crashloopbackoff.txt` | Why a pod is in CrashLoopBackOff and how to debug it |
| `docs/imagepullbackoff.txt` | Why a pod is in ImagePullBackOff and how to debug it |

The Colab notebooks write these same files if they are missing.

## Local script with LangSmith tracing

`rag_pipeline_traceable.py` is the same docs RAG as the first notebook, with `@traceable` on load, split, embed, setup, and the full run.

```bash
pip install langchain-openai langchain-core langchain-community langchain-text-splitters python-dotenv langsmith
```

Add this to a `.env` in the folder you run from (do not commit the key):

```
OPENAI_API_KEY=your-openai-api-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=rag-pipeline-docs-new
```

Create the LangSmith key at https://smith.langchain.com/settings. Then:

```bash
python3 rag_pipeline_traceable.py
```

Traces show up in LangSmith under project `rag-pipeline-docs-new` (or whatever you set in `.env`).

## Notes

- OpenAI and MiniLM embeddings have different vector sizes, so each notebook uses its own Chroma folder.
- On Colab, keep the Chroma index on local disk (`/content/...`), not Google Drive. Drive FUSE breaks Chroma's SQLite client.
- The Streamlit notebook starts the app on port 8501 and opens it through Colab's port proxy. The first page load downloads the models; wait for the spinners to finish.
