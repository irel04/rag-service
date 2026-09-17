from .config import collection

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

