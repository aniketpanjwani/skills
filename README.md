# Skills

<p align="center"><strong>Created by Aniket Panjwani, PhD</strong></p>
<p align="center">
  <a href="https://ai-mba.io"><strong>Website: ai-mba.io</strong></a> |
  <a href="https://www.youtube.com/@aniketapanjwani"><strong>YouTube: @aniketapanjwani</strong></a> |
  <a href="https://www.skool.com/the-ai-mba"><strong>Learn with 1000+ AI Devs</strong></a>

</p>

A set of skills created by Aniket Panjwani. The skills are usable through Codex and Claude Code. The repo comes with a bootstrap script to easily install all of them. 

There are two general sets of skills: ones for anyone/any developer, and others specifically for economists/social scientists/academics.

## Repo Layout

```text
.
├── README.md
├── scripts/
│   └── bootstrap.sh
└── skills/
    ├── general/
    │   └── starter-public-skill/
    │       └── SKILL.md
    └── economists/
        └── economist-briefing/
            └── SKILL.md
```

## Install Targets and Scope

Targets:

- `codex`
- `claude`
- `both` (simultaneous install)

Scopes:

- Global: `~/.codex/skills`, `~/.claude/skills`
- Project: `<project>/.codex/skills`, `<project>/.claude/skills`

## 1) Clone

```bash
git clone https://github.com/aniketpanjwani/public-agent-skills.git ~/projects/public-agent-skills
cd ~/projects/public-agent-skills
chmod +x scripts/bootstrap.sh
```

If your repo URL/path is different, replace those values.

## 2) Install All Skills

Global install for both Codex + Claude:

```bash
./scripts/bootstrap.sh --target both --scope global
```

Project-level install for both:

```bash
./scripts/bootstrap.sh --target both --scope project --project-dir /path/to/project
```

## 3) Let Users Choose What They Install

List available skills and types:

```bash
./scripts/bootstrap.sh --list
```

Install only specific skills:

```bash
./scripts/bootstrap.sh --target both --scope global --skills starter-public-skill,economist-briefing
```

Install by type (bundle):

```bash
./scripts/bootstrap.sh --target both --scope global --type economists
```

Install a union of type + specific skill:

```bash
./scripts/bootstrap.sh --target both --scope global --type economists --skills starter-public-skill
```

## Non-Destructive Behavior (Existing User Skills Stay Safe)

By default:

- Existing personal skills are untouched.
- Conflicts are skipped.
- Matching symlinks are left as-is.

Use `--force` only when you explicitly want replacements:

```bash
./scripts/bootstrap.sh --target both --scope global --type economists --force
```

## Update Flow

Users can keep this repo synced and get new/updated skills:

```bash
git pull
./scripts/bootstrap.sh --target both --scope global
```

If they installed with symlink mode (default), updated skill content is reflected immediately after pull.

## Optional Modes

Dry run:

```bash
./scripts/bootstrap.sh --target both --scope global --dry-run
```

Copy mode (instead of symlink mode):

```bash
./scripts/bootstrap.sh --target both --scope global --copy
```

## How To Organize Skills By Audience

Use subdirectories under `skills/`:

- `skills/general/<skill>/SKILL.md`
- `skills/economists/<skill>/SKILL.md`
- add more types as needed (for example `founders`, `students`)

Then users can install by `--type`.

Important:

- Skill folder names must be globally unique, even across different types.

## License

MIT
