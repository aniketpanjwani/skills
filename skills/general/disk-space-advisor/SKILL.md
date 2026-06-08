---
name: disk-space-advisor
description: Evidence-first disk cleanup and external-drive storage decisions for macOS/Linux. Use when the user asks what is using disk space, how to free hard-drive space, what can be deleted safely, what should be archived to an external drive, or how to build a cleanup decision log.
---

# Disk Space Advisor

Use this skill to turn disk-usage scans into safe decisions: `Keep local`, `Delete`, `Archive external`, `Change workflow`, or `Defer`.

## Core Rules

- Inspect first. Treat disk scans as inventory, not permission.
- Do not delete, move, archive, symlink, unmount, kill processes, empty Trash, or mark cloud files online-only until the user approves the exact paths or app-level actions.
- Never use size alone as the reason to delete. Check active use, source-of-truth status, rebuild cost, duplication, and open handles.
- Prefer reversible actions first: archive or app-supported online-only/offload behavior before permanent deletion, unless the data is clearly regenerable cache/build output.
- For repos and worktrees, inspect git status before recommending delete or archive. Protect uncommitted work, unpushed branches, detached states, and untracked payloads until reviewed.
- For external drives, verify the exact mounted path, free space, and intended archive layout before moving anything.
- Do not hardcode personal paths, drive names, or user-specific policies in shared instructions. Use placeholders such as `/Volumes/<drive-name>`, `/mnt/<drive-name>`, or `<archive-root>`.

## Quick Start

Run the read-only inventory from this skill's repo root:

```bash
python3 skills/general/disk-space-advisor/scripts/disk_space_inventory.py "$HOME" --min-gb 1 --top 40
```

Inspect a narrower area:

```bash
python3 skills/general/disk-space-advisor/scripts/disk_space_inventory.py "$HOME/Projects" --min-gb 0.5 --top 50
```

Include an external archive destination in the filesystem summary:

```bash
python3 skills/general/disk-space-advisor/scripts/disk_space_inventory.py "$HOME/Projects" \
  --external-path "/Volumes/<drive-name>" \
  --top 40
```

Save JSON for a decision log:

```bash
python3 skills/general/disk-space-advisor/scripts/disk_space_inventory.py "$HOME" \
  --json /tmp/disk-space-inventory.json
```

The script is read-only. It reports filesystem free space, large paths, conservative classifications, suggested outcomes, and git evidence for repo-like paths.

## Workflow

1. Establish the target:
   - current free space with `df -h`
   - the user's free-space goal, if any
   - scope: `$HOME`, a project directory, Downloads, app support folders, caches, cloud storage, or an external drive
2. Run a read-only inventory:
   - use `scripts/disk_space_inventory.py` for a first pass
   - use `du`, `find`, app CLIs, or platform tools for narrower follow-up checks
3. Convert large paths into decision buckets:
   - `Keep local`: active, source of truth, hard to recreate, or needed offline
   - `Delete`: regenerable, stale, duplicate, backup-like, failed, or low recovery value
   - `Archive external`: valuable, cold, annoying to recreate, and not needed weekly
   - `Change workflow`: recurring buildup from caches, worktrees, generated output, app data, or repeated local media copies
   - `Defer`: insufficient evidence, sensitive app state, unclear ownership, or possible active value
4. Verify risky candidates:
   - `git status --short --branch` for repos and worktrees
   - open handles with `lsof` before removing active-looking directories
   - app/source-of-truth status before deleting non-cache data
   - external drive free space and mount path before archive moves
5. Present a ranked recommendation list before mutation:
   - expected space
   - proposed outcome
   - why
   - risk level
   - exact action only after user approval
6. After approved action, verify and record:
   - removed, archived, or offloaded paths
   - actual size change
   - filesystem free-space change
   - archive readability when applicable
   - app/repo caveats when applicable

## Decision Rubric

Ask these questions in order:

1. Is it active right now?
2. Is it the source of truth?
3. Is it easy to rebuild or re-download?
4. Is it duplicated elsewhere?
5. Is it valuable but cold?
6. Does it keep growing back?

Likely mappings:

- active plus source of truth: `Keep local`
- not source of truth plus easy to rebuild: `Delete`
- valuable plus cold: `Archive external`
- recurring buildup: `Change workflow`
- unclear ownership, dirty git state, sensitive app data, or uncertain backup: `Defer`

## Common Safe-ish Cleanup Patterns

Use native tools where possible:

- Node/Bun/pnpm caches:
  - prefer `pnpm store prune` over deleting the pnpm store by hand
  - prefer package-manager cache commands when available
- Docker:
  - inspect first with `docker system df -v`
  - prune only approved images, containers, volumes, or build cache
- Xcode/iOS:
  - `~/Library/Developer/Xcode/DerivedData` is rebuildable
  - use `xcrun simctl list` and `xcrun simctl delete <device|unavailable|all>` for simulators after approval
- Android:
  - emulator AVDs are often large; delete only after confirming the user no longer needs them
- Rust:
  - `target/` is usually rebuildable; `.cargo` and toolchains are more workflow-sensitive
- Python:
  - `.venv`, `.mypy_cache`, `.pytest_cache`, and `__pycache__` are usually rebuildable
- Cloud storage:
  - prefer provider-supported "online-only" or "free up space" actions over raw file deletion
  - verify whether files are placeholders before assuming their apparent cloud size is local disk usage

## External Drive Policy

Use external storage when all are true:

- the data is valuable
- it is not needed weekly
- recreating it would be annoying, slow, or impossible
- keeping it local competes with active development or daily working space

Avoid external archive when:

- the data is only a cache or build artifact
- the data should be deleted outright
- the data is active enough that plugging in a drive every week would create friction

Before archiving:

```bash
df -h "/Volumes/<drive-name>" 2>/dev/null || df -h "/mnt/<drive-name>"
```

After archiving, verify with the archive format's listing command, for example:

```bash
tar -tf "<archive>.tar" >/dev/null
```

## Optional Project Catalog Integration

If the user refers to a project by nickname and a project-catalog skill or local catalog is available, resolve the project first. Do not require project-catalog; explicit paths are enough.

Example:

```bash
python3 skills/general/project-catalog/scripts/project_catalog.py resolve "<project nickname>" --json
```

If multiple matches are returned, do not choose silently. Show candidates and ask the user to pick.

## Decision Log

For multi-step cleanup sessions, create a local decision log before mutation. Use `templates/decision-log.md` as a starting point.

Record:

- baseline free space
- inspected candidates
- user-approved exact actions
- archive destination and verification
- final free space
- deferred or keep-local decisions

## Response Shape

Lead with the operational state:

- current free space
- biggest storage buckets
- best first decisions
- unsafe or ambiguous candidates

Then give a short table:

| Candidate | Size | Proposed outcome | Confidence | Why | Next check/action |
| --- | ---: | --- | --- | --- | --- |

End with a clear approval gate for any mutation. If the user has not approved a specific operation, stop at recommendations.
