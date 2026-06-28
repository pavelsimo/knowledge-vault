---
title: "How do you use HybridChunker in Docling, including saving and reloading the converted document?"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/d4d670cd-8b56-4ca4-ae72-6be60441fba7"
author:
  - "[[Devin]]"
published: 2026-04-20
created: 2026-06-03
description: "HybridChunker in DoclingImportfrom docling.chunking import HybridChunkerfrom docling.document_converter import DocumentConverterHybridChunker Parameters"
tags:
  - "clippings"
---
## HybridChunker in Docling

### Import

```python
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
```

---

### HybridChunker Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `tokenizer` | — | Tokenizer instance (e.g., HuggingFaceTokenizer) |
| `merge_peers` | — | Merges peer chunks together |
| `max_tokens` | (required if no tokenizer) | Maximum tokens per chunk |
| `repeat_table_header` | `True` | Repeats table header rows when a table is split across chunks, ensuring each chunk maintains context about the table structure |
| `omit_header_on_overflow` | `False` | When enabled with `repeat_table_header=True`, omits table headers for specific rows that would overflow with the header but fit without it; particularly useful for tables with very wide headers or strict token limits |

---

### Basic Usage

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
result = converter.convert("https://arxiv.org/pdf/2408.09869")
doc = result.document

chunker = HybridChunker()
chunk_iter = chunker.chunk(dl_doc=doc)

for i, chunk in enumerate(chunk_iter):
    print(f"=== Chunk {i} ===")
    print(f"Text: {chunk.text[:100]}...")

    # Get enriched/contextualized text (recommended for embeddings)
    enriched = chunker.contextualize(chunk=chunk)
    print(f"Enriched: {enriched[:100]}...")
```

---

### Advanced Usage with Custom Tokenizer

```python
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer

EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
MAX_TOKENS = 64

tokenizer = HuggingFaceTokenizer(
    tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL_ID),
    max_tokens=MAX_TOKENS,
)

chunker = HybridChunker(tokenizer=tokenizer, merge_peers=True)
chunks = list(chunker.chunk(dl_doc=doc))

for i, chunk in enumerate(chunks):
    print(f"Text ({tokenizer.count_tokens(chunk.text)} tokens): {chunk.text!r}")
    enriched = chunker.contextualize(chunk=chunk)
    print(f"Enriched ({tokenizer.count_tokens(enriched)} tokens): {enriched!r}")

    # Access provenance metadata
    for item in chunk.meta.doc_items:
        for prov in getattr(item, "prov", []):
            print(f" Page: {prov.page_no}, BBox: {prov.bbox}")
```

---

### Table Chunking Features

HybridChunker provides enhanced support for chunking tables while preserving their structure. When tables span multiple chunks, the chunker can repeat table headers for better context:

```python
# Enable table header repetition (default behavior)
chunker = HybridChunker(
    tokenizer=tokenizer,
    repeat_table_header=True, # Headers repeated in each chunk
    omit_header_on_overflow=False # Always include headers
)
```

For tables with very wide headers that might exceed token limits, you can use `omit_header_on_overflow=True` to maximize token efficiency:

```python
# Flexible header handling for wide tables
chunker = HybridChunker(
    tokenizer=tokenizer,
    repeat_table_header=True,
    omit_header_on_overflow=True # Omit headers for rows that would overflow
)
```

When `omit_header_on_overflow=True`, the chunker intelligently decides whether to include the header: if a table row fits within the token limit without the header but would overflow with it, the header is omitted for that specific row. This preserves line integrity while optimizing token usage.

---

### Saving and Reloading the Converted Document

**Save only the document (JSON):**

```python
result.document.save_as_json("output.json")
```

**Reload the document:**

```python
from docling_core.types.doc.document import DoclingDocument

doc = DoclingDocument.load_from_json("output.json")
```

**Save the entire ConversionResult (includes status, errors, pages, timings, etc.):**

```python
result.save(filename="conversion_result.zip")
```

**Reload the full result:**

```python
from docling.datamodel.document import ConversionResult

loaded_result = ConversionResult.load("conversion_result.zip")
doc = loaded_result.document
```

> YAML is also supported via `save_as_yaml()` and `load_from_yaml()` on the `DoclingDocument`.

A full working notebook example is available at [hybrid\_chunking.ipynb](https://github.com/docling-project/docling/blob/4e650af56d8d4fe12c4ad74bde3ca0d9a9481905/docs/examples/hybrid_chunking.ipynb).