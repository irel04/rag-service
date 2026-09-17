from pydantic import BaseModel
from typing import List, Optional

class IndexRequest(BaseModel):
	document: List[str]
	collection_name: Optional[str] = None

class QueryRequest(BaseModel):
	question: str
	n_results: Optional[int] = 3
	collection_name: Optional[str] = None

class QueryResponse(BaseModel):
	question: str
	answer: str
	relevant_chunks: List[str]