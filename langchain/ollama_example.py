from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("OLLAMA_MODEL", "llama3:8b")
llm = ChatOllama(model=model_name)
response = llm.invoke(
    "Explain Kubernetes CrashLoopBackOff in simple terms."
)
print(response.content)