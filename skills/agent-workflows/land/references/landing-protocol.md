# Full-verification landing protocol

Read and apply every section only when `$land` selected this protocol from an
explicit “land with full verification” request. A bare `$land` invocation uses
the thin default in `SKILL.md` instead. This protocol owns rigorous orchestration,
authorization boundaries, terminal merge, and reporting; the invoked Compound
Engineering skills own their internal procedures.

## 1. Normalize the request

The default is the full lifecycle:

`inspect -> approve scope -> branch -> atomic commits -> validate -> push -> create or reuse PR -> babysit -> revalidate -> merge -> verify -> synchronize local default -> report`

Only an explicit natural-language instruction may omit a stage. Record every omission in the scope proposal. Silence never means omit. An omission cannot weaken the suspected-secret hard stop, include unapproved work, or permit a stale-head merge.

## 2. Preflight without mutation

Confirm:

- the checkout is a Git repository;
- its target forge is GitHub;
- `git`, authenticated `gh`, `$ce-commit-push-pr`, and `$ce-babysit-pr` are available;
- the repository's default branch, remotes, merge-method settings, primary worktree, and relevant linked worktrees;
- current branch or detached HEAD, HEAD object ID, upstream and ahead/behind state;
- staged, unstaged, untracked, ignored, generated, and pre-existing paths;
- commits not represented by the upstream;
- a matching open, closed, or merged pull request, if any.

Use read-only commands and APIs. Do not switch or create a branch, stage, commit, push, edit a pull request, or merge during preflight.

Classify the starting state:

1. **Uncommitted work:** group changed files by concern.
2. **Existing commits:** describe the commits that still need publication or landing.
3. **Matching open PR:** reuse it; do not create a duplicate.
4. **Already merged:** verify the remote terminal state, then inspect whether the local default branch still needs synchronization.
5. **No landing work:** report a no-op.

A true terminal no-op needs no approval because it performs no mutation. An already-merged pull request with a stale local default branch is not a no-op; obtain approval for the local synchronization unless the invocation already authorized the full lifecycle.

## 3. Build the approved scope

Form the smallest independently coherent commit groups. For each group, list:

- exact paths;
- commit intent and proposed message;
- validation appropriate to that concern.

Separately list unrelated, generated, sensitive, pre-existing, and ambiguous paths. Do not infer ownership from proximity. Include existing commits and the intended pull-request create/reuse action.

### Suspected-secret hard stop

Before proposing approval, apply any repository-native secret scanner and inspect the complete candidate landing delta for credential material such as private keys, access tokens, passwords, signing material, or committed secret files. The delta includes every existing commit from the merge base or upstream through the candidate head plus staged, unstaged, and intended untracked content. Repeat this check for every new merge-candidate head produced later in the workflow.

Use a scanner's redacted or path-only output mode. If an available scanner cannot avoid displaying candidate values, do not run it in a way that puts raw output in chat or durable logs; use a safe inspection path and report only redacted metadata.

If any signal is positive:

- stop before branch creation, staging, commit, or push;
- report only the affected path, detector category, and remediation state;
- do not expose the candidate value;
- do not offer exclusion of the path as a bypass;
- for uncommitted material, resume only after it is removed from both the intended scope and checkout, or inspection verifies the signal is a false positive;
- for material already committed, stop until the branch history is sanitized and the complete candidate landing delta passes again; do not rewrite history automatically;
- for material already pushed, also require credential revocation or rotation and explicit remote-history remediation before continuing;
- repeat the full read-only inspection and complete secret check after remediation.

User approval cannot override this hard stop.

## 4. One approval boundary

Present one checkpoint containing:

- the exact commit groups, paths, messages, and validations;
- existing commits included in the landing scope;
- every excluded or preserved path;
- branch action and pull-request create/reuse action;
- every explicit lifecycle omission;
- the intended repository-allowed merge method, or how it will be selected;
- the intended primary-worktree switch and local default-branch synchronization, including how an unsafe primary worktree or conflicting branch owner will be reported;
- the statement that approval authorizes the approved scope and the later merge of its freshly revalidated exact head.

Ask the user to approve or revise this proposal. Perform no mutation before approval. If the scope changes later, or a remediation would alter intended behavior beyond the approved concern, stop and obtain a revised scope approval.

## 5. Publish the approved work

Invoke `$ce-commit-push-pr` through the active host's skill mechanism with:

`mode:pipeline babysit:off`

Pass the approval record as authoritative caller context: file groups, commit intent, existing commits, exclusions, explicit omissions, branch constraints, and matching pull-request state.

The delegated skill should:

- create a suitable feature branch for a detached or default-branch checkout, while preserving a suitable existing feature branch;
- create the approved atomic commits without staging excluded paths;
- run proportionate validation;
- push the live head exactly;
- create or reuse the matching pull request.

