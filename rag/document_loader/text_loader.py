from langchain_community.document_loaders import TextLoader


# 1. Create the loader
loader = TextLoader("sample.txt", encoding="utf-8")

# 2. Read the file into Document objects (page_content + metadata)
docs = loader.load()

# 4. Inspect the result
print(f"Loaded {len(docs)} document(s)")
print("Metadata:", docs[0].metadata)
print("Content:\n", docs[0].page_content)
