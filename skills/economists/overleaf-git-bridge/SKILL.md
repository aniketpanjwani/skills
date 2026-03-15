---
name: overleaf-git-bridge
description: Sync a Git-managed paper workspace with Overleaf through a filtered local mirror repo. Use when coauthors want Overleaf or its editor, but the manuscript, figures, tables, and code outputs should stay in Git and remain accessible to agentic coding tools.
---

# Overleaf Git Bridge

Use this skill to keep a paper in a normal Git repo while syncing only Overleaf-safe files to an Overleaf project.

## Use This Skill When

- You want a paper under `paper/` in the same repo as code, notes, and generated artifacts.
- Coauthors want to edit in Overleaf, but you still want Git-native authoring and agent help locally.
- You need to bootstrap a new Overleaf project from local LaTeX.
- You need to pull Overleaf edits back into Git or push local manuscript changes into the shared Overleaf project.

## Operating Model

- The main repo is the human-facing source of truth for paper, code, notes, and generated outputs.
- A local bridge repo under `.overleaf/.../mirror` is the only repo that talks to Overleaf Git.
- Overleaf `/devs` is only for first-time bootstrap and disposable previews.
- Ongoing collaboration uses Overleaf Git integration only.
- Do not enable Overleaf GitHub sync on the same canonical Overleaf project.

Read `references/overleaf_constraints.md` when you need the config format, the official Overleaf constraints, or the rationale behind the guardrails.

## Quick Start

1. Initialize the bridge in the paper repo:

```bash
python3 scripts/overleaf_bridge.py init \
  --repo "$PWD" \
  --main-document paper/main.tex \
  --paper-dir paper
```

2. Review `.overleaf-bridge.toml` and add any export-only mappings for generated tables or figures.

3. Attach the Overleaf Git URL after creating or locating the shared Overleaf project:

```bash
python3 scripts/overleaf_bridge.py attach-git \
  --repo "$PWD" \
  "https://git@git.overleaf.com/<project-id>"
```

4. Validate the setup before syncing:

```bash
python3 scripts/overleaf_bridge.py doctor --repo "$PWD"
```

5. Sync the canonical branch to the shared Overleaf project:

```bash
python3 scripts/overleaf_bridge.py sync --repo "$PWD"
```

## Core Commands

### Initialize

Use `init` once per paper repo to create:

- `.overleaf-bridge.toml`
- `.overleaf/.../mirror`
- a local `master` bridge repo with `core.fileMode=false`

Common options:

- `--paper-dir paper`
- `--generated-mapping results/tables:generated/tables`
- `--generated-mapping results/figures:generated/figures`
- `--canonical-branch main`

### Bootstrap Or Preview With `/devs`

Use `/devs` only when you want a new Overleaf project or a disposable preview from the current branch:

```bash
python3 scripts/overleaf_bridge.py bootstrap-api --repo "$PWD"
python3 scripts/overleaf_bridge.py preview --repo "$PWD"
```

These commands create a local HTML form that posts a ZIP snapshot to Overleaf and optionally opens it in a browser. They do not establish ongoing sync.

### Pull Shared Overleaf Edits

```bash
python3 scripts/overleaf_bridge.py pull --repo "$PWD"
```

- Fetches `overleaf/master` into the bridge repo
- Imports only `two_way` mappings back into the main repo
- Refuses to overwrite dirty working-tree changes in the mapped local paths

### Push Local Canonical Changes

```bash
python3 scripts/overleaf_bridge.py push --repo "$PWD"
```

- Allowed only from the configured `canonical_branch`
- Exports configured mappings into the bridge repo
- Blocks risky layout changes on comment-sensitive files
- Pushes `HEAD:master` to Overleaf

### Safe Branch Workflow

- Use `sync` and `push` only from the shared canonical branch.
- Use `preview` from feature branches.
- Keep generated outputs in `export_only` mappings.

## Guardrails

- No auto-polling. Sync is explicit.
- Symlinks, Git LFS pointers, nested submodules, and oversize exports are blocked.
- Risky rename or move-heavy pushes on comment-sensitive files are blocked.
- The skill does not promise preservation of Overleaf comments or track-changes metadata through Git round-trips.
- Ask coauthors to label versions before a `pull` when there were substantial Overleaf-side edits.

## When To Read The Reference File

Read `references/overleaf_constraints.md` when:

- you need a sample `.overleaf-bridge.toml`
- you need the Overleaf size and file-count limits enforced by `doctor`
- you need the exact rationale for `/devs` vs Git integration
- you need to explain why Overleaf GitHub sync should not be combined with this bridge
