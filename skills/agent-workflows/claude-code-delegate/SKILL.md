---
name: claude-code-delegate
description: Delegate a general task from Codex to a normal interactive Claude Code session in a target project. Use when Codex should stay the outer operator while Claude Code uses native skills or subagents, writes durable artifacts, and asks questions through Codex.
---

# Claude Code Delegate

Run a general Claude Code workflow from Codex while Codex monitors artifacts and brokers user answers.

Use this for Claude Code tasks that do not belong to a specialized delegate such as `$claude-ce` or `$claude-pr-review`.

This skill requires:

- Claude Code already logged in through its normal interactive auth flow
- `claudet` and `tmux`
- optional: a local `project-catalog` skill if you want to use `--project` aliases instead of `--repo`

## Invocation

Run commands from this skill's installed directory, or replace `scripts/claude_code_delegate.py` with the absolute path to the installed helper.

Run in an explicit repository:

```bash
python3 scripts/claude_code_delegate.py run \
  --repo /path/to/project \
  --task "Draft a narration outline using the relevant Claude Code writing skill if available."
```

Hint a Claude Code skill:

```bash
python3 scripts/claude_code_delegate.py run \
  --repo /path/to/project \
  --claude-skill humanizer \
  --task "Revise this draft for a technical audience."
```

Allow Claude Code to edit the target repo:

```bash
python3 scripts/claude_code_delegate.py run \
  --repo /path/to/project \
  --write-scope repo \
  --task "Create a first draft file for this documentation task."
```

Use a project alias when `project-catalog` is installed:

```bash
python3 scripts/claude_code_delegate.py run \
  --project docs-site \
  --task "Research the draft structure."
```

Monitor and answer:

```bash
python3 scripts/claude_code_delegate.py watch --run-id latest
python3 scripts/claude_code_delegate.py status --run-id latest
python3 scripts/claude_code_delegate.py answer --run-id latest --choice 1
python3 scripts/claude_code_delegate.py answer --run-id latest --text "Focus on the introduction."
```

`latest` is scoped to the current Codex thread when `CODEX_THREAD_ID` is available. Use the printed concrete run id for cross-thread recovery, old pre-scope runs, or plain-terminal operation.

## Workflow

1. Resolve the target:
   - Use `--repo /path/to/project` for public, portable usage.
   - Use `--project <alias>` only when a compatible local `project-catalog` skill is installed.
   - Omit both to run in the current working directory.
2. Choose write scope:
   - `artifacts`: default; Claude Code reads the target repo but writes only delegate artifacts.
   - `repo`: use when the user clearly asked Claude Code to create or edit files in the target repo.
   - `none`: use when Claude Code should only report and avoid file changes other than required completion files.
3. Use `--claude-skill <name>` only as a hint to Claude Code. Do not pass subagent names from Codex; the Claude Code skill owns its own subagent routing.
4. Prefer blocking `run` for short tasks. Use `--detach` for long writing, research, or review tasks.
5. If Claude is waiting for user input:
   - Read the printed question or run `status --json`.
   - Present the choices to the user.
   - Call `answer --run-id <id> --choice N` or `answer --run-id <id> --text "..."`.
   - Resume monitoring with `watch --run-id <id>`.
6. When complete, read `state.json`, `claude-pane.log`, `result.md`, `done.json`, and any extra artifact paths reported in `done.json`.
7. Report the durable artifact paths and the run artifact directory.

## Artifacts

Each run writes under:

```text
/tmp/agentic/claude-code-delegate/<run-id>/
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

- The default runner is `claudet` + `tmux`, because this preserves Claude Code's native skill and subagent behavior.
- Do not expose a Codex-side subagent selector. If a Claude Code skill uses subagents, let that skill own the pairing.
- The helper refuses to launch when `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `CLAUDE_CODE_OAUTH_TOKEN` are present in the process or global tmux environment. Use the normal Claude Code login path.
- Do not ask Claude Code to commit, push, or open PRs through this generic delegate unless the user explicitly asks for that broader flow.
- Keep failed tmux sessions open by default. Successful sessions are killed by default to avoid accumulating old terminals.
