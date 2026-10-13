import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load OLLAMA_API_KEY (and optional OLLAMA_CLOUD_MODEL) from .env
load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
if not api_key:
    raise ValueError(
        "Missing OLLAMA_API_KEY. Add it to your .env file "
        "(create one at https://ollama.com/settings/keys)."
    )

# Cloud models use a :cloud suffix (see https://ollama.com/search?c=cloud).
# You already have glm-5:cloud locally; other examples: gpt-oss:120b-cloud
model_name = os.getenv("OLLAMA_CLOUD_MODEL", "glm-5:cloud")

# 1. Same ChatOllama class as local Ollama, but pointed at Ollama Cloud.
# Local default is http://localhost:11434 with no auth.
# Cloud uses https://ollama.com and a Bearer API key — no local daemon required.
#
# Free tier (see https://ollama.com/pricing): Ollama does not publish a fixed
# "X free calls per day/hour" limit. Free includes starter usage credits each
# month for a smaller set of starter models (exact $ amount not public), resets
# monthly from signup (no rollover), and allows 1 concurrent request. Extra
# requests queue; if the queue is full they are rejected. No published RPM/TPM.
# Add paid credits to unlock all models; local Ollama stays unlimited.
llm = ChatOllama(
    model=model_name,
    temperature=0,
    base_url="https://ollama.com",
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {api_key}",
        },
    },
)

# 2. Create a reusable prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms for a DevOps engineer."
)

# 3. Create the parser
parser = StrOutputParser()

# 4. Compose the chain
chain = prompt | llm | parser

# 5. Run it
print(f"Using Ollama Cloud model: {model_name}")
response = chain.invoke({"topic": "Kubernetes"})
print(response)
