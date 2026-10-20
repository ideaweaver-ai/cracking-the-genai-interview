from langchain_community.document_loaders import PyPDFLoader

# 1. Create the loader
loader = PyPDFLoader("sample.pdf")

# 2. Read the PDF into Document objects (one per page)
docs = loader.load()

# 3. Inspect the result
print(f"Loaded {len(docs)} document(s)")
print("Metadata:", docs[0].metadata)
print("Content:\n", docs[0].page_content)
