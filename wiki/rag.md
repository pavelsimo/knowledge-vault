# Retrieval-Augmented Generation (RAG)

RAG is a technique that augments LLM generation by retrieving relevant external documents at inference time, grounding the model's output in up-to-date or domain-specific knowledge without retraining. The retrieved context is injected into the prompt alongside the user's query.

## Source

- `raw/00-clippings/Thread by @akshay_pachaar.md`

## 8 RAG Architectures

### 1. Naive RAG

**Pipeline:** User Query → Embedding → Vector DB → Prompt Template → LLM → Output

Retrieves documents purely based on **vector similarity** between the query embedding and stored document embeddings.

- Works best for simple, fact-based queries where direct semantic matching is sufficient
- Baseline approach: embed → retrieve top-k → generate

### 2. Multimodal RAG

**Pipeline:** User Query → Embedding → Vector DB (multi-modal data sources) → Prompt Template → LLM → Output

Handles multiple data types (text, images, audio) by embedding and retrieving **across modalities**.

- Ideal for cross-modal tasks: answering a text query with both text and image context
- Requires modality-specific encoders (e.g., CLIP for image-text)

### 3. HyDE (Hypothetical Document Embeddings)

**Pipeline:** User Query → Query Generator (Hypothetical Response) → Embedding → Vector DB → Prompt Template → LLM → Output

Addresses the problem where queries are not semantically similar to documents:

1. Generate a **hypothetical answer document** from the query using the LLM
2. Embed that hypothetical document
3. Use its embedding to retrieve real documents

Bridges the vocabulary/style gap between short queries and long documents.

### 4. Corrective RAG

**Pipeline:** User Query → Embedding → Analyzer → Search Web (Correct Info) → Prompt Template → LLM → Output

Validates retrieved results by comparing them against **trusted sources** (e.g., web search):

- Ensures up-to-date and accurate information
- Filters or corrects retrieved content before passing to the LLM
- Useful when the knowledge base may be stale or incomplete

### 5. Graph RAG

**Pipeline:** User Query → Graph Generator → Graph DB + Vector DB → Prompt Template → LLM → Output

Converts retrieved content into a **knowledge graph** capturing entities and relationships:

- Provides structured context (entity relationships) alongside raw text to the LLM
- Enhances multi-hop reasoning over interconnected facts
- Example: Microsoft GraphRAG

### 6. Hybrid RAG

**Pipeline:** User Query → Embedding → Vector DB (Context 1) + Graph Generator → Graph DB (Context 2) → Prompt Template → LLM → Output

Combines **dense vector retrieval** with **graph-based retrieval** in a single pipeline:

- Useful when the task requires both unstructured text and structured relational data
- Produces richer answers by leveraging complementary retrieval signals

### 7. Adaptive RAG

**Pipeline:** User Query → Query Analyzer → (Direct path to Vector DB) or (Reasoning Chain → Vector DB) → LLM → Output

Dynamically decides whether a query requires a simple retrieval or a **multi-step reasoning chain**:

- Routes simple queries directly to retrieval (faster, cheaper)
- Breaks complex queries into sub-queries via reasoning chain for better coverage
- Reduces unnecessary computation for easy queries

### 8. Agentic RAG

**Pipeline:** Query → Agent (Planning: ReAct/CoT, Short-term + Long-term Memory) → Agent 1 / Agent 2 → MCP Servers / Local Data / Search & Web / AWS Cloud Services → Output

Uses AI agents with **planning, reasoning (ReAct, CoT), and memory** to orchestrate retrieval from multiple sources:

- Best suited for complex workflows requiring tool use, external APIs, or combining multiple RAG techniques
- The agent decides what to retrieve, when, and from where
- Can iterate: retrieve → reason → retrieve again based on intermediate findings
- Supports tool integration: MCP servers, web search, local databases, cloud services (AWS/GCP)

## Architecture Selection Guide

| Use Case | Recommended Architecture |
|----------|--------------------------|
| Simple fact lookup | Naive RAG |
| Images + text context | Multimodal RAG |
| Short query, long docs | HyDE |
| Freshness-critical data | Corrective RAG |
| Multi-hop reasoning over facts | Graph RAG |
| Mixed structured + unstructured | Hybrid RAG |
| Mixed simple + complex queries | Adaptive RAG |
| Multi-tool / multi-source workflows | Agentic RAG |

## Related Topics

- [[attention-transformers]] — the LLM backbone that generates from retrieved context
- [[sentence-embeddings]] — vector similarity search is core to most RAG variants
- [[nlp]] — text retrieval and generation fundamentals
- [[multimodal-models]] — cross-modal retrieval in Multimodal RAG