If the delegate cannot honor the approved grouping, stop. Record the published head object ID and pull-request URL after it returns. Reinspect the checkout to ensure excluded work remains untouched.

For an explicitly omitted later stage, perform every preceding non-omitted stage and stop immediately before the omitted stage. For example, “do not merge” still establishes and freshly revalidates readiness unless the user also omitted readiness work. Report the precise resumable state.

## 6. Establish readiness

Invoke `$ce-babysit-pr` through the host's normal skill mechanism, with the pull-request URL and `mode:pipeline`. It is the sole owner of checks, review feedback, branch currency, and its bounded remediation loop.

Do not start a concurrent watcher, substitute a different readiness owner, or reconstruct the babysitting loop. If the babysitter changes the branch, diff the previous candidate against the new head at path and hunk level, then re-run the suspected-secret hard stop over the new commits and content. Accept the new head only when every change remains within the approved concern and the secret check passes; otherwise stop for remediation or revised scope approval. Capture the resulting live head as the merge candidate.

A ready or looks-ready return advances to fresh revalidation. A residual, failed gate, draft boundary, unresolved human decision, or unknown state blocks merge.

### Repositories without hosted CI

An otherwise-ready `no-checks-observed` result is not a user-facing blocker when hosted CI is intentionally absent. Apply this narrow classification only when all of the following fresh, read-only evidence agrees for the exact merge-candidate head and base branch:

- the babysitter's only residual is an empty check rollup, with no failing, pending, approval-gated, or unknown check;
- the repository exposes no GitHub Actions workflow through the Actions workflows API and the exact candidate tree contains no `.github/workflows/*.yml` or `.github/workflows/*.yaml` file;
- branch protection or repository rules require no status-check context for the target branch;
- the approved local validation completed successfully against the exact merge-candidate head; and
- every non-check babysitter readiness gate passed.

Record this internally as `hosted-CI-not-configured`, advance directly to exact-head revalidation, and do not interrupt the user or surface the expected absence as a warning. This is capability classification, not a substitute readiness loop: `$ce-babysit-pr` remains the sole owner of review feedback, observed checks, branch currency, and remediation.

If any probe is denied, malformed, stale, or ambiguous, or if any workflow, required context, configured check, or failed local validation exists, the exception does not apply. Preserve the ordinary blocker rather than inferring that CI is absent.

## 7. Revalidate the exact head

Immediately before merge, fetch fresh local and GitHub state. Require all of the following:

- the pull request is open and not draft;
- its current head object ID equals the approved, published merge-candidate head;
- the local feature head, pushed remote head, and pull-request head agree;
- when hosted CI is configured, required checks are present, terminal, and passing; otherwise the fresh classification is `hosted-CI-not-configured` and approved local validation passed against the exact head;
- review requirements pass and no actionable review thread or feedback remains;
- GitHub mergeability is certain and clean;
- the base branch identity and currency are current and known;
- no stack/dependency blocker or parked human decision remains;
- the suspected-secret check passed for the current merge-candidate head and every commit/content change since approval;
- the selected merge method is allowed by both the repository and any explicit user instruction.

Treat missing, empty, stale, changing, or unknown evidence as failure unless the empty check rollup has the complete fresh `hosted-CI-not-configured` evidence above. If the head changes, invalidate that classification and return to inspection for the new head; never merge using evidence from an earlier head. If its scope remains approved, re-invoke `$ce-babysit-pr mode:pipeline` as the same sole readiness owner before revalidation. If scope changed, obtain revised approval first.

Merge-method precedence:

1. explicit user instruction;
2. repository convention or required method;
3. an allowed method that preserves approved atomic commits.

If more than one method remains and selection would require guessing, stop. Use the corresponding non-interactive `gh pr merge` method only after every gate above passes.

## 8. Verify the remote merge

Re-read the pull request from GitHub and require:

- terminal state `MERGED`;
- a recorded merge timestamp and merge commit object ID;
- the pull request's recorded head object ID equals the exact merge-candidate head;
- the selected merge method is known;
- the base object ID used by the final exact-head gate is recorded as the validated base; and
- after fetching the validated base, approved head, and recorded integration commit, the recorded integration tree equals the tree produced by integrating that approved head into the applicable base with the selected method.

Use the deterministic helper rather than comparing the complete integration tree directly to the pull-request-head tree. Run it from the installed `$land` skill directory:

```bash
python3 scripts/verify-remote-merge.py \
  --repo <repository> \
  --method <merge|squash|rebase> \
  --candidate <exact-approved-head> \
  --validated-base <base-object-from-final-gate> \
  --integration <recorded-merge-commit>
```

The helper verifies method-specific structure and computes the expected integration tree with Git's merge machinery without changing a worktree or ref:

