# Retrieval-Augmented Generation (RAG): Overview

## What is RAG?

Retrieval-Augmented Generation (RAG) is an architecture pattern that combines a large language model (LLM) with an external retrieval system. Instead of relying solely on knowledge baked into the model's weights during training, a RAG system fetches relevant documents or passages from a knowledge base at query time and feeds them into the model's context window alongside the user's question. The model then generates an answer grounded in that retrieved evidence.

## Why RAG exists

LLMs have three core limitations that RAG addresses:

1. **Knowledge cutoff** — a model only knows what existed in its training data up to a certain date. RAG lets it access fresh or continuously updated information without retraining.
2. **Hallucination** — models can generate plausible-sounding but false statements. Grounding generation in retrieved source text reduces (but does not eliminate) this risk.
3. **Private/domain data** — organizations often have proprietary documents, internal wikis, or codebases the base model was never trained on. RAG allows the model to reason over this data without fine-tuning.

## Core architecture

A typical RAG pipeline has two phases:

**Indexing (offline)**
- Documents are collected and split into chunks.
- Each chunk is converted into a vector embedding using an embedding model.
- Embeddings are stored in a vector index/database alongside the original text and metadata.

**Query time (online)**
1. The user's query is embedded using the same embedding model.
2. The vector store is searched for the top-k most similar chunks (semantic search), often combined with keyword search (hybrid search).
3. Retrieved chunks are optionally re-ranked for relevance.
4. The chunks are inserted into a prompt template along with the user's question.
5. The LLM generates a response conditioned on both the question and the retrieved context.

## Common variants

- **Naive RAG** — simple embed → retrieve → generate pipeline.
- **Advanced RAG** — adds query rewriting, re-ranking, and result fusion (e.g. reciprocal rank fusion).
- **Agentic RAG** — the model decides iteratively whether to retrieve again, which tool/source to query, or when it has enough information to answer.
- **Graph RAG** — retrieval is performed over a knowledge graph instead of (or in addition to) flat text chunks, useful for multi-hop reasoning.

## Key failure modes

- **Retrieval miss** — the relevant chunk is never retrieved, so the model cannot answer correctly even if it "knows" the topic.
- **Context dilution** — too many irrelevant chunks are stuffed into the prompt, burying the useful one.
- **Chunk boundary loss** — a chunk is split mid-thought, losing the information needed to answer.
- **Stale index** — the vector store isn't updated when source documents change.

These failure modes are exactly what evaluation frameworks like RAGAS are designed to measure and diagnose (see `05_rag_evaluation_ragas.md`).
