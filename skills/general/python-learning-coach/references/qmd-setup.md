# QMD Setup For Python Learning Memory

Use this guide to make the skill memory searchable for any user.

## Recommended Python Runner (`uv`)

Use `uv` so the memory helper script runs consistently:

```bash
if ! command -v uv >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install uv
  elif command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  else
    echo "Install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
  fi
fi

python3 scripts/python_learning_memory.py doctor
```

## Install

```bash
if ! command -v qmd >/dev/null 2>&1; then
  if command -v bun >/dev/null 2>&1; then
    bun install -g @tobilu/qmd
  elif command -v npm >/dev/null 2>&1; then
    npm install -g @tobilu/qmd
  else
    echo "Install Bun or npm first, then install qmd from https://github.com/tobi/qmd"
  fi
fi

qmd status || echo "QMD unavailable; continue with file-based memory only."
```

QMD is optional. If `qmd status` fails, continue with local files.
If needed, run:

```bash
python3 scripts/python_learning_memory.py qmd-check
```
This command checks both `uv` and QMD, then prints guided next steps.

## Index Memory Files

1. Keep memory under this skill folder:
- `references/memory/profile.md`
- `references/memory/daily/*.md`
2. Ensure the parent directory of this skill is included in QMD indexing.
3. Run index refresh after each tutoring session:

```bash
if command -v qmd >/dev/null 2>&1 && qmd status >/dev/null 2>&1; then
  qmd update
fi
```

## Retrieval Commands

Use keyword retrieval:

```bash
qmd search "python learner strengths and gaps" -n 8
```

Use higher-quality hybrid retrieval:

```bash
qmd query "recent python mistakes and next learning goals" -n 8
```

Retrieve full memory documents when needed:

```bash
qmd get "skills/general/python-learning-coach/references/memory/profile.md" --full
```

## Fallback Without QMD

If QMD is unavailable, inspect memory directly:

```bash
cat references/memory/profile.md
ls -1 references/memory/daily | tail -n 5
```
