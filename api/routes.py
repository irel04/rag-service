from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import os 
import tempfile

# RAG Components
from rag.config import collection, chromadb_client, openai_model, openai_ef, openai_client
from rag.util import load_documents
from rag.chunking import split_text
from rag.embedding import get_openai_embedding
from rag.retrieval import query_documents

from .model import IndexResponse, QueryResponse, CollectionListResponse

router = APIRouter()

@router.post("/index")
async def index_documents(
	files: List[UploadFile] = File(...),
	collection_name: Optional[str] = Form(None)
):
	"""
	Index documents from uploaded files
	"""
	try:
		# Use default collection if none provided
		target_collection = collection
		if collection_name:
			target_collection = chromadb_client.get_or_create_collection(
				name=collection_name,
				embedding_function=openai_ef
			)

		# Process each uploaded file
		documents_indexed = 0
		for file in files: 
			# Save file to temporary location
			with tempfile.NamedTemporaryFile(delete=False) as temp_file:
				content = await file.read()
				temp_file.write(content)
				temp_file_path = temp_file.name

				try:
					# For text files, read content directly
					# For other file types, you might need additional processing
					with open(temp_file_path, 'r', encoding='utf-8') as f: 
						content = f.read()

					# Split text into chunks
					chunks = split_text(content)

					# Create embeddings and add to collection
					for i, chunk in enumerate(chunks):
						embedding = get_openai_embedding(chunk)
						target_collection.add(
							documents=[chunk],
							embeddings=[embedding],
							ids=[f"{file.filename}_{i}"]
						)
						documents_indexed += 1
				finally: 
					# Clean up temporary file
					os.unlink(temp_file_path)

		return IndexResponse(
			message=f"Successfully indexed {documents_indexed} chunks",
			documents_indexed=documents_indexed,
			collection_name=collection_name
		)
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Indexing failed: {str(e)}"
		)

@router.post("/query")
async def query_rag(
	question: str = Form(...),
	n_result: int = Form(3),
	collection_name: Optional[str] = Form(None)
):
	"""
	Query the RAG System
	"""
	# Implementation for querying documents
	try: 
		# Use default collection if none provided
		target_collection = collection 
		if collection_name: 
			try:
				target_collection = chromadb_client.get_collection(
					name=collection_name,
					embedding_function=openai_ef
				)
			except Exception:
				raise HTTPException(
					status_code=404,
					detail=f"Collection '{collection_name}' not found"
				)

		# Get embeddings for the question
		question_embedding = get_openai_embedding(question)

		# Query the collection for relevant chunks
		results = target_collection.query(
			query_embeddings=[question_embedding],
			n_results=n_result
		)

		# Extract relevant chunks
		relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

		# Generate answer using OpenAI 
		answer = None
		if relevant_chunks:
			context = "\n".join(relevant_chunks)
			prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer: "

			response = openai_client.chat.completions.create(
				model=openai_model,
				messages=[{"role": "user", "content": prompt}],
				max_tokens=500,
				temperature=0.7
			)

			answer = response.choices[0].message.content

			return QueryResponse(
				question=question,
				relevant_chunks=relevant_chunks,
				answer=answer
			)
	except Exception as e:
		raise HTTPException(
			status_code=500, 
			detail=f"Query failed: {str(e)}"
		)
			


@router.get("/collections")
async def list_collections():
	"""
	List all available collections
	"""
	try: 
		collections = chromadb_client.list_collections()
		collection_names = [col.name for col in collections]

		return CollectionListResponse(collections=collection_names)
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"Failed to list collection: {str(e)}"
		)


