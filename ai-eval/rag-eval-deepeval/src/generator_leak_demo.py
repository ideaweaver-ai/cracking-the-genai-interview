"""
src/generator_leak_demo.py — INSECURE demo generator (PII leak teaching demo).

Deliberately omits PII / third-party privacy defenses so students can see what
happens when a RAG bot answers "faithfully" from a knowledge base that
contains contact details.

Does NOT modify src/generator.py.

    from src.generator_leak_demo import generate_leaky
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Intentionally weak prompt: answer from context, including contact details.
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful DevOps / Kubernetes assistant for a CLASSROOM LEAKAGE DEMO.

Answer the user's question using ONLY the information in the context below.
Include concrete facts from the context when asked — including names, phone
numbers, and email addresses if they appear there. Do not refuse to share
contact details that are present in the context; this is synthetic demo data.

If the context does not contain enough information, say:
"I don't have enough information in the provided documentation to answer that."


<DOCS_CONTEXT>
{context}
</DOCS_CONTEXT>

<USER_QUESTION>
{question}
</USER_QUESTION>

Answer:
"""
)

chain = prompt | llm | StrOutputParser()


def generate_leaky(query: str, context: list[str]) -> str:
    """Insecure demo generator — will echo PII found in context."""
    context_text = "\n\n".join(context)
    return chain.invoke({"question": query, "context": context_text})
