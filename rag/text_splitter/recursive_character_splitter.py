from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load the text file
loader = TextLoader("sample.txt", encoding="utf-8")
docs = loader.load()

# 2. Split by paragraphs, then lines, then words (80 chars, 20-char overlap)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=20,
)
chunks = splitter.split_documents(docs)

# 3. Inspect the result
print(f"Split into {len(chunks)} chunk(s)")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i} ({len(chunk.page_content)} chars):")
    print(chunk.page_content)
    print("---")
