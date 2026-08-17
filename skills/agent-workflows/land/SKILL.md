---
name: land
description: "Finish one obvious coherent change through a thin GitHub landing lifecycle: preserve or create the feature branch and commits, reuse or run validation once, push, create or reuse a pull request, wait only for required checks, merge the exact head, verify GitHub's result, and safely synchronize the primary checkout's local default branch. Use when the user asks to land, finish, ship, merge, or cleanly wrap up work. Use the retained CE-backed rigorous lifecycle only when the user explicitly asks to land with full verification. Do not use for merely updating the repository default branch."
---

# Land

Bare `$land` is a thin, direct `git` and `gh` workflow. The invocation itself
authorizes landing one obvious coherent scope; do not turn it into a review or
release-governance ceremony.

## Thin default

A bare request such as “land,” “ship this,” “finish and merge,” or “wrap this
up” selects this path. It requires only `git`, authenticated GitHub CLI `gh`,
and the target repository's own hooks and validation.

### 1. Inspect and bound the scope

Use direct read-only `git` and `gh` commands to establish the repository,
GitHub remote, default branch, current branch or detached head, exact local
head, upstream, ahead/behind state, staged/unstaged/untracked paths, unpublished
commits, worktrees, and matching pull requests.

Proceed without another approval only when task context plus checkout evidence
identifies exactly one obvious coherent scope. Preserve unrelated paths and
existing commits. Reuse a matching pull request; never create a duplicate. A
true no-op needs no mutation. Ambiguous or changed scope stops before mutation.

Do not run a Land-specific credential or secret scan. Repository-native hooks,
push protection, and required hosted checks remain in force. Never bypass them.
If ordinary inspection reveals a concrete credential, stop and report only its
path and remediation need; never print its value.

### 2. Branch, commit, and validate once

Keep a suitable feature branch. If detached or on the default branch, create a
feature branch from the work using the repository or host naming convention;
never move another worktree to reclaim one.

Preserve existing commits and their separation. For one coherent uncommitted
scope, stage only its exact paths and create one concise commit. Never amend,
squash, reorder, or rewrite existing commits. Let repository-native commit
hooks run; a hook failure stops the attempt without unrelated repair.

Reuse successful validation from this task only when it covered identical
candidate content and nothing relevant changed. Otherwise run the repository's
documented standard validation once. If none is declared, record that and rely
on repository-native hooks plus required GitHub checks. Failure stops the path;
do not fix, weaken, repeatedly rerun, or bypass validation while landing.

### 3. Push and open or reuse the pull request

Push the exact live feature head without force, record its object ID, and create
or reuse the matching pull request against the verified default branch. Recheck
for an existing pull request immediately before creating one.

Do not start code review, request reviewers, inspect non-required bot chatter,
repair feedback, update the branch, or otherwise mutate the candidate after
push. Any head change stops this invocation; a later `$land` must inspect and
validate the new candidate.

### 4. Wait only for required GitHub gates

Query only required checks. Wait for pending required checks to become
terminal; do not add a quiet period or wait for optional checks, reactions,
comments, or review bots. An empty required-check set proceeds immediately
without auditing workflows, Actions configuration, or branch rules.

Read fresh draft, formal review, and mergeability state. Stop without
remediation on a failed, cancelled, or unknown required check;
`REVIEW_REQUIRED`; `CHANGES_REQUESTED`; a draft; a merge conflict; mergeability
that remains unknown after one fresh retry; or another repository-enforced
gate. Non-required bot comments and optional checks do not block this path. Do
not invoke a debugger, reviewer, feedback resolver, babysitter, or branch update.

### 5. Merge the exact head

Immediately before merge, require the local feature head, pushed remote head,
and pull-request head to equal the recorded candidate, with Section 4's gates
still passing.

Honor an explicit merge method. Otherwise use the repository's established
non-squashing convention, preferring an allowed merge commit and then an
allowed rebase merge. If only squash is allowed, stop for a user decision rather
than collapsing existing commits.

Use `gh pr merge --match-head-commit <candidate>` with the selected method,
without administrator privileges or branch deletion. If GitHub requires a
merge queue, use its ordinary path and wait only for the terminal queue result.

### 6. Verify remotely, then synchronize locally

Claim a remote merge only when a fresh GitHub read shows state `MERGED`, the
recorded pull-request head equals the exact candidate, a merge timestamp exists,
and GitHub identifies the integration commit when that field is available. Do
not run the full-verification integration-tree helper on this path.

Only after verified remote success, fetch the remote default and resolve the
primary checkout from `git worktree list --porcelain`, positively verifying it
is the regular non-bare worktree. A dirty primary checkout, in-progress Git
operation, default branch owned by another worktree, diverged local default, or
untracked collision leaves the primary untouched and local synchronization
incomplete; it never undoes or blocks the remote merge.

Never stash, reset, clean, detach, delete, or force. When safe, switch only the
primary checkout to the default branch and run
`git merge --ff-only <remote>/<default>`. Preserve untracked files and leave a
linked landing worktree on its feature branch.

### 7. Report concisely

State the pull request, exact candidate, merge method and remote result;
validation evidence; required-check and formal-review state; committed and
preserved paths; landing-worktree state; and primary-worktree synchronization.
On a stop, name completed mutations, the exact blocker, omitted stages, and the
safest resume point. Keep remote merge and local synchronization distinct.

## Explicit full verification

Only an explicit request to “land with full verification” (or unmistakable
equivalent wording requesting the existing rigorous lifecycle) selects this
route. Do not automatically escalate a bare invocation; a concrete blocker
stops the thin path.

For full verification, confirm `git`, authenticated `gh`,
`$ce-commit-push-pr`, and `$ce-babysit-pr`; then read
[references/landing-protocol.md](references/landing-protocol.md) completely and
follow it. Preserve that protocol's approval boundary, secret safeguards,
readiness ownership, exact-head revalidation, method-aware merge verification,
and primary-worktree synchronization. If a dependency is unavailable, stop;
never approximate this route with a partial workflow.

## Shared boundaries

Honor explicit omissions such as “do not merge.” Preserve unrelated work and
every worktree. Never use administrator merge privileges, bypass repository
protections, or delete a branch or worktree to manufacture success.
