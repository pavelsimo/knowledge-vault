---
title: "How can a student build a local, open-source LLM-based system to extract and analyze technical PDF documents (PMS/IDC) and generate instrumentation datasheets, using Python on a PC with limited resources?"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/da5b107d-66f1-4642-b9e9-860ed388e621"
author:
  - "[[Devin]]"
published: 2026-05-13
created: 2026-06-03
description: "Local LLM-Based PDF Analysis System for Technical Documents (PFE Project)Recommended ArchitecturePDF (PMS/IDC) → Docling (extraction) → JSON structuré → Vect"
tags:
  - "clippings"
---
## Local LLM-Based PDF Analysis System for Technical Documents (PFE Project)

### Recommended Architecture

```
PDF (PMS/IDC) → Docling (extraction) → JSON structuré → Vector DB → LLM local → Datasheets
```

---

### Key Components & Tools

| Component | Tool |
| --- | --- |
| PDF Extraction | `docling` (with OCR + TableFormer) |
| OCR Engine | EasyOCR (built into Docling) |
| Local LLM | Ollama + Mistral 7B / Phi-3 Mini / TinyLlama |
| Vector Database | ChromaDB (local) |
| RAG Framework | LangChain or LlamaIndex |
| UI | Streamlit |

---

### Privacy & Local Operation

**Docling runs 100% locally** — no data is sent to external servers. All OCR, layout analysis, and table extraction happen on your machine. You can pre-download all models for fully offline operation:

```bash
pip install docling-tools
docling-tools models download --all
```

The only exception is if `enable_remote_services=True` is explicitly set, which is disabled by default.

---

### Step-by-Step Implementation

**1\. Set up the environment:**

```bash
mkdir ~/mon-projet-pfe && cd ~/mon-projet-pfe
python3 -m venv venv && source venv/bin/activate
```

**2\. Install dependencies:**

```bash
pip install "docling[tesserocr]" docling-tools langchain-docling langchain-community \
    langchain-chroma chromadb sentence-transformers streamlit transformers torch
```

**3\. Install Ollama + a local LLM model:**

```bash
curl https://ollama.ai/install.sh | sh
ollama pull phi3:mini # Lightweight (~8 GB RAM needed)
# or
ollama pull tinyllama # Ultra-light (~4 GB RAM needed)
```

**4\. Extract PDFs to structured JSON (minimal test):**

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions, TableStructureV2Options
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from pathlib import Path

pdf_options = PdfPipelineOptions()
pdf_options.do_ocr = True
pdf_options.ocr_options = EasyOcrOptions(lang=["fr", "en"], use_gpu=False)
pdf_options.do_table_structure = True
pdf_options.table_structure_options = TableStructureV2Options(do_cell_matching=True)

converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_options)}
)

result = converter.convert("documents/your_document.pdf")
result.document.save_as_json("outputs/output.json")
md = result.document.export_to_markdown()
Path("outputs/output.md").write_text(md, encoding="utf-8")
```

**5\. Build a RAG pipeline:**

```python
from docling.chunking import HybridChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

chunker = HybridChunker(max_tokens=512)
chunks = list(chunker.chunk(dl_doc=result.document))

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")

llm = Ollama(model="phi3:mini")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)
```

**6\. Launch the Streamlit web UI:**

```bash
streamlit run app.py
# Opens at http://localhost:8501
```

---

### Hardware Constraints & Solutions

| Constraint | Solution |
| --- | --- |
| Low available RAM (< 2 GB free) | Close all other programs; use quantized models (GGUF 4-bit) via Ollama |
| Limited disk space | Use `generate_page_images=False` in pipeline options to reduce memory |
| Scanned PDF checkboxes | OCR + regex post-processing or a Vision Language Model (VLM) |
| Complex tables (merged cells) | Use TableFormer V2 or Granite Vision Table |
| Very large PDFs | Process in page batches |

> **Note:** If the PC has only ~1.6 GB of available RAM, even Docling alone may struggle. It is recommended to free RAM by closing background applications, or use Google Colab (free GPU) for processing while keeping local extraction for confidentiality.