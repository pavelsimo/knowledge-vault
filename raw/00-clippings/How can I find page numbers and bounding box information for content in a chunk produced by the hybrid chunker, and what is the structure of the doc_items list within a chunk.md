---
title: "How can I find page numbers and bounding box information for content in a chunk produced by the hybrid chunker, and what is the structure of the doc_items list within a chunk?"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/bfdfb141-1615-4b31-879d-5598be665588"
author:
  - "[[Devin]]"
published: 2025-12-30
created: 2026-06-03
description: "Page numbers and bounding box information for content in a chunk produced by the hybrid chunker are available through the chunk's provenance metadata. Specifica"
tags:
  - "clippings"
---
Page numbers and bounding box information for content in a chunk produced by the hybrid chunker are available through the chunk's provenance metadata. Specifically, each chunk has a `meta.doc_items` list, where each `doc_item` represents a discrete document element (such as a paragraph, list item, table, image, etc.). Each `doc_item` contains a `prov` list with provenance information, including:

- `page_no`: the page number (integer)
- `bbox`: the bounding box (with absolute coordinates: `l`, `t`, `r`, `b`)
- `charspan`: the character span (start, end)

**Note:** Bounding box coordinates are absolute (pixels/points), not normalized. To normalize them to a 0–1.0 range, use the `normalized()` method on the bounding box and provide the page's size.

**Example to extract page numbers:**

```python
for item in chunk.meta.doc_items:
    for prov in getattr(item, "prov", []):
        print(prov.page_no)
```

**Why multiple doc\_items per chunk?** The hybrid chunker combines consecutive document elements (doc\_items) into a chunk until a token limit is reached. For example, if three paragraphs fit within the token limit, all three will be included in the chunk's `doc_items` list. This allows you to trace which original document elements contributed to each chunk.

**Table-aware chunking:** When a table is too large to fit in a single chunk, the HybridChunker can automatically split it across multiple chunks while preserving context:

- The `repeat_table_header` parameter (default: `True`) controls whether table headers are automatically repeated when tables are split. When enabled, each chunk containing table rows includes the header, making chunks self-contained and independently understandable. This is especially valuable when chunks are processed separately or stored in different locations
- The `omit_header_on_overflow` parameter (default: `False`) controls behavior specifically when the table header itself exceeds `max_tokens`. When set to `True`, oversized headers are omitted from subsequent chunks; when `False`, headers are included even if they cause chunks to exceed `max_tokens`. This parameter is particularly useful for tables with very wide headers that might violate token limits
- These behaviors can be adjusted by setting `repeat_table_header=False` or `omit_header_on_overflow=True` when initializing the chunker
- Table header repetition is supported for both markdown and HTML-serialized tables

**Example of HybridChunker with table header repetition:**

```python
from docling_core.transforms.chunker import HybridChunker

# Default behavior: table headers are repeated
chunker = HybridChunker(max_tokens=512)

# Disable header repetition if needed
chunker = HybridChunker(max_tokens=512, repeat_table_header=False)

# Handle wide tables with large headers using omit_header_on_overflow
chunker = HybridChunker(
    max_tokens=512,
    repeat_table_header=True,
    omit_header_on_overflow=True # Omit headers when they would cause overflow
)
```

**Limitations:**

- Line numbers are not available.
- DOCX files do not provide page or bounding box metadata; convert to PDF if you need this data.
- Table items may have empty provenance lists, so page info may not be available for tables even in PDFs.

**References:**

- [ProvenanceItem definition](https://github.com/docling-project/docling-core/blob/9eca661df795b9335fcf05b32705614be674e60f/docling_core/types/doc/document.py#L1188-L1199)
- [DocItemLabel enum](https://github.com/docling-project/docling-core/blob/9eca661df795b9335fcf05b32705614be674e60f/docling_core/types/doc/labels.py#L6-L36)
- [HybridChunker algorithm](https://github.com/docling-project/docling-core/blob/9eca661df795b9335fcf05b32705614be674e60f/docling_core/transforms/chunker/hybrid_chunker.py#L172-L213)