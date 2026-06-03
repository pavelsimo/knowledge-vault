---
title: "What is the best practice for processing a mixed PDF (digital + scanned pages) containing sensitive financial data in Docling, given no GPU and limited cost?"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/d9feb0c4-7825-49c9-bfd1-1591073b8d14"
author:
  - "[[Devin]]"
published: 2026-03-09
created: 2026-06-03
description: "Best Practice: Mixed PDF, CPU-Only, Sensitive Financial Data in DoclingKey Insight: No Manual Combination NeededDocling automatically handles mixed PDFs (dig"
tags:
  - "clippings"
---
## Best Practice: Mixed PDF, CPU-Only, Sensitive Financial Data in Docling

### Key Insight: No Manual Combination Needed

Docling **automatically handles mixed PDFs** (digital + scanned in one file). Per-page bitmap coverage analysis determines:

- **Digital pages** → text extracted directly from PDF (no OCR)
- **Scanned pages** → OCR runs automatically only on bitmap areas
- **Mixed pages** → native text + OCR combined, duplicates filtered via spatial analysis

---

### Recommended Pipeline (CPU-Only, No Cost)

```python
import os
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions, RapidOcrOptions,
    TableStructureOptions, TableFormerMode,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions

os.environ["OMP_NUM_THREADS"] = "4"

pipeline_options = PdfPipelineOptions(
    do_ocr=True,
    ocr_options=RapidOcrOptions(), # CPU-friendly, ~6s/page
    images_scale=2.0, # Higher resolution = better number accuracy
    do_table_structure=True,
    table_structure_options=TableStructureOptions(
        mode=TableFormerMode.ACCURATE, # Most precise for financial tables
        do_cell_matching=False, # Important for scanned pages
    ),
    generate_page_images=False,
    generate_picture_images=False,
    do_code_enrichment=False,
    do_formula_enrichment=False,
    accelerator_options=AcceleratorOptions(num_threads=4, device=AcceleratorDevice.CPU),
)

converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
)

result = converter.convert("laporan_keuangan.pdf")
doc = result.document

# Export for AI agent
md = doc.export_to_markdown(traverse_pictures=True) # traverse_pictures=True is required
doc.save_as_json("output/document.json") # Lossless backup
```

**Key configuration choices:**

| Option | Reason |
| --- | --- |
| `RapidOcrOptions()` | CPU-friendly OCR, ~6s/page (vs EasyOCR ~70s/page on CPU) |
| `images_scale=2.0` | 2x resolution improves readability of small numbers |
| `TableFormerMode.ACCURATE` | Most precise mode for financial tables |
| `do_cell_matching=False` | Let TableFormer define cells independently (critical for scanned pages) |
| `traverse_pictures=True` | Required during export so OCR text from scanned pages is included |

---

### OCR Engine Comparison (CPU-Only)

| Engine | Speed (CPU) | Accuracy | Notes |
| --- | --- | --- | --- |
| **RapidOCR** ✅ | ~6s/page | Good | Best choice for CPU |
| EasyOCR | ~70s/page | Better for numeric tables | Too slow without GPU |
| Tesseract | ~6s/page | Good for standard text | Stable and lightweight |

**Recommendation:** Use **RapidOCR** for CPU. EasyOCR is more accurate for numeric tables but ~10x slower without a GPU.

---

### If the PDF Contains Multiple Logical Documents (e.g., invoice + report + receipt)

Split by keyword first, then process each logical document independently:

```python
import fitz # PyMuPDF

BOUNDARY_KEYWORDS = ["INVOICE", "FAKTUR", "LAPORAN KEUANGAN", "BANK STATEMENT", "RECEIPT"]

def detect_boundaries(pdf_path):
    doc = fitz.open(pdf_path)
    documents = []
    current_doc = {"type": "unknown", "start_page": 0}
    for page_num in range(len(doc)):
        text = doc[page_num].get_text().upper()
        for keyword in BOUNDARY_KEYWORDS:
            if keyword in text:
                current_doc["end_page"] = page_num - 1
                if page_num > 0:
                    documents.append(current_doc)
                current_doc = {"type": keyword.lower(), "start_page": page_num}
                break
    current_doc["end_page"] = len(doc) - 1
    documents.append(current_doc)
    doc.close()
    return documents
```

Then run Docling on each split document separately.

---

### Estimated Processing Time (50 pages, CPU)

| Scenario | Time |
| --- | --- |
| All digital pages (no OCR) | ~1–2 minutes |
| 50% scanned pages | ~5–8 minutes |
| All scanned pages | ~10–15 minutes |

---

### When to Use VLM Pipeline (OpenAI API)

Skip VLM for now. Use it **only** if specific pages have very complex layouts (e.g., merged cells, extreme hierarchical tables) after reviewing the initial output. At ~$0.01–$0.04/page for GPT-4o, selectively sending only problematic pages keeps costs low.

**All built-in OCR engines (RapidOCR, EasyOCR, Tesseract) are free, local, and send no data to external APIs.**