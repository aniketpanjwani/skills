---
name: land
description: "Finish approved work through the complete GitHub landing lifecycle: inspect the checkout, propose atomic commit groups, create or preserve a feature branch, commit, validate, push, create or reuse a pull request, babysit readiness, merge the exact approved head, verify the result, and return the repository's primary worktree to an updated local default branch. Use when the user asks to land, finish, ship, merge, or cleanly wrap up work in a Git worktree. Do not use for merely updating the repository default branch; use $git-up for that."
---

# Land

Use `$land` to finish work without making the user restate the branch, atomic-commit, pull-request, readiness, merge, verification, and local-default synchronization sequence.

## Required dependencies

This skill orchestrates, but does not reimplement:

- `$ce-commit-push-pr`
- `$ce-babysit-pr`
- `git`
- authenticated GitHub CLI `gh`

Confirm every dependency before mutation. If one is unavailable, stop with the missing prerequisite and a resume instruction. Do not replace a missing Compound skill with an improvised workflow.

## Contract

- Run the full lifecycle by default. Omit a stage only when the user's invocation explicitly requests that omission.
- Read [references/landing-protocol.md](references/landing-protocol.md) completely before taking action, then follow it as the authoritative workflow.
- Inspect first and present one concern-based, file-specific atomic commit proposal before the first branch, staging, commit, push, pull-request, or merge mutation.
- Treat that one approval as bounded authorization for the approved scope and its later exact-head merge. Do not ask for a routine second merge confirmation.
- Hard-stop before staging or pushing if a suspected credential or secret is found anywhere in the complete candidate history or a later merge-candidate head. Resume only after the required removal, history remediation, and credential response or false-positive verification; never continue by silently omitting it.
- Verify that the exact approved head was integrated into the actual base with the selected merge method. Never require the entire integrated tree to equal the pull-request-head tree when the base may contain newer, nonconflicting changes.
- Preserve unrelated work and every linked or managed worktree. Never delete the feature branch or any worktree.
- After a verified remote merge, return the repository's primary worktree—the regular checkout recorded by Git—to the local default branch and safely fast-forward it. When the landing checkout is the primary worktree, switch that checkout; when landing from a linked Codex, Claude, or other managed worktree, leave it in place and update the primary worktree separately. Never stash, reset, clean, force-switch, or discard work to make synchronization succeed.
- Do not interrupt or warn the user merely because a repository intentionally has no hosted CI. When the protocol freshly proves that no GitHub Actions workflows and no required status checks are configured, use successful approved local validation and continue the landing lifecycle silently.
- Stop on ambiguity, changed scope, failed or unknown readiness gates, unresolved human decisions, or stale head evidence.

## Delegation

After approval:

1. Invoke `$ce-commit-push-pr` through the host's normal skill mechanism with `mode:pipeline babysit:off`. Pass the approved commit groups, existing commits, explicit omissions, and pull-request reuse context as authoritative scope.
2. Invoke `$ce-babysit-pr` as the sole readiness owner, with `mode:pipeline` and the resulting pull-request URL. Never run a concurrent or substitute watcher.
3. Resume the landing protocol's fresh exact-head gate. `$ce-babysit-pr` returning ready is evidence to revalidate, not permission to skip revalidation.

The landing protocol's narrow `hosted-CI-not-configured` classification is the only case in which a `no-checks-observed` babysitter residual may advance. It classifies repository capability with fresh read-only evidence; it does not replace the babysitter or reinterpret a configured check.

Do not copy or approximate either Compound skill's internal procedure.

## User interaction

Use the host's blocking question mechanism for the single scope approval when available. Otherwise ask one concise numbered chat question and wait. Any later question must represent a real scope change, safety decision, or external blocker.

Every stopped or completed result must state what completed, what did not, whether mutation occurred, the exact blocker or merge evidence, the landing-worktree state, and the primary-worktree/default-branch synchronization state.
