from langchain_community.document_loaders import DirectoryLoader, TextLoader

# 1. Create the loader
loader = DirectoryLoader(
    "docs",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)

# 2. Read every matching file into Document objects
docs = loader.load()

# 3. Inspect the result
print(f"Loaded {len(docs)} document(s)")
for doc in docs:
    print("Metadata:", doc.metadata)
    print("Content:\n", doc.page_content)
    print("---")
