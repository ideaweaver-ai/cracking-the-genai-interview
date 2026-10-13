from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini")
response = llm.invoke(
    "Explain Kubernetes CrashLoopBackOff in simple terms."
)
print(response.content)