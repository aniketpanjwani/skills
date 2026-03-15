#!/usr/bin/env python3

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from table_cleanup import CellTextCleanupReport, TableCleanupReport, normalize_cell_text

SUMMARY_ROW_PATTERNS = (
    r"^observations?$",
    r"^r[\s-]?squared$",
    r"^adjusted r[\s-]?squared$",
    r"^mean dependent var",
    r"^std\.? dev",
    r"^fixed effects$",
)

CONTROL_VALUE_PATTERN = re.compile(r"^(yes|no|y|n|x|checkmark|included|excluded|\u2713)$", flags=re.IGNORECASE)
NUMERIC_PATTERN = re.compile(r"^[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:%|\*{1,3})?$")
STDERR_PATTERN = re.compile(r"^\(([+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:\*{1,3})?)\)$")
NUMERIC_WITH_STARS_PATTERN = re.compile(r"^([+-]?(?:\d+(?:\.\d+)?|\.\d+))(?:\s*)(\*{1,3})$")
PAREN_NUMERIC_WITH_STARS_PATTERN = re.compile(r"^\(([+-]?(?:\d+(?:\.\d+)?|\.\d+))(?:\s*)(\*{1,3})?\)$")
LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def _json_ready(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        try:
            return value.model_dump(mode="json")
        except TypeError:
            return value.model_dump()
    if hasattr(value, "value"):
        return value.value
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def bbox_to_dict(bbox: Any) -> dict[str, Any] | None:
    if bbox is None:
        return None
    payload = _json_ready(bbox)
    if not isinstance(payload, dict):
        return None
    origin = payload.get("coord_origin")
    if hasattr(origin, "value"):
        origin = origin.value
    if origin is not None:
        payload["coord_origin"] = str(origin)
    return payload


def to_top_left_bbox(bbox: Any, page_height: float | None = None) -> dict[str, Any] | None:
    payload = bbox_to_dict(bbox)
    if payload is None:
        return None
    origin = payload.get("coord_origin")
    if origin == "BOTTOMLEFT":
        if page_height is None:
            return payload
        payload = {
            "l": payload["l"],
            "t": page_height - payload["t"],
            "r": payload["r"],
            "b": page_height - payload["b"],
            "coord_origin": "TOPLEFT",
        }
    return payload


def _cell_id(row_start: int, col_start: int) -> str:
    return f"r{row_start}_c{col_start}"


def _row_key(cell: dict[str, Any]) -> tuple[int, int, int]:
    return (cell["row_start"], cell["col_start"], cell["col_end"])


def _text_issue_score(text: str) -> int:
    score = 0
    if re.search(r"/periodori|\(cid:4\)|\x04", text):
        score += 4
    if re.search(r"[\x00-\x08\x0b-\x1f\x7f]", text):
        score += 4
    if re.search(r"\b[A-Za-z]{20,}\b", text):
        score += 2
    if not text.strip():
        score += 3
    return score


def _estimate_confidence(source: str, report: CellTextCleanupReport, text: str) -> float:
    base = {"docling": 0.84, "pdfplumber": 0.91, "ocr": 0.78}.get(source, 0.8)
    base -= 0.05 * len(report.repairs)
    base -= 0.1 * len(report.suspicious_markers)
    base -= 0.04 * _text_issue_score(text)
    if NUMERIC_PATTERN.match(text) or STDERR_PATTERN.match(text):
        base += 0.04
    if not text.strip():
        base -= 0.3
    return round(max(0.0, min(0.99, base)), 3)


def _build_candidate(text_raw: str | None, source: str, report: CellTextCleanupReport) -> dict[str, Any]:
    return {
        "source": source,
        "text_raw": text_raw or "",
        "text_normalized": report.normalized_text,
        "confidence": _estimate_confidence(source, report, report.normalized_text),
        "repair_actions": list(report.repairs),
        "suspicious_markers": list(report.suspicious_markers),
        "needs_review": report.needs_review,
    }


def _prefer_candidate(current: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    if candidate is None:
        return current
    if current is None:
        return candidate
    if not candidate["text_normalized"] and current["text_normalized"]:
        return current
    if candidate["text_normalized"] == current["text_normalized"]:
        return candidate if candidate["confidence"] > current["confidence"] else current
    if not current["text_normalized"] and candidate["text_normalized"]:
        return candidate
    if current["needs_review"] and not candidate["needs_review"]:
        return candidate
    if _text_issue_score(candidate["text_normalized"]) + 1 < _text_issue_score(current["text_normalized"]):
        return candidate
    if candidate["confidence"] > current["confidence"] + 0.1:
        return candidate
    return current


def _extract_pdfplumber_text(page: Any, bbox: dict[str, Any]) -> str | None:
    try:
        cropped = page.crop((bbox["l"], bbox["t"], bbox["r"], bbox["b"]))
        text = cropped.extract_text(x_tolerance=1, y_tolerance=3, layout=False)
    except Exception:
        return None
    if not text:
        return None
    return re.sub(r"\s*\n\s*", " ", text).strip()


def _cell_crop_from_table_image(
    table_image: Any,
    table_bbox: dict[str, Any] | None,
    cell_bbox: dict[str, Any] | None,
) -> tuple[int, int, int, int] | None:
    if table_image is None or table_bbox is None or cell_bbox is None:
        return None
    table_width = max(1.0, table_bbox["r"] - table_bbox["l"])
    table_height = max(1.0, table_bbox["b"] - table_bbox["t"])
    scale_x = table_image.size[0] / table_width
    scale_y = table_image.size[1] / table_height
    left = max(0, int((cell_bbox["l"] - table_bbox["l"]) * scale_x) - 2)
    top = max(0, int((cell_bbox["t"] - table_bbox["t"]) * scale_y) - 2)
    right = min(table_image.size[0], int((cell_bbox["r"] - table_bbox["l"]) * scale_x) + 2)
    bottom = min(table_image.size[1], int((cell_bbox["b"] - table_bbox["t"]) * scale_y) + 2)
    if left >= right or top >= bottom:
        return None
    return left, top, right, bottom


def _extract_ocr_text(
    table_image: Any,
    table_bbox: dict[str, Any] | None,
    cell_bbox: dict[str, Any] | None,
) -> str | None:
    tesseract = shutil.which("tesseract")
    crop_box = _cell_crop_from_table_image(table_image, table_bbox, cell_bbox)
    if tesseract is None or crop_box is None:
        return None
    cell_image = table_image.crop(crop_box)
    if cell_image.size[0] < 8 or cell_image.size[1] < 8:
        return None
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
        temp_path = Path(handle.name)
    try:
        cell_image.save(temp_path)
        result = subprocess.run(
            [tesseract, str(temp_path), "stdout", "--psm", "6", "-l", "eng"],
            capture_output=True,
            check=False,
            text=True,
        )
        text = re.sub(r"\s*\n\s*", " ", result.stdout).strip()
        return text or None
    finally:
        temp_path.unlink(missing_ok=True)


def _cell_role(cell: Any, normalized_text: str) -> str:
    if getattr(cell, "column_header", False):
        return "column_header"
    if getattr(cell, "row_section", False):
        return "row_section"
    if getattr(cell, "row_header", False):
        return "row_header"
    if not normalized_text:
        return "empty"
    if getattr(cell, "start_col_offset_idx", 0) == 0:
        return "stub"
    return "data"


def _escape_latex_text(text: str) -> str:
    return "".join(LATEX_SPECIALS.get(char, char) for char in text)


def cell_text_to_latex(text: str, role: str = "data") -> tuple[str, str, float]:
    normalized = text.strip()
    if not normalized:
        return "", "deterministic", 0.99
    if normalized.lower() == "checkmark":
        return r"\checkmark", "deterministic", 0.98
    if CONTROL_VALUE_PATTERN.match(normalized) and normalized.lower() != "checkmark":
        return _escape_latex_text(normalized), "deterministic", 0.98

    numeric_match = NUMERIC_WITH_STARS_PATTERN.match(normalized)
    if numeric_match:
        value, stars = numeric_match.groups()
        return f"${value}^{{{stars}}}$", "deterministic", 0.99

    paren_match = PAREN_NUMERIC_WITH_STARS_PATTERN.match(normalized)
    if paren_match:
        value, stars = paren_match.groups()
        if stars:
            return f"$({value}^{{{stars}}})$", "deterministic", 0.99
        return f"({value})", "deterministic", 0.99

    if role in {"column_header", "row_header", "row_section", "stub"}:
        return _escape_latex_text(normalized), "deterministic", 0.97

    return _escape_latex_text(normalized), "deterministic", 0.96


def _extract_text_from_ref(item: Any) -> str | None:
    if item is None:
        return None
    if isinstance(item, str):
        return item.strip() or None
    if isinstance(item, dict):
        text = item.get("text")
        return text.strip() if isinstance(text, str) and text.strip() else None
    text = getattr(item, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()
    return None


def _extract_notes(table: Any, doc: Any) -> tuple[str | None, list[str]]:
    title = None
    try:
        title = table.caption_text(doc) or None
    except Exception:
        title = None

    notes: list[str] = []
    for item in getattr(table, "footnotes", []) or []:
        text = _extract_text_from_ref(item)
        if text and text not in notes:
            notes.append(text)
    return title, notes


def _grid_shape(table: Any) -> tuple[int, int]:
    max_row = 0
    max_col = 0
    for cell in getattr(table.data, "table_cells", []):
        max_row = max(max_row, int(cell.end_row_offset_idx))
        max_col = max(max_col, int(cell.end_col_offset_idx))
    return max_row, max_col


def _row_covering_cells(cells: list[dict[str, Any]], row_idx: int) -> list[dict[str, Any]]:
    return [cell for cell in cells if cell["row_start"] <= row_idx < cell["row_end"]]


def _cell_covering(cells: list[dict[str, Any]], row_idx: int, col_idx: int) -> dict[str, Any] | None:
    for cell in cells:
        if cell["row_start"] <= row_idx < cell["row_end"] and cell["col_start"] <= col_idx < cell["col_end"]:
            return cell
    return None


def _first_stub_label(cells: list[dict[str, Any]], row_idx: int) -> str:
    row_cells = sorted(_row_covering_cells(cells, row_idx), key=_row_key)
    for cell in row_cells:
        if cell["role"] in {"stub", "row_header", "row_section"} and cell["text_normalized"]:
            return cell["text_normalized"]
    return ""


def _row_data_cells(cells: list[dict[str, Any]], row_idx: int) -> list[dict[str, Any]]:
    return [cell for cell in _row_covering_cells(cells, row_idx) if cell["role"] == "data"]


def _header_paths(cells: list[dict[str, Any]], n_rows: int, n_cols: int) -> dict[int, list[str]]:
    paths: dict[int, list[str]] = {}
    for col_idx in range(n_cols):
        labels: list[str] = []
        for row_idx in range(n_rows):
            cell = _cell_covering(cells, row_idx, col_idx)
            if cell is None or cell["role"] != "column_header":
                continue
            text = cell["text_normalized"]
            if text and (not labels or labels[-1] != text):
                labels.append(text)
        if labels:
            paths[col_idx] = labels
    return paths


def infer_regression_semantics(cells: list[dict[str, Any]], n_rows: int, n_cols: int) -> dict[str, Any]:
    header_paths = _header_paths(cells, n_rows, n_cols)
    models: list[dict[str, Any]] = []
    for col_idx in range(1, n_cols):
        labels = header_paths.get(col_idx, [])
        models.append(
            {
                "column_index": col_idx,
                "header_path": labels,
                "label": " / ".join(labels) if labels else f"Column {col_idx}",
            }
        )

    summary_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    coefficient_rows: list[dict[str, Any]] = []
    stderr_rows: list[dict[str, Any]] = []
    coefficient_cells: list[dict[str, Any]] = []

    for row_idx in range(n_rows):
        label = _first_stub_label(cells, row_idx)
        data_cells = _row_data_cells(cells, row_idx)
        values = [cell["text_normalized"] for cell in data_cells if cell["text_normalized"]]

        if label and any(re.match(pattern, label, flags=re.IGNORECASE) for pattern in SUMMARY_ROW_PATTERNS):
            summary_rows.append({"row_index": row_idx, "label": label})

        if label and values and sum(1 for value in values if CONTROL_VALUE_PATTERN.match(value)) >= max(1, len(values) // 2):
            control_rows.append({"row_index": row_idx, "label": label})

        if not label or not values:
            continue

        numeric_cells = [cell for cell in data_cells if NUMERIC_PATTERN.match(cell["text_normalized"])]
        if not numeric_cells:
            continue

        next_row = row_idx + 1
        if next_row >= n_rows:
            continue
        next_label = _first_stub_label(cells, next_row)
        next_data_cells = _row_data_cells(cells, next_row)
        stderr_like = [cell for cell in next_data_cells if STDERR_PATTERN.match(cell["text_normalized"])]
        if next_label:
            continue
        if not stderr_like:
            continue

        coefficient_rows.append({"row_index": row_idx, "label": label})
        stderr_rows.append({"row_index": next_row, "paired_with_row": row_idx})
        stderr_by_col = {cell["col_start"]: cell for cell in stderr_like}
        for cell in numeric_cells:
            stderr_cell = stderr_by_col.get(cell["col_start"])
            coefficient_cells.append(
                {
                    "variable_label": label,
                    "column_index": cell["col_start"],
                    "model_label": " / ".join(header_paths.get(cell["col_start"], [])) or f"Column {cell['col_start']}",
                    "coefficient_cell_id": cell["cell_id"],
                    "stderr_cell_id": stderr_cell["cell_id"] if stderr_cell else None,
                    "coefficient": cell["text_normalized"],
                    "stderr": stderr_cell["text_normalized"] if stderr_cell else None,
                }
            )

    return {
        "models": models,
        "coefficient_rows": coefficient_rows,
        "stderr_rows": stderr_rows,
        "summary_rows": summary_rows,
        "control_rows": control_rows,
        "coefficient_cells": coefficient_cells,
    }


def render_latex_tabular(cells: list[dict[str, Any]], n_rows: int, n_cols: int) -> str:
    origin_map = {(cell["row_start"], cell["col_start"]): cell for cell in cells}
    consumed: set[tuple[int, int]] = set()
    row_lines: list[str] = []

    for row_idx in range(n_rows):
        parts: list[str] = []
        col_idx = 0
        while col_idx < n_cols:
            if (row_idx, col_idx) in consumed:
                col_idx += 1
                continue
            cell = origin_map.get((row_idx, col_idx))
            if cell is None:
                parts.append("")
                col_idx += 1
                continue

            row_span = max(1, cell["row_end"] - cell["row_start"])
            col_span = max(1, cell["col_end"] - cell["col_start"])
            content = cell["latex"]
            alignment = "l" if col_idx == 0 else "c"

            for covered_row in range(cell["row_start"], cell["row_end"]):
                for covered_col in range(cell["col_start"], cell["col_end"]):
                    if covered_row == row_idx and covered_col == col_idx:
                        continue
                    consumed.add((covered_row, covered_col))

            if row_span > 1 and col_span > 1:
                content = rf"\multirow{{{row_span}}}{{*}}{{\multicolumn{{{col_span}}}{{{alignment}}}{{{content}}}}}"
            elif row_span > 1:
                content = rf"\multirow{{{row_span}}}{{*}}{{{content}}}"
            elif col_span > 1:
                content = rf"\multicolumn{{{col_span}}}{{{alignment}}}{{{content}}}"

            parts.append(content)
            col_idx += col_span

        row_lines.append(" & ".join(parts) + r" \\")

    alignment = "l" + ("c" * max(0, n_cols - 1))
    lines = [rf"\begin{{tabular}}{{{alignment}}}", r"\hline"]
    lines.extend(row_lines)
    lines.extend([r"\hline", r"\end{tabular}"])
    return "\n".join(lines) + "\n"


def render_latex_notes(notes: list[str]) -> str | None:
    if not notes:
        return None
    lines = [r"\begin{tablenotes}[flushleft]"]
    for note in notes:
        lines.append(rf"\item {_escape_latex_text(note)}")
    lines.append(r"\end{tablenotes}")
    return "\n".join(lines)


def render_full_latex_table(title: str | None, tabular: str, latex_notes: str | None) -> str:
    lines = [r"\begin{table}[htbp]", r"\centering"]
    if title:
        lines.append(rf"\caption{{{_escape_latex_text(title)}}}")
    if latex_notes:
        lines.append(r"\begin{threeparttable}")
    lines.append(tabular.rstrip())
    if latex_notes:
        lines.append(latex_notes.rstrip())
        lines.append(r"\end{threeparttable}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


def build_agent_table(
    *,
    table: Any,
    doc: Any,
    pdf_path: Path,
    table_index: int,
    raw_markdown: str,
    cleaned_markdown: str,
    cleaned_report: TableCleanupReport,
    html: str | None,
    otsl: str | None,
    crop_path: Path | None,
    table_image: Any,
    plumber_pdf: Any | None,
) -> tuple[dict[str, Any], str]:
    page_no = None
    page = None
    page_height = None
    if getattr(table, "prov", None):
        page_no = getattr(table.prov[0], "page_no", None)
    if plumber_pdf is not None and page_no is not None and 1 <= page_no <= len(plumber_pdf.pages):
        page = plumber_pdf.pages[page_no - 1]
        page_height = page.height

    table_bbox = None
    if getattr(table, "prov", None):
        table_bbox = to_top_left_bbox(table.prov[0].bbox, page_height=page_height)

    title, notes = _extract_notes(table, doc)
    n_rows, n_cols = _grid_shape(table)
    cells: list[dict[str, Any]] = []

    for cell in sorted(getattr(table.data, "table_cells", []), key=lambda item: (item.start_row_offset_idx, item.start_col_offset_idx)):
        raw_text = getattr(cell, "text", "") or ""
        normalized_text, base_report = normalize_cell_text(raw_text)
        best_candidate = _build_candidate(raw_text, "docling", base_report)
        provenance = [best_candidate]
        cell_bbox = to_top_left_bbox(getattr(cell, "bbox", None), page_height=page_height)

        if page is not None and cell_bbox is not None:
            pdfplumber_raw = _extract_pdfplumber_text(page, cell_bbox)
            if pdfplumber_raw:
                pdfplumber_text, pdfplumber_report = normalize_cell_text(pdfplumber_raw)
                pdfplumber_candidate = _build_candidate(pdfplumber_raw, "pdfplumber", pdfplumber_report)
                provenance.append(pdfplumber_candidate)
                preferred = _prefer_candidate(best_candidate, pdfplumber_candidate)
                if preferred is not None:
                    best_candidate = preferred

        if best_candidate["needs_review"] and table_image is not None and cell_bbox is not None:
            ocr_raw = _extract_ocr_text(table_image, table_bbox, cell_bbox)
            if ocr_raw:
                _, ocr_report = normalize_cell_text(ocr_raw)
                ocr_candidate = _build_candidate(ocr_raw, "ocr", ocr_report)
                provenance.append(ocr_candidate)
                preferred = _prefer_candidate(best_candidate, ocr_candidate)
                if preferred is not None:
                    best_candidate = preferred

        role = _cell_role(cell, best_candidate["text_normalized"])
        latex, latex_source, latex_confidence = cell_text_to_latex(best_candidate["text_normalized"], role=role)
        cell_entry = {
            "cell_id": _cell_id(int(cell.start_row_offset_idx), int(cell.start_col_offset_idx)),
            "row_start": int(cell.start_row_offset_idx),
            "row_end": int(cell.end_row_offset_idx),
            "col_start": int(cell.start_col_offset_idx),
            "col_end": int(cell.end_col_offset_idx),
            "bbox": cell_bbox,
            "role": role,
            "text_raw": best_candidate["text_raw"],
            "text_normalized": best_candidate["text_normalized"],
            "latex": latex,
            "latex_source": latex_source,
            "latex_confidence": latex_confidence,
            "source": best_candidate["source"],
            "confidence": best_candidate["confidence"],
            "needs_review": best_candidate["needs_review"],
            "provenance": provenance,
        }
        cells.append(cell_entry)

    semantics = infer_regression_semantics(cells, n_rows, n_cols)
    latex_tabular = render_latex_tabular(cells, n_rows, n_cols)
    latex_notes = render_latex_notes(notes)
    full_latex = render_full_latex_table(title, latex_tabular, latex_notes)

    agent_table = {
        "schema_version": "2026-03-15",
        "table_id": f"table_{table_index:03d}",
        "source_pdf": str(pdf_path),
        "page": page_no,
        "table_bbox": table_bbox,
        "crop_path": str(crop_path) if crop_path is not None else None,
        "title": title,
        "notes": notes,
        "n_rows": n_rows,
        "n_cols": n_cols,
        "cells": cells,
        "cleanup_report": {
            "verification_required": cleaned_report.verification_required,
            "reasons": list(cleaned_report.reasons),
        },
        "regression_semantics": semantics,
        "renderings": {
            "markdown": cleaned_markdown,
            "html": html,
            "latex_tabular": latex_tabular,
            "latex_notes": latex_notes,
        },
    }
    return agent_table, full_latex
