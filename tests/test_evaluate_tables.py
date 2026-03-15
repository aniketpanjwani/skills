from __future__ import annotations

from evaluate_tables import compare_agent_tables


def test_compare_agent_tables_scores_exact_match() -> None:
    table = {
        "table_id": "table_001",
        "cells": [
            {
                "cell_id": "r0_c0",
                "row_start": 0,
                "row_end": 1,
                "col_start": 0,
                "col_end": 1,
                "role": "stub",
                "text_normalized": "Observations",
                "latex": "Observations",
                "needs_review": False,
            },
            {
                "cell_id": "r0_c1",
                "row_start": 0,
                "row_end": 1,
                "col_start": 1,
                "col_end": 2,
                "role": "data",
                "text_normalized": "1000",
                "latex": "1000",
                "needs_review": False,
            },
        ],
        "regression_semantics": {
            "coefficient_cells": [],
            "summary_rows": [{"row_index": 0, "label": "Observations"}],
        },
    }
    metrics = compare_agent_tables(table, table)
    assert metrics["structure_accuracy"] == 1.0
    assert metrics["cell_text_exact_accuracy"] == 1.0
    assert metrics["summary_row_accuracy"] == 1.0
    assert metrics["near_perfect_gate"] is True
