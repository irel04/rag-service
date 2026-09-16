# Chunking Strategies for RAG

## Why chunking matters

Documents must be split into smaller pieces ("chunks") before embedding, for two reasons: embedding models have a maximum input length, and retrieval works best when each chunk represents one coherent idea rather than an entire multi-topic document. Poor chunking is one of the most common root causes of weak RAG performance — even a perfect embedding model can't retrieve information that was split apart or buried inside an unrelated chunk.

## Fixed-size chunking

The simplest approach: split text every N tokens or characters, often with an overlap (e.g. 500 tokens per chunk with 50 tokens of overlap) so that information near a boundary isn't lost entirely. Easy to implement and fast, but ignores document structure — it can split a sentence, table row, or code block in half.

## Recursive/structure-aware chunking

Splits text using a hierarchy of separators (e.g. try to split on section headers first, then paragraphs, then sentences, then words) so chunks stay as close as possible to a target size while respecting natural boundaries. This is the default strategy in most RAG frameworks (e.g. LangChain's `RecursiveCharacterTextSplitter`).

## Semantic chunking

Instead of splitting by a fixed size, semantic chunking embeds consecutive sentences and looks for points where semantic similarity drops sharply — indicating a topic shift — and splits there. Produces more topically coherent chunks at the cost of extra embedding calls during indexing.

## Document-aware chunking

For structured documents (Markdown, HTML, code, PDFs with headers/tables), chunking respects the native structure: Markdown headers become chunk boundaries, code is split by function/class definitions, tables are kept intact or given surrounding context. This preserves the meaning that structure conveys.

## Parent-child / hierarchical chunking

Small chunks are used for retrieval (because small chunks embed more precisely to a specific fact), but when a small chunk is retrieved, its larger "parent" chunk (or the full section/document) is passed to the LLM for generation. This balances retrieval precision with generation context.

## Chunk size tradeoffs

- **Smaller chunks** → more precise retrieval matches, but risk losing surrounding context needed to fully answer a question.
- **Larger chunks** → more context per retrieved item, but noisier embeddings (a chunk covering multiple topics embeds as a blurry average) and fewer chunks fit in the context window.
- Typical starting points are 200–500 tokens per chunk with 10–20% overlap, tuned empirically per corpus and embedding model.

## Evaluating chunking choices

Chunking strategy should be evaluated empirically against a held-out set of representative questions, measuring whether the correct chunk is retrieved (see `05_rag_evaluation_ragas.md` for retrieval metrics like context precision and context recall).
