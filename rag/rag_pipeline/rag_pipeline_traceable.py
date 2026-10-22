# Same RAG as rag_pipeline.py, with LangSmith @traceable on each step.
# Set LANGCHAIN_API_KEY / LANGSMITH_API_KEY in .env before running.

import os

from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ.setdefault("LANGCHAIN_PROJECT", "rag-pipeline-docs-new")
os.environ.setdefault("LANGSMITH_PROJECT", os.environ["LANGCHAIN_PROJECT"])
if os.getenv("LANGCHAIN_API_KEY") and not os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]

from langsmith import Client, traceable
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


@traceable(name="load_docs")
def load_docs(docs_dir: str = "docs"):
    loader = DirectoryLoader(
        docs_dir,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


@traceable(name="split_documents")
def split_documents(docs, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)


@traceable(name="build_vectorstore")
def build_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return InMemoryVectorStore.from_documents(chunks, embeddings)


@traceable(name="setup_pipeline", tags=["setup"])
def setup_pipeline(docs_dir: str = "docs"):
    docs = load_docs(docs_dir)
    chunks = split_documents(docs)
    return build_vectorstore(chunks)


def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


@traceable(name="docs_rag_full_run")
def setup_pipeline_and_query(question: str, docs_dir: str = "docs"):
    vectorstore = setup_pipeline(docs_dir)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    prompt = ChatPromptTemplate.from_template(
        "Answer the question using only the context below. "
        "If the context does not contain the answer, say you do not know.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}"
    )
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | ChatOpenAI(model="gpt-4.1-mini")
        | StrOutputParser()
    )
    return rag_chain.invoke(question, config={"run_name": "docs_rag_query"})


if __name__ == "__main__":
    if not (os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")):
        raise SystemExit(
            "Missing LANGCHAIN_API_KEY / LANGSMITH_API_KEY in .env. "
            "Create one at https://smith.langchain.com/settings"
        )
    question = "Why is my pod in CrashLoopBackOff and how do I debug it?"
    answer = setup_pipeline_and_query(question)
    Client().flush()
    print(answer)
