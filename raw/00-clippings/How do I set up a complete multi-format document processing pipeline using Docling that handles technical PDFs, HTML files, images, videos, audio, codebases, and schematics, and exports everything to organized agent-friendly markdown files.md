---
title: "How do I set up a complete multi-format document processing pipeline using Docling that handles technical PDFs, HTML files, images, videos, audio, codebases, and schematics, and exports everything to organized agent-friendly markdown files?"
source: "https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/documents/5cf33ffc-a9ed-485c-9a8c-b7b534c38ce2"
author:
  - "[[Devin]]"
published: 2025-12-17
created: 2026-06-03
description: "Complete Docling Multi-Format PipelinePrerequisitesbrew install tesseract leptonica pkg-config ffmpegexport TESSDATA_PREFIX=/opt/homebrew/share/tessdata/d"
tags:
  - "clippings"
---
## Complete Docling Multi-Format Pipeline

### Prerequisites

```bash
brew install tesseract leptonica pkg-config ffmpeg
export TESSDATA_PREFIX=/opt/homebrew/share/tessdata/
docling-tools models download
pip install "docling[asr,vlm,tesserocr,htmlrender]"
```

---

### Recommended Input Folder Structure

```
input_documents/
├── datasheets/
├── manuals/
├── books/
├── patents/
├── interviews/
├── html/
│ ├── page1.html
│ └── page1_files/ ← companion images, NOT converted individually
├── images/
├── videos/
├── schematics/ ← circuit diagrams, block diagrams, pinout drawings
└── repos/ ← local code repositories
```

---

### Pipeline Setup

```python
from pathlib import Path
from docling.datamodel import asr_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AsrPipelineOptions
from docling.datamodel.backend_options import HTMLBackendOptions
from docling.document_converter import (
    DocumentConverter, PdfFormatOption, AudioFormatOption, HTMLFormatOption,
)
from docling.pipeline.asr_pipeline import AsrPipeline

# --- PDF pipeline (datasheets, manuals, books, patents) ---
pdf_options = PdfPipelineOptions()
pdf_options.do_ocr = True
pdf_options.ocr_engine = "tesseract"
pdf_options.do_table_structure = True
pdf_options.do_code_enrichment = True
pdf_options.generate_picture_images = True
# For scanned/image-only PDFs: pdf_options.force_ocr = True

# --- Schematics-specific options ---
schematic_options = PdfPipelineOptions()
schematic_options.do_ocr = True
schematic_options.ocr_engine = "tesseract"
schematic_options.images_scale = 2.0 # higher res for detail
schematic_options.generate_picture_images = True
schematic_options.picture_description_preset = "granite_vision" # VLM describes diagrams

# --- ASR pipeline (video/audio transcription) ---
asr_options = AsrPipelineOptions()
asr_options.asr_options = asr_model_specs.WHISPER_TURBO

# --- HTML pipeline ---
html_options = HTMLBackendOptions(
    render_page=True,
    fetch_images=True,
    enable_local_fetch=True, # resolves relative image paths from HTML source
)

# --- Main converter ---
converter = DocumentConverter(
    allowed_formats=[
        InputFormat.PDF, InputFormat.IMAGE, InputFormat.HTML,
        InputFormat.AUDIO, InputFormat.DOCX, InputFormat.PPTX, InputFormat.MD,
    ],
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_options),
        InputFormat.IMAGE: PdfFormatOption(pipeline_options=pdf_options),
        InputFormat.AUDIO: AudioFormatOption(
            pipeline_cls=AsrPipeline, pipeline_options=asr_options,
        ),
        InputFormat.HTML: HTMLFormatOption(backend_options=html_options),
    },
)

# --- Schematics converter (separate, tuned for diagrams) ---
schematic_converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF, InputFormat.IMAGE],
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=schematic_options),
        InputFormat.IMAGE: PdfFormatOption(pipeline_options=schematic_options),
    },
)
```

---

### Codebase Preprocessing

Docling does not natively support source code files. Preprocess them into markdown first:

