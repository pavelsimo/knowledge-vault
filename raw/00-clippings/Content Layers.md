---
title: "Content Layers"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/e596ee79-fc7f-43a4-90e2-74891e0cf12f"
author:
  - "[[Devin]]"
published: 2025-10-13
created: 2026-06-03
description: "Content LayersDocling uses content layers to categorize different parts of a document for flexible processing and export. Each element—such as main text, tabl"
tags:
  - "clippings"
---
Docling uses content layers to categorize different parts of a document for flexible processing and export. Each element—such as main text, tables, figures, page headers, and footers—is assigned to a specific content layer. This abstraction allows for fine-grained control over which parts of a document are included in downstream tasks or exports.

## Headers and Footers in DOCX Documents

When processing `.docx` files, Docling automatically parses page headers and footers. These are represented as `GroupItem` objects in the `ContentLayer.FURNITURE` layer, with:

- **label:** `GroupLabel.SECTION`
- **name:** `page header` (for headers) or `page footer` (for footers)

The content of each header or footer (which may include formatted text, lists, tables, images, etc.) is grouped inside these section groups. If a document contains multiple sections with different headers or footers, each distinct header or footer is added as a separate group. However, since Docling does not currently support pagination, only the unique headers and footers are included—there is no per-page association.

**Known limitations:**

- Only distinct headers and footers are included per section; repeated headers/footers across pages are not duplicated.
- Pagination is not supported, so headers/footers are not linked to specific pages.

## Default Export Behavior

By default, Docling excludes content in the `FURNITURE` layer (such as headers and footers) from export functionalities like Markdown, HTML, WebVTT, and plain text output. This helps produce clean, focused data by omitting repeated or non-essential elements from exported content.

## Including Headers and Footers in Exports

To include headers and footers (and other furniture) in your exports, you must explicitly specify the content layers to include using the Python API. For example, to export a document to Markdown, HTML, WebVTT, or plain text with both the main body and furniture:

```python
from docling_core.types.doc.document import ContentLayer
from docling import DocumentConverter

source = "/path/to/your/file.docx"
converter = DocumentConverter()
result = converter.convert(source)
doc = result.document

# Export to Markdown including headers and footers (FURNITURE)
md = doc.export_to_markdown(
    included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
)
with open("output_with_headers.md", "w") as f:
    f.write(md)

# Export to HTML including headers and footers (FURNITURE)
html = doc.export_to_html(
    included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
)
with open("output_with_headers.html", "w") as f:
    f.write(html)

# Export to plain text including headers and footers (FURNITURE)
text = doc.export_to_text(
    included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
)
with open("output_with_headers.txt", "w") as f:
    f.write(text)

# Export to WebVTT including headers and footers (FURNITURE)
vtt = doc.export_to_vtt(
    included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
)
with open("output_with_headers.vtt", "w") as f:
    f.write(vtt)
```

This ensures that both the main body and any detected headers or footers are present in the exported file.

### Exporting OCR Text from Scanned PDFs

When processing scanned or image-based PDFs with `force_full_page_ocr=True`, the layout model may classify the entire page as a `PictureItem`, with OCR text added as children of that picture node. In these cases, set `traverse_pictures=True` to include the OCR text in your exports:

```python
# For scanned/image-based PDFs processed with full-page OCR
text = doc.export_to_text(traverse_pictures=True)
md = doc.export_to_markdown(traverse_pictures=True)
```

Without this parameter, the export functions will return empty results even when OCR text is present in the document.

The `export_to_text()` method produces clean plain text without Markdown decoration (no heading markers `#`, bold/italic markers, or hyperlink syntax), while still preserving list bullets, ordered list numbers, and table separators for readability. The `export_to_vtt()` method serializes documents with TrackSource data to valid WebVTT format with configurable timestamp and voice tag formatting.

All four export methods (`export_to_text()`, `export_to_markdown()`, `export_to_html()`, `export_to_vtt()`) support the `included_content_layers` parameter:

- `included_content_layers`: Optional\[set\[ContentLayer\]\] = None

