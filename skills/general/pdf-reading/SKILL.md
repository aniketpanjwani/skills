---
name: pdf-reading
description: Read, summarize, search, and extract structured artifacts from PDF files, especially papers and reports. Use when the user wants a PDF converted before reading, needs figures or tables pulled out, wants image labels or captions, or needs cleaner Markdown/text than reading the PDF directly.
---

# PDF Reading

Use this skill for PDF-first work on papers and reports. The default path is Docling-first.

## Rules

- Never read a PDF directly. Convert it first, then read the generated artifact.
- Default to Docling for reading. Use `--fast` only when the user explicitly prefers speed over fidelity.
- Extract figures or tables only when the user asks for them or when the answer depends on them.
- For tables, prefer the cleaned Markdown for quick review, but inspect the crop image when numeric fidelity matters.
- If values or labels look suspicious, cite the crop or page artifact rather than trusting the structured export.
- If Docling fails, fall back to `pdftotext -layout` and continue with a degraded-quality warning.

## Quick Start

Run the extractor on a PDF:

```bash
python3 skills/general/pdf-reading/scripts/pdf_extract.py /path/to/paper.pdf
```

Extract figures with structural labels:

```bash
python3 skills/general/pdf-reading/scripts/pdf_extract.py /path/to/paper.pdf --extract-figures
```

Extract figures with richer descriptions instead of classifier labels:

```bash
python3 skills/general/pdf-reading/scripts/pdf_extract.py /path/to/paper.pdf --extract-figures --figure-label-mode description
```

Extract tables, agent-facing JSON, LaTeX, cleaned Markdown, CSV, and crop images:

```bash
python3 skills/general/pdf-reading/scripts/pdf_extract.py /path/to/paper.pdf --extract-tables
```

Extract both figures and tables:

```bash
python3 skills/general/pdf-reading/scripts/pdf_extract.py /path/to/paper.pdf --extract-figures --extract-tables
```

Use the faster MarkItDown path only when requested:

```bash
python3 skills/general/pdf-reading/scripts/pdf_extract.py /path/to/paper.pdf --fast
```

## Outputs

- `<basename>.docling.md`: primary reading artifact from Docling.
- Inline tables inside `<basename>.docling.md` now get a compact YAML artifact block immediately after the table with links to the extracted table sidecars.
- `<basename>.layout.txt`: fallback text artifact when Docling fails.
- `<basename>.docling_artifacts/`: extracted figure images referenced by Markdown.
- `<basename>.figures.json`: figure metadata, labels, captions, and image paths.
- `<basename>.tables/`: raw and cleaned table Markdown, CSV exports, and crop images.
- `<basename>.tables/<table_nnn>.raw_docling.json`: full Docling table object dump.
- `<basename>.tables/<table_nnn>.agent.json`: cell/span AST with provenance, regression semantics, and embedded LaTeX.
- `<basename>.tables/<table_nnn>.html`: Docling HTML rendering for the table.
- `<basename>.tables/<table_nnn>.otsl.txt`: Docling OTSL table structure dump.
- `<basename>.tables/<table_nnn>.tex`: synthesized canonical LaTeX table output.
- `<basename>.tables.json`: table metadata, paths, and verification flags.

The script prints a JSON summary with the exact artifact paths to read next.

Maintainer benchmark fixtures and runners live under `tests/pdf-reading/` rather than inside the installable skill.