```python
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".hpp",
    ".go", ".rs", ".rb", ".swift", ".kt", ".cs", ".sh", ".bash",
    ".yaml", ".yml", ".json", ".toml", ".xml", ".sql",
}

def preprocess_codebase(repo_dir: Path, staging_dir: Path):
    staging_dir.mkdir(parents=True, exist_ok=True)
    for code_file in repo_dir.rglob("*"):
        if code_file.suffix not in CODE_EXTENSIONS or not code_file.is_file():
            continue
        relative = code_file.relative_to(repo_dir)
        safe_name = str(relative).replace("/", "__").replace("\\", "__")
        lang = code_file.suffix.lstrip(".")
        content = code_file.read_text(errors="replace")
        md_content = (
            f"# {relative}\n\n"
            f"**Repository:** {repo_dir.name}\n"
            f"**Language:** {lang}\n"
            f"**Path:** \`{relative}\`\n\n"
            f"\`\`\`{lang}\n{content}\n\`\`\`\n"
        )
        (staging_dir / f"{safe_name}.md").write_text(md_content)
    return list(staging_dir.glob("*.md"))

staging = Path("./staging/code")
code_files = []
for repo in Path("./input_documents/repos").iterdir():
    if repo.is_dir():
        code_files += preprocess_codebase(repo, staging / repo.name)
```

---

### Categorized Conversion & Export

```python
input_dir = Path("./input_documents")
output_dir = Path("./output_markdown")

categorized = {
    "datasheets": list((input_dir / "datasheets").glob("**/*.pdf")),
    "manuals": list((input_dir / "manuals").glob("**/*.pdf")),
    "books": list((input_dir / "books").glob("**/*.pdf")),
    "patents": list((input_dir / "patents").glob("**/*.pdf")),
    "interviews": list((input_dir / "interviews").glob("**/*.mp3"))
                 + list((input_dir / "interviews").glob("**/*.wav"))
                 + list((input_dir / "interviews").glob("**/*.mp4")),
    "html_pages": list((input_dir / "html").glob("**/*.html")), # skips companion image folders
    "images": list((input_dir / "images").glob("**/*.png"))
                 + list((input_dir / "images").glob("**/*.jpg")),
    "videos": list((input_dir / "videos").glob("**/*.mp4"))
                 + list((input_dir / "videos").glob("**/*.mov")),
    "schematics": list((input_dir / "schematics").glob("**/*.pdf"))
                 + list((input_dir / "schematics").glob("**/*.png"))
                 + list((input_dir / "schematics").glob("**/*.jpg")),
    "codebase": code_files,
}

for category, files in categorized.items():
    if not files:
        continue
    cat_dir = output_dir / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    active_converter = schematic_converter if category == "schematics" else converter

    for source in files:
        try:
            result = active_converter.convert(str(source))
            md = result.document.export_to_markdown()
            out_path = cat_dir / f"{source.stem}.md"
            out_path.write_text(md)
            print(f"✅ [{category}] {source.name} → {out_path}")
        except Exception as e:
            print(f"❌ [{category}] {source.name}: {e}")
```

---

### Format → Pipeline Reference

| Resource Type | Input Format | Pipeline |
| --- | --- | --- |
| Datasheets, manuals, books, patents (PDF) | `PDF` | `StandardPdfPipeline` with Tesseract OCR |
| Circuit board pictures, diagrams | `IMAGE` | `StandardPdfPipeline` |
| Schematics | `PDF` / `IMAGE` | `StandardPdfPipeline` with VLM (`granite_vision`) + `images_scale=2.0` |
| Locally saved HTML files | `HTML` | `SimplePipeline` with headless browser rendering |
| Downloaded videos (MP4/MOV) | `AUDIO` | `AsrPipeline` — audio extracted via ffmpeg |
| Interviews (MP3/WAV/M4A) | `AUDIO` | `AsrPipeline` with Whisper Turbo |
| Codebases | `MD` (preprocessed) | `SimplePipeline` |
| USPTO patent XML files | `XML_USPTO` | Dedicated USPTO pipeline |

---

### Key Notes

- **HTML companion folders**: Using `glob("**/*.html")` ensures only `.html` files are converted — images inside `page_files/` folders are skipped as standalone inputs but still resolved by the HTML backend via `enable_local_fetch=True`.
- **Scanned PDFs**: Add `pdf_options.force_ocr = True` and use `result.document.export_to_markdown(traverse_pictures=True)`.
- **Video transcription output** includes timestamps per segment, e.g., `[time: 0.0-4.0] Transcribed text here`.
- **READMEs and `.txt` files** in repos can be fed directly to Docling without preprocessing.
- **Schematics should be grouped separately** so VLM-based processing can be applied and agents can query them distinctly from text-heavy datasheets.