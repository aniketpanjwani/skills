#!/usr/bin/env python3
"""
Persistent memory manager for python-learning-coach.

Stores:
- references/memory/profile.json (canonical learner state)
- references/memory/profile.md (searchable summary for QMD)
- references/memory/daily/YYYY-MM-DD.md (daily Q/A logs)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

MAX_STRENGTHS = 12
MAX_GAPS = 12
MAX_GOALS = 10
MAX_TOPICS = 20

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_MEMORY_ROOT = SCRIPT_DIR.parent / "references" / "memory"
QMD_INSTALL_COMMAND = "bun install -g https://github.com/tobi/qmd"
UV_INSTALL_URL = "https://docs.astral.sh/uv/getting-started/installation/"


def now_local() -> datetime:
    return datetime.now().astimezone()


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def default_profile(ts: str) -> dict[str, Any]:
    return {
        "learner_id": "default",
        "ability_level": "beginner",
        "mastery_score": 35.0,
        "sessions_logged": 0,
        "last_updated": ts,
        "strengths": [],
        "gaps": ["Needs continued Python fundamentals practice"],
        "next_goals": ["Build confidence with variables, loops, and functions"],
        "topic_counts": {},
        "last_session_notes": "No sessions logged yet.",
    }


def ensure_memory_paths(root: Path) -> tuple[Path, Path, Path]:
    root.mkdir(parents=True, exist_ok=True)
    daily_dir = root / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    profile_json = root / "profile.json"
    profile_md = root / "profile.md"
    return profile_json, profile_md, daily_dir


def load_profile(root: Path) -> dict[str, Any]:
    profile_json, _, _ = ensure_memory_paths(root)
    if not profile_json.exists():
        profile = default_profile(now_local().isoformat(timespec="seconds"))
        save_profile(root, profile)
        return profile
    with profile_json.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def unique_recent(existing: list[str], additions: list[str], limit: int) -> list[str]:
    ordered = [item.strip() for item in existing if item and item.strip()]
    for item in additions:
        normalized = item.strip()
        if not normalized:
            continue
        if normalized in ordered:
            ordered.remove(normalized)
        ordered.insert(0, normalized)
    return ordered[:limit]


def level_from_mastery(score: float) -> str:
    if score < 30:
        return "novice"
    if score < 55:
        return "beginner"
    if score < 75:
        return "intermediate"
    return "advanced"


def render_profile_markdown(profile: dict[str, Any]) -> str:
    strengths = profile.get("strengths", [])
    gaps = profile.get("gaps", [])
    goals = profile.get("next_goals", [])
    topic_counts = profile.get("topic_counts", {})

    def bullets(items: list[str], fallback: str) -> str:
        if not items:
            return f"- {fallback}"
        return "\n".join(f"- {item}" for item in items)

    sorted_topics = sorted(topic_counts.items(), key=lambda pair: (-pair[1], pair[0]))
    topic_lines = "\n".join(f"- {topic}: {count}" for topic, count in sorted_topics)
    if not topic_lines:
        topic_lines = "- No topics logged yet."

    return textwrap.dedent(
        f"""\
        # Python Learner Profile

        - Learner ID: {profile.get("learner_id", "default")}
        - Ability Level: {profile.get("ability_level", "beginner")}
        - Mastery Score: {profile.get("mastery_score", 0.0):.2f} / 100
        - Sessions Logged: {profile.get("sessions_logged", 0)}
        - Last Updated: {profile.get("last_updated", "unknown")}

        ## Strengths
        {bullets(strengths, "No strengths tracked yet.")}

        ## Gaps
        {bullets(gaps, "No gaps tracked yet.")}

        ## Next Goals
        {bullets(goals, "No goals tracked yet.")}

        ## Recent Topics
        {topic_lines}

        ## Last Session Notes
        {profile.get("last_session_notes", "No session notes available.")}
        """
    ).strip() + "\n"


def save_profile(root: Path, profile: dict[str, Any]) -> None:
    profile_json, profile_md, _ = ensure_memory_paths(root)
    with profile_json.open("w", encoding="utf-8") as handle:
        json.dump(profile, handle, indent=2, sort_keys=True)
        handle.write("\n")
    profile_md.write_text(render_profile_markdown(profile), encoding="utf-8")


def detect_qmd() -> dict[str, Any]:
    qmd_bin = shutil.which("qmd")
    if not qmd_bin:
        return {
            "installed": False,
            "path": None,
            "status_ok": False,
            "status_output": "",
            "error": "qmd binary is not on PATH.",
        }

    try:
        result = subprocess.run(["qmd", "status"], capture_output=True, text=True, check=False)
    except Exception as exc:  # noqa: BLE001
        return {
            "installed": True,
            "path": qmd_bin,
            "status_ok": False,
            "status_output": "",
            "error": f"Could not run `qmd status`: {exc}",
        }

    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    return {
        "installed": True,
        "path": qmd_bin,
        "status_ok": result.returncode == 0,
        "status_output": output or error,
        "error": "" if result.returncode == 0 else "qmd is installed, but `qmd status` failed.",
    }


def detect_uv() -> dict[str, Any]:
    uv_bin = shutil.which("uv")
    return {
        "installed": bool(uv_bin),
        "path": uv_bin,
        "error": "" if uv_bin else f"Install uv: {UV_INSTALL_URL}",
    }


def print_uv_check() -> None:
    uv = detect_uv()
    print("# uv Check")
    print(f"- Installed: {'yes' if uv['installed'] else 'no'}")
    if uv["path"]:
        print(f"- Path: {uv['path']}")
    if uv["error"]:
        print(f"- Next step: {uv['error']}")


def print_qmd_check() -> None:
    qmd = detect_qmd()
    print("# QMD Check")
    print(f"- Installed: {'yes' if qmd['installed'] else 'no'}")
    if qmd["path"]:
        print(f"- Path: {qmd['path']}")
    print(f"- `qmd status` healthy: {'yes' if qmd['status_ok'] else 'no'}")

    if qmd["status_output"]:
        print("")
        print("## qmd status output")
        print(qmd["status_output"])

    if qmd["error"]:
        print("")
        print("## Next Steps")
        print(f"- Install qmd: `{QMD_INSTALL_COMMAND}`")
        print("- Verify install: `qmd status`")
        print("- Refresh index after log updates: `qmd update`")


def in_virtual_environment() -> bool:
    return bool(os.environ.get("VIRTUAL_ENV")) or sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def format_code_block(text: str) -> str:
    payload = text.strip()
    if not payload:
        return "```text\n(empty)\n```"
    return f"```text\n{payload}\n```"


def append_daily_entry(
    *,
    daily_dir: Path,
    now: datetime,
    session_number: int,
    question: str,
    answer: str,
    source: str,
    topics: list[str],
    difficulty: int,
    confidence: int,
    correctness: float,
    delta: float,
    before: float,
    after: float,
    level: str,
    strengths: list[str],
    gaps: list[str],
    goals: list[str],
) -> Path:
    date_str = now.strftime("%Y-%m-%d")
    file_path = daily_dir / f"{date_str}.md"

    if not file_path.exists():
        file_path.write_text(f"# Python Learning Log - {date_str}\n\n", encoding="utf-8")

    topics_display = ", ".join(topics) if topics else "unspecified"
    strengths_md = "\n".join(f"- {item}" for item in strengths) or "- none"
    gaps_md = "\n".join(f"- {item}" for item in gaps) or "- none"
    goals_md = "\n".join(f"- {item}" for item in goals) or "- none"
    delta_prefix = "+" if delta >= 0 else ""
    entry = (
        f"## Session {session_number} - {now.strftime('%H:%M:%S')}\n\n"
        f"- Timestamp: {now.isoformat(timespec='seconds')}\n"
        f"- Source: {source}\n"
        f"- Topics: {topics_display}\n"
        f"- Difficulty: {difficulty}/5\n"
        f"- Confidence: {confidence}/5\n"
        f"- Correctness: {correctness:.2f}\n"
        f"- Mastery Delta: {delta_prefix}{delta:.2f} ({before:.2f} -> {after:.2f})\n"
        f"- Updated Level: {level}\n\n"
        f"### Learner Question\n"
        f"{format_code_block(question)}\n\n"
        f"### Tutor Answer\n"
        f"{format_code_block(answer)}\n\n"
        f"### Strengths Observed\n"
        f"{strengths_md}\n\n"
        f"### Gaps Observed\n"
        f"{gaps_md}\n\n"
        f"### Next Goals\n"
        f"{goals_md}\n\n"
    )

    with file_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)

    return file_path


def cmd_init(root: Path) -> None:
    profile = load_profile(root)
    save_profile(root, profile)
    print(f"Initialized memory root: {root}")
    print(f"Profile file: {root / 'profile.json'}")
    print(f"Profile summary: {root / 'profile.md'}")
    print(f"Daily logs directory: {root / 'daily'}")
    print("")
    print_uv_check()
    print("")
    print_qmd_check()


def summarize_recent_logs(daily_dir: Path, days: int) -> str:
    log_files = sorted(daily_dir.glob("*.md"), reverse=True)[: max(days, 1)]
    if not log_files:
        return "No daily logs yet."

    lines: list[str] = []
    for path in log_files:
        content = path.read_text(encoding="utf-8")
        sessions = 0
        topic_lines = [
            stripped.removeprefix("- Topics: ").strip()
            for line in content.splitlines()
            for stripped in [line.strip()]
            if stripped.startswith("- Topics: ")
        ]
        for line in content.splitlines():
            if line.strip().startswith("## Session "):
                sessions += 1
        topic_preview = ", ".join(topic_lines[-3:]) if topic_lines else "none"
        lines.append(
            f"- {path.name}: {sessions} session(s); recent topics: {topic_preview}; path: {path}"
        )
    return "\n".join(lines)


def cmd_snapshot(root: Path, days: int) -> None:
    profile = load_profile(root)
    _, _, daily_dir = ensure_memory_paths(root)

    topic_counts = profile.get("topic_counts", {})
    sorted_topics = sorted(topic_counts.items(), key=lambda pair: (-pair[1], pair[0]))[:10]
    topics_line = ", ".join(f"{topic} ({count})" for topic, count in sorted_topics)
    if not topics_line:
        topics_line = "none"

    print("# Python Learning Snapshot")
    print(f"- Generated: {now_local().isoformat(timespec='seconds')}")
    print(f"- Ability Level: {profile.get('ability_level', 'beginner')}")
    print(f"- Mastery Score: {profile.get('mastery_score', 0.0):.2f}")
    print(f"- Sessions Logged: {profile.get('sessions_logged', 0)}")
    print(f"- Last Updated: {profile.get('last_updated', 'unknown')}")
    print(f"- Top Topics: {topics_line}")
    print("")

    print("## Strengths")
    strengths = profile.get("strengths", [])
    if strengths:
        for item in strengths:
            print(f"- {item}")
    else:
        print("- none")
    print("")

    print("## Gaps")
    gaps = profile.get("gaps", [])
    if gaps:
        for item in gaps:
            print(f"- {item}")
    else:
        print("- none")
    print("")

    print("## Next Goals")
    goals = profile.get("next_goals", [])
    if goals:
        for item in goals:
            print(f"- {item}")
    else:
        print("- none")
    print("")

    print("## Daily Logs (Most Recent First)")
    print(summarize_recent_logs(daily_dir=daily_dir, days=days))


def cmd_doctor(root: Path) -> None:
    uv = detect_uv()
    venv_active = in_virtual_environment()

    print("# Environment Doctor")
    print(f"- Memory root: {root}")
    print(f"- Python executable: {sys.executable}")
    print(f"- Virtual environment active: {'yes' if venv_active else 'no'}")
    print(f"- uv installed: {'yes' if uv['installed'] else 'no'}")
    if uv["path"]:
        print(f"- uv path: {uv['path']}")
    else:
        print(f"- Install uv: {UV_INSTALL_URL}")

    print("")
    print_qmd_check()

    if not venv_active:
        print("")
        print("## Recommended uv workflow")
        print("- Create environment: `uv venv`")
        print("- Activate environment: `source .venv/bin/activate`")
        print("- Run helper script: `uv run python3 scripts/python_learning_memory.py snapshot --days 5`")
    else:
        print("")
        print("## Environment status")
        print("- Virtual environment is active. Continue using `uv run` or `python3`.")


def cmd_record(args: argparse.Namespace, root: Path) -> None:
    if not (0.0 <= args.correctness <= 1.0):
        raise ValueError("--correctness must be between 0.0 and 1.0")

    profile = load_profile(root)
    _, _, daily_dir = ensure_memory_paths(root)
    now = now_local()

    before = float(profile.get("mastery_score", 25.0))
    confidence_norm = (args.confidence - 1) / 4
    signal = 0.7 * args.correctness + 0.3 * confidence_norm
    difficulty_factor = 0.8 + (args.difficulty - 1) * 0.1
    delta = (signal - 0.5) * 4 * difficulty_factor
    after = round(clamp(before + delta, 0.0, 100.0), 2)
    level = level_from_mastery(after)

    profile["mastery_score"] = after
    profile["ability_level"] = level
    profile["sessions_logged"] = int(profile.get("sessions_logged", 0)) + 1
    profile["last_updated"] = now.isoformat(timespec="seconds")
    profile["last_session_notes"] = (
        f"{now.strftime('%Y-%m-%d %H:%M:%S')} | topics={', '.join(args.topic or ['unspecified'])} "
        f"| delta={delta:+.2f} | level={level}"
    )

    profile["strengths"] = unique_recent(
        profile.get("strengths", []), args.strength or [], MAX_STRENGTHS
    )
    profile["gaps"] = unique_recent(profile.get("gaps", []), args.gap or [], MAX_GAPS)
    profile["next_goals"] = unique_recent(profile.get("next_goals", []), args.next_goal or [], MAX_GOALS)

    topics = [topic.strip().lower() for topic in (args.topic or []) if topic.strip()]
    topic_counts = profile.get("topic_counts", {})
    for topic in topics:
        topic_counts[topic] = int(topic_counts.get(topic, 0)) + 1
    sorted_topics = sorted(topic_counts.items(), key=lambda pair: (-pair[1], pair[0]))[:MAX_TOPICS]
    profile["topic_counts"] = {topic: count for topic, count in sorted_topics}

    daily_file = append_daily_entry(
        daily_dir=daily_dir,
        now=now,
        session_number=profile["sessions_logged"],
        question=args.question,
        answer=args.answer,
        source=args.source,
        topics=topics,
        difficulty=args.difficulty,
        confidence=args.confidence,
        correctness=args.correctness,
        delta=delta,
        before=before,
        after=after,
        level=level,
        strengths=args.strength or [],
        gaps=args.gap or [],
        goals=args.next_goal or [],
    )

    save_profile(root, profile)

    print("Recorded interaction and updated profile.")
    print(f"Profile: {root / 'profile.json'}")
    print(f"Profile summary: {root / 'profile.md'}")
    print(f"Daily log: {daily_file}")
    print(f"New mastery score: {after:.2f}")
    print(f"Ability level: {level}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Memory manager for python-learning-coach skill.")
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_MEMORY_ROOT,
        help=f"Memory root directory (default: {DEFAULT_MEMORY_ROOT})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create memory files if missing.")
    subparsers.add_parser("qmd-check", help="Detect qmd install and print setup guidance.")
    subparsers.add_parser("doctor", help="Check Python, uv, virtual environment, and qmd status.")

    snapshot = subparsers.add_parser("snapshot", help="Print learner profile and recent logs.")
    snapshot.add_argument("--days", type=int, default=5, help="Number of recent daily logs to summarize.")

    record = subparsers.add_parser("record", help="Append a tutoring interaction and update profile.")
    record.add_argument("--question", required=True, help="Learner question text.")
    record.add_argument("--answer", required=True, help="Tutor answer text.")
    record.add_argument("--topic", action="append", help="Topic tag. Repeat for multiple topics.")
    record.add_argument("--difficulty", type=int, choices=range(1, 6), default=3, help="Session difficulty (1-5).")
    record.add_argument("--confidence", type=int, choices=range(1, 6), default=3, help="Learner confidence (1-5).")
    record.add_argument("--correctness", type=float, default=0.6, help="Estimated correctness (0.0-1.0).")
    record.add_argument("--strength", action="append", help="Observed strength. Repeat as needed.")
    record.add_argument("--gap", action="append", help="Observed gap. Repeat as needed.")
    record.add_argument("--next-goal", action="append", help="Next goal. Repeat as needed.")
    record.add_argument("--source", default="assistant", help="Session source label (e.g., codex, claude, chat).")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    root = args.root.resolve()

    if args.command == "init":
        cmd_init(root)
        return

    if args.command == "snapshot":
        cmd_snapshot(root=root, days=args.days)
        return

    if args.command == "qmd-check":
        print_uv_check()
        print("")
        print_qmd_check()
        return

    if args.command == "doctor":
        cmd_doctor(root=root)
        return

    if args.command == "record":
        cmd_record(args=args, root=root)
        return

    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
