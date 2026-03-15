#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

RUNTIME_SCRIPTS_DIR = Path(__file__).resolve().parents[3] / "skills" / "general" / "pdf-reading" / "scripts"
if str(RUNTIME_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SCRIPTS_DIR))

from table_agent import cell_text_to_latex, infer_regression_semantics


@dataclass
class SyntheticCellSpec:
    row_start: int
    row_end: int
    col_start: int
    col_end: int
    text: str
    role: str
    latex: str | None = None


@dataclass
class SyntheticRenderOptions:
    inner_env: str = "tabular"
    outer_env: str = "table"
    column_spec: str | None = None
    use_booktabs: bool = True
    use_threeparttable: bool = False
    use_resizebox: bool = False
    use_adjustbox: bool = False
    use_landscape: bool = False
    font_size: str | None = None
    header_rows: int = 1
    packages: list[str] = field(default_factory=list)
    preamble_lines: list[str] = field(default_factory=list)
    placement: str = "htbp"


@dataclass
class SyntheticCaseSpec:
    case_id: str
    title: str
    caption: str
    category: str
    description: str
    cells: list[SyntheticCellSpec]
    notes: list[str] = field(default_factory=list)
    qa: list[dict[str, str]] = field(default_factory=list)
    render: SyntheticRenderOptions = field(default_factory=SyntheticRenderOptions)
    source_description: str = "synthetic-latex"


