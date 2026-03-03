# QMD Setup For Python Learning Memory

Use this guide to make the skill memory searchable for any user.

## Recommended Python Runner (`uv`)

Use `uv` so the memory helper script runs consistently:

```bash
uv venv
source .venv/bin/activate
uv run python3 scripts/python_learning_memory.py doctor
```

## Install

```bash
bun install -g https://github.com/tobi/qmd
qmd status
```

If `qmd status` fails, fix installation before continuing.
If needed, run:

```bash
uv run python3 scripts/python_learning_memory.py qmd-check
```
This command checks both `uv` and QMD, then prints guided next steps.

## Index Memory Files

1. Keep memory under this skill folder:
- `references/memory/profile.md`
- `references/memory/daily/*.md`
2. Ensure the parent directory of this skill is included in QMD indexing.
3. Run index refresh after each tutoring session:

```bash
qmd update
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
