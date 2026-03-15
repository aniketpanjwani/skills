# Overleaf Git Bridge Reference

This file is the compact reference for the `overleaf-git-bridge` skill. Load it when you need the config format, the official constraints, or the workflow rationale.

## Official Model

- Overleaf `/devs` imports LaTeX or files into Overleaf. Treat it as bootstrap or preview only.
- Overleaf Git integration is the steady-state sync surface. It is a single-branch workflow centered on Overleaf `master`.
- Overleaf creates Git commits just in time, so authorship can collapse to the latest editor if versions are not labeled.
- Overleaf comments and track changes can be displaced by Git or GitHub sync on affected files.
- Do not combine this bridge with Overleaf's direct GitHub synchronization on the same shared project.

## Config Format

Create `.overleaf-bridge.toml` at the repo root.

```toml
canonical_branch = "main"
main_document = "paper/main.tex"
engine = "xelatex"
visual_editor = false
overleaf_git_url = "https://git@git.overleaf.com/<project-id>"
bridge_repo_path = ".overleaf/paper/mirror"

[[mapping]]
local = "paper"
overleaf = "."
mode = "two_way"
comment_sensitive = true
exclude = [
  "build/**",
  "*.aux",
  "*.bbl",
  "*.bcf",
  "*.blg",
  "*.fdb_latexmk",
  "*.fls",
  "*.log",
  "*.out",
  "*.run.xml",
  "*.synctex.gz",
  ".DS_Store",
]

[[mapping]]
local = "results/tables"
overleaf = "generated/tables"
mode = "export_only"
comment_sensitive = false
exclude = []

[[mapping]]
local = "results/figures"
overleaf = "generated/figures"
mode = "export_only"
comment_sensitive = false
exclude = []
```

## Mapping Rules

- `two_way`: exported to Overleaf and imported back on `pull`
- `export_only`: exported to Overleaf but never imported back
- `main_document`: local repo path to the canonical `.tex` file; the bridge maps it into the Overleaf-relative path during bootstrap and preview
- `local`: path inside the main repo
- `overleaf`: path inside the Overleaf project root
- `exclude`: glob patterns relative to `local`
- `comment_sensitive`: enable conservative rename and move blocking for that mapping

## Safety Rules Enforced By The CLI

- Block symlinks in exported content.
- Block Git LFS pointer files in exported content.
- Block Git submodules inside mapped content.
- Block exports above:
  - 2,000 files
  - 7 MB of editable text
  - 2 MB for a single editable text file
  - 100 MB total project size
- Block risky rename or move-heavy pushes on comment-sensitive mappings.
- Refuse canonical `push` or `sync` from a non-canonical branch.
- Refuse `pull` if the main repo has dirty changes in `two_way` local paths.

## Recommended Workflow

1. Keep manuscript sources and bibliography in `two_way`.
2. Keep generated tables, figures, and appendices in `export_only`.
3. Use `preview` for feature branches.
4. Use `sync` from the canonical branch.
5. Ask coauthors to label versions before `pull`.

## Why Not Push The Whole Repo

- Overleaf is a constrained project workspace, not a general Git remote.
- Large repos and code-heavy trees hit size, file-count, and UX limits quickly.
- A filtered bridge preserves the monorepo ergonomics locally while keeping the shared Overleaf project clean.
