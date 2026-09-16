# Embeddings for Retrieval

## What is an embedding?

An embedding is a dense numerical vector (typically a few hundred to a few thousand floating-point dimensions) that represents a piece of text — a word, sentence, paragraph, or document — such that semantically similar text maps to nearby points in vector space. Embeddings are produced by a neural network (an "embedding model") trained so that similarity in meaning corresponds to geometric closeness, usually measured with cosine similarity or dot product.

## How embedding models are trained

Most modern text embedding models are trained with contrastive learning: the model sees pairs of texts labeled as similar (e.g. a question and its correct answer passage) and dissimilar (unrelated passages), and is optimized so similar pairs end up close together in vector space while dissimilar pairs are pushed apart. Popular training objectives include InfoNCE loss and triplet loss.

## Types of embedding models

- **Symmetric/bi-encoder models** — encode query and document independently into fixed-size vectors, then compare with a simple distance metric. Fast at query time because document vectors are precomputed. Examples: OpenAI's `text-embedding-3` family, Cohere `embed-v3`, open models like `bge`, `e5`, and `gte`.
- **Asymmetric models** — trained specifically to handle short queries retrieving longer documents, since queries and documents have different statistical structure.
- **Cross-encoders** — take the query and a candidate document together as a single input and output a relevance score directly. Much more accurate than bi-encoders but too slow to run over an entire corpus, so they're typically used only for re-ranking a small shortlist.

## Choosing an embedding dimension and model

- Higher-dimensional embeddings (e.g. 1536 or 3072) generally capture more nuance but cost more to store and search.
- Some newer models support **Matryoshka Representation Learning**, letting you truncate a large embedding down to fewer dimensions with graceful degradation rather than retraining a smaller model.
- Domain-specific fine-tuning of embedding models (e.g. on legal or medical text) can meaningfully improve retrieval quality over general-purpose models.

## Similarity metrics

- **Cosine similarity** — measures the angle between two vectors, ignoring magnitude. Most common choice for text embeddings.
- **Dot product** — sensitive to vector magnitude; used when embeddings are trained to encode both direction and importance/confidence.
- **Euclidean (L2) distance** — less common for text but used in some vector index implementations.

## Practical pitfalls

- Mixing embeddings from two different models in the same index produces meaningless similarity scores — always re-embed the whole corpus when switching models.
- Very short queries and very long documents can be poorly matched by symmetric models; asymmetric or instruction-tuned embedding models handle this better.
- Embedding quality caps the ceiling of the entire RAG system — no amount of prompt engineering can recover information that was never retrieved.
