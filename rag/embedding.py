from .config import openai_client, embedding_model

# Create a function to generate embedding for each chunk using openai
def get_openai_embedding(text: str):
    response = openai_client.embeddings.create(input=text, model=embedding_model)
    embedding = response.data[0].embedding
    print("=== Generating embeddings... ===")
    return embedding
