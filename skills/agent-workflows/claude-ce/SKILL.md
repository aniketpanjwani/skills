---
name: claude-ce
description: Delegate Compound Engineering ideation, brainstorming, and planning workflows to an interactive Claude Code session from Codex. Use when Codex should stay the outer operator while Claude Code runs CE slash skills, preserves native question prompts, and writes durable local artifacts.
---

# Claude CE

Run selected Compound Engineering workflows inside Claude Code while Codex monitors the run and brokers user answers.

This skill requires:

- Claude Code already logged in through its normal interactive auth flow
- `claudet` and `tmux`
- the Compound Engineering Claude Code plugin with the CE skills you want to invoke

Supported routes:

- `ideate` -> `/compound-engineering:ce-ideate`
- `brainstorm` -> `/compound-engineering:ce-brainstorm`
- `plan` -> `/compound-engineering:ce-plan`

## Invocation

Run commands from this skill's installed directory, or replace `scripts/claude_ce.py` with the absolute path to the installed helper.

Start a workflow and block until it completes or asks a question:

```bash
python3 scripts/claude_ce.py run ideate "what should we improve in this repo?" --repo /path/to/project
```

Start in the background:

```bash
python3 scripts/claude_ce.py run brainstorm "better onboarding flow" --repo /path/to/project --detach
```

Watch, inspect, and answer:

```bash
python3 scripts/claude_ce.py watch --run-id latest
python3 scripts/claude_ce.py status --run-id latest
python3 scripts/claude_ce.py answer --run-id latest --choice 2
python3 scripts/claude_ce.py answer --run-id latest --text "Focus on checkout reliability."
```

Attach manually if needed:

```bash
tmux attach -t "$(python3 scripts/claude_ce.py status --run-id latest --json | jq -r .claude_tmux_session)"
```

`latest` is scoped to the current Codex thread when `CODEX_THREAD_ID` is available. Use the printed concrete run id for cross-thread recovery, old pre-scope runs, or plain-terminal operation.

## Workflow

1. Determine the route: `ideate`, `brainstorm`, or `plan`.
2. Run the helper against the target repo, usually with `--repo /path/to/project`.
3. Prefer blocking `run` for short requests. Use `--detach` when the workflow is likely to be long.
4. If Claude is waiting for user input:
   - Read the printed question or run `status --json`.
   - Present the choices to the user.
   - Call `answer --run-id <id> --choice N` or `answer --run-id <id> --text "..."`.
   - Resume monitoring with `watch --run-id <id>`.
5. When complete, read `state.json`, `claude-pane.log`, `result.md`, `done.json`, and any artifact paths reported in `done.json`.
6. Report the durable artifact paths and the run artifact directory.

## Artifacts

Each run writes under:

```text
/tmp/agentic/claude-ce/<run-id>/
```

Important files:

- `state.json`
- `prompt.md`
- `claude-pane.log`
- `pending-question.json` when Claude needs user input
- `answers.jsonl`
- `result.md`
- `done.json`

The artifact directory is the source of truth. Treat the terminal transcript as debugging context, not the final handoff.

## Guardrails

- Do not use `claude -p` for this workflow. The point is to preserve Claude Code's interactive skill behavior.
- The helper refuses to launch when `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `CLAUDE_CODE_OAUTH_TOKEN` are present in the process or global tmux environment. Use the normal Claude Code login path.
- Do not ask Claude to commit, push, or open PRs from this workflow. These routes produce CE artifacts and recommendations; Codex or the user performs follow-on implementation.
- Keep failed tmux sessions open by default. Successful sessions are killed by default to avoid accumulating old terminals.
- Add future CE workflows to the route table in `scripts/claude_ce.py` rather than creating another tmux runner.
