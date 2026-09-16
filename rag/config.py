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
