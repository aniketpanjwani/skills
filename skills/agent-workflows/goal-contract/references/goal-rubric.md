# Goal Rubric

Use this reference when drafting or reviewing a non-trivial agent Goal.

## Fit Check

A Goal is a good fit when the task has:

- Durable objective: the thread should keep working until a defined state is true.
- Evidence-based finish line: completion can be checked against concrete artifacts, tests, benchmark output, command output, source material, or a final report.
- Discovery path: the next useful action may depend on what the agent learns while working.

A normal prompt is better for:

- One-line edits
- Simple explanations
- Short code reviews
- Single commands
- Questions that need one answer
- Vague improvement requests with no audit surface

## Contract Fields

| Field | Question | Good Signal |
| --- | --- | --- |
| Outcome | What should be true when done? | Specific end state, not activity |
| Verification surface | What proves completion? | Test, benchmark, artifact, report, evidence table, checked diff |
| Constraints | What must not regress? | Public API, tests, scope boundaries, terminology, data safety, performance floor |
| Boundaries | What may the agent use or touch? | Source docs, repos, files, tools, data, allowed resources |
| Iteration policy | How should the agent choose the next action? | Inspect latest evidence, address next failing check, pursue highest-value unresolved claim |
| Blocked condition | When should the agent stop honestly? | No valid path remains, evidence unavailable, command cannot run, user decision needed |

## Strong Goal Pattern

```text
/goal <desired end state>, verified by <specific evidence>, while preserving <constraints>. Use <allowed inputs, tools, or boundaries>. Between iterations, <how the agent should choose the next best action>. If blocked or no valid paths remain, <what the agent should report and what would unlock progress>.
```

## Doc-Backed Goal Pattern

Use the document as the scope anchor and the Goal as the completion contract.

```text
/goal Implement the plan in docs/plans/<plan>.md so <intended outcome>. Verify by <tests/checks/artifacts named or implied by the plan>. Preserve the plan's stated scope boundaries and do not add deferred follow-up work unless required to satisfy the plan. Between iterations, inspect the next failing validation or weakest unmet plan item, patch the smallest relevant surface, and re-check. If blocked, stop with the attempted changes, evidence gathered, blocked plan item, and next input needed.
```

Avoid Goal text that only says `Implement docs/plans/<plan>.md`; that points to scope but does not define what evidence decides completion.

## Research Goal Pattern

Research Goals need an evidence standard before the investigation starts.

```text
/goal Produce the strongest evidence-backed audit described in <source-doc>, using the available materials and local resources. Verify by producing <final report/artifact> that separates confirmed findings, partial or proxy support, blocked claims, and remaining uncertainty. Preserve the source doc's scope boundaries and label unavailable evidence explicitly. Between iterations, pursue the next highest-value unresolved claim. If blocked, stop with the claim inventory, evidence gathered, blocker, and next input needed.
```

## Weak To Strong Examples

Weak:

```text
/goal Improve performance
```

Strong:

```text
/goal Reduce p95 checkout latency below 120 ms on the checkout benchmark while keeping the correctness suite green. Between iterations, record what changed, what the benchmark showed, and the next best experiment. If the benchmark cannot run or no valid paths remain, stop with attempted paths, evidence gathered, blocker, and next input needed.
```

Weak:

```text
/goal Write docs for this feature
```

Strong:

```text
/goal Produce a docs page for the feature that explains the lifecycle, command surface, and two examples. Verify that the page builds locally and all referenced commands match current CLI behavior. Preserve existing terminology from CONTEXT.md. If blocked, report the missing command behavior, unavailable source, or user decision needed.
```

## Review Checklist

Before presenting a Goal, check:

- Does it say what done means?
- Can the agent verify completion from evidence in the thread or workspace?
- For Claude Code Goals, will the agent surface enough evidence in the conversation for the evaluator to judge completion?
- Does it define what must not regress?
- Does it give enough boundary to avoid scope creep?
- Is it open enough for the agent to choose the next action?
- Does it name what to do when blocked?
- Does it preserve source-doc decisions instead of reopening them?
- Is it short enough that the objective remains legible during continuation?
