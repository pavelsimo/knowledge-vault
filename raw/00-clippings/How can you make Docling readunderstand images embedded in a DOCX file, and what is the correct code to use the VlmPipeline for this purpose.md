---
title: "How can you make Docling read/understand images embedded in a DOCX file, and what is the correct code to use the VlmPipeline for this purpose?"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/418425aa-73df-4e48-b5cc-00c2f674d526"
author:
  - "[[Devin]]"
published: 2026-05-13
created: 2026-06-03
description: "When processing a DOCX file with Docling, images are replaced with [image] placeholders by default because DOCX files use the SimplePipeline, which lacks OCR or"
tags:
  - "clippings"
---
When processing a DOCX file with Docling, images are replaced with `[image]` placeholders by default because DOCX files use the **SimplePipeline**, which lacks OCR or image understanding capabilities.

## Options to Read Images

### Option 1: Use VlmPipeline (Vision-Language Model)

**Note:** VlmPipeline does **not** support DOCX directly. You must first convert the DOCX to PDF (using Microsoft Word, LibreOffice, etc.), then use the following code:

```python
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=VlmPipeline,
        ),
    }
)

result = converter.convert("your_document.pdf")
print(result.document.export_to_markdown())
```

> ⚠️ **Common mistake:** Do **not** pass `pipeline_options` directly to `DocumentConverter(...)` — it will throw:
> 
> ```
> TypeError: DocumentConverter.__init__() got an unexpected keyword argument 'pipeline_options'
> ```
> 
> Pipeline configuration must go inside `format_options`.

### Handling PARTIAL\_SUCCESS Status

When using VlmPipeline, the conversion may return `PARTIAL_SUCCESS` status if the vision-language model encounters issues processing certain pages. This can happen when:

- **Token limit reached (`LENGTH`)** — The VLM hits its maximum token limit and truncates output
- **Content filtered (`CONTENT_FILTERED`)** — The API provider blocks the output due to content policies
- **Missing predictions (`NONE`)** — VLM predictions are missing for some pages

To detect incomplete results, check the conversion status and errors:

```python
result = converter.convert("your_document.pdf")

# Check if conversion completed successfully
if result.status == ConversionStatus.PARTIAL_SUCCESS:
    print("Warning: Some pages were not fully processed")
    for error in result.errors:
        print(f" - {error.error_message}")

print(result.document.export_to_markdown())
```

Import `ConversionStatus` to check the result:

```python
from docling.datamodel.base_models import ConversionStatus, InputFormat
```

This is particularly important when processing documents with many images or complex content, as VLM processing may encounter rate limits, token limits, or content filtering.

### Option 2: Convert DOCX → PDF and Use StandardPdfPipeline with OCR

If the images contain text you need to extract, convert the DOCX to PDF and process it with Docling's PDF pipeline, which supports OCR backends like EasyOCR, Tesseract, or RapidOCR.

## Important Limitation

Even with the correct VlmPipeline setup, results may still show `[image]` placeholders — native OCR/image description for DOCX files is not supported, and image handling depends entirely on the backend converter with no tunable options for non-PDF formats.