- **Merge:** require exactly two parents, require the approved head to be the second parent and an ancestor of the integration commit, use the first parent as the actual integration base, require the validated base to equal or precede that actual base, and compare the recorded tree with the expected merge tree.
- **Squash:** require exactly one parent, use that parent as the actual integration base, require the validated base to equal or precede that actual base, and compare the recorded tree with the expected merge tree. Do not require approved-head ancestry.
- **Rebase:** require the validated base to be an ancestor of the recorded terminal integration commit and compare its recorded tree with the expected tree for integrating the approved head into that validated base. Do not require approved-head ancestry because the commits were rewritten. If the base moved after validation or the validated base cannot unambiguously anchor the replay, fail closed and repeat readiness plus exact-head validation before another merge attempt.

This verification deliberately permits newer, nonconflicting base changes for merge and squash: those changes belong in both the actual integration base and the expected integration tree. A direct equality check between the recorded integration tree and the pull-request-head tree is invalid whenever the base advanced independently.

If terminal evidence is missing or mismatched, report the result as unverified and do not claim success.

## 9. Synchronize the primary worktree and local default branch

Only after the remote merge passes Section 8, return the repository's primary worktree to the verified pull request's base branch and synchronize it. The **primary worktree** is Git's regular repository checkout, not whichever linked worktree happens to own the default branch. This stage is part of the full lifecycle, including an already-merged invocation whose remote result is verified but whose primary worktree is on another branch or whose local default branch is stale.

1. Resolve the verified pull request's base branch `<base>` and its corresponding remote `<remote>`. Fetch `<remote>/<base>` without changing any checkout.
2. Run `git worktree list --porcelain`. Treat its first `worktree` record as the primary-worktree candidate, then positively verify it is the non-bare main checkout by requiring `git -C <primary> rev-parse --is-bare-repository` to return `false` and `git -C <primary> rev-parse --path-format=absolute --git-dir` to equal `git -C <primary> rev-parse --path-format=absolute --git-common-dir`. Do not infer the primary worktree from a human-looking path. If the candidate is missing, inaccessible, bare, or fails this identity check, record `primary-worktree-unresolved` and stop local synchronization.
3. Inspect every worktree's branch entry. If a worktree other than `<primary>` owns `refs/heads/<base>`, record `default-branch-owned-outside-primary` and stop; do not switch, detach, delete, or otherwise disrupt that worktree to reclaim the branch.
4. Inspect `<primary>` before mutation. Require:
   - no merge, rebase, cherry-pick, or revert is in progress;
   - no staged or unstaged tracked changes;
   - the local `<base>` branch exists and its current commit is either equal to or an ancestor of the freshly fetched `<remote>/<base>`;
   - when `<primary>` is also the landing checkout, its checked-out HEAD still equals the verified merge-candidate head and no post-merge work appeared.
5. Preserve untracked paths exactly as found. Never stash, delete, clean, reset, or overwrite them. A branch switch or fast-forward that would collide with an untracked path must fail closed and leave that path untouched.
6. If `<primary>` is not already on `<base>`, run `git -C <primary> switch <base>`. This switch is expected when the landing checkout is the primary worktree; from a linked Codex, Claude, or other managed worktree, leave the landing worktree untouched and switch only `<primary>`. Never force the switch.
7. If the two heads already agree, record a synchronization no-op. Otherwise run `git -C <primary> merge --ff-only <remote>/<base>`. Do not use pull, rebase, a merge commit, or a forced update.
8. Verify that `<primary>` is on `<base>` and its HEAD equals `<remote>/<base>`. Record the primary path, whether it was also the landing checkout, its prior branch and old HEAD, its new branch and HEAD, the remote HEAD, ahead/behind counts, and staged, unstaged, and untracked paths.

If any precondition, switch, fast-forward, or verification fails, do not undo the remote merge or mutate around the blocker. Report that the remote merge remains successful, local synchronization is incomplete, the exact blocker, and the safe resume command or condition.

## 10. Preserve and report the worktrees

Leave every linked or managed worktree in place and preserve its branch and contents. Do not delete a branch or worktree, stash, reset, clean, or discard excluded work. Section 9 is the sole exception for checkout movement: it may switch the primary worktree—including the current landing worktree when they are the same—to the verified base branch and fast-forward it.

Report:

- pull-request URL and final state;
- merge method, approved head, recorded PR head, merge commit, and merge timestamp;
- landing-worktree path, branch or detached state, local HEAD, upstream, ahead/behind counts, and whether it was also the primary worktree;
- primary-worktree path, prior/new branches, old/new/remote HEADs, synchronization outcome, and staged, unstaged, and untracked paths;
- every preserved linked or managed worktree relevant to the landing decision;
- preserved exclusions and whether the checkout is clean or intentionally dirty;
- completed stages, explicit omissions, and any follow-up command.

Every stopped report must also name the exact blocker, mutations already performed, stages not performed, and the safest resume point.
