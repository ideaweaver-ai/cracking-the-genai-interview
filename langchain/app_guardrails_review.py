"""
Streamlit + LangChain + Guardrails — jailbreak checks on input and output.

Install: pip install langchain-openai streamlit guardrails-ai python-dotenv
         guardrails hub install hub://guardrails/detect_jailbreak

Run: streamlit run app_guardrails_review.py
"""
import os

import streamlit as st
from dotenv import load_dotenv
from guardrails import Guard
from guardrails.hub import DetectJailbreak
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

st.title("LangChain + Streamlit Demo with Guardrails")
st.write("Ask a question — input and output are checked for jailbreaks.")

if not os.environ.get("OPENAI_API_KEY"):
    st.error("Set **OPENAI_API_KEY** in your environment (or `.env`).")
    st.stop()


@st.cache_resource
def setup():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that can answer questions clearly."),
            ("user", "{input}"),
        ]
    )
    chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()
    guard = Guard().use(DetectJailbreak(threshold=0.9))
    return chain, guard


chain, guard = setup()
user_input = st.text_input("Enter your prompt")

if not user_input:
    st.stop()

try:
    guard.validate(user_input)
except Exception:
    st.error("Input was flagged as unsafe. Please rephrase your question.")
    st.stop()

try:
    with st.spinner("Thinking..."):
        response = chain.invoke({"input": user_input})
except Exception as e:
    st.error(f"Request failed: {e}")
    st.stop()

try:
    guard.validate(response)
except Exception:
    st.warning("Response was filtered and not displayed.")
    st.stop()

st.write(response)