Additionally, `export_to_text()`, `export_to_markdown()`, and `export_to_html()` support:

- `page_no`: Optional\[int\] = None
- `page_break_placeholder`: Optional\[str\] = None

The `export_to_text()` and `export_to_markdown()` methods also support:

- `traverse_pictures`: bool = False – When True, traverses into PictureItem nodes during serialization to include their child text content. This is particularly useful when processing scanned/image-based PDFs with `force_full_page_ocr=True`, where the layout model classifies full-page scans as PictureItems and OCR text is added as children of those picture nodes. Without setting this to True, the export functions will return empty results even when OCR text is present in the document.

The `export_to_vtt()` method has additional WebVTT-specific parameters:

- `omit_hours_if_zero`: bool = False – If True, omit hours when they are 0 in the timings (e.g., "00:11.000" instead of "00:00:11.000")
- `omit_voice_end`: bool = False – If True and cue blocks have a WebVTT cue voice span as the only component, omit the voice end tag for brevity

The corresponding save methods (`save_as_text()`, `save_as_markdown()`, `save_as_html()`, `save_as_vtt()`) support the same parameters as their export counterparts, with one difference: `save_as_vtt()` defaults `omit_voice_end` to True (while `export_to_vtt()` defaults it to False) for more concise output files.

### Doclang (Experimental) Serializer

The experimental Doclang serializer (`docling_core/experimental/doclang.py`) also supports content layer filtering and annotation via `DoclangParams`.

**Content layer filtering:** The `layers` field controls which content layers are serialized. It accepts a `set[ContentLayer]` and defaults to all content layers. To serialize only the body layer, for example:

```python
from docling_core.experimental.doclang import DoclangParams
from docling_core.types.doc import ContentLayer

params = DoclangParams(layers={ContentLayer.BODY})
```

**Layer annotation:** The `layer_mode` field of type `LayerMode` controls whether a `<layer class="..."/>` self-closing XML token is emitted for each item:

- `LayerMode.MINIMAL` (default): emits `<layer class="..."/>` only when the item's content layer differs from `ContentLayer.BODY`.
- `LayerMode.ALWAYS`: emits `<layer class="..."/>` for every item, regardless of its layer.

```python
from docling_core.experimental.doclang import DoclangParams, LayerMode
from docling_core.types.doc import ContentLayer

params = DoclangParams(
    layers={ContentLayer.BODY, ContentLayer.FURNITURE},
    layer_mode=LayerMode.MINIMAL,
)
```

In the serialized XML output, content layer information appears as an embedded self-closing token, for example:

```xml
<page_header>
  <layer class="furniture"/>
  Page Header
</page_header>
<text>
  Main body content
</text>
```

With `LayerMode.ALWAYS`, `<layer class="body"/>` would also appear inside the `<text>` block above.

## Iterating Over Items Including Furniture

For advanced use cases, such as iterating over document items including headers and footers, use the `iterate_items` method with the appropriate content layers:

```python
for item, level in doc.iterate_items(
    included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
):
    # process item, including headers and footers
```

By default, `doc.iterate_items()` omits furniture, but you can include them as shown above.

## API and CLI Limitations

Currently, the ability to include furniture in exports is only available via the Python API. The `docling-serve` API and CLI exports do not support specifying content layers and will always export with the default (BODY only).

## Customization and Post-processing

Headers and footers are detected automatically by Docling’s layout model for `.docx` files. There is currently no rule-based mechanism to customize their detection during processing. However, you can manually remove or further process these elements after extraction if needed.

---

For more details, see the [relevant discussion](https://github.com/docling-project/docling/issues/1916#issuecomment-3057363280) and [API documentation](https://github.com/docling-project/docling/issues/2058).

---

**Summary:**

- Headers and footers from `.docx` files are parsed as section groups in the `FURNITURE` content layer.
- By default, furniture is excluded from exports, but can be included via the Python API.
- Only unique headers/footers per section are included; pagination is not supported.
- Further customization is possible after extraction.