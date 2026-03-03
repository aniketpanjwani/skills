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

## One-Time Setup

1. (Recommended) use `uv` for an isolated environment:
```bash
uv venv
source .venv/bin/activate
```
2. Run environment checks:
```bash
uv run python3 scripts/python_learning_memory.py doctor
uv run python3 scripts/python_learning_memory.py qmd-check
```
`qmd-check` verifies both `uv` and QMD availability.
3. Initialize local memory files:
```bash
uv run python3 scripts/python_learning_memory.py init
```
4. Install QMD if missing (recommended for semantic memory retrieval):
```bash
bun install -g https://github.com/tobi/qmd
qmd status
```
5. Ensure the directory containing this skill is indexed by QMD, then refresh:
```bash
qmd update
```
For detailed setup and fallback commands, read `references/qmd-setup.md`.

If QMD is unavailable, continue using the memory files directly.

## Session Workflow

1. Load learner context before answering:
```bash
uv run python3 scripts/python_learning_memory.py snapshot --days 5
qmd query "python learner profile strengths gaps and next goals" -n 8
qmd query "recent python confusion mistakes or weak areas" -n 8
```
2. Teach at the learner's current level from `ability_level` and `mastery_score`.
3. End each meaningful Q/A with a memory update:
```bash
uv run python3 scripts/python_learning_memory.py record \
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
4. Refresh QMD index after updates:
```bash
qmd update
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
