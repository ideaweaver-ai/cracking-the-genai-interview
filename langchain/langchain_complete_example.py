from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize the model
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# 2. Create a reusable prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms for a DevOps engineer."
)

# 3. Create the parser
parser = StrOutputParser()

# 4. Compose the chain
chain = prompt | llm | parser

# 5. Run it
response = chain.invoke({"topic": "Kubernetes"})
print(response)
