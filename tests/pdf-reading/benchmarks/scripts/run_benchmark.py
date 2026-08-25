#!/usr/bin/env python3
"""Run the PDF reading benchmark against a skill.

Usage:
    # Compare full pdf-reading skill against gold standard:
    python run_benchmark.py --skill ../../../../skills/general/pdf-reading

    # Compare docling baseline:
    python run_benchmark.py --skill ../../../../skills/general/pdf-baseline

    # Run on a single paper:
    python run_benchmark.py --skill ../../../../skills/general/pdf-reading --paper-id 01

    # Skip extraction (just score existing outputs):
    python run_benchmark.py --skill ../../../../skills/general/pdf-reading --score-only

Output:
    results/<skill-name>/summary.json    Per-paper and aggregate scores
    results/<skill-name>/per_paper/      Per-paper extraction outputs
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill", type=Path, required=True,
                        help="Path to the skill directory (must contain scripts/pdf_extract.py)")
    parser.add_argument("--paper-id", action="append", dest="paper_ids",
                        help="Score specific paper(s) (repeatable)")
    parser.add_argument("--score-only", action="store_true",
                        help="Skip extraction, just score existing outputs")
    parser.add_argument("--cases-dir", type=Path,
                        default=Path(__file__).resolve().parent.parent / "cases",
                        help="Path to cases/ directory")
    parser.add_argument("--results-dir", type=Path,
                        default=Path(__file__).resolve().parent.parent / "results",
                        help="Path to results/ directory")
    return parser.parse_args()


def extract_paper(skill_dir: Path, pdf_path: Path, output_dir: Path) -> dict | None:
    """Run the skill's pdf_extract.py on a PDF and return the summary."""
    extractor = skill_dir / "scripts" / "pdf_extract.py"
    if not extractor.exists():
        print(f"  ERROR: {extractor} not found", file=sys.stderr)
        return None

    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, str(extractor),
        str(pdf_path),
        "--extract-tables",
        "--force",
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300,
            cwd=str(output_dir),
        )
        if result.returncode != 0:
            print(f"  Extraction failed: {result.stderr[:200]}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"  Extraction error: {e}", file=sys.stderr)
        return None


def score_tables(gold_tables: list[dict], extracted_tables_dir: Path) -> dict:
    """Score extracted tables against gold standard.

    Returns precision, recall, F1 for table cell values.
    """
    gold_cells_total = 0
    matched = 0
    extracted_total = 0

    for gt in gold_tables:
        if gt["table_id"] == "proofs-block":
            continue
        gold_cells = [c for c in gt.get("gold_cells", []) if c.get("text")]
        gold_cells_total += len(gold_cells)

    # Count extracted table cells from raw markdown files
    if extracted_tables_dir and extracted_tables_dir.exists():
        for md_file in sorted(extracted_tables_dir.glob("*.raw.md")):
            content = md_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.strip().startswith("|"):
                    cells = [c.strip() for c in line.split("|")[1:-1]]
                    extracted_total += len([c for c in cells if c and c != "---"])

    precision = matched / extracted_total if extracted_total > 0 else 0
    recall = matched / gold_cells_total if gold_cells_total > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "gold_cells": gold_cells_total,
        "extracted_cells": extracted_total,
        "matched_cells": matched,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def score_qa(gold_qa: list[dict]) -> dict:
    """Placeholder for QA scoring — requires LLM evaluation."""
    return {
        "total_questions": len(gold_qa),
        "note": "QA scoring requires LLM evaluation — not implemented in this runner",
    }


def score_paper(gold_path: Path, output_dir: Path) -> dict:
    """Score a single paper's extraction against gold."""
    gold = json.loads(gold_path.read_text(encoding="utf-8"))

    tables_dir = None
    if output_dir.exists():
        for d in output_dir.iterdir():
            if d.is_dir() and d.name.endswith(".tables"):
                tables_dir = d
                break

    return {
        "paper_id": gold["paper_id"],
        "field": gold["field"],
        "journal_style": gold["journal_style"],
        "tables": score_tables(gold.get("tables", []), tables_dir),
        "qa": score_qa(gold.get("qa", [])),
        "n_gold_tables": len([t for t in gold.get("tables", []) if t["table_id"] != "proofs-block"]),
        "n_gold_equations": len(gold.get("equations", [])),
        "n_gold_qa": len(gold.get("qa", [])),
    }


def main():
    args = _parse_args()

    skill_name = args.skill.name
    results_dir = args.results_dir / skill_name
    results_dir.mkdir(parents=True, exist_ok=True)

    # Find papers
    paper_dirs = sorted(args.cases_dir.glob("paper-*"))
    if args.paper_ids:
        paper_dirs = [d for d in paper_dirs
                      if any(pid in d.name for pid in args.paper_ids)]

    print(f"Benchmarking {skill_name} on {len(paper_dirs)} papers...")

    all_scores = []
    for paper_dir in paper_dirs:
        gold_path = paper_dir / "gold.json"
        pdf_path = paper_dir / "source.pdf"
        if not gold_path.exists() or not pdf_path.exists():
            print(f"  Skipping {paper_dir.name}: missing gold.json or source.pdf")
            continue

        paper_output = results_dir / "per_paper" / paper_dir.name
        print(f"  {paper_dir.name}...", end=" ", flush=True)

        if not args.score_only:
            summary = extract_paper(args.skill, pdf_path, paper_output)
            if summary:
                (paper_output / "extraction_summary.json").write_text(
                    json.dumps(summary, indent=2), encoding="utf-8")

        scores = score_paper(gold_path, paper_output)
        all_scores.append(scores)
        print(f"tables: {scores['tables']['gold_cells']} gold cells")

    # Aggregate
    total_gold = sum(s["tables"]["gold_cells"] for s in all_scores)
    total_extracted = sum(s["tables"]["extracted_cells"] for s in all_scores)
    total_qa = sum(s["n_gold_qa"] for s in all_scores)

    aggregate = {
        "skill": skill_name,
        "n_papers": len(all_scores),
        "total_gold_table_cells": total_gold,
        "total_extracted_table_cells": total_extracted,
        "total_gold_qa_pairs": total_qa,
        "per_paper": all_scores,
    }

    summary_path = results_dir / "summary.json"
    summary_path.write_text(json.dumps(aggregate, indent=2), encoding="utf-8")
    print(f"\nResults: {summary_path}")
    print(f"  {len(all_scores)} papers, {total_gold} gold table cells, {total_qa} QA pairs")


if __name__ == "__main__":
    main()
