#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluate_tables import compare_agent_tables

SCRIPT_DIR = Path(__file__).resolve().parent
PDF_READING_TEST_DIR = SCRIPT_DIR.parent
BENCHMARKS_DIR = PDF_READING_TEST_DIR / "benchmarks"
REPO_ROOT = SCRIPT_DIR.parents[2]
EXTRACTOR_SCRIPT = REPO_ROOT / "skills" / "general" / "pdf-reading" / "scripts" / "pdf_extract.py"
DEFAULT_MANIFEST = BENCHMARKS_DIR / "manifest.synthetic.json"
DEFAULT_RESULTS_DIR = BENCHMARKS_DIR / "results" / "current"
METRIC_KEYS = (
    "structure_accuracy",
    "role_accuracy",
    "cell_text_exact_accuracy",
    "cell_text_normalized_accuracy",
    "numeric_cell_accuracy",
    "latex_exact_accuracy",
    "coefficient_pair_accuracy",
    "summary_row_accuracy",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_json_tail(output: str) -> dict[str, Any]:
    stripped = output.strip()
    if not stripped:
        raise ValueError("No output captured from extractor.")
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    for line_index, line in enumerate(stripped.splitlines()):
        candidate = "\n".join(stripped.splitlines()[line_index:]).strip()
        if not candidate.startswith("{"):
            continue
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ValueError(f"No JSON object found in output:\n{output}")


def _run_extractor(pdf_path: Path) -> dict[str, Any]:
    cmd = [sys.executable, str(EXTRACTOR_SCRIPT), str(pdf_path), "--extract-tables", "--force"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return _parse_json_tail(result.stdout)


def _evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    pdf_path = BENCHMARKS_DIR / case["files"]["pdf"]
    gold_agent_path = BENCHMARKS_DIR / case["files"]["gold_agent_table"]
    gold_latex_path = BENCHMARKS_DIR / case["files"]["gold_latex"]
    metadata_path = BENCHMARKS_DIR / case["files"]["metadata"]

    extraction_summary = _run_extractor(pdf_path)
    tables_manifest = _load_json(Path(extraction_summary["tables_manifest"]))
    if not tables_manifest:
        raise RuntimeError(f"No extracted tables found for {case['case_id']}")

    predicted_agent_path = Path(tables_manifest[0]["agent_table_path"])
    predicted_latex_path = Path(tables_manifest[0]["latex_path"])
    predicted_agent = _load_json(predicted_agent_path)
    gold_agent = _load_json(gold_agent_path)
    metrics = compare_agent_tables(predicted_agent, gold_agent)

    predicted_latex = predicted_latex_path.read_text(encoding="utf-8")
    gold_latex = gold_latex_path.read_text(encoding="utf-8")
    metrics["latex_file_exact_match"] = predicted_latex == gold_latex
    metrics["latex_file_normalized_match"] = " ".join(predicted_latex.split()) == " ".join(gold_latex.split())

    metadata = _load_json(metadata_path)
    metrics.update(
        {
            "case_id": case["case_id"],
            "category": metadata["category"],
            "pdf_path": str(pdf_path),
            "predicted_agent_table": str(predicted_agent_path),
            "gold_agent_table": str(gold_agent_path),
            "predicted_latex": str(predicted_latex_path),
            "gold_latex": str(gold_latex_path),
            "extractor_summary": extraction_summary,
        }
    )
    return metrics


def _aggregate_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    successful = [result for result in results if "error" not in result]
    aggregate: dict[str, Any] = {
        "case_count": len(results),
        "success_count": len(successful),
        "failure_count": len(results) - len(successful),
        "near_perfect_pass_count": sum(1 for result in successful if result.get("near_perfect_gate")),
        "near_perfect_pass_rate": round(
            sum(1 for result in successful if result.get("near_perfect_gate")) / len(successful), 4
        )
        if successful
        else 0.0,
    }
    for key in METRIC_KEYS:
        values = [result[key] for result in successful]
        aggregate[f"avg_{key}"] = round(statistics.mean(values), 4) if values else 0.0
    aggregate["avg_unresolved_false_negatives"] = round(
        statistics.mean(result["unresolved_false_negatives"] for result in successful), 4
    ) if successful else 0.0
    return aggregate


def _render_markdown_report(manifest_path: Path, aggregate: dict[str, Any], results: list[dict[str, Any]]) -> str:
    lines = [
        "# Current Benchmark Results",
        "",
        f"- Generated at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Manifest: `{manifest_path}`",
        f"- Cases run: `{aggregate['case_count']}`",
        f"- Near-perfect passes: `{aggregate['near_perfect_pass_count']}`",
        f"- Near-perfect pass rate: `{aggregate['near_perfect_pass_rate']}`",
        "",
        "## Aggregate",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in aggregate.items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Per Case",
            "",
            "| Case | Category | Structure | Text (norm) | Numeric | LaTeX | Coeff pairs | Near perfect |",
            "|---|---|---:|---:|---:|---:|---:|---|",
        ]
    )

    for result in sorted(results, key=lambda item: item["case_id"]):
        if "error" in result:
            lines.append(f"| {result['case_id']} | error | - | - | - | - | - | error |")
            continue
        lines.append(
            "| {case_id} | {category} | {structure_accuracy:.4f} | {cell_text_normalized_accuracy:.4f} | "
            "{numeric_cell_accuracy:.4f} | {latex_exact_accuracy:.4f} | {coefficient_pair_accuracy:.4f} | {near_perfect_gate} |".format(
                **result
            )
        )

    failures = [result for result in results if "error" in result]
    if failures:
        lines.extend(["", "## Failures", ""])
        for failure in failures:
            lines.append(f"- `{failure['case_id']}`: {failure['error']}")

    return "\n".join(lines) + "\n"


def _write_results(results_dir: Path, manifest_path: Path, aggregate: dict[str, Any], results: list[dict[str, Any]]) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    per_case_dir = results_dir / "per_case"
    per_case_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(manifest_path),
        "aggregate": aggregate,
        "results": results,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (results_dir / "summary.md").write_text(_render_markdown_report(manifest_path, aggregate, results), encoding="utf-8")

    for result in results:
        case_id = result["case_id"]
        (per_case_dir / f"{case_id}.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run extraction benchmarks and write current results.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Benchmark manifest to execute.")
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR), help="Directory to write benchmark results into.")
    parser.add_argument("--case-id", action="append", help="Optional case id filter. Can be passed multiple times.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    results_dir = Path(args.results_dir).expanduser().resolve()

    manifest = _load_json(manifest_path)
    if args.case_id:
        selected = set(args.case_id)
        manifest = [case for case in manifest if case["case_id"] in selected]

    results: list[dict[str, Any]] = []
    for case in manifest:
        try:
            results.append(_evaluate_case(case))
        except Exception as exc:
            results.append({"case_id": case["case_id"], "error": str(exc)})

    aggregate = _aggregate_results(results)
    _write_results(results_dir, manifest_path, aggregate, results)
    print(json.dumps({"results_dir": str(results_dir), "case_count": len(results), "aggregate": aggregate}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
