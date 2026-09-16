import os

# Load documents
def load_documents(dir: str):
    print(f"Loading documents from {dir}...")
    docs = []
    
    for filename in os.listdir(dir):
        if filename.endswith(".md"):
            with open(os.path.join(dir, filename), "r", encoding="utf-8") as f:
                docs.append({"id": filename, "text": f.read()})
    print(f"Loaded {len(docs)} documents")
    return docs