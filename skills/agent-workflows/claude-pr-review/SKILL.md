---
name: claude-pr-review
description: Delegate the current PR branch to Claude Code and Compound Engineering for code review, post GitHub PR review comments, then let Codex fix actionable findings. Use when a PR needs an external Claude Code review loop with durable artifacts and guarded GitHub posting.
---

# Claude PR Review

Run Claude Code with the Compound Engineering review skill against the current PR branch, post the review to GitHub, and give Codex a machine-readable queue of findings to resolve.

This skill requires:

- Claude Code already logged in through its normal interactive auth flow
- `claudet` and `tmux` for the default runner
- `gh` authenticated to the target GitHub repository
- a local branch with an open GitHub PR
- the Compound Engineering Claude Code plugin with `/compound-engineering:ce-code-review` or `/compound-engineering:ce-review`

## Invocation

Run commands from this skill's installed directory, or replace `scripts/claude_pr_review.py` with the absolute path to the installed helper.

Run the current repo:

```bash
python3 scripts/claude_pr_review.py run
```

Run an explicit repo:

```bash
python3 scripts/claude_pr_review.py run --repo /path/to/project
```

Start in the background and monitor:

```bash
python3 scripts/claude_pr_review.py run --detach
python3 scripts/claude_pr_review.py watch --run-id latest
python3 scripts/claude_pr_review.py status --run-id latest
python3 scripts/claude_pr_review.py actions --run-id latest
```

Preview without posting to GitHub:

```bash
python3 scripts/claude_pr_review.py run --dry-run
```

Use the legacy `claude -p` runner only when explicitly requested:

```bash
python3 scripts/claude_pr_review.py run --runner claude-p
```

`latest` is scoped to the current Codex thread when `CODEX_THREAD_ID` is available. Use the printed concrete run id for cross-thread recovery, old pre-scope runs, or plain-terminal operation.

## Default Workflow

When the user invokes `$claude-pr-review` without saying "review only", "monitor only", or "do not fix", run the full loop:

1. Confirm the current checkout is a clean PR branch.
2. Run the helper with the default `tmux` runner. Use `run --detach` only when Codex needs to do independent work while Claude reviews.
3. Expect substantive Compound Engineering reviews to take 20-30+ minutes on larger PRs. Do not treat missing final artifacts as a stall while `state.json` shows recent `last_event_at` activity.
4. Wait until the run is `complete` or `failed`; do not ask the user to monitor it manually.
5. After completion, read:
   - `state.json`
   - `claude-pane.log`
   - `done.json`
   - `findings.json`
   - `claude-result.md`
   - `summary.md`
6. Run `actions --run-id <id> --json` to get the actionable queue sorted by Claude's severity ranking.
7. Fix findings in order: P0, P1, P2, then P3. Skip `pre_existing: true` unless the user explicitly asked to fix pre-existing issues.
8. Validate each finding against the current code before editing. Apply the smallest defensible patch and run targeted verification.
9. Write `codex-resolution.json` and `codex-resolution.md` in the run artifact directory.
10. Commit or push only when the user asked for that broader flow.

## Review-Only Workflow

If the user explicitly asks to only run Claude's review, stop after the helper completes and report the artifact path plus PR review URL. Do not enter the fix loop.

## Artifacts

Each run writes under:

```text
/tmp/agentic/claude-pr-review/<run-id>/
```

The helper treats `done.json` as a completion latch only; it still requires a valid machine-readable review artifact before posting or handing findings to Codex.

## Guardrails

- Current v0 is intentionally current-branch/current-PR only. Do not pass arbitrary PR URLs yet.
- The helper requires a clean worktree by default because it posts comments against the remote PR diff.
- If local `HEAD` does not match the PR head, push the branch first, or rerun with `--allow-head-mismatch` only when you understand comments may not map perfectly.
- Use `--dry-run` before first use in a new repo if you want to inspect the generated review payload.
- Do not use `claude -p` unless the user explicitly asks for the legacy runner.
- If the helper refuses because billing/auth env vars are set, unset them or clear the tmux global environment before rerunning; do not work around that guardrail by enabling API keys.
- Do not ask Claude to post to GitHub directly. Claude writes local artifacts; this helper validates, maps inline comments to the PR diff, avoids duplicate/invalid review payloads, and posts the GitHub review.
- Do not ask Claude to edit, commit, push, or create PRs in this workflow. Claude reviews; Codex or the user fixes afterward.
- Do not blindly trust the review. Codex must validate each finding against the current code before editing.
- Do not post duplicate Claude review comments on re-runs unless the user wants another GitHub review; use `--dry-run` for verification-only rechecks.

## Notes

- The script auto-detects the installed Claude review skill, preferring `/compound-engineering:ce-code-review` when available and falling back to `/compound-engineering:ce-review`.
- Inline comments are posted only when `file:line` is present and the line exists in the PR diff. All findings still appear in the summary.
- `actions --json` is the handoff format Codex should use for autonomous fixing; GitHub comments are for durable human-visible review context.
