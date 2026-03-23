# Skills Folder

Organize skills by audience/type. Shared skill content lives at the skill root, and
optional tool-specific overrides can live under `codex/`, `claude/`, or `gemini/`.

```text
skills/
  general/
    your-skill/
      SKILL.md
      scripts/
      codex/
        SKILL.md
      gemini/
        SKILL.md
  economists/
    your-skill/
      SKILL.md
```

You can also keep uncategorized skills at:

```text
skills/your-skill/SKILL.md
```

## Rules

- Every installable skill must have `SKILL.md`.
- Skill folder names must be globally unique across all types.
- Keep shared files in the skill root whenever possible.
- Tool-specific subdirectories are optional overlays. Their files are layered on top of the
  root skill for that tool rather than replacing the whole skill.
- If a tool-specific overlay exists, it must include its own `SKILL.md`.
- Keep secrets out of skills.

## Selection Examples

List catalog:

```bash
./scripts/bootstrap.sh --list
```

Install one type:

```bash
./scripts/bootstrap.sh --target both --scope global --type economists
```

Install two explicit skills:

```bash
./scripts/bootstrap.sh --target both --scope global --skills skill-a,skill-b
```
