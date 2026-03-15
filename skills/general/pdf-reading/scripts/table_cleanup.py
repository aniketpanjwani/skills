#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class TableCleanupReport:
    repaired_decimal_markers: int = 0
    repaired_checkmarks: int = 0
    repaired_misplaced_signs: int = 0
    tightened_numeric_spacing: int = 0
    suspicious_merged_tokens: int = 0
    max_line_length: int = 0
    max_pipe_count: int = 0
    verification_required: bool = False
    reasons: list[str] = field(default_factory=list)


@dataclass
class CellTextCleanupReport:
    original_text: str
    normalized_text: str
    repaired_decimal_markers: int = 0
    repaired_checkmarks: int = 0
    tightened_numeric_spacing: int = 0
    repairs: list[str] = field(default_factory=list)
    suspicious_markers: list[str] = field(default_factory=list)
    needs_review: bool = False
    confidence: float = 1.0


def _subn(pattern: str, repl: str, text: str, count_attr: str, report: TableCleanupReport) -> str:
    updated, count = re.subn(pattern, repl, text)
    setattr(report, count_attr, getattr(report, count_attr) + count)
    return updated


def _subn_cell(pattern: str, repl: str, text: str, count_attr: str, report: CellTextCleanupReport) -> str:
    updated, count = re.subn(pattern, repl, text)
    setattr(report, count_attr, getattr(report, count_attr) + count)
    return updated


def _append_reason(report: TableCleanupReport, reason: str) -> None:
    if reason not in report.reasons:
        report.reasons.append(reason)


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _repair_misplaced_signs(text: str, report: TableCleanupReport) -> str:
    lines = text.splitlines()
    for index in range(1, len(lines)):
        prev_line = lines[index - 1]
        curr_line = lines[index]
        if not prev_line.lstrip().startswith("|") or not curr_line.lstrip().startswith("|"):
            continue

        prev_cells = prev_line.split("|")
        curr_cells = curr_line.split("|")
        if len(prev_cells) != len(curr_cells):
            continue

        updated = False
        for cell_index in range(2, len(prev_cells) - 1):
            prev_cell = prev_cells[cell_index]
            curr_cell = curr_cells[cell_index]
            if not re.match(r"^\s*\d", prev_cell):
                continue
            if not re.match(r"^\s*-\s*\(", curr_cell):
                continue

            leading = re.match(r"^(\s*)", prev_cell).group(1)
            prev_cells[cell_index] = f"{leading}-{prev_cell[len(leading):].lstrip()}"
            curr_cells[cell_index] = re.sub(r"^(\s*)-\s*", r"\1", curr_cell, count=1)
            report.repaired_misplaced_signs += 1
            updated = True

        if updated:
            lines[index - 1] = "|".join(prev_cells)
            lines[index] = "|".join(curr_cells)

    return "\n".join(lines)


def normalize_cell_text(text: str | None) -> tuple[str, CellTextCleanupReport]:
    original = (text or "").replace("\u00a0", " ")
    report = CellTextCleanupReport(original_text=original, normalized_text=original)
    cleaned = original.replace("\u2212", "-")

    decimal_patterns = (
        r"(?<=\d)\s*/periodori\s*(?=\d)",
        r"(?<=\()\s*/periodori\s*(?=\d)",
        r"(?<=\d)\s*\(cid:4\)\s*(?=\d)",
        r"(?<=\()\s*\(cid:4\)\s*(?=\d)",
        r"(?<=\d)\s*\x04\s*(?=\d)",
        r"(?<=\()\s*\x04\s*(?=\d)",
    )
    for pattern in decimal_patterns:
        cleaned = _subn_cell(pattern, ".", cleaned, "repaired_decimal_markers", report)

    cleaned = _subn_cell(r"\s*/check\b", " checkmark", cleaned, "repaired_checkmarks", report)

    spacing_patterns = (
        (r"(?<!\w)-\s+(?=\d)", "-"),
        (r"\(\s+(?=[-0-9])", "("),
        (r"(?<=\d)\s+\)", ")"),
        (r"(?<=\d)\s*\.\s*(?=\d)", "."),
        (r"\s+", " "),
    )
    for pattern, repl in spacing_patterns:
        cleaned = _subn_cell(pattern, repl, cleaned, "tightened_numeric_spacing", report)

    cleaned = cleaned.strip()

    if report.repaired_decimal_markers:
        _append_unique(report.repairs, "repaired_decimal_markers")
    if report.repaired_checkmarks:
        _append_unique(report.repairs, "repaired_checkmarks")
    if report.tightened_numeric_spacing:
        _append_unique(report.repairs, "tightened_numeric_spacing")

    if re.search(r"/periodori|\(cid:4\)|\x04", cleaned):
        _append_unique(report.suspicious_markers, "corrupted_decimal_marker")
    if re.search(r"[\x00-\x08\x0b-\x1f\x7f]", cleaned):
        _append_unique(report.suspicious_markers, "control_character")
    if re.search(r"\b[A-Za-z]{20,}\b", cleaned):
        _append_unique(report.suspicious_markers, "merged_token")
    if re.search(r"(?<!\w)-\s+\(", cleaned):
        _append_unique(report.suspicious_markers, "misplaced_sign")

    report.needs_review = bool(report.suspicious_markers)
    confidence = 0.98
    confidence -= 0.05 * len(report.repairs)
    confidence -= 0.12 * len(report.suspicious_markers)
    if not cleaned:
        confidence -= 0.3
    report.confidence = round(max(0.0, min(0.99, confidence)), 3)
    report.normalized_text = cleaned
    return cleaned, report