def _json_dump(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _cell_id(row_start: int, col_start: int) -> str:
    return f"r{row_start}_c{col_start}"


def _column_spec(case: SyntheticCaseSpec, n_cols: int) -> str:
    if case.render.column_spec:
        return case.render.column_spec
    return "l" + ("c" * max(0, n_cols - 1))


def _column_tokens(column_spec: str) -> list[str]:
    return [char for char in column_spec if char in {"l", "c", "r", "S", "X"}]


def _grid_shape(cells: list[SyntheticCellSpec]) -> tuple[int, int]:
    n_rows = max(cell.row_end for cell in cells)
    n_cols = max(cell.col_end for cell in cells)
    return n_rows, n_cols


def _build_gold_cells(case: SyntheticCaseSpec) -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    for cell in sorted(case.cells, key=lambda item: (item.row_start, item.col_start, item.col_end)):
        if cell.latex is not None:
            latex = cell.latex
            latex_source = "synthetic"
            latex_confidence = 1.0
        else:
            latex, latex_source, latex_confidence = cell_text_to_latex(cell.text, role=cell.role)
        payload.append(
            {
                "cell_id": _cell_id(cell.row_start, cell.col_start),
                "row_start": cell.row_start,
                "row_end": cell.row_end,
                "col_start": cell.col_start,
                "col_end": cell.col_end,
                "bbox": None,
                "role": cell.role,
                "text_raw": cell.text,
                "text_normalized": cell.text,
                "latex": latex,
                "latex_source": latex_source,
                "latex_confidence": latex_confidence,
                "source": "synthetic",
                "confidence": 1.0,
                "needs_review": False,
                "provenance": [
                    {
                        "source": "synthetic",
                        "text_raw": cell.text,
                        "text_normalized": cell.text,
                        "confidence": 1.0,
                        "repair_actions": [],
                        "suspicious_markers": [],
                        "needs_review": False,
                    }
                ],
            }
        )
    return payload


def _render_tabular(case: SyntheticCaseSpec, cells: list[dict[str, Any]], n_rows: int, n_cols: int) -> str:
    origin_map = {(cell["row_start"], cell["col_start"]): cell for cell in cells}
    consumed: set[tuple[int, int]] = set()
    row_lines: list[str] = []
    column_spec = _column_spec(case, n_cols)
    column_tokens = _column_tokens(column_spec)

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
            alignment = "l" if col_idx == 0 else "c"
            content = cell["latex"]

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
            elif col_idx < len(column_tokens) and column_tokens[col_idx] == "S" and cell["role"] != "data":
                content = rf"\multicolumn{{1}}{{c}}{{{content}}}"

            parts.append(content)
            col_idx += col_span
        row_lines.append(" & ".join(parts) + r" \\")

    lines: list[str] = []
    if case.render.inner_env == "longtable":
        lines.append(rf"\begin{{longtable}}{{{column_spec}}}")
        lines.append(rf"\caption{{{case.caption}}}\\")
    elif case.render.inner_env == "tabularx":
        lines.append(rf"\begin{{tabularx}}{{\textwidth}}{{{column_spec}}}")
    else:
        lines.append(rf"\begin{{{case.render.inner_env}}}{{{column_spec}}}")

    if case.render.use_booktabs:
        lines.append(r"\toprule")
    else:
        lines.append(r"\hline")

    for row_idx, line in enumerate(row_lines, start=1):
        lines.append(line)
        if row_idx == case.render.header_rows:
            lines.append(r"\midrule" if case.render.use_booktabs else r"\hline")

    lines.append(r"\bottomrule" if case.render.use_booktabs else r"\hline")
    lines.append(rf"\end{{{case.render.inner_env}}}")
    return "\n".join(lines) + "\n"


def _render_notes(case: SyntheticCaseSpec) -> str | None:
    if not case.notes:
        return None
    lines = [r"\begin{tablenotes}[flushleft]"]
    for note in case.notes:
        lines.append(rf"\item {note}")
    lines.append(r"\end{tablenotes}")
    return "\n".join(lines) + "\n"


def _render_table_fragment(case: SyntheticCaseSpec, tabular: str, notes: str | None) -> str:
    if case.render.inner_env == "longtable":
        suffix = ""
        if notes:
            suffix = "\n" + r"\par\smallskip{\footnotesize " + " ".join(note for note in case.notes) + "}" + "\n"
        return tabular + suffix

    outer_env = case.render.outer_env
    lines = [rf"\begin{{{outer_env}}}[{case.render.placement}]"]
    if case.render.font_size:
        lines.append(rf"\{case.render.font_size}")
    lines.append(r"\centering")
    lines.append(rf"\caption{{{case.caption}}}")
    if case.render.use_threeparttable and notes:
        lines.append(r"\begin{threeparttable}")
    if case.render.use_resizebox:
        lines.append(r"\resizebox{\textwidth}{!}{%")
        lines.append(tabular.rstrip())
        lines.append(r"}")
    elif case.render.use_adjustbox:
        lines.append(r"\begin{adjustbox}{width=\textwidth}")
        lines.append(tabular.rstrip())
        lines.append(r"\end{adjustbox}")
    else:
        lines.append(tabular.rstrip())
    if case.render.use_threeparttable and notes:
        lines.append(notes.rstrip())
        lines.append(r"\end{threeparttable}")
    elif notes:
        lines.append(r"\par\smallskip")
        for note in case.notes:
            lines.append(rf"{{\footnotesize {note}}}")
    lines.append(rf"\end{{{outer_env}}}")
    return "\n".join(lines) + "\n"


def _required_packages(case: SyntheticCaseSpec) -> list[str]:
    packages = {
        "geometry": r"\usepackage[margin=1in]{geometry}",
        "booktabs": r"\usepackage{booktabs}",
        "multirow": r"\usepackage{multirow}",
        "threeparttable": r"\usepackage{threeparttable}",
        "graphicx": r"\usepackage{graphicx}",
        "adjustbox": r"\usepackage{adjustbox}",
        "rotating": r"\usepackage{rotating}",
        "pdflscape": r"\usepackage{pdflscape}",
        "tabularx": r"\usepackage{tabularx}",
        "longtable": r"\usepackage{longtable}",
        "siunitx": r"\usepackage{siunitx}",
        "amssymb": r"\usepackage{amssymb}",
        "array": r"\usepackage{array}",
    }

    needed = {"geometry"}
    if case.render.use_booktabs:
        needed.add("booktabs")
    if case.render.use_threeparttable:
        needed.add("threeparttable")
    if case.render.use_resizebox:
        needed.add("graphicx")
    if case.render.use_adjustbox:
        needed.add("adjustbox")
    if case.render.outer_env == "sidewaystable":
        needed.add("rotating")
    if case.render.use_landscape:
        needed.add("pdflscape")
    if case.render.inner_env == "tabularx":
        needed.add("tabularx")
    if case.render.inner_env == "longtable":
        needed.add("longtable")
    if any("S" in _column_spec(case, _grid_shape(case.cells)[1]) for _ in [0]):
        needed.add("siunitx")
    if any(cell.row_end - cell.row_start > 1 for cell in case.cells):
        needed.add("multirow")
    if any(cell.latex and r"\checkmark" in cell.latex for cell in case.cells):
        needed.add("amssymb")
    needed.update(case.render.packages)
    return [packages[name] for name in sorted(needed) if name in packages]


def _render_document(case: SyntheticCaseSpec, table_fragment: str) -> str:
    lines = [r"\documentclass{article}"]
    lines.extend(_required_packages(case))
    lines.append(r"\pagestyle{empty}")
    lines.extend(case.render.preamble_lines)
    lines.append(r"\begin{document}")
    if case.render.use_landscape:
        lines.append(r"\begin{landscape}")
    lines.append(table_fragment.rstrip())
    if case.render.use_landscape:
        lines.append(r"\end{landscape}")
    lines.append(r"\end{document}")
    return "\n".join(lines) + "\n"


def build_case_artifacts(case: SyntheticCaseSpec, source_pdf: str = "") -> dict[str, Any]:
    gold_cells = _build_gold_cells(case)
    n_rows, n_cols = _grid_shape(case.cells)
    semantics = infer_regression_semantics(gold_cells, n_rows, n_cols)
    notes = _render_notes(case)
    latex_tabular = _render_tabular(case, gold_cells, n_rows, n_cols)
    table_fragment = _render_table_fragment(case, latex_tabular, notes)

    agent_table = {
        "schema_version": "2026-03-15",
        "table_id": case.case_id,
        "source_pdf": source_pdf,
        "page": 1,
        "table_bbox": None,
        "crop_path": None,
        "title": case.caption,
        "notes": case.notes,
        "n_rows": n_rows,
        "n_cols": n_cols,
        "cells": gold_cells,
        "cleanup_report": {"verification_required": False, "reasons": []},
        "regression_semantics": semantics,
        "renderings": {
            "markdown": None,
            "html": None,
            "latex_tabular": latex_tabular,
            "latex_notes": notes,
        },
        "benchmark_metadata": {
            "case_id": case.case_id,
            "category": case.category,
            "description": case.description,
            "source_description": case.source_description,
        },
    }
    return {
        "agent_table": agent_table,
        "table_tex": table_fragment,
        "document_tex": _render_document(case, table_fragment),
        "qa": case.qa,
        "metadata": {
            "case_id": case.case_id,
            "title": case.title,
            "caption": case.caption,
            "category": case.category,
            "description": case.description,
            "source_description": case.source_description,
            "notes": case.notes,
            "render": asdict(case.render),
        },
    }


def _compile_latex(tex_path: Path, compiler: str) -> Path:
    if compiler == "tectonic":
        subprocess.run(["tectonic", "--outdir", str(tex_path.parent), str(tex_path)], check=True, capture_output=True, text=True)
    elif compiler == "latexmk":
        subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={tex_path.parent}", str(tex_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    else:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={tex_path.parent}", str(tex_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    return tex_path.with_suffix(".pdf")


def _render_pdf_preview(pdf_path: Path, output_png: Path) -> None:
    subprocess.run(
        ["pdftoppm", "-f", "1", "-l", "1", "-singlefile", "-png", str(pdf_path), str(output_png.with_suffix(""))],
        check=True,
        capture_output=True,
        text=True,
    )


def write_case(case: SyntheticCaseSpec, output_root: Path, compiler: str) -> dict[str, Any]:
    case_dir = output_root / case.case_id
    case_dir.mkdir(parents=True, exist_ok=True)

    artifacts = build_case_artifacts(case, source_pdf=str(case_dir / "source.pdf"))
    source_tex = case_dir / "source.tex"
    source_pdf = case_dir / "source.pdf"
    table_tex = case_dir / "table.tex"
    agent_json = case_dir / "agent_table.json"
    metadata_json = case_dir / "metadata.json"
    spec_json = case_dir / "spec.json"
    qa_json = case_dir / "qa.json"
    preview_png = case_dir / "crop.png"

    table_tex.write_text(artifacts["table_tex"], encoding="utf-8")
    source_tex.write_text(artifacts["document_tex"], encoding="utf-8")
    _json_dump(agent_json, artifacts["agent_table"])
    _json_dump(metadata_json, artifacts["metadata"])
    _json_dump(spec_json, asdict(case))
    _json_dump(qa_json, artifacts["qa"])

    compiled_pdf = _compile_latex(source_tex, compiler=compiler)
    if compiled_pdf != source_pdf and compiled_pdf.exists():
        shutil.move(str(compiled_pdf), str(source_pdf))
    _render_pdf_preview(source_pdf, preview_png)

    return {
        "case_id": case.case_id,
        "paper_title": case.title,
        "source_url": None,
        "table_label": case.caption,
        "page": 1,
        "files": {
            "pdf": str(source_pdf.relative_to(output_root.parent)),
            "crop": str(preview_png.relative_to(output_root.parent)),
            "gold_agent_table": str(agent_json.relative_to(output_root.parent)),
            "gold_latex": str(table_tex.relative_to(output_root.parent)),
            "qa": str(qa_json.relative_to(output_root.parent)),
            "source_tex": str(source_tex.relative_to(output_root.parent)),
            "metadata": str(metadata_json.relative_to(output_root.parent)),
        },
    }


def _regression_cells(
    model_labels: list[str],
    row_groups: list[tuple[str | None, list[tuple[str, list[str], list[str] | None]]]],
    *,
    include_controls: list[tuple[str, list[str]]] | None = None,
    include_summary: list[tuple[str, list[str]]] | None = None,
) -> list[SyntheticCellSpec]:
    cells: list[SyntheticCellSpec] = []
    n_models = len(model_labels)
    cells.append(SyntheticCellSpec(0, 1, 0, 1, "", "column_header"))
    cells.append(SyntheticCellSpec(0, 1, 1, n_models + 1, "Models", "column_header"))
    cells.append(SyntheticCellSpec(1, 2, 0, 1, "Variable", "column_header"))
    for index, label in enumerate(model_labels, start=1):
        cells.append(SyntheticCellSpec(1, 2, index, index + 1, label, "column_header"))

    row_idx = 2
    for panel_label, rows in row_groups:
        if panel_label:
            cells.append(SyntheticCellSpec(row_idx, row_idx + 1, 0, n_models + 1, panel_label, "row_section"))
            row_idx += 1
        for label, coeffs, stderrs in rows:
            cells.append(SyntheticCellSpec(row_idx, row_idx + 1, 0, 1, label, "stub"))
            for col_idx, value in enumerate(coeffs, start=1):
                cells.append(SyntheticCellSpec(row_idx, row_idx + 1, col_idx, col_idx + 1, value, "data"))
            row_idx += 1
            if stderrs:
                cells.append(SyntheticCellSpec(row_idx, row_idx + 1, 0, 1, "", "empty"))
                for col_idx, value in enumerate(stderrs, start=1):
                    cells.append(SyntheticCellSpec(row_idx, row_idx + 1, col_idx, col_idx + 1, value, "data"))
                row_idx += 1

    for label, values in include_controls or []:
        cells.append(SyntheticCellSpec(row_idx, row_idx + 1, 0, 1, label, "stub"))
        for col_idx, value in enumerate(values, start=1):
            latex = r"\checkmark" if value == "checkmark" else None
            text = "checkmark" if value == "checkmark" else value
            cells.append(SyntheticCellSpec(row_idx, row_idx + 1, col_idx, col_idx + 1, text, "data", latex=latex))
        row_idx += 1

    for label, values in include_summary or []:
        cells.append(SyntheticCellSpec(row_idx, row_idx + 1, 0, 1, label, "stub"))
        for col_idx, value in enumerate(values, start=1):
            cells.append(SyntheticCellSpec(row_idx, row_idx + 1, col_idx, col_idx + 1, value, "data"))
        row_idx += 1

    return cells


def build_default_cases() -> list[SyntheticCaseSpec]:
    cases: list[SyntheticCaseSpec] = []

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-regression-booktabs",
            title="Synthetic Regression Benchmark",
            caption="Table I: Baseline Regression Results",
            category="regression",
            description="Booktabs regression table with coefficient and standard-error rows plus controls and notes.",
            cells=_regression_cells(
                ["(1)", "(2)", "(3)", "(4)"],
                [
                    (
                        None,
                        [
                            ("Robot exposure", ["-0.123***", "-0.118***", "-0.090**", "-0.076*"], ["(0.045)", "(0.044)", "(0.038)", "(0.041)"]),
                            ("Manufacturing share", ["0.210***", "0.185***", "0.164***", "0.152***"], ["(0.052)", "(0.048)", "(0.046)", "(0.045)"]),
                        ],
                    )
                ],
                include_controls=[("County controls", ["No", "Yes", "Yes", "Yes"]), ("State-year FE", ["No", "No", "Yes", "Yes"])],
                include_summary=[("Observations", ["1000", "1000", "950", "950"]), ("R-squared", ["0.21", "0.27", "0.34", "0.39"])],
            ),
            notes=["Robust standard errors in parentheses.", "Significance: * p<0.10, ** p<0.05, *** p<0.01."],
            qa=[
                {"question": "What is the coefficient for Robot exposure in column (4)?", "answer": "-0.076*"},
                {"question": "Does column (3) include State-year FE?", "answer": "Yes"},
            ],
            render=SyntheticRenderOptions(use_booktabs=True, use_threeparttable=True, header_rows=2),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-regression-panels",
            title="Synthetic Panel Regression Benchmark",
            caption="Table II: Heterogeneity by Task Type",
            category="regression",
            description="Multi-panel regression table with separate panels and repeated coefficient/stderr structures.",
            cells=_regression_cells(
                ["(1)", "(2)", "(3)"],
                [
                    ("Panel A: Routine tasks", [("Robot exposure", ["-0.081**", "-0.075**", "-0.070*"], ["(0.032)", "(0.031)", "(0.036)"])]),
                    ("Panel B: Non-routine tasks", [("Robot exposure", ["0.012", "0.019", "0.021"], ["(0.021)", "(0.022)", "(0.020)"])]),
                ],
                include_summary=[("Observations", ["880", "880", "880"])],
            ),
            notes=["Panels split counties by routine task intensity."],
            qa=[
                {"question": "What is the sign of Robot exposure in Panel B, column (2)?", "answer": "Positive"},
                {"question": "What is the standard error for Panel A, column (1)?", "answer": "(0.032)"},
            ],
            render=SyntheticRenderOptions(use_booktabs=True, use_threeparttable=True, header_rows=2),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-summary-stats-siunitx",
            title="Synthetic Summary Statistics Benchmark",
            caption="Table III: Summary Statistics",
            category="summary-stats",
            description="Summary statistics table using siunitx-style numeric alignment.",
            cells=[
                SyntheticCellSpec(0, 1, 0, 1, "Variable", "column_header"),
                SyntheticCellSpec(0, 1, 1, 6, "Moments", "column_header"),
                SyntheticCellSpec(1, 2, 1, 2, "Mean", "column_header"),
                SyntheticCellSpec(1, 2, 2, 3, "SD", "column_header"),
                SyntheticCellSpec(1, 2, 3, 4, "P25", "column_header"),
                SyntheticCellSpec(1, 2, 4, 5, "P50", "column_header"),
                SyntheticCellSpec(1, 2, 5, 6, "P75", "column_header"),
                SyntheticCellSpec(2, 3, 0, 1, "Employment growth", "stub"),
                SyntheticCellSpec(2, 3, 1, 2, "0.014", "data"),
                SyntheticCellSpec(2, 3, 2, 3, "0.087", "data"),
                SyntheticCellSpec(2, 3, 3, 4, "-0.040", "data"),
                SyntheticCellSpec(2, 3, 4, 5, "0.011", "data"),
                SyntheticCellSpec(2, 3, 5, 6, "0.063", "data"),
                SyntheticCellSpec(3, 4, 0, 1, "Robot exposure", "stub"),
                SyntheticCellSpec(3, 4, 1, 2, "0.221", "data"),
                SyntheticCellSpec(3, 4, 2, 3, "0.109", "data"),
                SyntheticCellSpec(3, 4, 3, 4, "0.138", "data"),
                SyntheticCellSpec(3, 4, 4, 5, "0.216", "data"),
                SyntheticCellSpec(3, 4, 5, 6, "0.291", "data"),
            ],
            render=SyntheticRenderOptions(
                use_booktabs=True,
                header_rows=2,
                column_spec="lSSSSS",
                packages=["siunitx"],
                preamble_lines=[r"\sisetup{detect-all,table-number-alignment=center}"],
            ),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-wide-appendix-resizebox",
            title="Synthetic Wide Appendix Benchmark",
            caption="Appendix Table A1: Robustness Checks Across Sectors",
            category="appendix-wide",
            description="Wide table with twelve model columns wrapped in a resizebox.",
            cells=[
                SyntheticCellSpec(0, 1, 0, 1, "", "column_header"),
                SyntheticCellSpec(0, 1, 1, 7, "Manufacturing", "column_header"),
                SyntheticCellSpec(0, 1, 7, 13, "Services", "column_header"),
                SyntheticCellSpec(1, 2, 0, 1, "Specification", "column_header"),
                *[SyntheticCellSpec(1, 2, idx, idx + 1, f"({idx})", "column_header") for idx in range(1, 13)],
                SyntheticCellSpec(2, 3, 0, 1, "Robot exposure", "stub"),
                *[SyntheticCellSpec(2, 3, idx, idx + 1, value, "data") for idx, value in enumerate(
                    ["-0.11", "-0.10", "-0.08", "-0.07", "-0.06", "-0.05", "-0.02", "-0.01", "0.00", "0.01", "0.03", "0.04"],
                    start=1,
                )],
            ],
            render=SyntheticRenderOptions(use_booktabs=True, use_resizebox=True, header_rows=2, font_size="small"),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-multirow-headers",
            title="Synthetic Multirow Header Benchmark",
            caption="Table IV: Outcomes by Demographic Group",
            category="complex-headers",
            description="Table with multirow and multicolumn headers to stress header hierarchy reconstruction.",
            cells=[
                SyntheticCellSpec(0, 2, 0, 1, "Outcome", "column_header"),
                SyntheticCellSpec(0, 1, 1, 3, "Men", "column_header"),
                SyntheticCellSpec(0, 1, 3, 5, "Women", "column_header"),
                SyntheticCellSpec(1, 2, 1, 2, "Mean", "column_header"),
                SyntheticCellSpec(1, 2, 2, 3, "SD", "column_header"),
                SyntheticCellSpec(1, 2, 3, 4, "Mean", "column_header"),
                SyntheticCellSpec(1, 2, 4, 5, "SD", "column_header"),
                SyntheticCellSpec(2, 3, 0, 1, "Employment", "stub"),
                SyntheticCellSpec(2, 3, 1, 2, "0.82", "data"),
                SyntheticCellSpec(2, 3, 2, 3, "0.39", "data"),
                SyntheticCellSpec(2, 3, 3, 4, "0.74", "data"),
                SyntheticCellSpec(2, 3, 4, 5, "0.44", "data"),
            ],
            render=SyntheticRenderOptions(use_booktabs=True, header_rows=2),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-controls-checkmarks",
            title="Synthetic Controls Benchmark",
            caption="Table V: Incremental Controls",
            category="controls",
            description="Regression table with checkmarks, yes/no controls, and note-heavy footer.",
            cells=_regression_cells(
                ["(1)", "(2)", "(3)"],
                [(None, [("Automation intensity", ["-0.044", "-0.051*", "-0.060**"], ["(0.028)", "(0.027)", "(0.025)"])])],
                include_controls=[("Baseline controls", ["checkmark", "checkmark", "checkmark"]), ("Region trends", ["No", "Yes", "Yes"])],
                include_summary=[("Observations", ["720", "720", "720"])],
            ),
            notes=["Checkmarks indicate included control sets.", "All columns use population weights."],
            render=SyntheticRenderOptions(use_booktabs=True, use_threeparttable=True, header_rows=2, packages=["amssymb"]),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-math-headers",
            title="Synthetic Math Header Benchmark",
            caption="Table VI: Structural Parameter Estimates",
            category="math",
            description="Math-heavy headers and cells with explicit LaTeX overrides.",
            cells=[
                SyntheticCellSpec(0, 1, 0, 1, "Parameter", "column_header"),
                SyntheticCellSpec(0, 1, 1, 2, "Estimate", "column_header", latex=r"$\hat{\beta}$"),
                SyntheticCellSpec(0, 1, 2, 3, "SE", "column_header", latex=r"$\widehat{\mathrm{SE}}$"),
                SyntheticCellSpec(1, 2, 0, 1, "Labor elasticity", "stub", latex=r"$\epsilon_L$"),
                SyntheticCellSpec(1, 2, 1, 2, "0.83", "data", latex=r"$0.83$"),
                SyntheticCellSpec(1, 2, 2, 3, "(0.12)", "data", latex=r"$(0.12)$"),
                SyntheticCellSpec(2, 3, 0, 1, "Capital elasticity", "stub", latex=r"$\epsilon_K$"),
                SyntheticCellSpec(2, 3, 1, 2, "0.17", "data", latex=r"$0.17$"),
                SyntheticCellSpec(2, 3, 2, 3, "(0.08)", "data", latex=r"$(0.08)$"),
            ],
            notes=[r"Parameters satisfy $\epsilon_L + \epsilon_K = 1$ by construction."],
            render=SyntheticRenderOptions(use_booktabs=True, use_threeparttable=True, header_rows=1),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-tabularx-wrapped-stubs",
            title="Synthetic Wrapped Stub Benchmark",
            caption="Table VII: Survey Outcomes With Long Labels",
            category="wrapped-stubs",
            description="Tabularx case with long variable labels that should wrap inside the stub column.",
            cells=[
                SyntheticCellSpec(0, 1, 0, 1, "Outcome", "column_header"),
                SyntheticCellSpec(0, 1, 1, 2, "Control", "column_header"),
                SyntheticCellSpec(0, 1, 2, 3, "Treatment", "column_header"),
                SyntheticCellSpec(1, 2, 0, 1, "Share reporting that their main job tasks changed substantially after automation adoption", "stub"),
                SyntheticCellSpec(1, 2, 1, 2, "0.18", "data"),
                SyntheticCellSpec(1, 2, 2, 3, "0.31", "data"),
                SyntheticCellSpec(2, 3, 0, 1, "Share expecting training needs to increase over the next two years", "stub"),
                SyntheticCellSpec(2, 3, 1, 2, "0.42", "data"),
                SyntheticCellSpec(2, 3, 2, 3, "0.58", "data"),
            ],
            render=SyntheticRenderOptions(use_booktabs=True, inner_env="tabularx", column_spec="Xcc", header_rows=1, packages=["tabularx"]),
        )
    )

    longtable_rows = [
        SyntheticCellSpec(0, 1, 0, 1, "Variable", "column_header"),
        SyntheticCellSpec(0, 1, 1, 2, "Mean", "column_header"),
        SyntheticCellSpec(0, 1, 2, 3, "SD", "column_header"),
    ]
    for idx in range(1, 31):
        longtable_rows.extend(
            [
                SyntheticCellSpec(idx, idx + 1, 0, 1, f"Appendix variable {idx}", "stub"),
                SyntheticCellSpec(idx, idx + 1, 1, 2, f"{0.1 * idx:.2f}", "data"),
                SyntheticCellSpec(idx, idx + 1, 2, 3, f"{0.03 * idx:.2f}", "data"),
            ]
        )
    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-longtable-appendix",
            title="Synthetic Longtable Benchmark",
            caption="Appendix Table A2: Extended Variable Definitions",
            category="longtable",
            description="Longtable spanning many rows to test extraction beyond a short one-page table.",
            cells=longtable_rows,
            render=SyntheticRenderOptions(use_booktabs=True, inner_env="longtable", header_rows=1, packages=["longtable"]),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-sidewaystable",
            title="Synthetic Sideways Benchmark",
            caption="Table VIII: Sector-by-Sector Coefficients",
            category="landscape",
            description="Landscape sidewaystable with many columns.",
            cells=[
                SyntheticCellSpec(0, 1, 0, 1, "Sector", "column_header"),
                *[SyntheticCellSpec(0, 1, idx, idx + 1, f"({idx})", "column_header") for idx in range(1, 11)],
                SyntheticCellSpec(1, 2, 0, 1, "Robot exposure", "stub"),
                *[SyntheticCellSpec(1, 2, idx, idx + 1, value, "data") for idx, value in enumerate(
                    ["-0.11", "-0.09", "-0.07", "-0.05", "-0.03", "-0.01", "0.00", "0.02", "0.03", "0.05"],
                    start=1,
                )],
                SyntheticCellSpec(2, 3, 0, 1, "Standard error", "stub"),
                *[SyntheticCellSpec(2, 3, idx, idx + 1, value, "data") for idx, value in enumerate(
                    ["(0.04)", "(0.04)", "(0.03)", "(0.03)", "(0.02)", "(0.02)", "(0.02)", "(0.02)", "(0.03)", "(0.03)"],
                    start=1,
                )],
            ],
            render=SyntheticRenderOptions(use_booktabs=True, outer_env="sidewaystable", header_rows=1, packages=["rotating"], font_size="small"),
        )
    )

    cases.append(
        SyntheticCaseSpec(
            case_id="synthetic-vertical-rules",
            title="Synthetic Vertical Rules Benchmark",
            caption="Table IX: Non-Booktabs Formatting",
            category="formatting-variant",
            description="Classic tabular with vertical rules and hlines instead of booktabs.",
            cells=[
                SyntheticCellSpec(0, 1, 0, 1, "Item", "column_header"),
                SyntheticCellSpec(0, 1, 1, 2, "A", "column_header"),
                SyntheticCellSpec(0, 1, 2, 3, "B", "column_header"),
                SyntheticCellSpec(1, 2, 0, 1, "Count", "stub"),
                SyntheticCellSpec(1, 2, 1, 2, "12", "data"),
                SyntheticCellSpec(1, 2, 2, 3, "18", "data"),
                SyntheticCellSpec(2, 3, 0, 1, "Share", "stub"),
                SyntheticCellSpec(2, 3, 1, 2, "40%", "data"),
                SyntheticCellSpec(2, 3, 2, 3, "60%", "data"),
            ],
            render=SyntheticRenderOptions(use_booktabs=False, header_rows=1, column_spec="|l|c|c|"),
        )
    )

    return cases


