#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from table_cleanup import clean_table_markdown


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert PDFs into readable Markdown and optional figure/table artifacts.")
    parser.add_argument("pdf", help="Path to the source PDF.")
    parser.add_argument("--extract-figures", action="store_true", help="Extract figure images and write figures.json.")
    parser.add_argument(
        "--figure-label-mode",
        choices=("classification", "description", "none"),
        default="classification",
        help="How figure labels should be added to Markdown and figures.json.",
    )
    parser.add_argument("--extract-tables", action="store_true", help="Extract tables, cleaned Markdown, CSV, and crop images.")
    parser.add_argument(
        "--table-cleanup",
        choices=("normal", "off"),
        default="normal",
        help="Whether to run readability cleanup on exported table Markdown.",
    )
    parser.add_argument("--fast", action="store_true", help="Use MarkItDown instead of Docling for the read artifact.")
    parser.add_argument("--force", action="store_true", help="Ignore cache and regenerate outputs.")
    return parser.parse_args()


def _uv_bootstrap(args: argparse.Namespace) -> None:
    if os.environ.get("PDF_READING_UV_BOOTSTRAPPED") == "1":
        return

    docling_missing = False
    markitdown_missing = False

    if not args.fast or args.extract_figures or args.extract_tables:
        try:
            import docling  # noqa: F401
        except ImportError:
            docling_missing = True

    if args.fast:
        try:
            import markitdown  # noqa: F401
        except ImportError:
            markitdown_missing = True

    if not docling_missing and not markitdown_missing:
        return

    uv = shutil.which("uv")
    if uv is None:
        missing = []
        if docling_missing:
            missing.append("docling")
        if markitdown_missing:
            missing.append("markitdown[pdf]")
        raise SystemExit(f"Missing dependencies: {', '.join(missing)}. Install them or install uv first.")

    cmd = [uv, "run"]
    if docling_missing or args.extract_figures or args.extract_tables or not args.fast:
        cmd.extend(["--with", "docling"])
    if markitdown_missing or args.fast:
        cmd.extend(["--with", "markitdown[pdf]"])
    cmd.extend(["python", str(Path(__file__).resolve()), *sys.argv[1:]])
    env = os.environ.copy()
    env["PDF_READING_UV_BOOTSTRAPPED"] = "1"
    raise SystemExit(subprocess.call(cmd, env=env))


