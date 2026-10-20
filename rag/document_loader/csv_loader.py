from langchain_community.document_loaders import CSVLoader

# 1. Create the loader
loader = CSVLoader("sample.csv", encoding="utf-8")

# 2. Read each CSV row into a Document
docs = loader.load()

# 3. Inspect the result
print(f"Loaded {len(docs)} document(s)")
for doc in docs:
    print("Metadata:", doc.metadata)
    print("Content:\n", doc.page_content)
    print("---")
