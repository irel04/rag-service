# Vector Databases and Indexing

## What is a vector database?

A vector database (or vector index) is a data store purpose-built to hold high-dimensional embedding vectors and answer approximate nearest neighbor (ANN) queries efficiently: given a query vector, return the top-k most similar stored vectors. Popular options include Pinecone, Weaviate, Qdrant, Milvus, Chroma, and pgvector (a Postgres extension), as well as vector search features built into Elasticsearch/OpenSearch and Redis.

## Why approximate, not exact, search

Exact nearest-neighbor search (brute-force comparison against every vector) is O(n) per query, which becomes too slow once a corpus reaches millions of vectors. Approximate Nearest Neighbor (ANN) algorithms trade a small amount of recall for large gains in speed by building an index structure that avoids scanning the full dataset.

## Common indexing algorithms

- **HNSW (Hierarchical Navigable Small World)** — builds a multi-layer graph where each node connects to its nearest neighbors; search starts at a coarse top layer and descends. Offers strong recall/speed tradeoffs and is the default in many vector databases.
- **IVF (Inverted File Index)** — clusters vectors into buckets (via k-means) and only searches the buckets closest to the query vector. Often combined with product quantization (IVF-PQ) to compress vectors and reduce memory.
- **Product Quantization (PQ)** — compresses vectors by splitting them into sub-vectors and quantizing each independently, trading some accuracy for a large reduction in memory footprint.
- **Flat/brute-force index** — exact search, used for small corpora or as a correctness baseline.

## Hybrid search

Pure vector search can miss exact keyword matches (product codes, names, acronyms) that a user explicitly typed. Hybrid search combines:
- **Sparse retrieval** (e.g. BM25, TF-IDF) — good at exact term matching.
- **Dense retrieval** (embeddings) — good at semantic/paraphrase matching.

Results from both are merged, commonly using Reciprocal Rank Fusion (RRF), which combines ranked lists without needing to calibrate scores across the two systems.

## Metadata filtering

Most vector databases support attaching metadata (e.g. `source`, `date`, `author`, `access_level`) to each vector and filtering search results by that metadata (pre-filtering or post-filtering). This is essential for multi-tenant systems, access control, and time-bounded queries.

## Operational considerations

- **Index build time** grows with corpus size; some indexes (like HNSW) are expensive to rebuild from scratch, so incremental insertion support matters for frequently updated corpora.
- **Recall vs. latency tuning** — most ANN indexes expose parameters (e.g. `ef_search` in HNSW, `nprobe` in IVF) that trade off search speed against how close to exact the results are.
- **Sharding and replication** are needed at scale for both query throughput and availability.
