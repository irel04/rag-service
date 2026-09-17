"""RAG Service Package Initialization."""

# Import key components for easier access
from .config import (
    openai_client,
    collection,
    openai_ef,
    openai_key,
    openai_model,
    embedding_model,
    base_url
)
from .retrieval import query_documents

# Import utility functions
from .util import load_documents
from .chunking import split_text
from .embedding import get_openai_embedding

__all__ = [
    "openai_client",
    "collection",
    "openai_ef",
    "openai_key",
    "openai_model",
    "embedding_model",
    "base_url",
    "query_documents",
    "load_documents",
    "split_text",
    "get_openai_embedding"
]