def _sanitize_description(text: str | None) -> str | None:
    if not text:
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"<end_of_utteranc.*$", "", cleaned).strip()
    cleaned = re.sub(r"<\|.*?\|>", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or None


def _sanitize_markdown_artifacts(markdown: str) -> str:
    cleaned = re.sub(r"<end_of_utteranc[^ \n]*", "", markdown)
    cleaned = re.sub(r"<\|.*?\|>", "", cleaned)
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    return cleaned


def _parse_table_title(table_markdown: str) -> str | None:
    for line in table_markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("|"):
            return None
        return stripped
    return None


def _json_dump(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_fresh(pdf_path: Path, sentinels: list[Path]) -> bool:
    if not sentinels:
        return False
    if not all(path.exists() for path in sentinels):
        return False
    pdf_mtime = pdf_path.stat().st_mtime
    return all(path.stat().st_mtime >= pdf_mtime for path in sentinels)


def _build_summary(
    pdf_path: Path,
    read_artifact: Path,
    engine: str,
    cached: bool,
    figures_json: Path | None,
    tables_json: Path | None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "source_pdf": str(pdf_path),
        "read_artifact": str(read_artifact),
        "engine": engine,
        "cached": cached,
    }
    if figures_json is not None:
        summary["figures_manifest"] = str(figures_json)
    if tables_json is not None:
        summary["tables_manifest"] = str(tables_json)
    return summary


def _run_markitdown(pdf_path: Path, output_path: Path) -> Path:
    from markitdown import MarkItDown

    result = MarkItDown().convert(str(pdf_path))
    output_path.write_text(result.text_content, encoding="utf-8")
    return output_path


def _run_pdftotext(pdf_path: Path, output_path: Path) -> Path:
    pdftotext = shutil.which("pdftotext")
    if pdftotext is None:
        raise RuntimeError("Docling failed and pdftotext is unavailable for fallback.")
    subprocess.run([pdftotext, "-layout", str(pdf_path), str(output_path)], check=True)
    return output_path


def _rename_docling_artifacts(md_path: Path, artifacts_dir: Path, label_prefix: str = "figure") -> list[Path]:
    markdown = md_path.read_text(encoding="utf-8")
    generated = sorted(path for path in artifacts_dir.iterdir() if path.is_file())
    renamed: list[Path] = []

    for index, old_path in enumerate(generated, start=1):
        new_name = f"{label_prefix}_{index:03d}{old_path.suffix.lower()}"
        new_path = artifacts_dir / new_name
        if old_path != new_path:
            old_path.replace(new_path)
        new_ref = f"{artifacts_dir.name}/{new_path.name}"
        markdown = markdown.replace(str(old_path), new_ref)
        markdown = markdown.replace(old_path.as_posix(), new_ref)
        markdown = markdown.replace(f"{artifacts_dir.name}/{old_path.name}", new_ref)
        renamed.append(new_path)

    markdown = _sanitize_markdown_artifacts(markdown)
    md_path.write_text(markdown, encoding="utf-8")
    return renamed


def _extract_figures(doc: Any, pdf_path: Path, artifacts_dir: Path, figures_json: Path, renamed_artifacts: list[Path]) -> None:
    figures: list[dict[str, Any]] = []
    for index, picture in enumerate(doc.pictures, start=1):
        page_no = None
        if getattr(picture, "prov", None):
            page_no = getattr(picture.prov[0], "page_no", None)

        description = None
        top_label = None
        top_confidence = None
        if getattr(picture, "meta", None) is not None:
            description = _sanitize_description(getattr(getattr(picture.meta, "description", None), "text", None))
            classification = getattr(picture.meta, "classification", None)
            if classification and getattr(classification, "predictions", None):
                top_prediction = classification.predictions[0]
                top_label = top_prediction.class_name
                top_confidence = round(float(top_prediction.confidence), 3)

        image_path = None
        if index <= len(renamed_artifacts):
            image_path = renamed_artifacts[index - 1]

        figures.append(
            {
                "id": index,
                "page": page_no,
                "caption": picture.caption_text(doc) or None,
                "label": top_label,
                "label_confidence": top_confidence,
                "description": description,
                "image_path": str(image_path) if image_path is not None else None,
            }
        )

    _json_dump(figures_json, figures)


def _extract_tables(doc: Any, tables_dir: Path, tables_json: Path, table_cleanup_mode: str) -> None:
    tables_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []

    for index, table in enumerate(doc.tables, start=1):
        prefix = f"table_{index:03d}"
        raw_md_path = tables_dir / f"{prefix}.raw.md"
        cleaned_md_path = tables_dir / f"{prefix}.cleaned.md"
        crop_path = tables_dir / f"{prefix}.crop.png"
        csv_path = tables_dir / f"{prefix}.csv"

        raw_markdown = table.export_to_markdown(doc=doc)
        raw_md_path.write_text(raw_markdown, encoding="utf-8")

        cleanup_report = None
        cleaned_markdown = raw_markdown
        if table_cleanup_mode == "normal":
            cleaned_markdown, cleanup_report = clean_table_markdown(raw_markdown)
        cleaned_md_path.write_text(cleaned_markdown, encoding="utf-8")

        csv_output = None
        try:
            dataframe = table.export_to_dataframe(doc=doc)
            dataframe.to_csv(csv_path, index=False)
            csv_output = csv_path
        except Exception:
            csv_output = None

        crop_saved = None
        try:
            crop = table.get_image(doc)
            if crop is not None:
                crop.save(crop_path)
                crop_saved = crop_path
        except Exception:
            crop_saved = None

        page_no = None
        if getattr(table, "prov", None):
            page_no = getattr(table.prov[0], "page_no", None)

        if cleanup_report is None:
            _, cleanup_report = clean_table_markdown(raw_markdown)

        manifest.append(
            {
                "id": index,
                "page": page_no,
                "title": _parse_table_title(raw_markdown),
                "raw_markdown_path": str(raw_md_path),
                "cleaned_markdown_path": str(cleaned_md_path),
                "csv_path": str(csv_output) if csv_output is not None else None,
                "crop_path": str(crop_saved) if crop_saved is not None else None,
                "verification_required": cleanup_report.verification_required,
                "verification_reasons": cleanup_report.reasons,
                "cleanup_report": asdict(cleanup_report),
            }
        )

    _json_dump(tables_json, manifest)


def _run_docling(
    args: argparse.Namespace,
    pdf_path: Path,
    md_path: Path,
    artifacts_dir: Path,
    figures_json: Path | None,
    tables_dir: Path | None,
    tables_json: Path | None,
) -> Path:
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling_core.types.doc import ImageRefMode

    options = PdfPipelineOptions()
    options.generate_picture_images = args.extract_figures
    options.generate_page_images = args.extract_tables
    options.do_picture_classification = args.extract_figures and args.figure_label_mode == "classification"
    options.do_picture_description = args.extract_figures and args.figure_label_mode == "description"

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=options),
        }
    )
    result = converter.convert(str(pdf_path))
    doc = result.document

    md_path.parent.mkdir(parents=True, exist_ok=True)
    if args.extract_figures and artifacts_dir.exists():
        shutil.rmtree(artifacts_dir)
    if args.extract_tables and tables_dir.exists():
        shutil.rmtree(tables_dir)
    image_mode = ImageRefMode.REFERENCED if args.extract_figures else ImageRefMode.PLACEHOLDER
    doc.save_as_markdown(
        md_path,
        artifacts_dir=artifacts_dir if args.extract_figures else None,
        image_mode=image_mode,
        include_annotations=args.extract_figures and args.figure_label_mode != "none",
    )

    renamed_artifacts: list[Path] = []
    if args.extract_figures:
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        renamed_artifacts = _rename_docling_artifacts(md_path, artifacts_dir, label_prefix="figure")
        _extract_figures(doc, pdf_path, artifacts_dir, figures_json, renamed_artifacts)

    if args.extract_tables:
        _extract_tables(doc, tables_dir, tables_json, args.table_cleanup)

    return md_path


