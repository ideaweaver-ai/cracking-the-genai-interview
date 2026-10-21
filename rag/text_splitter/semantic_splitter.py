from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Load OPENAI_API_KEY from .env
load_dotenv()

# 1. Load a file with two different topics
loader = TextLoader("sample_semantic.txt", encoding="utf-8")
docs = loader.load()

# 2. Split where the meaning changes (uses embeddings, not a fixed length)
splitter = SemanticChunker(OpenAIEmbeddings())
chunks = splitter.split_documents(docs)

# 3. Inspect the result
print(f"Split into {len(chunks)} chunk(s)")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i} ({len(chunk.page_content)} chars):")
    print(chunk.page_content)
    print("---")
