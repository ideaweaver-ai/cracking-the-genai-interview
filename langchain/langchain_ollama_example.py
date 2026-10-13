import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load optional overrides from .env (e.g. OLLAMA_MODEL)
load_dotenv()

# Models available on this machine (from `ollama list`):
#   llama3:8b, gemma3:4b, qwen2.5:3b, phi4-mini, qwen3:0.6b, ...
model_name = os.getenv("OLLAMA_MODEL", "llama3:8b")

# 1. Initialize the local Ollama chat model (no API key needed).
# ChatOllama does not scan for Ollama — it calls the default local HTTP API at
# http://localhost:11434 (where the Ollama app/daemon listens). On invoke(), it
# POSTs to that server; if Ollama is not running, you get a connection error.
# Override with base_url / OLLAMA_BASE_URL if Ollama is not on localhost.
llm = ChatOllama(model=model_name, temperature=0)

# 2. Create a reusable prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms for a DevOps engineer."
)

# 3. Create the parser
parser = StrOutputParser()

# 4. Compose the chain
chain = prompt | llm | parser

# 5. Run it
print(f"Using Ollama model: {model_name}")
response = chain.invoke({"topic": "Kubernetes"})
print(response)
