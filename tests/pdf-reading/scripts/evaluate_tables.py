#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def _normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip().lower()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index_cells(table: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {cell["cell_id"]: cell for cell in table.get("cells", [])}


def _safe_ratio(matches: int, total: int) -> float:
    if total <= 0:
        return 1.0
    return round(matches / total, 4)


def compare_agent_tables(predicted: dict[str, Any], gold: dict[str, Any]) -> dict[str, Any]:
    predicted_cells = _index_cells(predicted)
    gold_cells = _index_cells(gold)
    all_cell_ids = sorted(set(predicted_cells) | set(gold_cells))

    structure_matches = 0
    role_matches = 0
    exact_text_matches = 0
    normalized_text_matches = 0
    numeric_matches = 0
    numeric_total = 0
    latex_exact_matches = 0
    unresolved_false_negatives = 0

    for cell_id in all_cell_ids:
        predicted_cell = predicted_cells.get(cell_id)
        gold_cell = gold_cells.get(cell_id)
        if predicted_cell is None or gold_cell is None:
            continue

        if (
            predicted_cell.get("row_start") == gold_cell.get("row_start")
            and predicted_cell.get("row_end") == gold_cell.get("row_end")
            and predicted_cell.get("col_start") == gold_cell.get("col_start")
            and predicted_cell.get("col_end") == gold_cell.get("col_end")
        ):
            structure_matches += 1
        if predicted_cell.get("role") == gold_cell.get("role"):
            role_matches += 1
        if predicted_cell.get("text_normalized") == gold_cell.get("text_normalized"):
            exact_text_matches += 1
        if _normalize_text(predicted_cell.get("text_normalized")) == _normalize_text(gold_cell.get("text_normalized")):
            normalized_text_matches += 1
        if predicted_cell.get("latex") == gold_cell.get("latex"):
            latex_exact_matches += 1

        gold_text = gold_cell.get("text_normalized", "")
        if re.fullmatch(r"[()+\-.\d%*]+", gold_text):
            numeric_total += 1
            if _normalize_text(predicted_cell.get("text_normalized")) == _normalize_text(gold_text):
                numeric_matches += 1
            elif not predicted_cell.get("needs_review", False):
                unresolved_false_negatives += 1

    gold_semantics = gold.get("regression_semantics", {})
    predicted_semantics = predicted.get("regression_semantics", {})

    coefficient_total = len(gold_semantics.get("coefficient_cells", []))
    predicted_coefficients = {
        (
            item.get("variable_label"),
            item.get("column_index"),
            item.get("coefficient"),
            item.get("stderr"),
        )
        for item in predicted_semantics.get("coefficient_cells", [])
    }
    gold_coefficients = {
        (
            item.get("variable_label"),
            item.get("column_index"),
            item.get("coefficient"),
            item.get("stderr"),
        )
        for item in gold_semantics.get("coefficient_cells", [])
    }
    coefficient_matches = len(predicted_coefficients & gold_coefficients)

    summary_rows_pred = {(item.get("row_index"), item.get("label")) for item in predicted_semantics.get("summary_rows", [])}
    summary_rows_gold = {(item.get("row_index"), item.get("label")) for item in gold_semantics.get("summary_rows", [])}
    summary_matches = len(summary_rows_pred & summary_rows_gold)

    table_metrics = {
        "table_id": gold.get("table_id") or predicted.get("table_id"),
        "cell_count": len(all_cell_ids),
        "structure_accuracy": _safe_ratio(structure_matches, len(gold_cells)),
        "role_accuracy": _safe_ratio(role_matches, len(gold_cells)),
        "cell_text_exact_accuracy": _safe_ratio(exact_text_matches, len(gold_cells)),
        "cell_text_normalized_accuracy": _safe_ratio(normalized_text_matches, len(gold_cells)),
        "numeric_cell_accuracy": _safe_ratio(numeric_matches, numeric_total),
        "latex_exact_accuracy": _safe_ratio(latex_exact_matches, len(gold_cells)),
        "coefficient_pair_accuracy": _safe_ratio(coefficient_matches, coefficient_total),
        "summary_row_accuracy": _safe_ratio(summary_matches, len(summary_rows_gold)),
        "unresolved_false_negatives": unresolved_false_negatives,
    }
    table_metrics["near_perfect_gate"] = (
        table_metrics["numeric_cell_accuracy"] >= 0.98
        and table_metrics["structure_accuracy"] >= 0.95
        and table_metrics["coefficient_pair_accuracy"] >= 0.95
        and unresolved_false_negatives == 0
    )
    return table_metrics


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare predicted agent_table.json against gold fixtures.")
    parser.add_argument("predicted", help="Path to the predicted agent_table.json file.")
    parser.add_argument("gold", help="Path to the gold agent_table.json file.")
    parser.add_argument("--gold-latex", help="Optional gold table.tex path.")
    parser.add_argument("--predicted-latex", help="Optional predicted table.tex path.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    predicted = _load_json(Path(args.predicted).expanduser().resolve())
    gold = _load_json(Path(args.gold).expanduser().resolve())
    metrics = compare_agent_tables(predicted, gold)

    if args.gold_latex and args.predicted_latex:
        predicted_latex = Path(args.predicted_latex).expanduser().resolve().read_text(encoding="utf-8")
        gold_latex = Path(args.gold_latex).expanduser().resolve().read_text(encoding="utf-8")
        metrics["latex_file_exact_match"] = predicted_latex == gold_latex
        metrics["latex_file_normalized_match"] = _normalize_text(predicted_latex) == _normalize_text(gold_latex)

    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
