Docling is a local document-conversion and extraction toolkit for turning PDFs, DOCX files, HTML, images, audio, and other source material into structured documents, Markdown, JSON, and chunks suitable for RAG. In this vault it is most useful as a bridge between messy technical documents and downstream AI workflows: OCR, table extraction, provenance metadata, content-layer filtering, and agent-friendly exports.

## Sources

- [[raw/clippings/docling-multiformat-pipeline.md|raw/clippings/docling-multiformat-pipeline.md]]
- [[raw/clippings/How do you use HybridChunker in Docling, including saving and reloading the converted document.md|raw/clippings/How do you use HybridChunker in Docling, including saving and reloading the converted document.md]]
- [[raw/clippings/docling-hybrid-chunker-provenance.md|raw/clippings/docling-hybrid-chunker-provenance.md]]
- [[raw/clippings/Content Layers.md|raw/clippings/Content Layers.md]]
- [[raw/clippings/How can you make Docling readunderstand images embedded in a DOCX file, and what is the correct code to use the VlmPipeline for this purpose.md|raw/clippings/How can you make Docling readunderstand images embedded in a DOCX file, and what is the correct code to use the VlmPipeline for this purpose.md]]
- [[raw/clippings/What is the best practice for processing a mixed PDF (digital + scanned pages) containing sensitive financial data in Docling, given no GPU and limited cost.md|raw/clippings/What is the best practice for processing a mixed PDF (digital + scanned pages) containing sensitive financial data in Docling, given no GPU and limited cost.md]]
- [[raw/clippings/local-llm-pdf-datasheet-extraction.md|raw/clippings/local-llm-pdf-datasheet-extraction.md]]

## Pipeline Shape

A robust Docling pipeline separates document categories before conversion:

| Input class | Recommended handling |
|---|---|
| Technical PDFs, manuals, datasheets, books, patents | `PdfPipelineOptions` with OCR, table structure, and optional image generation |
| Schematics and pinout diagrams | Separate converter with higher `images_scale` and picture descriptions |
| HTML pages | HTML backend with local fetch enabled for companion images |
| Audio and video | ASR pipeline, usually Whisper Turbo |
| Code repositories | Preprocess source files into Markdown before handing them to Docling |
| Local RAG systems | Export JSON for lossless storage, Markdown for agent use, then chunk with `HybridChunker` |

The practical architecture for technical-document QA is:

```text
PDF or document source -> Docling conversion -> JSON/Markdown -> HybridChunker -> embeddings -> vector DB -> local or hosted LLM
```

For privacy-sensitive work, keep `enable_remote_services` disabled. The local stack can run OCR, layout analysis, table extraction, chunking, and export without sending documents to external services.

## Mixed PDFs and OCR

Docling can handle PDFs that mix digital text and scanned pages. It performs per-page bitmap coverage analysis:

- Digital pages use native PDF text extraction.
- Scanned pages run OCR only where needed.
- Mixed pages combine native text and OCR while filtering duplicates through spatial analysis.

For CPU-only sensitive financial PDFs, the raw notes recommend RapidOCR or Tesseract over EasyOCR when speed and local processing matter:

```python
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions

options = PdfPipelineOptions()
options.do_ocr = True
options.ocr_options = RapidOcrOptions()
options.images_scale = 2.0
options.do_table_structure = True
options.generate_page_images = False
options.generate_picture_images = False

converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)}
)

result = converter.convert("document.pdf")
result.document.save_as_json("output/document.json")
markdown = result.document.export_to_markdown(traverse_pictures=True)
```

`traverse_pictures=True` matters for scanned PDFs where OCR text may be attached under picture nodes. Without it, export can look empty even when OCR succeeded.

## Chunking and Provenance

`HybridChunker` creates token-bounded chunks while preserving document structure. Each chunk contains `chunk.text` plus metadata under `chunk.meta.doc_items`.

Each `doc_item` usually corresponds to a source document element: paragraph, list item, table, image, or similar. Provenance lives in `doc_item.prov`:

```python
for item in chunk.meta.doc_items:
    for prov in getattr(item, "prov", []):
        print(prov.page_no, prov.bbox, prov.charspan)
```

Key details:

- `page_no` gives the page number.
- `bbox` stores absolute coordinates, not normalized coordinates.
- `charspan` stores the character span.
- A chunk may contain multiple `doc_items` because the chunker merges consecutive elements until the token budget is reached.
- DOCX does not provide page or bounding-box metadata; convert to PDF if page geometry matters.
- Large tables can be split with repeated headers using `repeat_table_header=True`.
- `omit_header_on_overflow=True` helps wide tables stay inside strict token limits.

## Content Layers

Docling classifies document elements into content layers. The main body is exported by default, while page furniture such as headers and footers is usually excluded.

For DOCX headers and footers, Docling represents page furniture as `GroupItem` objects in `ContentLayer.FURNITURE`. To include them:

```python
from docling_core.types.doc.document import ContentLayer

md = doc.export_to_markdown(
    included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
)
```

This is useful when the header or footer contains meaningful metadata, document numbers, revision state, or contractual context. Leave furniture excluded when repeated page material would pollute retrieval.

## DOCX Images and VLMs

DOCX files use the simpler Docling pipeline, so embedded images may become `[image]` placeholders. The raw guidance is explicit: `VlmPipeline` does not support DOCX directly. Convert DOCX to PDF first, then use a PDF format option with `pipeline_cls=VlmPipeline`.

```python
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline),
    }
)

result = converter.convert("document.pdf")
print(result.document.export_to_markdown())
```

Do not pass `pipeline_options` directly to `DocumentConverter`; pipeline configuration belongs inside `format_options`.

## Local Technical-Document RAG

For limited hardware, the local stack in the raw notes is:

| Layer | Tool |
|---|---|
| Extraction | Docling with OCR and TableFormer |
| Chunking | `HybridChunker` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | ChromaDB |
| Local LLM | Ollama with Phi-3 Mini, Mistral 7B, or TinyLlama |
| UI | Streamlit |

This pairs naturally with [[rag]] and [[sentence-embeddings]]. The main design rule is to preserve structured JSON as a lossless backup, export Markdown for agent workflows, and carry provenance into chunks so answers can point back to source pages.

## Related Topics

- [[rag]] - retrieval pipeline patterns that can consume Docling chunks
- [[sentence-embeddings]] - embedding models for chunk retrieval
- [[multimodal-models]] - vision-language models for image-heavy documents
- [[ai-coding]] - agent-friendly Markdown and structured source preparation
- [[system-design]] - pipeline design and data-flow tradeoffs
