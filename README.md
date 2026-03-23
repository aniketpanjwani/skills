# Skills

<p align="center"><strong>Created by Aniket Panjwani, PhD</strong></p>
<p align="center">
  <a href="https://ai-mba.io"><strong>Website: ai-mba.io</strong></a> |
  <a href="https://www.youtube.com/@aniketapanjwani"><strong>YouTube: @aniketapanjwani</strong></a> |
  <a href="https://www.skool.com/the-ai-mba"><strong>Learn with 1000+ AI Devs</strong></a>

</p>

A set of reusable skills for Codex, Claude Code, and Gemini CLI.

## Start Here (Simple)

Skills are small instruction packs that make your coding agent better at specific jobs.

- They help your agent follow a workflow instead of starting from scratch each time.
- You can install all skills, only some skills, or only one category.
- You can install for Codex, Claude, Gemini, or all.

### Easiest Path

Clone this repo, then ask your coding agent:

`Install this skills repo for me using scripts/bootstrap.sh for all tools globally.`

If you want to run it manually, this is the one command most people need:

```bash
./scripts/bootstrap.sh --target both --scope global
```

## Learn More (Video)

- [The Only Claude Code Skill You Need](https://youtu.be/MMpaPV3KMFI?si=b6PWSAtfawmk564R)
- [Claude Code Skills vs MCPs: Complete Beginner's Guide 2026](https://youtu.be/42nz2FfKA9A?si=EUTr1Daohu-unqiP)

## Skills Catalog

| Skill | Audience | What it does | Path |
|---|---|---|---|
| `pdf-reading` | General | Docling-first PDF reading with optional figure, image, and table extraction artifacts | `skills/general/pdf-reading` |
| `python-learning-coach` | General | Personalized Python tutoring with memory, daily logs, and level adaptation | `skills/general/python-learning-coach` |

## Install Options

### 1) Clone

```bash
git clone https://github.com/aniketpanjwani/skills.git ~/projects/skills
cd ~/projects/skills
chmod +x scripts/bootstrap.sh
```

### 2) Install all skills (global, all agents)

```bash
./scripts/bootstrap.sh --target both --scope global
```

### 3) Install all skills (project only)

```bash
./scripts/bootstrap.sh --target both --scope project --project-dir /path/to/project
```

### 4) Install only selected skills

```bash
./scripts/bootstrap.sh --target both --scope global --skills pdf-reading
```

### 5) Install by category/type

```bash
./scripts/bootstrap.sh --target both --scope global --type general
```

### 6) See what is available

```bash
./scripts/bootstrap.sh --list
```

## Technical Reference

### Targets

- `codex`
- `claude`
- `gemini`
- `both` (Installs for all of the above)

### Scopes

- Global: `~/.codex/skills`, `~/.claude/skills`, `~/.gemini/skills`
- Project: `<project>/.codex/skills`, `<project>/.claude/skills`, `<project>/.gemini/skills`

### Safe-by-default behavior

- Existing personal skills are not overwritten.
- Conflicts are skipped unless you pass `--force`.

Use `--force` only when you intentionally want to replace files:

```bash
./scripts/bootstrap.sh --target both --scope global --type general --force
```

### Update flow

```bash
git pull
./scripts/bootstrap.sh --target both --scope global
```

### Optional modes

Dry run:

```bash
./scripts/bootstrap.sh --target both --scope global --dry-run
```

Copy mode (instead of symlink mode):

```bash
./scripts/bootstrap.sh --target both --scope global --copy
```

## License

MIT
