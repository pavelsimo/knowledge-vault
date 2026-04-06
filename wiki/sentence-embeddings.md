# Sentence Embeddings

Sentence embeddings are dense vector representations of text that capture semantic meaning. Similar sentences map to nearby vectors in the embedding space, enabling semantic search, clustering, and retrieval without keyword matching.

## Source

- [[raw/01-open-source-models-hugging-face/04_sentence_embeddings.py|raw/01-open-source-models-hugging-face/04_sentence_embeddings.py]]

## Core Model: all-MiniLM-L6-v2

`sentence-transformers/all-MiniLM-L6-v2` is the standard go-to sentence embedding model:

- Architecture: based on the **MiniLM** family (distilled from larger BERT-like models)
- Output: **384-dimensional** dense vector per sentence or short paragraph
- Fine-tuned for: sentence similarity and semantic search tasks
- Tradeoff: excellent accuracy-vs-speed balance, high throughput

## Model Comparison

| Model | Best for | Tradeoff |
|-------|----------|----------|
| `all-MiniLM-L6-v2` | Fast, general-purpose embeddings | Lower accuracy than mpnet |
| `all-mpnet-base-v2` | Higher accuracy (semantic search, retrieval) | Slower, larger, more resources |
| `paraphrase-multilingual-MiniLM-L12-v2` | Multilingual embeddings | Slightly larger than L6 |
| `multi-qa-mpnet-base-cos-v1` | Question-answering / retrieval-heavy tasks | More specialized |

Full list of pretrained sentence embedding models: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html

## How Embedding Distance Works

Two embeddings that are **close** in vector space have **similar semantic meaning**:
- "I love dogs" and "Puppies are great" → close vectors
- "I love dogs" and "Quantum physics paper" → distant vectors

Common similarity metrics:
- **Cosine similarity** — angle between vectors (most common for sentence embeddings)
- **Dot product** — magnitude-aware similarity
- **L2 / Euclidean distance** — raw spatial distance

## Use Cases

- **Semantic search:** find documents semantically similar to a query (not just keyword-matching)
- **Clustering:** group similar texts without labels
- **Duplicate detection:** find near-duplicate content
- **Retrieval-Augmented Generation (RAG):** retrieve relevant context for LLM prompts

## Related Topics

- [[nlp]] — text processing tasks
- [[multimodal-models]] — contrastive learning creates similar embedding spaces for cross-modal similarity
- [[transformers-library]] — the library used to load embedding models
- [[hugging-face]] — hosting sentence embedding models
