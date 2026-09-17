"""API Package Initialization."""

# Import key components for easier access
from .model import IndexRequest, QueryRequest, QueryResponse

__all__ = [
    "IndexRequest",
    "QueryRequest",
    "QueryResponse"
]