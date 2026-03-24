# PDF Reading Benchmarks

Two benchmark suites for evaluating PDF extraction quality.

---

## Long-form economics papers (20 papers)

Twenty synthetic full-length economics papers (50-86 pages each) with cell-level
gold standard data. Generated deterministically from Python — the LaTeX source
IS the ground truth.

### Quick start

Regenerate all papers:

```bash
cd tests/pdf-reading/benchmarks/scripts
python3 generate_long_form.py
```

Run the benchmark against a skill:

```bash
python3 run_benchmark.py --skill ../../../../skills/general/pdf-reading
python3 run_benchmark.py --skill ../../../../skills/general/pdf-baseline
```

### What's in each paper

| File | Contents |
|------|----------|
| `source.tex` | LaTeX source |
| `source.pdf` | Compiled PDF |
| `gold.json` | Metadata + sections + tables (cell-level) + equations + QA pairs |

### Variation across papers

**14 document formats** — 8 journal styles (AER, Econometrica, QJE, JPE, REStud,
JF, RFS, JFE) plus 6 non-journal formats (working paper, typewriter, NBER WP,
Word-like, two-column, old-school). Different fonts, spacing, margins, section
numbering.

**20 table styles** — Each paper uses a distinct table formatting convention
reflecting real-world software: Stata esttab, Stata outreg2, R stargazer,
R modelsummary, Python statsmodels, SAS, Excel-style, etc. Variations include
booktabs vs hline rules, parentheses vs brackets around standard errors, stars
on coefficients vs SEs vs none, and different note formats.

**Complex math notation** — Equations include hats, bars, tildes, dots over
variables; integrals and summations with complex bounds; matrix notation;
partial derivatives; calligraphic and blackboard bold letters; nested
sub/superscripts; convergence arrows; and floor/ceiling brackets.

### Benchmark comparison

The `pdf-baseline` skill variant in `skills/general/pdf-baseline/` strips the
table post-processing pipeline (table_agent, table_cleanup) from the full
`pdf-reading` skill. Run both against the benchmark to measure the value added
by post-processing.

### Scoring

The benchmark runner (`run_benchmark.py`) compares extracted tables against
`gold.json` cell data. QA scoring requires LLM evaluation and is not automated
in the runner.

---

## Synthetic table benchmarks

Store gold cases here for regression-first table extraction evaluation.

### Synthetic generation

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