def _default_output_root() -> Path:
    return Path(__file__).resolve().parents[1] / "benchmarks" / "cases"


def _default_manifest_path() -> Path:
    return Path(__file__).resolve().parents[1] / "benchmarks" / "manifest.synthetic.json"


def _select_compiler() -> str:
    if shutil.which("tectonic"):
        return "tectonic"
    if shutil.which("latexmk"):
        return "latexmk"
    if shutil.which("pdflatex"):
        return "pdflatex"
    raise SystemExit("No LaTeX compiler found. Install tectonic, latexmk, or pdflatex.")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic LaTeX table benchmarks and compile them to PDFs.")
    parser.add_argument("--output-root", default=str(_default_output_root()), help="Directory to write case folders into.")
    parser.add_argument("--manifest", default=str(_default_manifest_path()), help="Path to write the synthetic manifest.")
    parser.add_argument("--compiler", choices=("tectonic", "latexmk", "pdflatex", "auto"), default="auto")
    parser.add_argument("--case-id", action="append", help="Optional specific case id to generate. Can be passed multiple times.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    compiler = _select_compiler() if args.compiler == "auto" else args.compiler

    cases = build_default_cases()
    if args.case_id:
        selected = set(args.case_id)
        cases = [case for case in cases if case.case_id in selected]
        missing = selected - {case.case_id for case in cases}
        if missing:
            raise SystemExit(f"Unknown case ids: {', '.join(sorted(missing))}")

    manifest = [write_case(case, output_root=output_root, compiler=compiler) for case in cases]
    _json_dump(manifest_path, manifest)
    print(json.dumps({"output_root": str(output_root), "manifest": str(manifest_path), "case_count": len(manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
