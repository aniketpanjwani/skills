---
name: goal-contract
description: Draft, critique, refine, or activate evidence-checkable agent Goals from rough tasks, brainstorm requirements, implementation plans, grill-with-docs decisions, or existing weak /goal text. Use when the user asks to create a Codex or Claude Code goal, turn a plan or brainstorm into a goal, strengthen a goal, decide whether a goal is appropriate, or set a goal for multi-turn work.
---

# Goal Contract

Use this skill to turn a rough intent, existing artifact, or weak `/goal` into a durable agent completion contract.

A strong Goal is not a larger prompt. It defines what should be true, how the agent can verify it, what must stay intact, how the agent should iterate, and when the agent should stop as blocked instead of pretending the work is done.

## Core Rules

- Use Goals for durable, evidence-based work where the next useful action may depend on what the agent learns along the way.
- Prefer a normal prompt for one-off edits, simple explanations, short reviews, or questions where the user wants one answer and then a stop.
- Keep the Goal narrow enough to audit and broad enough to let the agent choose the next action.
- Let source documents anchor scope, but make the Goal define done.
- Use repo-relative paths for source docs inside the current repo.
- Do not activate a Goal unless the user explicitly asks to start, set, create, or activate it.
- If activating in Claude Code, send the complete `/goal ...` command.
- If activating through the Codex goal tool, pass only the objective text, not the literal `/goal` prefix.
- Set runtime budgets only when the user explicitly asks for one. Codex may support a token budget; Claude Code should encode any requested turn or time bound in the Goal condition.

## Workflow

### 1. Resolve The Source

Identify the strongest available source of truth:

- Rough user request
- Existing weak `/goal`
- `docs/brainstorms/*-requirements.md` or `.html`
- `docs/plans/*-plan.md` or `.html`
- Decisions captured through `grill-with-docs`, such as `CONTEXT.md` terms or ADRs
- Issue text, PR description, benchmark output, failing test, research brief, or other task artifact

If the user references a file, read it before drafting. If multiple likely docs match, ask which one to use.

When using a `ce-brainstorm` requirements doc, extract product intent, scope boundaries, acceptance examples, success criteria, and non-goals. Do not pull implementation detail forward unless the brainstorm is explicitly architectural.

When using a `ce-plan` plan doc, extract implementation scope, source path, test strategy, validation expectations, risks, and deferred/blocking items. Do not make the Goal re-plan unless the user asks for a planning Goal.

When using `grill-with-docs` outputs, preserve canonical terms and ADR decisions. If the proposed Goal conflicts with glossary language or a documented decision, surface the conflict before drafting.

### 2. Decide Whether A Goal Fits

Recommend a Goal when all three are true:

- The work has a durable objective.
- There is an evidence-based finish line: tests, benchmark, artifact, report, source material, command output, or checked diff.
- The work may need several turns of investigation, implementation, testing, or research.

Recommend a normal prompt when the request is a one-line edit, quick explanation, simple code review, single command, or vague improvement request with no reliable completion condition.

If a Goal is close but underspecified, ask for the one missing detail that most affects auditability. Prefer drafting with explicit assumptions over interrogating the user about details the source artifact already answers.

### 3. Draft The Goal Contract

Read `references/goal-rubric.md` before drafting or reviewing a non-trivial Goal.

Compose one recommended Goal by default. It should include:

- Outcome: what must be true when done.
- Verification surface: how completion will be checked.
- Constraints: what must not regress or expand.
- Boundaries: allowed source docs, repos, files, tools, data, or resources.
- Iteration policy: how the agent should choose the next action after each attempt.
- Blocked stop condition: what to report if success is not reachable under current constraints.

Use this shape when useful:

```text
/goal <desired end state>, verified by <specific evidence>, while preserving <constraints>. Use <allowed inputs, tools, or boundaries>. Between iterations, <how the agent should choose the next best action>. If blocked or no valid paths remain, <what the agent should report and what would unlock progress>.
```

For doc-backed implementation Goals, prefer:

```text
/goal Implement the plan in docs/plans/<plan>.md so <intended outcome>. Verify by <tests/checks/artifacts from the plan>. Preserve the plan's stated scope boundaries and do not add deferred follow-up work unless required to satisfy the plan. Between iterations, inspect the next failing validation or weakest unmet plan item, patch the smallest relevant surface, and re-check. If blocked, stop with the attempted changes, evidence gathered, blocked plan item, and next input needed.
```

For doc-backed research or audit Goals, prefer:

```text
/goal Produce the strongest evidence-backed audit described in <source-doc>, using the available materials and local resources. Verify by producing <final report/artifact> that separates confirmed findings, partial/proxy support, blocked claims, and remaining uncertainty. Preserve the source doc's scope boundaries and label unavailable evidence explicitly. Between iterations, pursue the next highest-value unresolved claim. If blocked, stop with the claim inventory, evidence gathered, blocker, and next input needed.
```

### 4. Review And Refine

Before presenting the Goal, audit it for common failures:

- Vague finish line: "improve", "clean up", "make better", "finish this".
- Missing verification surface.
- Missing constraints or regression guard.
- Too narrow: prescribes the next command instead of the desired state.
- Too broad: spans unrelated systems or has no practical audit boundary.
- Hidden uncertainty: unavailable data, flaky benchmarks, or proxy evidence are not named.
- No blocked condition.
- Reopens product, planning, or domain decisions that the source doc already settled.

If refining an existing `/goal`, show the improved version and a short "what changed" note focused on auditability.

### 5. Activate Only On Explicit Request

If the user asks to activate the Goal, choose the runtime-specific path.

Codex:

- Call `create_goal` with the objective text only.
- Preserve the exact drafted objective except for removing the `/goal` command prefix.
- Include `token_budget` only when the user explicitly requested a budget.
- If a Goal already exists, inspect it with `get_goal` and explain that the current tool surface cannot edit the objective in place. Offer a replacement command for the user to apply after clearing or pausing the current Goal.

Claude Code:

- Requires Claude Code 2.1.139 or newer for `/goal` support.
- Send the complete `/goal ...` command when operating inside Claude Code.
- Claude Code has one active Goal per session; a new `/goal` replaces the active one.
- Use `/goal clear` when the user explicitly asks to clear the active Goal.
- Claude Code's Goal evaluator only reviews the conversation transcript, so the agent must surface verification evidence in the conversation instead of relying on hidden workspace state.
- If the user requests a turn or time limit, encode it in the Goal condition, for example "within 10 turns" or "within 1 hour."

If the user only asks for a draft, critique, or suggestion, do not activate the Goal. Leave the `/goal ...` command ready to paste.

## Output Shape

Keep the response compact:

```text
Recommended /goal:

<goal command>

Why this works:
- Outcome: ...
- Evidence: ...
- Constraints: ...
- Blocked condition: ...
```

For obvious lightweight cases, the "why this works" section can be one sentence.

For unsuitable Goal requests, say so plainly and give the better normal prompt.