def main() -> int:
    args = _parse_args()
    if args.fast and (args.extract_figures or args.extract_tables):
        raise SystemExit("--fast cannot be combined with --extract-figures or --extract-tables.")

    _uv_bootstrap(args)

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    stem = pdf_path.stem
    docling_md = pdf_path.parent / f"{stem}.docling.md"
    fast_md = pdf_path.parent / f"{stem}.markitdown.md"
    fallback_txt = pdf_path.parent / f"{stem}.layout.txt"
    artifacts_dir = pdf_path.parent / f"{stem}.docling_artifacts"
    figures_json = pdf_path.parent / f"{stem}.figures.json" if args.extract_figures else None
    tables_dir = pdf_path.parent / f"{stem}.tables" if args.extract_tables else None
    tables_json = pdf_path.parent / f"{stem}.tables.json" if args.extract_tables else None

    read_artifact = fast_md if args.fast else docling_md
    sentinels = [read_artifact]
    if not args.fast and fallback_txt.exists() and not docling_md.exists():
        sentinels = [fallback_txt]
    if figures_json is not None:
        sentinels.append(figures_json)
    if tables_json is not None:
        sentinels.append(tables_json)

    engine = "markitdown" if args.fast else "docling"
    if not args.force and _is_fresh(pdf_path, sentinels):
        summary = _build_summary(
            pdf_path=pdf_path,
            read_artifact=sentinels[0],
            engine=engine,
            cached=True,
            figures_json=figures_json,
            tables_json=tables_json,
        )
        print(json.dumps(summary, indent=2))
        return 0

    if args.fast:
        read_artifact = _run_markitdown(pdf_path, fast_md)
    else:
        try:
            read_artifact = _run_docling(
                args=args,
                pdf_path=pdf_path,
                md_path=docling_md,
                artifacts_dir=artifacts_dir,
                figures_json=figures_json,
                tables_dir=tables_dir,
                tables_json=tables_json,
            )
        except Exception as exc:
            read_artifact = _run_pdftotext(pdf_path, fallback_txt)
            engine = "pdftotext-fallback"
            note = (
                "Degraded extraction quality: Docling failed, so this artifact was created with "
                "pdftotext -layout instead.\n\n"
            )
            read_artifact.write_text(note + read_artifact.read_text(encoding="utf-8"), encoding="utf-8")
            if figures_json is not None:
                _json_dump(figures_json, [])
            if tables_json is not None:
                _json_dump(tables_json, [])
            print(f"Docling failed, falling back to pdftotext: {exc}", file=sys.stderr)

    summary = _build_summary(
        pdf_path=pdf_path,
        read_artifact=read_artifact,
        engine=engine,
        cached=False,
        figures_json=figures_json,
        tables_json=tables_json,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
