"""
Streamlit + LangChain + Guardrails + chat memory.

Same jailbreak checks as app_guardrails_review.py, plus conversation history
so follow-ups like "what did I just ask?" work.

How memory is added:
  1. Store turns in st.session_state["messages"] (survives Streamlit reruns).
  2. Put MessagesPlaceholder("history") in the prompt so the model sees prior turns.
  3. Pass history=... when invoking the chain; append each new user/assistant turn.

Install: pip install langchain-openai streamlit guardrails-ai python-dotenv
         guardrails hub install hub://guardrails/detect_jailbreak

Run: streamlit run app_guardrails_memory.py
"""
import os

import streamlit as st
from dotenv import load_dotenv
from guardrails import Guard
from guardrails.hub import DetectJailbreak
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()

st.title("LangChain + Guardrails + Memory")
st.write("Chat with memory. Input and output are checked for jailbreaks.")

if not os.environ.get("OPENAI_API_KEY"):
    st.error("Set **OPENAI_API_KEY** in your environment (or `.env`).")
    st.stop()


@st.cache_resource
def setup():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that can answer questions clearly."),
            MessagesPlaceholder("history"),
            ("user", "{input}"),
        ]
    )
    chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()
    guard = Guard().use(DetectJailbreak(threshold=0.9))
    return chain, guard


chain, guard = setup()

# Chat history lives in session state (one conversation per browser tab).
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Enter your prompt")
if not user_input:
    st.stop()

try:
    guard.validate(user_input)
except Exception:
    st.error("Input was flagged as unsafe. Please rephrase your question.")
    st.stop()

st.session_state.messages.append({"role": "user", "content": user_input})
with st.chat_message("user"):
    st.write(user_input)

# Convert stored turns into LangChain messages for the prompt.
history = []
for msg in st.session_state.messages[:-1]:  # exclude the message we just added
    if msg["role"] == "user":
        history.append(HumanMessage(content=msg["content"]))
    else:
        history.append(AIMessage(content=msg["content"]))

try:
    with st.spinner("Thinking..."):
        response = chain.invoke({"input": user_input, "history": history})
except Exception as e:
    st.error(f"Request failed: {e}")
    st.stop()

try:
    guard.validate(response)
except Exception:
    st.warning("Response was filtered and not displayed.")
    st.stop()

st.session_state.messages.append({"role": "assistant", "content": response})
with st.chat_message("assistant"):
    st.write(response)
