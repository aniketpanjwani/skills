#!/usr/bin/env python3
"""Read-only disk-space inventory for cleanup decisions.

This script ranks large paths and attaches conservative decision hints. It never
deletes, moves, archives, or mutates files.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


GIB = 1024**3


@dataclass
class FilesystemInfo:
    path: str
    total_gb: float
    used_gb: float
    free_gb: float


@dataclass
class Candidate:
    path: str
    size_gb: float
    size_human: str
    category: str
    suggested_outcome: str
    confidence: str
    rationale: str
    git_state: str | None = None
    open_handles: str | None = None


def run(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def human_size(size_bytes: int) -> str:
    value = float(size_bytes)
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if value < 1024 or unit == "TiB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TiB"


def disk_usage(path: Path) -> FilesystemInfo | None:
    try:
        usage = shutil.disk_usage(path)
    except OSError:
        return None

    return FilesystemInfo(
        path=str(path),
        total_gb=round(usage.total / GIB, 2),
        used_gb=round(usage.used / GIB, 2),
        free_gb=round(usage.free / GIB, 2),
    )


def parse_du_line(line: str) -> tuple[int, Path] | None:
    parts = line.rstrip("\n").split("\t", 1)
    if len(parts) != 2:
        parts = line.strip().split(None, 1)
    if len(parts) != 2:
        return None
    try:
        kib = int(parts[0])
    except ValueError:
        return None
    return kib * 1024, Path(parts[1])


def collect_du(target: Path, depth: int) -> list[tuple[int, Path]]:
    result = run(["du", "-k", "-d", str(depth), str(target)], timeout=300)
    if result.returncode != 0 and not result.stdout:
        result = run(["du", "-k", str(target)], timeout=300)

    entries: list[tuple[int, Path]] = []
    for line in result.stdout.splitlines():
        parsed = parse_du_line(line)
        if parsed:
            entries.append(parsed)
    return entries


def classify(path: Path) -> tuple[str, str, str, str]:
    lower = str(path).lower()
    name = path.name.lower()
    parts = {part.lower() for part in path.parts}

    if name in {"node_modules", ".next", "target", "dist", "build", ".turbo"}:
        return (
            "generated dependency/build output",
            "Delete",
            "medium",
            "usually rebuildable; verify no unusual generated source lives inside",
        )
    if "cache" in lower or "caches" in parts:
        return (
            "cache",
            "Delete",
            "high",
            "cache-like data is usually rebuildable or re-downloadable",
        )
    if name in {"tmp", "temp"} or "/tmp/" in lower or "temporary" in lower:
        return (
            "temporary data",
            "Delete",
            "medium",
            "temporary data is often safe after checking age and open handles",
        )
    if any(token in lower for token in ["backup", ".old", "quarantine", "archive"]):
        return (
            "historical or backup-like data",
            "Delete or Archive external",
            "medium",
            "looks stale or historical; decide whether it has recovery value",
        )
    if name == ".git" or ".git" in parts:
        return (
            "git repository data",
            "Keep local or Change workflow",
            "low",
            "repo history may be useful; inspect status and remotes before cleanup",
        )
    if "downloads" in parts:
        return (
            "downloads",
            "Delete or Archive external",
            "medium",
            "downloads often contain installers, media, and one-off artifacts",
        )
    if any(name.endswith(ext) for ext in [".dmg", ".pkg", ".iso", ".zip", ".tar", ".gz"]):
        return (
            "installer or archive file",
            "Delete or Archive external",
            "medium",
            "large archives may be redundant if installed or backed up elsewhere",
        )
    if any(token in lower for token in ["reference_repos", "reference-repos", "corpus", "dataset"]):
        return (
            "valuable cold data",
            "Archive external",
            "medium",
            "reference or corpus-like data is often valuable but not daily-use",
        )

    return (
        "needs review",
        "Defer",
        "low",
        "needs active-use, source-of-truth, and rebuild-cost checks",
    )


def git_state(path: Path) -> str | None:
    probe = path if path.is_dir() else path.parent
    result = run(["git", "-C", str(probe), "rev-parse", "--show-toplevel"], timeout=10)
    if result.returncode != 0:
        return None

    root = result.stdout.strip()
    status = run(["git", "-C", root, "status", "--short", "--branch"], timeout=20)
    if status.returncode != 0:
        return f"git repo: {root}; status unavailable"

    lines = [line.strip() for line in status.stdout.splitlines() if line.strip()]
    summary = "; ".join(lines[:6])
    if len(lines) > 6:
        summary += f"; ... {len(lines) - 6} more lines"
    return f"git repo: {root}; {summary or 'clean status output'}"


def open_handle_state(path: Path) -> str:
    if not shutil.which("lsof"):
        return "lsof unavailable"
    result = run(["lsof", "+D", str(path)], timeout=20)
    if result.returncode == 0 and result.stdout.strip():
        count = max(0, len(result.stdout.splitlines()) - 1)
        return f"{count} open handle rows found"
    return "no open handles found by lsof +D"


def build_candidates(
    target: Path,
    min_gb: float,
    top: int,
    depth: int,
    check_open_handles: bool,
) -> list[Candidate]:
    min_bytes = int(min_gb * GIB)
    entries = collect_du(target, depth)
    candidates: list[Candidate] = []

    for size_bytes, path in entries:
        if path.resolve() == target.resolve() or size_bytes < min_bytes:
            continue
        category, outcome, confidence, rationale = classify(path)
        candidate = Candidate(
            path=str(path),
            size_gb=round(size_bytes / GIB, 2),
            size_human=human_size(size_bytes),
            category=category,
            suggested_outcome=outcome,
            confidence=confidence,
            rationale=rationale,
            git_state=git_state(path),
        )
        if check_open_handles:
            candidate.open_handles = open_handle_state(path)
        candidates.append(candidate)

    candidates.sort(key=lambda item: item.size_gb, reverse=True)
    return candidates[:top]


def print_table(filesystems: Iterable[FilesystemInfo], candidates: list[Candidate]) -> None:
    print("FILESYSTEMS")
    for fs in filesystems:
        print(
            f"- {fs.path}: {fs.free_gb:.2f} GiB free / "
            f"{fs.total_gb:.2f} GiB total"
        )

    print("\nLARGE CANDIDATES")
    print("Note: nested rows can overlap; do not sum all rows as reclaimable space.\n")
    for index, item in enumerate(candidates, 1):
        print(f"{index}. {item.path}")
        print(f"   Size: {item.size_human} ({item.size_gb:.2f} GiB)")
        print(f"   Category: {item.category}")
        print(f"   Suggested outcome: {item.suggested_outcome} ({item.confidence} confidence)")
        print(f"   Why: {item.rationale}")
        if item.git_state:
            print(f"   Git: {item.git_state}")
        if item.open_handles:
            print(f"   Open handles: {item.open_handles}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=str(Path.home()))
    parser.add_argument("--min-gb", type=float, default=1.0)
    parser.add_argument("--top", type=int, default=30)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--external-path", action="append", default=[])
    parser.add_argument("--check-open-handles", action="store_true")
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 2

    fs_paths = [target] + [Path(path).expanduser().resolve() for path in args.external_path]
    filesystems = [info for path in fs_paths if (info := disk_usage(path))]
    candidates = build_candidates(
        target=target,
        min_gb=args.min_gb,
        top=args.top,
        depth=args.depth,
        check_open_handles=args.check_open_handles,
    )

    output = {
        "target": str(target),
        "filesystems": [asdict(item) for item in filesystems],
        "candidates": [asdict(item) for item in candidates],
    }

    if args.json_path:
        json_path = Path(args.json_path).expanduser()
        json_path.write_text(json.dumps(output, indent=2) + "\n")
        print(f"Wrote JSON inventory to {json_path}")

    print_table(filesystems, candidates)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
