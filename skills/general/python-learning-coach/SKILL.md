---
name: python-learning-coach
description: Personalized Python tutoring with persistent memory, daily Q/A logs, and dynamic level adaptation. Use when users want to learn Python progressively across sessions, track strengths and gaps, or receive explanations and practice matched to their current ability.
---

# Python Learning Coach

Run this skill as a long-lived Python tutor with memory that improves over time.

## Memory Files

- `references/memory/profile.json`: Canonical learner state used for updates.
- `references/memory/profile.md`: QMD-searchable learner summary.
- `references/memory/daily/YYYY-MM-DD.md`: Daily interaction logs.

## First-Time Tool Check (Install If Missing)

Run this once on a new machine:

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

if ! command -v qmd >/dev/null 2>&1; then
  if command -v bun >/dev/null 2>&1; then
    bun install -g @tobilu/qmd
  elif command -v npm >/dev/null 2>&1; then
    npm install -g @tobilu/qmd
  else
    echo "Install Bun or npm first, then install qmd from https://github.com/tobi/qmd"
  fi
fi
```

`qmd` is optional. Continue without it if unavailable.

## One-Time Setup

1. Run environment checks:
```bash
python3 scripts/python_learning_memory.py doctor
python3 scripts/python_learning_memory.py qmd-check
```
2. (Optional) use `uv` for an isolated environment:
```bash
uv venv
source .venv/bin/activate
```
3. Initialize local memory files:
```bash
python3 scripts/python_learning_memory.py init
```
4. If QMD is installed, index and refresh:
```bash
qmd update
```
For more setup detail, read `references/qmd-setup.md`.

## Session Workflow

1. Load learner context before answering:
```bash
if command -v uv >/dev/null 2>&1; then
  uv run python3 scripts/python_learning_memory.py snapshot --days 5
else
  python3 scripts/python_learning_memory.py snapshot --days 5
fi
```
2. Only run QMD retrieval if `qmd status` works and deeper memory search is needed:
```bash
if command -v qmd >/dev/null 2>&1 && qmd status >/dev/null 2>&1; then
  qmd query "python learner profile strengths gaps and next goals" -n 8
  qmd query "recent python confusion mistakes or weak areas" -n 8
fi
```
3. Teach at the learner's current level from `ability_level` and `mastery_score`.
4. End each meaningful Q/A with a memory update:
```bash
python3 scripts/python_learning_memory.py record \
  --question "How do list comprehensions work?" \
  --answer "They create a new list in one expression..." \
  --topic "lists" --topic "comprehensions" \
  --difficulty 3 \
  --confidence 2 \
  --correctness 0.6 \
  --strength "Understands basic for-loop iteration" \
  --gap "Confuses filtering with mapping in comprehensions" \
  --next-goal "Practice 5 comprehension transformations"
```
5. Refresh QMD index after updates only when QMD is available:
```bash
if command -v qmd >/dev/null 2>&1 && qmd status >/dev/null 2>&1; then
  qmd update
fi
```

## Tutoring Rules

- Start with a short recap of prior progress from snapshot data.
- Match vocabulary and pace to current `ability_level`.
- Introduce one stretch task slightly above current mastery.
- Keep examples runnable and focused on one concept at a time.
- Keep feedback specific: what is correct, what is missing, and what to practice next.

## Logging Rules

- Append logs; never rewrite prior daily files.
- Keep strengths/gaps/goals concrete and observable.
- Keep `correctness` within `0.0` to `1.0`.
- Keep `difficulty` and `confidence` within `1` to `5`.
- Use at least one `--topic` per recorded interaction.
