# Table Benchmarks

Store gold cases here for regression-first table extraction evaluation.

## Synthetic generation

You can generate a local synthetic benchmark corpus directly from built-in LaTeX table specs:

```bash
python3 tests/pdf-reading/scripts/synthetic_benchmarks.py
```

This writes:

- `tests/pdf-reading/benchmarks/cases/<case_id>/source.tex`
- `tests/pdf-reading/benchmarks/cases/<case_id>/source.pdf`
- `tests/pdf-reading/benchmarks/cases/<case_id>/crop.png`
- `tests/pdf-reading/benchmarks/cases/<case_id>/agent_table.json`
- `tests/pdf-reading/benchmarks/cases/<case_id>/table.tex`
- `tests/pdf-reading/benchmarks/cases/<case_id>/qa.json`
- `tests/pdf-reading/benchmarks/cases/<case_id>/metadata.json`
- `tests/pdf-reading/benchmarks/manifest.synthetic.json`

The built-in synthetic corpus covers multiple LaTeX styles and structures, including:

- booktabs regression tables
- multi-panel regression tables
- siunitx summary-stat tables
- wide resizebox appendix tables
- multirow and multicolumn headers
- control rows with checkmarks
- math-heavy cells and headers
- tabularx wrapped stubs
- longtable appendix layouts
- sidewaystable landscape layouts
- classic vertical-rule tables

## Recommended layout

Each case should live in its own folder:

```text
tests/pdf-reading/benchmarks/
  manifest.example.json
  cases/
    autor-levy-murnane-table-i/
      metadata.json
      source.pdf
      crop.png
      agent_table.json
      table.tex
      qa.json
```

## Minimum gold artifacts per case

- `metadata.json`: case id, source citation, page number, and table label
- `crop.png`: reference crop used for human verification
- `agent_table.json`: gold cell/span schema for the table
- `table.tex`: canonical LaTeX rendering for the gold table
- `qa.json`: 3-5 downstream QA prompts with exact answers

## Suggested case mix

- clean born-digital regression table
- corrupted text-layer regression table
- multi-panel table
- notes-heavy table
- summary-statistics table
- wide appendix table
- scanned or OCR-degraded case

## Evaluation

Use the evaluator to compare a predicted `agent_table.json` against a gold case:

```bash
python3 tests/pdf-reading/scripts/evaluate_tables.py \
  /path/to/predicted.agent.json \
  tests/pdf-reading/benchmarks/cases/example/agent_table.json \
  --predicted-latex /path/to/predicted.tex \
  --gold-latex tests/pdf-reading/benchmarks/cases/example/table.tex
```

To run the current synthetic benchmark suite end to end and write a report into a stable repo location:

```bash
python3 tests/pdf-reading/scripts/run_benchmarks.py
```

This writes:

- `tests/pdf-reading/benchmarks/results/current/summary.md`
- `tests/pdf-reading/benchmarks/results/current/summary.json`
- `tests/pdf-reading/benchmarks/results/current/per_case/<case_id>.json`

## Real-world runs

For non-gold smoke tests against public PDFs, store runs under:

```text
tests/pdf-reading/benchmarks/
  runs/
    real-world/
      <paper-slug>/
        <run-id>/
          source_ref.json
          extract.stdout.json
          time.txt
          run.json
          run.md
          source.docling.md
          source.tables.json
          source.tables/
            table_001.agent.json
            table_001.cleaned.md
            table_001.tex
            ...
```

Commit-friendly policy:

- do commit `source_ref.json`, `extract.stdout.json`, `time.txt`, `run.json`, `run.md`, `source.docling.md`, `source.tables.json`, and extracted table artifacts
- do not commit the downloaded PDF itself; `tests/pdf-reading/benchmarks/runs/.gitignore` ignores PDFs by default

Recommended `source_ref.json` fields:

- `source_url`
- `paper_title`
- `downloaded_at`
- `sha256`
- `license_notes`

Recommended `run.json` fields:

- `run_id`
- `benchmark_kind`
- `paper_slug`
- `paper_title`
- `source_ref`
- `commit_hash`
- `run_started_at`
- `run_finished_at`
- `elapsed_seconds`
- `engine`
- `table_count`
- `notes`
