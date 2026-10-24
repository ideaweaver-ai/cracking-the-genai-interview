---
title: LangChain Hugging Face Chatbot
emoji: 💬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.30.0
python_version: '3.12'
app_file: app.py
pinned: false
---

# LangChain + Hugging Face Chatbot (Gradio)

Gradio chatbot powered by **LangChain** and **Hugging Face Inference Providers**.

Live Space example: [lakhera2023/huggingface-demo](https://huggingface.co/spaces/lakhera2023/huggingface-demo)

## What changed from the original Streamlit + OpenAI app

| Original | This app |
|----------|----------|
| Streamlit UI | **Gradio** (`gr.ChatInterface`) |
| `ChatOpenAI` + `OPENAI_API_KEY` | `HuggingFaceEndpoint` + `ChatHuggingFace` + `HF_TOKEN` |
| OpenAI model (e.g. `gpt-4o-mini`) | HF model via Inference Providers (default: `meta-llama/Llama-3.1-8B-Instruct`) |
| Recreate model every UI rerun | Lazy-init chain inside the chat handler |

Inference runs **remotely** through Hugging Face Providers (`provider="auto"`). The Space does not download a full LLM onto local GPU.

## Why Gradio (not Streamlit)?

Hugging Face **ZeroGPU (free GPU)** is only available for **Gradio** Spaces. Streamlit is no longer offered as a built-in SDK option for that free-GPU path (Streamlit apps typically use Docker now).

Create the Space with:

1. **SDK:** Gradio  
2. **Template:** Blank  
3. **Hardware:** ZeroGPU Free **or** CPU Basic  

### ZeroGPU note

If the Space uses **ZeroGPU**, Gradio handlers that need GPU scheduling must be decorated with `@spaces.GPU`. Without that you get:

```text
Runtime error: No @spaces.GPU function detected during startup
```

This app already decorates `respond` with `@spaces.GPU(duration=60)`. On non-ZeroGPU hardware the decorator is a no-op.

Because this app uses **remote Inference Providers**, **CPU Basic** is enough. ZeroGPU is optional here; it mainly matters if you later load a model locally with `transformers`.

## Files in this folder

| File | Purpose |
|------|---------|
| `app.py` | Gradio + LangChain chatbot |
| `requirements.txt` | Python dependencies for the Space / local run |
| `.env.example` | Template for local secrets (do **not** commit a real `.env`) |
| `README.md` | This file (also used as Space config via the YAML header) |

## Secrets and environment variables

### Local (`.env`)

```bash
cp .env.example .env
```

```env
HF_TOKEN=hf_your_token_here
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

Get a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

### Hugging Face Space

`.env` is **not** uploaded to the Space. Add secrets under **Settings → Secrets**:

```env
HF_TOKEN=hf_xxxxxxxx
```

Optional override:

```env
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

`HF_TOKEN` and `HUGGINGFACEHUB_API_TOKEN` are both accepted by `app.py`.

## Local run

```bash
cd chatbot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add your HF_TOKEN
python app.py
```

Open the local Gradio URL (usually `http://127.0.0.1:7860`).

> Local tip: the `spaces` package is provided on HF Gradio Spaces. If `import spaces` fails locally, install it with `pip install spaces` (the decorator is a no-op off ZeroGPU).

## Deploy to Hugging Face Spaces

### Option A — New Space from the UI

1. Create a Space: **Gradio** → **Blank**.
2. Pick **CPU Basic** or **ZeroGPU Free**.
3. Upload / push the contents of this `chatbot/` folder (`app.py`, `requirements.txt`, `README.md`).
4. Add `HF_TOKEN` under **Settings → Secrets**.
5. Wait for the build, then open the Space.

### Option B — Git push (what we used)

```bash
git clone https://huggingface.co/spaces/<USER>/<SPACE_NAME>
# copy app.py, requirements.txt, README.md into the clone
cd <SPACE_NAME>
git add app.py requirements.txt README.md
git commit -m "Add LangChain Gradio chatbot"
git push
```

For HTTPS push, username = HF username, password = HF access token (Write scope).

Example Space used in this project:

```text
https://huggingface.co/spaces/lakhera2023/huggingface-demo
```

## Choosing a model (`HF_MODEL`)

Not every Hub model works with Inference Providers. If you see:

```text
model_not_supported
The requested model '...' is not supported by any provider you have enabled.
```

switch to a model that **is** enabled for your account. Models verified working with a typical free token during setup:

- `meta-llama/Llama-3.1-8B-Instruct` (**default**)
- `deepseek-ai/DeepSeek-V3.1`
- `moonshotai/Kimi-K2-Instruct`
- `deepseek-ai/DeepSeek-R1` (may include long reasoning/`think` text)

Models that often fail (example): `microsoft/Phi-3-mini-4k-instruct`.

Browse providers/models: [huggingface.co/docs/inference-providers](https://huggingface.co/docs/inference-providers) and [huggingface.co/inference/models](https://huggingface.co/inference/models).

Set the model via Space secret or `.env`:

```env
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

## Common logs / warnings (safe to ignore if the app works)

| Log | Meaning |
|-----|---------|
| `Running pip as the 'root' user...` | HF Space install runs as root; ignore |
| `Will cache examples...` | Gradio informational message |
| `ValueError: Invalid file descriptor: -1` (asyncio `__del__`) | Common ZeroGPU / event-loop cleanup noise when workers fork |

`app.py` lazy-inits the LangChain chain inside the `@spaces.GPU` handler to reduce the asyncio FD warnings.

## Troubleshooting checklist

1. Space shows **Runtime error: No @spaces.GPU...** → keep `@spaces.GPU` on the function passed to `gr.ChatInterface` (already done).
2. **Missing Hugging Face token** in the UI → add `HF_TOKEN` in Space Secrets (not only local `.env`).
3. **model_not_supported** → change `HF_MODEL` to a provider-enabled model (see above). Remove a bad `HF_MODEL` secret if it overrides the code default.
4. App rebuild stuck → open **Logs**, confirm `requirements.txt` installed, then **Factory reboot** if needed.

## Requirements

See `requirements.txt`:

- `gradio`
- `langchain-core`
- `langchain-huggingface`
- `huggingface_hub`
- `python-dotenv`

Do **not** pin `spaces` in `requirements.txt`; Gradio Spaces provide it.
