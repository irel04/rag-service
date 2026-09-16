from dotenv import load_dotenv
from openai import OpenAI
from chromadb.utils import embedding_functions
import chromadb
import os

load_dotenv()

def get_env(name: str) -> str:
    value = os.getenv(name)
    assert value, f"Set {name} in your .env"
    return value


openai_key = get_env("LLM_BINDING_API_KEY")
openai_model = get_env("LLM_MODEL")
embedding_model = get_env("EMBEDDING_MODEL")
base_url = get_env("LLM_BINDING_HOST")

# Embedding Function (Gemini OPENAI Compatible model)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
	api_key=openai_key,
	model_name=embedding_model,
  api_base=base_url
)

# Chromadb Client
chromadb_client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection_name = 'document_qa_collection'
collection = chromadb_client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

# Create OpenAI Client 
openai_client = OpenAI(api_key=openai_key, base_url=base_url)

response = openai_client.chat.completions.create(
  model=openai_model,
  messages=[
    {"role": "system", "content": "You are a helpful assistant that can answer questions about the documents in the collection."},
    {"role": "user", "content": "What is the main idea of the document?"}
  ]
)

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
                
documents = load_documents("./knowledge")

# Split texts into overlapping chunks
def split_text(text: str, chunk_size=1000, chunk_overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        # step forward but overlap a little to keep context
        start = end - chunk_overlap
    return chunks

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

# Create a function to generate embedding for each chunk using openai
def get_openai_embedding(text: str):
    response = openai_client.embeddings.create(input=text, model=embedding_model)
    embedding = response.data[0].embedding
    print("=== Generating embeddings... ===")
    return embedding

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

# Query Function to get the most relevant chunks
def query_documents(questions, n_results=3):
    print("=== Querying documents... ===")
    # query the collection for the most relevant chunks
    results = collection.query(query_texts=questions, n_results=n_results)

    # Extract the relevant chunks
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    print("=== Returning relevant chunks ===")

		# return the relevant chunks
    return relevant_chunks


# Function to generate a response from OpenAI
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = openai_client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": prompt, 
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message
    return answer


question = "Tell me RAG"
relevant_chunks = query_documents(question)
response = generate_response(question, relevant_chunks)
print(response)
    
    