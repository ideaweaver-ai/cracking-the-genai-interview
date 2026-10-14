import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

# HF Spaces: add HF_TOKEN under Settings → Secrets
hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
model_id = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

# 1) Title and description for the app UI
st.title("LangChain + Hugging Face Demo")
st.write("Type a question below and get an answer from the model.")

# 2) Create the model (reads HF_TOKEN from environment)
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

# 3) Define prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer questions clearly."),
    ("user", "{input}")
])

# 4) Output parser
output_parser = StrOutputParser()

# 5) Build the chain (prompt → model → string output)
chain = prompt | llm | output_parser

# 6) Streamlit input
user_input = st.text_input("Enter your prompt")

# 7) Run the chain when input is provided
if user_input:
    response = chain.invoke({"input": user_input})
    st.write(response)
