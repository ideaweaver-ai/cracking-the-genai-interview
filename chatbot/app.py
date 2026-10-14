import os

import gradio as gr
import spaces
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

# HF Spaces: add HF_TOKEN under Settings → Secrets
# ZeroGPU requires @spaces.GPU on the Gradio handler (no-op on CPU/local).
hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
model_id = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

# Lazy init inside @spaces.GPU avoids asyncio "Invalid file descriptor" noise
# from HTTP clients created at import time before ZeroGPU forks a worker.
_chain = None


def get_chain():
    global _chain
    if _chain is None:
        endpoint = HuggingFaceEndpoint(
            repo_id=model_id,
            task="text-generation",
            max_new_tokens=512,
            do_sample=False,
            temperature=0.1,
            huggingfacehub_api_token=hf_token,
            provider="auto",
        )
        llm = ChatHuggingFace(llm=endpoint)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant that can answer questions clearly."),
                ("user", "{input}"),
            ]
        )
        _chain = prompt | llm | StrOutputParser()
    return _chain


@spaces.GPU(duration=60)
def respond(message: str, history: list):
    if not hf_token:
        return (
            "Missing Hugging Face token. Set **HF_TOKEN** "
            "(or **HUGGINGFACEHUB_API_TOKEN**) in Space Secrets or local `.env`."
        )
    if not message.strip():
        return "Please enter a question."
    try:
        return get_chain().invoke({"input": message})
    except Exception as exc:
        return f"Model call failed: {exc}"


demo = gr.ChatInterface(
    fn=respond,
    title="LangChain + Hugging Face Chatbot",
    description=(
        f"Gradio Space using LangChain + Hugging Face model `{model_id}`. "
        "Uses HF Inference Providers."
    ),
)

if __name__ == "__main__":
    demo.launch()
