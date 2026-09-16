from util import load_documents
from chunking import split_text
from embedding import get_openai_embedding 
from config import collection

''' 
This is the ingestion pipeline for learning the knowledge

'''
documents = load_documents("./rag/knowledge")

# Expand docs into chunked docs with unique IDs
chunked_docs = []
for doc in documents:
    chunks = split_text(doc["text"])
    for i, chunk in enumerate(chunks, start=1):
        chunked_docs.append({
            "id": f"{doc["id"]}_chunk{i}",
            "text": chunk,
            "source": doc["id"],
            "chunk_index": i
				})

print(f"Split into {len(chunked_docs)} chunks")

# Generate embeddings for the document chunks
for doc in chunked_docs:
    print("=== Generating embeddings... ===")
     # adding the embedding to the chunked_documents list for each chunk
    doc["embedding"] = get_openai_embedding(doc["text"])

# Add the document with embedding to the collection
for doc in chunked_docs:
	collection.upsert(
        documents=[doc["text"]],
        ids=[doc["id"]],
        embeddings=[doc["embedding"]]
  )


