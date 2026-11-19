"""
src/app_leak_demo.py — INSECURE Streamlit UI for a PII leakage teaching demo.

Shows what happens when the generator answers faithfully from a knowledge base
that contains contact details — WITHOUT the privacy defenses in src/generator.py.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src.rag_pipeline_leak_demo import LeakyRagPipeline

st.set_page_config(
    page_title="PII Leak Demo (INSECURE)",
    page_icon="⚠️",
    layout="centered",
)

st.title("⚠️ PII Leakage Demo (INSECURE)")
st.warning(
    "Teaching demo only. This app intentionally omits privacy defenses so you "
    "can show a successful leak."
)


@st.cache_resource(show_spinner="Loading leaky demo pipeline…")
def get_leaky_pipeline(mode: str, fetch_k: int, top_k: int) -> LeakyRagPipeline:
    return LeakyRagPipeline(fetch_k=fetch_k, top_k=top_k, mode=mode)


with st.sidebar:
    st.header("Demo settings")
    mode = st.radio(
        "Context source",
        options=["planted", "live"],
        index=0,
        help=(
            "planted = fixed synthetic contact card (reliable classroom demo). "
            "live = real retriever, with refusal sentences stripped from chunks."
        ),
    )
    fetch_k = 10
    top_k = 5
    if mode == "live":
        fetch_k = st.slider("fetch_k", 5, 30, 10)
        top_k = st.slider("top_k", 1, 10, 5)

if "leak_messages" not in st.session_state:
    st.session_state.leak_messages = []

for msg in st.session_state.leak_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("meta"):
            st.caption(msg["meta"])

if prompt := st.chat_input("Ask a question…"):
    st.session_state.leak_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving + generating (leaky)…"):
            t0 = time.perf_counter()
            rag = get_leaky_pipeline(mode, fetch_k, top_k)
            result = rag.invoke(prompt)
            elapsed = time.perf_counter() - t0

        st.markdown(result["answer"])
        with st.expander(f"{len(result['context'])} context chunk(s) · {elapsed:.1f}s"):
            for i, chunk in enumerate(result["context"]):
                st.markdown(f"**[{i}]**")
                st.text(chunk[:800])

        meta = f"mode={result['mode']} · {len(result['context'])} chunk(s) · {elapsed:.1f}s"
        st.session_state.leak_messages.append(
            {"role": "assistant", "content": result["answer"], "meta": meta}
        )
