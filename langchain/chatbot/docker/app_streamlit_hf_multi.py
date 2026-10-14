import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

# Free / provider-enabled models via Hugging Face Inference Providers.
# Override with HF_MODEL secret, or pick from the sidebar.
FREE_HF_MODELS = [
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "HuggingFaceH4/zephyr-7b-beta",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "deepseek-ai/DeepSeek-V3.1",
    "moonshotai/Kimi-K2-Instruct",
]

hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
default_model = os.getenv("HF_MODEL", FREE_HF_MODELS[0])
model_options = (
    FREE_HF_MODELS
    if default_model in FREE_HF_MODELS
    else [default_model, *FREE_HF_MODELS]
)


@st.cache_resource
def get_chain(model_id: str):
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
    return prompt | llm | StrOutputParser()


st.title("LangChain + Hugging Face Chatbot")
st.write(
    "Ask a question using a free Hugging Face Inference Providers model. "
    "No OpenAI key required — set **HF_TOKEN** in Space Secrets or local `.env`."
)

with st.sidebar:
    st.header("Model")
    model_id = st.selectbox(
        "Hugging Face model",
        options=model_options,
        index=model_options.index(default_model),
        help="These models are called remotely via Inference Providers (provider=auto).",
    )
    st.caption(f"Token set: {'yes' if hf_token else 'no'}")

user_input = st.text_input("Enter your prompt")

if user_input:
    if not hf_token:
        st.error(
            "Missing Hugging Face token. Set **HF_TOKEN** "
            "(or **HUGGINGFACEHUB_API_TOKEN**) in Space Secrets or local `.env`."
        )
    elif not user_input.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner(f"Calling `{model_id}`…"):
                response = get_chain(model_id).invoke({"input": user_input.strip()})
            st.write(response)
        except Exception as exc:
            st.error(f"Model call failed: {exc}")
            st.info(
                "If you see `model_not_supported`, pick another model in the sidebar "
                "or set `HF_MODEL` to one enabled for your account."
            )
