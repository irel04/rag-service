# Evaluating RAG Systems with RAGAS

## Why RAG needs its own evaluation approach

A RAG system has two components that can each fail independently — the **retriever** and the **generator** — so evaluating only the final answer's quality hides whether a wrong answer came from bad retrieval, bad generation, or both. RAGAS (Retrieval-Augmented Generation Assessment) is an open-source framework that scores each component separately using LLM-as-judge techniques, without requiring human-labeled ground truth for every metric.

## The four core RAGAS metrics

1. **Context Precision** — of the chunks that were retrieved, what fraction were actually relevant to answering the question? Penalizes retrieving noisy, irrelevant chunks even if a good chunk is also present. Computed by having an LLM judge each retrieved chunk's relevance to the question.

2. **Context Recall** — of the information needed to produce the ground-truth answer, how much of it was present in the retrieved chunks? Requires a reference/ground-truth answer to compare against. Low context recall means the retriever is missing necessary information regardless of how good the generator is.

3. **Faithfulness** — of the claims made in the generated answer, what fraction are actually supported by the retrieved context? This measures hallucination: a low faithfulness score means the model is asserting things not grounded in the retrieved evidence, even if those things happen to be true.

4. **Answer Relevancy** — how well does the generated answer actually address the question asked, independent of whether it's correct or grounded? Computed by generating several synthetic questions from the answer and measuring their embedding similarity to the original question — a relevant answer should let you reconstruct a question close to the original.

## Additional RAGAS metrics

- **Answer Correctness** — combines semantic similarity and factual overlap between the generated answer and a ground-truth answer.
- **Answer Semantic Similarity** — embedding-based similarity between generated and reference answers.
- **Noise Sensitivity** — how much irrelevant retrieved context degrades answer quality.

## What a RAGAS test set looks like

Each test case (often called a "sample") typically includes:
- `question` — the user query.
- `contexts` — the list of text chunks the retriever returned for that question.
- `answer` — the RAG system's generated response (filled in after running your pipeline).
- `ground_truth` — a reference answer written or verified by a human, used for recall/correctness metrics.

RAGAS also ships a **testset generation** module that can synthesize question/ground-truth/context triples automatically from a source document corpus, using an LLM to write questions of varying complexity (simple factual, reasoning, multi-context) — this is useful for bootstrapping an evaluation set before real user queries exist.

## Interpreting results

- Low context recall + low faithfulness → retrieval is the bottleneck; improve chunking, embeddings, or top-k.
- High context recall + low faithfulness → generation is the bottleneck; the model is ignoring or contradicting good retrieved context, often fixable with prompt changes.
- High faithfulness + low answer relevancy → the answer is grounded but doesn't actually address what was asked; often a sign the question was ambiguous or the generation prompt needs tightening.
