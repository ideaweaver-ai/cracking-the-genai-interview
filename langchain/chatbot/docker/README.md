---
title: LangChain HF Docker Chatbot
emoji: 🐳
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# LangChain + Hugging Face Chatbot (Docker / Streamlit)

Streamlit chatbot for a **Hugging Face Docker Space**, powered by **LangChain** and
**Hugging Face Inference Providers** (free-tier remote models — no OpenAI).

## What this Space uses

| Piece | Choice |
|-------|--------|
| UI | Streamlit |
| SDK | Docker (`sdk: docker`) |
| LLM | `HuggingFaceEndpoint` + `ChatHuggingFace` |
| Auth | `HF_TOKEN` Space secret |
| Model | Single HF model via `HF_MODEL` (default: `meta-llama/Llama-3.1-8B-Instruct`) |

Inference runs **remotely** through Hugging Face Providers (`provider="auto"`).
The Space does **not** download a full LLM onto local GPU — **CPU Basic** is enough.

## Files to push to the Space

Upload / push the contents of this folder as the Space root:

| File | Purpose |
|------|---------|
| `app.py` | Streamlit + LangChain chatbot |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Docker Space image |
| `README.md` | This file (YAML header configures the Space) |
| `.env.example` | Local secrets template (do not commit a real `.env`) |

## Secrets

In the Space: **Settings → Secrets**

```env
HF_TOKEN=hf_xxxxxxxx
```

Optional:

```env
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

Get a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
For gated models (e.g. Llama), accept the model license on the Hub first.

## Deploy

1. Create a Space → **Docker** → Blank → **CPU Basic**.
2. Push the files in this folder to the Space repo root.
3. Add `HF_TOKEN` under **Settings → Secrets**.
4. Wait for the build, then open the Space.

```bash
git clone https://huggingface.co/spaces/<USER>/<SPACE_NAME>
# copy app.py, requirements.txt, Dockerfile, README.md into the clone
cd <SPACE_NAME>
git add app.py requirements.txt Dockerfile README.md
git commit -m "Add LangChain Streamlit Docker chatbot"
git push
```

## Local run (optional)

```bash
cd chatbot/docker
cp .env.example .env   # add HF_TOKEN
docker build -t hf-chatbot .
docker run --rm -p 7860:7860 --env-file .env hf-chatbot
```

Or without Docker:

```bash
pip install -r requirements.txt
streamlit run app.py --server.port=7860
```

## Choosing a model

Set `HF_MODEL` in Space Secrets or `.env`. Default is `meta-llama/Llama-3.1-8B-Instruct`.
If you see `model_not_supported`, pick another provider-enabled model for your account.

Browse: [Inference Providers](https://huggingface.co/docs/inference-providers) ·
[Inference models](https://huggingface.co/inference/models)