def clean_table_markdown(text: str) -> tuple[str, TableCleanupReport]:
    report = TableCleanupReport()
    cleaned = text.replace("\u2212", "-")

    decimal_patterns = (
        r"(?<=\d)\s*/periodori\s*(?=\d)",
        r"(?<=\()\s*/periodori\s*(?=\d)",
        r"(?<=\d)\s*\(cid:4\)\s*(?=\d)",
        r"(?<=\()\s*\(cid:4\)\s*(?=\d)",
        r"(?<=\d)\s*\x04\s*(?=\d)",
        r"(?<=\()\s*\x04\s*(?=\d)",
    )
    for pattern in decimal_patterns:
        cleaned = _subn(pattern, ".", cleaned, "repaired_decimal_markers", report)

    cleaned = _subn(r"\s*/check\b", " checkmark", cleaned, "repaired_checkmarks", report)

    spacing_patterns = (
        (r"(?<!\w)-\s+(?=\d)", "-"),
        (r"\(\s+(?=[-0-9])", "("),
        (r"(?<=\d)\s+\)", ")"),
        (r"(?<=\d)\s*\.\s*(?=\d)", "."),
    )
    for pattern, repl in spacing_patterns:
        cleaned = _subn(pattern, repl, cleaned, "tightened_numeric_spacing", report)

    cleaned = _repair_misplaced_signs(cleaned, report)

    merged_tokens = re.findall(r"\b[A-Za-z]{20,}\b", cleaned)
    report.suspicious_merged_tokens = len(merged_tokens)
    report.max_line_length = max((len(line) for line in cleaned.splitlines()), default=0)
    report.max_pipe_count = max((line.count("|") for line in cleaned.splitlines()), default=0)

    if report.repaired_decimal_markers >= 4:
        _append_reason(report, "repaired many corrupted decimal markers")
    if report.repaired_checkmarks > 0:
        _append_reason(report, "repaired checkmark placeholders")
    if report.repaired_misplaced_signs > 0:
        _append_reason(report, "repaired misplaced negative signs")
    if report.max_line_length > 240:
        _append_reason(report, "contains very wide rows")
    if report.max_pipe_count > 6:
        _append_reason(report, "contains many columns")
    if re.search(r"\bPANEL\s+[A-Z]\b", cleaned):
        _append_reason(report, "contains multi-panel headers")
    if report.suspicious_merged_tokens > 0:
        _append_reason(report, "contains merged-text artifacts")
    if re.search(r"\b2SLS\b|\bR-squared\b|\bObservations\b", cleaned, flags=re.IGNORECASE):
        _append_reason(report, "looks like a dense academic regression table")

    report.verification_required = bool(report.reasons)
    return cleaned, report


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Docling table markdown for readability.")
    parser.add_argument("input", help="Path to the raw table markdown file.")
    parser.add_argument("-o", "--output", help="Path to write the cleaned markdown.")
    parser.add_argument("--report", help="Optional JSON report output path.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    input_path = Path(args.input).expanduser().resolve()
    text = input_path.read_text(encoding="utf-8")
    cleaned, report = clean_table_markdown(text)

    if args.output:
        Path(args.output).expanduser().resolve().write_text(cleaned, encoding="utf-8")
    else:
        print(cleaned)

    if args.report:
        Path(args.report).expanduser().resolve().write_text(
            json.dumps(asdict(report), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
