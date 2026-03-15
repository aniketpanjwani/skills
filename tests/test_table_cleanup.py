from __future__ import annotations

from table_cleanup import clean_table_markdown, normalize_cell_text


def test_normalize_cell_text_repairs_decimal_markers() -> None:
    normalized, report = normalize_cell_text("1 /periodori 23")
    assert normalized == "1.23"
    assert "repaired_decimal_markers" in report.repairs
    assert report.needs_review is False


def test_normalize_cell_text_flags_merged_tokens() -> None:
    normalized, report = normalize_cell_text("ThisCellHasAReallyReallyLongMergedToken")
    assert normalized == "ThisCellHasAReallyReallyLongMergedToken"
    assert report.needs_review is True
    assert "merged_token" in report.suspicious_markers


def test_clean_table_markdown_repairs_misplaced_signs() -> None:
    raw = "\n".join(
        [
            "| Variable | (1) |",
            "|---|---|",
            "| Robots | 0.123 |",
            "|  | - (0.045) |",
        ]
    )
    cleaned, report = clean_table_markdown(raw)
    assert "| Robots | -0.123 |" in cleaned
    assert "|  | (0.045) |" in cleaned
    assert report.repaired_misplaced_signs == 1
