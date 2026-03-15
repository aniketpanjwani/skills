#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
import fnmatch
import html
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import tomllib
import webbrowser
import zipfile


EDITABLE_TEXT_SUFFIXES = {
    ".bbx",
    ".bib",
    ".bst",
    ".cbx",
    ".cfg",
    ".cls",
    ".csv",
    ".def",
    ".json",
    ".latexmkrc",
    ".md",
    ".pgf",
    ".Rnw",
    ".Rtex",
    ".sty",
    ".tex",
    ".tikz",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

DEFAULT_EXCLUDES = [
    ".DS_Store",
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
]

MAX_FILE_COUNT = 2000
MAX_EDITABLE_TOTAL_BYTES = 7 * 1024 * 1024
MAX_EDITABLE_FILE_BYTES = 2 * 1024 * 1024
MAX_PROJECT_BYTES = 100 * 1024 * 1024
MAX_BOOTSTRAP_ZIP_BYTES = 50 * 1024 * 1024
MASS_CHANGE_THRESHOLD = 10
REMOTE_NAME = "overleaf"
REMOTE_BRANCH = "master"


class BridgeError(RuntimeError):
    pass


@dataclass(frozen=True)
class Mapping:
    local: str
    overleaf: str
    mode: str
    exclude: tuple[str, ...]
    comment_sensitive: bool

    def local_path(self, repo_root: Path) -> Path:
        return repo_root / Path(self.local)

    def bridge_path(self, bridge_root: Path) -> Path:
        if self.overleaf in ("", "."):
            return bridge_root
        return bridge_root / Path(self.overleaf)

    def destination_for_export(self, source_root: Path, relative: Path) -> PurePosixPath:
        if source_root.is_file():
            if self.overleaf in ("", "."):
                return PurePosixPath(source_root.name)
            return PurePosixPath(self.overleaf)
        if self.overleaf in ("", "."):
            return PurePosixPath(relative.as_posix())
        return PurePosixPath(self.overleaf) / PurePosixPath(relative.as_posix())


@dataclass(frozen=True)
class Config:
    canonical_branch: str
    main_document: str
    engine: str
    visual_editor: bool
    overleaf_git_url: str
    bridge_repo_path: str
    mappings: tuple[Mapping, ...]

    def bridge_repo(self, repo_root: Path) -> Path:
        return repo_root / Path(self.bridge_repo_path)


@dataclass(frozen=True)
class ExportedFile:
    source: Path
    dest: PurePosixPath
    size: int
    is_text: bool
    mapping: Mapping


def run(
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=capture_output,
    )


def git(
    cwd: Path,
    *args: str,
    check: bool = True,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    return run("git", *args, cwd=cwd, check=check, capture_output=capture_output)


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def human_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(amount)} {unit}"
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{value} B"


def validate_relative_path(raw: str, label: str) -> str:
    if not raw:
        raise BridgeError(f"{label} must not be empty.")
    pure = PurePosixPath(raw)
    if pure.is_absolute():
        raise BridgeError(f"{label} must be repo-relative, not absolute: {raw}")
    if ".." in pure.parts:
        raise BridgeError(f"{label} must not contain '..': {raw}")
    normalized = pure.as_posix()
    if normalized in ("", "."):
        return "."
    return normalized.rstrip("/")


def normalize_overleaf_url(url: str) -> str:
    value = url.strip()
    if not value:
        return ""
    if "overleaf.com" not in value:
        raise BridgeError(
            "Overleaf Git URL must point at git.overleaf.com or overleaf.com."
        )
    return value


def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise BridgeError(f"Config file not found: {config_path}")
    data = tomllib.loads(config_path.read_text())
    mappings_raw = data.get("mapping")
    if not isinstance(mappings_raw, list) or not mappings_raw:
        raise BridgeError("Config must include at least one [[mapping]] entry.")
    mappings: list[Mapping] = []
    for index, entry in enumerate(mappings_raw, start=1):
        if not isinstance(entry, dict):
            raise BridgeError(f"mapping #{index} must be a TOML table.")
        local = validate_relative_path(str(entry.get("local", "")).strip(), f"mapping #{index} local")
        overleaf = validate_relative_path(
            str(entry.get("overleaf", "")).strip() or ".",
            f"mapping #{index} overleaf",
        )
        mode = str(entry.get("mode", "")).strip()
        if mode not in {"two_way", "export_only"}:
            raise BridgeError(
                f"mapping #{index} mode must be 'two_way' or 'export_only', got {mode!r}"
            )
        exclude_raw = entry.get("exclude", [])
        if exclude_raw is None:
            exclude_raw = []
        if not isinstance(exclude_raw, list):
            raise BridgeError(f"mapping #{index} exclude must be a TOML array.")
        exclude = tuple(str(item) for item in exclude_raw)
        comment_sensitive = bool(entry.get("comment_sensitive", mode == "two_way"))
        mappings.append(
            Mapping(
                local=local,
                overleaf=overleaf,
                mode=mode,
                exclude=exclude,
                comment_sensitive=comment_sensitive,
            )
        )

    config = Config(
        canonical_branch=str(data.get("canonical_branch", "")).strip() or "main",
        main_document=validate_relative_path(
            str(data.get("main_document", "")).strip(), "main_document"
        ),
        engine=str(data.get("engine", "")).strip() or "pdflatex",
        visual_editor=bool(data.get("visual_editor", False)),
        overleaf_git_url=normalize_overleaf_url(
            str(data.get("overleaf_git_url", "")).strip()
        ),
        bridge_repo_path=validate_relative_path(
            str(data.get("bridge_repo_path", "")).strip(), "bridge_repo_path"
        ),
        mappings=tuple(mappings),
    )
    validate_config(config)
    return config


def validate_config(config: Config) -> None:
    if not config.canonical_branch:
        raise BridgeError("canonical_branch must not be empty.")
    if not config.main_document.endswith(".tex"):
        raise BridgeError("main_document must point to a .tex file.")
    seen_two_way_local: list[PurePosixPath] = []
    seen_two_way_overleaf: list[PurePosixPath] = []
    for mapping in config.mappings:
        if mapping.mode == "two_way":
            local_path = PurePosixPath(mapping.local)
            overleaf_path = PurePosixPath(mapping.overleaf)
            for other in seen_two_way_local:
                if local_path == other or local_path.is_relative_to(other) or other.is_relative_to(local_path):
                    raise BridgeError(
                        "two_way mappings must not overlap in local paths."
                    )
            for other in seen_two_way_overleaf:
                if overleaf_path == other or overleaf_path.is_relative_to(other) or other.is_relative_to(overleaf_path):
                    raise BridgeError(
                        "two_way mappings must not overlap in Overleaf paths."
                    )
            seen_two_way_local.append(local_path)
            seen_two_way_overleaf.append(overleaf_path)
    if not any(
        PurePosixPath(config.main_document).is_relative_to(PurePosixPath(mapping.local))
        for mapping in config.mappings
        if mapping.mode == "two_way"
    ):
        raise BridgeError("main_document must live inside a two_way mapping.")


def mapped_main_document(config: Config, repo_root: Path) -> PurePosixPath:
    main_doc = PurePosixPath(config.main_document)
    for mapping in config.mappings:
        mapping_local = PurePosixPath(mapping.local)
        if not path_is_within(main_doc, mapping_local):
            continue
        source_root = mapping.local_path(repo_root)
        if source_root.is_file():
            relative = Path(source_root.name)
        else:
            relative = Path(main_doc.relative_to(mapping_local).as_posix())
        return mapping.destination_for_export(source_root, relative)
    raise BridgeError(
        f"main_document is not covered by any mapping: {config.main_document}"
    )


def config_to_toml(config: Config) -> str:
    def q(value: str) -> str:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'

    lines = [
        f"canonical_branch = {q(config.canonical_branch)}",
        f"main_document = {q(config.main_document)}",
        f"engine = {q(config.engine)}",
        f"visual_editor = {'true' if config.visual_editor else 'false'}",
        f"overleaf_git_url = {q(config.overleaf_git_url)}",
        f"bridge_repo_path = {q(config.bridge_repo_path)}",
        "",
    ]
    for mapping in config.mappings:
        lines.extend(
            [
                "[[mapping]]",
                f"local = {q(mapping.local)}",
                f"overleaf = {q(mapping.overleaf)}",
                f"mode = {q(mapping.mode)}",
                f"comment_sensitive = {'true' if mapping.comment_sensitive else 'false'}",
                "exclude = ["
                + ", ".join(q(item) for item in mapping.exclude)
                + "]",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def resolve_repo_root(repo_arg: str) -> Path:
    repo_path = Path(repo_arg).expanduser().resolve()
    if not repo_path.exists():
        raise BridgeError(f"Repo path does not exist: {repo_path}")
    result = git(repo_path, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve()


def resolve_config_path(repo_root: Path, config_arg: str | None) -> Path:
    if config_arg:
        candidate = Path(config_arg).expanduser()
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        return candidate.resolve()
    return (repo_root / ".overleaf-bridge.toml").resolve()


def current_branch(repo_root: Path) -> str:
    return git(repo_root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def has_commit(repo_root: Path, ref: str = "HEAD") -> bool:
    result = git(repo_root, "rev-parse", "--verify", ref, check=False)
    return result.returncode == 0


def is_git_repo_root(repo_path: Path) -> bool:
    result = git(repo_path, "rev-parse", "--show-toplevel", check=False)
    if result.returncode != 0:
        return False
    return Path(result.stdout.strip()).resolve() == repo_path.resolve()


def repo_clean(repo_root: Path, scoped_paths: list[str] | None = None) -> bool:
    args = ["status", "--porcelain"]
    if scoped_paths:
        args.append("--")
        args.extend(scoped_paths)
    return git(repo_root, *args).stdout.strip() == ""


def ensure_clean(repo_root: Path, label: str, scoped_paths: list[str] | None = None) -> None:
    if not repo_clean(repo_root, scoped_paths=scoped_paths):
        if scoped_paths:
            joined = ", ".join(scoped_paths)
            raise BridgeError(f"{label} has uncommitted changes under: {joined}")
        raise BridgeError(f"{label} has uncommitted changes.")


def matches_exclude(relative_path: Path, patterns: tuple[str, ...]) -> bool:
    rel = relative_path.as_posix().lstrip("./")
    name = relative_path.name
    for pattern in patterns:
        candidate = pattern.strip()
        if not candidate:
            continue
        if fnmatch.fnmatch(rel, candidate) or fnmatch.fnmatch(name, candidate):
            return True
    return False


def is_text_file(path: Path) -> bool:
    if path.suffix in EDITABLE_TEXT_SUFFIXES:
        return True
    try:
        with path.open("rb") as handle:
            chunk = handle.read(8192)
    except OSError as exc:
        raise BridgeError(f"Failed to read {path}: {exc}") from exc
    if b"\x00" in chunk:
        return False
    try:
        chunk.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def is_lfs_pointer(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(256)
    except OSError as exc:
        raise BridgeError(f"Failed to read {path}: {exc}") from exc
    return chunk.startswith(b"version https://git-lfs.github.com/spec/v1")


def submodule_paths(repo_root: Path) -> set[PurePosixPath]:
    result = git(repo_root, "ls-files", "--stage")
    paths: set[PurePosixPath] = set()
    for line in result.stdout.splitlines():
        if not line:
            continue
        left, path = line.split("\t", 1)
        mode = left.split()[0]
        if mode == "160000":
            paths.add(PurePosixPath(path))
    return paths


def path_is_within(child: PurePosixPath, parent: PurePosixPath) -> bool:
    return child == parent or child.is_relative_to(parent)


def iter_mapping_files(
    repo_root: Path,
    mapping: Mapping,
    *,
    allow_missing_export_only: bool,
) -> list[tuple[Path, PurePosixPath]]:
    source_root = mapping.local_path(repo_root)
    if not source_root.exists():
        if mapping.mode == "export_only" and allow_missing_export_only:
            return []
        raise BridgeError(f"Mapped local path does not exist: {source_root}")
    if source_root.is_symlink():
        raise BridgeError(f"Symlinked mapping roots are not supported: {source_root}")

    entries: list[tuple[Path, PurePosixPath]] = []
    if source_root.is_file():
        relative = Path(source_root.name)
        if not matches_exclude(relative, mapping.exclude):
            entries.append((source_root, mapping.destination_for_export(source_root, relative)))
        return entries

    for current_root, dirnames, filenames in os.walk(source_root, followlinks=False):
        current_path = Path(current_root)
        rel_dir = current_path.relative_to(source_root)

        filtered_dirnames: list[str] = []
        for dirname in sorted(dirnames):
            rel_path = (rel_dir / dirname) if rel_dir != Path(".") else Path(dirname)
            if matches_exclude(rel_path, mapping.exclude):
                continue
            full_dir = current_path / dirname
            if full_dir.is_symlink():
                raise BridgeError(f"Symlinks are not supported in exported content: {full_dir}")
            if dirname == ".git":
                raise BridgeError(f"Nested Git directories are not supported: {full_dir}")
            filtered_dirnames.append(dirname)
        dirnames[:] = filtered_dirnames

        for filename in sorted(filenames):
            rel_path = (rel_dir / filename) if rel_dir != Path(".") else Path(filename)
            if matches_exclude(rel_path, mapping.exclude):
                continue
            full_path = current_path / filename
            if full_path.is_symlink():
                raise BridgeError(f"Symlinks are not supported in exported content: {full_path}")
            if filename == ".git":
                raise BridgeError(f"Nested Git files are not supported: {full_path}")
            if not full_path.is_file():
                continue
            entries.append((full_path, mapping.destination_for_export(source_root, rel_path)))
    return entries


def collect_export(
    repo_root: Path,
    config: Config,
    *,
    allow_missing_export_only: bool,
) -> tuple[list[ExportedFile], list[str]]:
    exported: list[ExportedFile] = []
    warnings: list[str] = []
    collisions: dict[PurePosixPath, Path] = {}
    repo_submodules = submodule_paths(repo_root)

    for mapping in config.mappings:
        source_root = mapping.local_path(repo_root)
        if not source_root.exists() and mapping.mode == "export_only" and allow_missing_export_only:
            warnings.append(f"Skipping missing export_only mapping: {mapping.local}")
            continue
        for source, dest in iter_mapping_files(
            repo_root,
            mapping,
            allow_missing_export_only=allow_missing_export_only,
        ):
            rel_repo = PurePosixPath(source.relative_to(repo_root).as_posix())
            if any(path_is_within(rel_repo, submodule) for submodule in repo_submodules):
                raise BridgeError(f"Mapped content contains a Git submodule: {source}")
            if is_lfs_pointer(source):
                raise BridgeError(f"Git LFS pointer files are not supported: {source}")
            if dest in collisions and collisions[dest] != source:
                raise BridgeError(
                    f"Multiple mappings export to the same Overleaf path: {dest}"
                )
            collisions[dest] = source
            size = source.stat().st_size
            exported.append(
                ExportedFile(
                    source=source,
                    dest=dest,
                    size=size,
                    is_text=is_text_file(source),
                    mapping=mapping,
                )
            )
    exported.sort(key=lambda item: item.dest.as_posix())
    main_doc_dest = mapped_main_document(config, repo_root)
    if main_doc_dest not in {item.dest for item in exported}:
        raise BridgeError(
            "main_document is excluded from the export. "
            f"Expected {main_doc_dest.as_posix()} in the Overleaf snapshot."
        )
    validate_export_limits(exported)
    return exported, warnings


def validate_export_limits(exported: list[ExportedFile]) -> None:
    file_count = len(exported)
    if file_count > MAX_FILE_COUNT:
        raise BridgeError(
            f"Export would contain {file_count} files, above the {MAX_FILE_COUNT} file limit."
        )
    total_bytes = sum(item.size for item in exported)
    if total_bytes > MAX_PROJECT_BYTES:
        raise BridgeError(
            f"Export would be {human_bytes(total_bytes)}, above the {human_bytes(MAX_PROJECT_BYTES)} project limit."
        )
    editable_total = sum(item.size for item in exported if item.is_text)
    if editable_total > MAX_EDITABLE_TOTAL_BYTES:
        raise BridgeError(
            "Editable text exceeds Overleaf's recommended total limit "
            f"({human_bytes(editable_total)} > {human_bytes(MAX_EDITABLE_TOTAL_BYTES)})."
        )
    large_editable = [item for item in exported if item.is_text and item.size > MAX_EDITABLE_FILE_BYTES]
    if large_editable:
        details = ", ".join(
            f"{item.dest.as_posix()} ({human_bytes(item.size)})"
            for item in large_editable[:5]
        )
        raise BridgeError(
            "One or more editable text files exceed the recommended 2 MB limit: "
            f"{details}"
        )


def materialize_export(exported: list[ExportedFile], destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for item in exported:
        dest_path = destination / Path(item.dest.as_posix())
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.source, dest_path)


def sync_exact(source_root: Path, dest_root: Path, *, preserve_top_level: tuple[str, ...] = (".git",)) -> None:
    source_files: dict[PurePosixPath, Path] = {}
    for current_root, _, filenames in os.walk(source_root):
        current_path = Path(current_root)
        for filename in filenames:
            full_path = current_path / filename
            rel = PurePosixPath(full_path.relative_to(source_root).as_posix())
            source_files[rel] = full_path

    dest_files: dict[PurePosixPath, Path] = {}
    for current_root, dirnames, filenames in os.walk(dest_root):
        current_path = Path(current_root)
        rel_dir = PurePosixPath(current_path.relative_to(dest_root).as_posix())
        filtered_dirnames: list[str] = []
        for dirname in dirnames:
            if rel_dir == PurePosixPath(".") and dirname in preserve_top_level:
                continue
            filtered_dirnames.append(dirname)
        dirnames[:] = filtered_dirnames
        for filename in filenames:
            rel = PurePosixPath((current_path / filename).relative_to(dest_root).as_posix())
            if rel.parts and rel.parts[0] in preserve_top_level:
                continue
            dest_files[rel] = current_path / filename

    for rel, path in dest_files.items():
        if rel not in source_files:
            path.unlink()
    for rel, source_path in source_files.items():
        dest_path = dest_root / Path(rel.as_posix())
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)

    for current_root, dirnames, _ in os.walk(dest_root, topdown=False):
        current_path = Path(current_root)
        for dirname in list(dirnames):
            child = current_path / dirname
            relative = PurePosixPath(child.relative_to(dest_root).as_posix())
            if relative.parts and relative.parts[0] in preserve_top_level:
                continue
            try:
                child.rmdir()
            except OSError:
                pass


def fetch_remote(bridge_repo: Path) -> bool:
    result = git(bridge_repo, "remote", check=False)
    remotes = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    if REMOTE_NAME not in remotes:
        return False
    git(bridge_repo, "fetch", REMOTE_NAME)
    return True


def ensure_bridge_repo(config: Config, repo_root: Path) -> Path:
    bridge_repo = config.bridge_repo(repo_root)
    if not bridge_repo.exists():
        raise BridgeError(
            f"Bridge repo does not exist yet: {bridge_repo}. Run init first."
        )
    if not is_git_repo_root(bridge_repo):
        raise BridgeError(f"Bridge path is not a Git repo: {bridge_repo}")
    return bridge_repo


def ensure_bridge_ready_for_remote(bridge_repo: Path) -> None:
    ensure_clean(bridge_repo, "Bridge repo")
    if fetch_remote(bridge_repo):
        if not has_commit(bridge_repo) and git(
            bridge_repo,
            "rev-parse",
            "--verify",
            f"{REMOTE_NAME}/{REMOTE_BRANCH}",
            check=False,
        ).returncode == 0:
            git(bridge_repo, "checkout", "-B", REMOTE_BRANCH, f"{REMOTE_NAME}/{REMOTE_BRANCH}")
        elif has_commit(bridge_repo):
            git(bridge_repo, "checkout", REMOTE_BRANCH)
            merge = git(
                bridge_repo,
                "merge",
                "--ff-only",
                f"{REMOTE_NAME}/{REMOTE_BRANCH}",
                check=False,
            )
            if merge.returncode != 0:
                raise BridgeError(
                    "Bridge repo cannot fast-forward to Overleaf. Resolve the bridge repo first."
                )
    else:
        if current_branch(bridge_repo) != REMOTE_BRANCH:
            git(bridge_repo, "checkout", REMOTE_BRANCH)


def stage_export_in_bridge(bridge_repo: Path, export_root: Path) -> None:
    sync_exact(export_root, bridge_repo, preserve_top_level=(".git",))
    git(bridge_repo, "add", "-A")


def diff_name_status(bridge_repo: Path) -> list[str]:
    if has_commit(bridge_repo):
        result = git(
            bridge_repo,
            "diff",
            "--cached",
            "--name-status",
            "--find-renames",
            "--find-copies",
            "HEAD",
        )
    else:
        result = git(bridge_repo, "diff", "--cached", "--name-status", "--find-renames", "--find-copies", "--")
    return [line for line in result.stdout.splitlines() if line.strip()]


def detect_risky_layout_changes(bridge_repo: Path, config: Config) -> None:
    sensitive_prefixes = [
        PurePosixPath(mapping.overleaf)
        for mapping in config.mappings
        if mapping.comment_sensitive
    ]
    lines = diff_name_status(bridge_repo)
    additions = 0
    deletions = 0
    renames: list[str] = []

    def sensitive(path_text: str) -> bool:
        pure = PurePosixPath(path_text)
        return any(
            prefix == PurePosixPath(".")
            or path_is_within(pure, prefix)
            for prefix in sensitive_prefixes
        )

    for line in lines:
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith("R") and len(parts) >= 3:
            if sensitive(parts[1]) or sensitive(parts[2]):
                renames.append(f"{parts[1]} -> {parts[2]}")
        elif status.startswith("A") and len(parts) >= 2 and sensitive(parts[1]):
            additions += 1
        elif status.startswith("D") and len(parts) >= 2 and sensitive(parts[1]):
            deletions += 1

    if renames:
        preview = ", ".join(renames[:3])
        raise BridgeError(
            "Push blocked because comment-sensitive files appear to be renamed or moved: "
            f"{preview}"
        )
    if additions and deletions and additions + deletions >= MASS_CHANGE_THRESHOLD:
        raise BridgeError(
            "Push blocked because comment-sensitive files show a move-heavy layout change. "
            "Use a smaller sync step or move the change out of the Overleaf-tracked paths."
        )


def commit_if_needed(bridge_repo: Path, message: str) -> bool:
    if git(bridge_repo, "diff", "--cached", "--quiet", check=False).returncode == 0:
        return False
    git(bridge_repo, "commit", "-m", message)
    return True


def zip_export(export_root: Path) -> bytes:
    buffer_path = tempfile.NamedTemporaryFile(delete=False)
    buffer_path.close()
    zip_path = Path(buffer_path.name)
    try:
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for current_root, _, filenames in os.walk(export_root):
                current_path = Path(current_root)
                for filename in filenames:
                    file_path = current_path / filename
                    archive.write(file_path, file_path.relative_to(export_root).as_posix())
        data = zip_path.read_bytes()
    finally:
        zip_path.unlink(missing_ok=True)
    if len(data) > MAX_BOOTSTRAP_ZIP_BYTES:
        raise BridgeError(
            "Bootstrap ZIP exceeds the 50 MB upload limit "
            f"({human_bytes(len(data))} > {human_bytes(MAX_BOOTSTRAP_ZIP_BYTES)})."
        )
    return data


def build_overleaf_html(
    zip_bytes: bytes,
    *,
    main_document: str,
    engine: str,
    visual_editor: bool,
    title: str,
) -> str:
    data_uri = "data:application/zip;base64," + base64.b64encode(zip_bytes).decode("ascii")
    engine = html.escape(engine)
    main_document = html.escape(main_document)
    visual_editor = "true" if visual_editor else "false"
    escaped_title = html.escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escaped_title}</title>
</head>
<body>
  <p>Opening Overleaf import form...</p>
  <form id="open-in-overleaf" method="post" action="https://www.overleaf.com/docs">
    <input type="hidden" name="snip_uri" value="{html.escape(data_uri)}">
    <input type="hidden" name="engine" value="{engine}">
    <input type="hidden" name="main_document" value="{main_document}">
    <input type="hidden" name="visual_editor" value="{visual_editor}">
    <button type="submit">Open in Overleaf</button>
  </form>
  <script>
    document.getElementById("open-in-overleaf").submit();
  </script>
</body>
</html>
"""


def export_snapshot(
    repo_root: Path,
    config: Config,
    *,
    allow_missing_export_only: bool,
) -> tuple[Path, list[ExportedFile], list[str], tempfile.TemporaryDirectory[str]]:
    exported, warnings = collect_export(
        repo_root,
        config,
        allow_missing_export_only=allow_missing_export_only,
    )
    tempdir = tempfile.TemporaryDirectory(prefix="overleaf-bridge-export-")
    export_root = Path(tempdir.name)
    materialize_export(exported, export_root)
    return export_root, exported, warnings, tempdir


def print_export_summary(exported: list[ExportedFile]) -> None:
    total_bytes = sum(item.size for item in exported)
    editable_bytes = sum(item.size for item in exported if item.is_text)
    print(f"Exported files: {len(exported)}")
    print(f"Project size:   {human_bytes(total_bytes)}")
    print(f"Editable text:  {human_bytes(editable_bytes)}")


def write_config_file(config_path: Path, config: Config, *, force: bool) -> None:
    if config_path.exists() and not force:
        raise BridgeError(f"Config already exists: {config_path}")
    config_path.write_text(config_to_toml(config))


def ensure_gitignore_entry(repo_root: Path, entry: str) -> None:
    gitignore = repo_root / ".gitignore"
    if gitignore.exists():
        lines = gitignore.read_text().splitlines()
    else:
        lines = []
    if entry not in lines:
        lines.append(entry)
        gitignore.write_text("\n".join(lines).rstrip() + "\n")


def create_bridge_repo(bridge_repo: Path) -> None:
    bridge_repo.mkdir(parents=True, exist_ok=True)
    if not is_git_repo_root(bridge_repo):
        git(bridge_repo, "init", "-b", REMOTE_BRANCH)
    git(bridge_repo, "config", "core.fileMode", "false")


def update_remote(bridge_repo: Path, git_url: str) -> None:
    existing = git(bridge_repo, "remote", check=False).stdout.splitlines()
    if REMOTE_NAME in existing:
        git(bridge_repo, "remote", "set-url", REMOTE_NAME, git_url)
    else:
        git(bridge_repo, "remote", "add", REMOTE_NAME, git_url)


def create_default_config(args: argparse.Namespace, repo_root: Path) -> Config:
    paper_dir = validate_relative_path(args.paper_dir, "paper_dir")
    main_document = validate_relative_path(args.main_document, "main_document")
    generated_mappings: list[Mapping] = []
    for raw in args.generated_mapping:
        if ":" not in raw:
            raise BridgeError(
                f"generated mapping must use local:overleaf syntax, got {raw!r}"
            )
        local, overleaf = raw.split(":", 1)
        generated_mappings.append(
            Mapping(
                local=validate_relative_path(local, "generated mapping local"),
                overleaf=validate_relative_path(overleaf or ".", "generated mapping overleaf"),
                mode="export_only",
                exclude=tuple(),
                comment_sensitive=False,
            )
        )
    base_name = Path(paper_dir).name or repo_root.name
    bridge_path = args.bridge_repo_path or f".overleaf/{base_name}/mirror"
    two_way_mapping = Mapping(
        local=paper_dir,
        overleaf=".",
        mode="two_way",
        exclude=tuple(DEFAULT_EXCLUDES),
        comment_sensitive=True,
    )
    return Config(
        canonical_branch=args.canonical_branch,
        main_document=main_document,
        engine=args.engine,
        visual_editor=args.visual_editor,
        overleaf_git_url="",
        bridge_repo_path=validate_relative_path(bridge_path, "bridge_repo_path"),
        mappings=tuple([two_way_mapping, *generated_mappings]),
    )


def maybe_warn_token_setup(config: Config, bridge_repo: Path) -> list[str]:
    warnings: list[str] = []
    if not config.overleaf_git_url:
        warnings.append("No overleaf_git_url is configured yet.")
    if os.environ.get("OVERLEAF_GIT_TOKEN"):
        return warnings
    helper = git(bridge_repo, "config", "--get", "credential.helper", check=False)
    if helper.returncode != 0 or not helper.stdout.strip():
        warnings.append(
            "No OVERLEAF_GIT_TOKEN env var and no Git credential helper detected."
        )
    return warnings


def import_two_way_mappings(repo_root: Path, bridge_repo: Path, config: Config) -> None:
    target_paths = [mapping.local for mapping in config.mappings if mapping.mode == "two_way"]
    ensure_clean(repo_root, "Main repo", scoped_paths=target_paths)

    for mapping in config.mappings:
        if mapping.mode != "two_way":
            continue
        source_base = mapping.bridge_path(bridge_repo)
        dest_base = mapping.local_path(repo_root)
        source_files: dict[PurePosixPath, Path] = {}

        if source_base.exists():
            if source_base.is_file():
                rel = PurePosixPath(source_base.name)
                if not matches_exclude(Path(rel.as_posix()), mapping.exclude):
                    source_files[rel] = source_base
            else:
                for current_root, _, filenames in os.walk(source_base):
                    current_path = Path(current_root)
                    rel_dir = current_path.relative_to(source_base)
                    for filename in filenames:
                        rel = (rel_dir / filename) if rel_dir != Path(".") else Path(filename)
                        if matches_exclude(rel, mapping.exclude):
                            continue
                        source_files[PurePosixPath(rel.as_posix())] = current_path / filename

        dest_files: dict[PurePosixPath, Path] = {}
        if dest_base.exists():
            if dest_base.is_file():
                rel = PurePosixPath(dest_base.name)
                if not matches_exclude(Path(rel.as_posix()), mapping.exclude):
                    dest_files[rel] = dest_base
            else:
                for current_root, _, filenames in os.walk(dest_base):
                    current_path = Path(current_root)
                    rel_dir = current_path.relative_to(dest_base)
                    for filename in filenames:
                        rel = (rel_dir / filename) if rel_dir != Path(".") else Path(filename)
                        if matches_exclude(rel, mapping.exclude):
                            continue
                        dest_files[PurePosixPath(rel.as_posix())] = current_path / filename

        for rel, path in dest_files.items():
            if rel not in source_files:
                path.unlink()
        for rel, source_path in source_files.items():
            if dest_base.suffix and not dest_base.is_dir():
                dest_path = dest_base
            else:
                dest_path = dest_base / Path(rel.as_posix())
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)

        if dest_base.exists() and dest_base.is_dir():
            for current_root, dirnames, _ in os.walk(dest_base, topdown=False):
                current_path = Path(current_root)
                for dirname in dirnames:
                    child = current_path / dirname
                    try:
                        child.rmdir()
                    except OSError:
                        pass


def cmd_init(args: argparse.Namespace) -> None:
    repo_root = resolve_repo_root(args.repo)
    config_path = resolve_config_path(repo_root, args.config)
    config = create_default_config(args, repo_root)
    write_config_file(config_path, config, force=args.force)
    create_bridge_repo(config.bridge_repo(repo_root))
    ensure_gitignore_entry(repo_root, ".overleaf/")
    print(f"Wrote config: {config_path}")
    print(f"Created bridge repo: {config.bridge_repo(repo_root)}")
    print("Added .overleaf/ to .gitignore")


def cmd_attach_git(args: argparse.Namespace) -> None:
    repo_root = resolve_repo_root(args.repo)
    config_path = resolve_config_path(repo_root, args.config)
    config = load_config(config_path)
    bridge_repo = ensure_bridge_repo(config, repo_root)
    git_url = normalize_overleaf_url(args.git_url)
    update_remote(bridge_repo, git_url)
    updated = Config(
        canonical_branch=config.canonical_branch,
        main_document=config.main_document,
        engine=config.engine,
        visual_editor=config.visual_editor,
        overleaf_git_url=git_url,
        bridge_repo_path=config.bridge_repo_path,
        mappings=config.mappings,
    )
    config_path.write_text(config_to_toml(updated))
    print(f"Updated Overleaf remote in {config_path}")
    print(f"Configured {REMOTE_NAME} remote in {bridge_repo}")


def cmd_doctor(args: argparse.Namespace) -> None:
    if not command_exists("git"):
        raise BridgeError("git is required.")
    repo_root = resolve_repo_root(args.repo)
    config_path = resolve_config_path(repo_root, args.config)
    config = load_config(config_path)
    bridge_repo = config.bridge_repo(repo_root)
    print(f"Repo root:      {repo_root}")
    print(f"Config:         {config_path}")
    print(f"Canonical:      {config.canonical_branch}")
    print(f"Main document:  {config.main_document}")
    print(f"Overleaf main:  {mapped_main_document(config, repo_root).as_posix()}")
    print(f"Bridge repo:    {bridge_repo}")
    print(f"Engine:         {config.engine}")
    print(f"Visual editor:  {config.visual_editor}")

    if not bridge_repo.exists():
        raise BridgeError(f"Bridge repo does not exist: {bridge_repo}")
    if not is_git_repo_root(bridge_repo):
        raise BridgeError(f"Bridge path is not a Git repo: {bridge_repo}")

    exported, warnings = collect_export(
        repo_root,
        config,
        allow_missing_export_only=True,
    )
    print_export_summary(exported)
    for mapping in config.mappings:
        print(
            f"- mapping {mapping.local} -> {mapping.overleaf} "
            f"[{mapping.mode}, comment_sensitive={mapping.comment_sensitive}]"
        )

    extra_warnings = maybe_warn_token_setup(config, bridge_repo)
    for item in warnings + extra_warnings:
        print(f"WARNING: {item}")
    print("NOTE: Do not enable Overleaf GitHub synchronization on the same shared project.")


def require_canonical_branch(repo_root: Path, config: Config) -> None:
    branch = current_branch(repo_root)
    if branch != config.canonical_branch:
        raise BridgeError(
            f"Current branch is {branch!r}; push/sync require the canonical branch "
            f"{config.canonical_branch!r}. Use preview for feature branches."
        )


def build_default_commit_message(repo_root: Path) -> str:
    branch = current_branch(repo_root)
    commit = git(repo_root, "rev-parse", "--short", "HEAD").stdout.strip()
    return f"Sync from {repo_root.name}:{branch}@{commit}"


def cmd_push(args: argparse.Namespace) -> None:
    repo_root = resolve_repo_root(args.repo)
    config = load_config(resolve_config_path(repo_root, args.config))
    require_canonical_branch(repo_root, config)
    bridge_repo = ensure_bridge_repo(config, repo_root)
    if not config.overleaf_git_url:
        raise BridgeError("Config does not have overleaf_git_url yet. Run attach-git first.")

    export_root, exported, warnings, tempdir = export_snapshot(
        repo_root,
        config,
        allow_missing_export_only=True,
    )
    try:
        ensure_bridge_ready_for_remote(bridge_repo)
        stage_export_in_bridge(bridge_repo, export_root)
        detect_risky_layout_changes(bridge_repo, config)
        commit_message = args.message or build_default_commit_message(repo_root)
        committed = commit_if_needed(bridge_repo, commit_message)
        if committed:
            git(bridge_repo, "push", REMOTE_NAME, f"HEAD:{REMOTE_BRANCH}")
            print(f"Pushed bridge repo to {REMOTE_NAME}/{REMOTE_BRANCH}")
        else:
            print("No bridge changes to push.")
        print_export_summary(exported)
        for item in warnings:
            print(f"WARNING: {item}")
        print("NOTE: Git pushes can displace Overleaf comments or track-changes on touched files.")
    finally:
        tempdir.cleanup()


def cmd_pull(args: argparse.Namespace) -> None:
    repo_root = resolve_repo_root(args.repo)
    config = load_config(resolve_config_path(repo_root, args.config))
    bridge_repo = ensure_bridge_repo(config, repo_root)
    if not config.overleaf_git_url:
        raise BridgeError("Config does not have overleaf_git_url yet. Run attach-git first.")

    ensure_clean(bridge_repo, "Bridge repo")
    if not fetch_remote(bridge_repo):
        raise BridgeError("Bridge repo has no Overleaf remote configured.")

    if has_commit(bridge_repo):
        git(bridge_repo, "checkout", REMOTE_BRANCH)
        result = git(
            bridge_repo,
            "merge",
            "--ff-only",
            f"{REMOTE_NAME}/{REMOTE_BRANCH}",
            check=False,
        )
        if result.returncode != 0:
            raise BridgeError(
                "Bridge repo cannot fast-forward to Overleaf. Resolve the bridge repo first."
            )
    else:
        git(bridge_repo, "checkout", "-B", REMOTE_BRANCH, f"{REMOTE_NAME}/{REMOTE_BRANCH}")

    import_two_way_mappings(repo_root, bridge_repo, config)
    print("Imported two_way mappings from Overleaf into the main repo.")
    print("NOTE: Ask coauthors to label versions before pull when Overleaf-side edits were substantial.")


def cmd_sync(args: argparse.Namespace) -> None:
    repo_root = resolve_repo_root(args.repo)
    config = load_config(resolve_config_path(repo_root, args.config))
    require_canonical_branch(repo_root, config)
    cmd_pull(args)
    cmd_push(args)


def write_html_and_open(target: Path, content: str, *, open_browser: bool) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(f"Wrote HTML bootstrap form: {target}")
    if open_browser:
        webbrowser.open(target.as_uri())
        print("Opened bootstrap form in a browser.")


def cmd_bootstrap_like(args: argparse.Namespace, *, preview: bool) -> None:
    repo_root = resolve_repo_root(args.repo)
    config = load_config(resolve_config_path(repo_root, args.config))
    export_root, exported, warnings, tempdir = export_snapshot(
        repo_root,
        config,
        allow_missing_export_only=True,
    )
    try:
        zip_bytes = zip_export(export_root)
        title = "Overleaf Preview" if preview else "Open in Overleaf"
        html_doc = build_overleaf_html(
            zip_bytes,
            main_document=mapped_main_document(config, repo_root).as_posix(),
            engine=config.engine,
            visual_editor=config.visual_editor,
            title=title,
        )
        suffix = "preview" if preview else "bootstrap"
        default_path = config.bridge_repo(repo_root).parent / f"{suffix}.html"
        output_path = (
            Path(args.output_html).expanduser().resolve()
            if args.output_html
            else default_path.resolve()
        )
        write_html_and_open(output_path, html_doc, open_browser=not args.no_open)
        print_export_summary(exported)
        for item in warnings:
            print(f"WARNING: {item}")
        if preview:
            print("NOTE: preview creates a disposable Overleaf project from the current branch snapshot.")
        else:
            print("NOTE: bootstrap-api creates a new Overleaf project snapshot and does not configure ongoing sync.")
    finally:
        tempdir.cleanup()


def cmd_bootstrap_api(args: argparse.Namespace) -> None:
    cmd_bootstrap_like(args, preview=False)


def cmd_preview(args: argparse.Namespace) -> None:
    cmd_bootstrap_like(args, preview=True)


def cmd_status(args: argparse.Namespace) -> None:
    repo_root = resolve_repo_root(args.repo)
    config = load_config(resolve_config_path(repo_root, args.config))
    bridge_repo = ensure_bridge_repo(config, repo_root)
    branch = current_branch(repo_root)
    print(f"Repo root:      {repo_root}")
    print(f"Current branch: {branch}")
    print(f"Canonical:      {config.canonical_branch}")
    print(f"Push allowed:   {branch == config.canonical_branch}")
    print(f"Bridge repo:    {bridge_repo}")
    print(f"Bridge clean:   {repo_clean(bridge_repo)}")
    print(f"Main clean:     {repo_clean(repo_root)}")
    print(f"Overleaf URL:   {config.overleaf_git_url or '(not set)'}")
    if args.fetch and config.overleaf_git_url:
        if fetch_remote(bridge_repo):
            print("Fetched latest Overleaf master.")
    if has_commit(bridge_repo):
        print(f"Bridge HEAD:    {git(bridge_repo, 'rev-parse', '--short', 'HEAD').stdout.strip()}")
    remote_ref = git(
        bridge_repo,
        "rev-parse",
        "--short",
        f"{REMOTE_NAME}/{REMOTE_BRANCH}",
        check=False,
    )
    if remote_ref.returncode == 0:
        print(f"Remote HEAD:    {remote_ref.stdout.strip()}")
    exported, warnings = collect_export(
        repo_root,
        config,
        allow_missing_export_only=True,
    )
    print_export_summary(exported)
    for item in warnings:
        print(f"WARNING: {item}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Filtered Overleaf <-> Git bridge for paper workflows.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path inside the Git repo that contains .overleaf-bridge.toml (default: current directory).",
    )
    parser.add_argument(
        "--config",
        help="Custom path to the bridge config. Defaults to .overleaf-bridge.toml at the repo root.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create config and local bridge repo.")
    init_parser.add_argument("--canonical-branch", default="main")
    init_parser.add_argument("--paper-dir", default="paper")
    init_parser.add_argument("--main-document", default="paper/main.tex")
    init_parser.add_argument("--engine", default="pdflatex")
    init_parser.add_argument("--bridge-repo-path")
    init_parser.add_argument(
        "--generated-mapping",
        action="append",
        default=[],
        help="Add an export_only mapping with local:overleaf syntax.",
    )
    init_parser.add_argument(
        "--visual-editor",
        action="store_true",
        help="Request Overleaf visual editor for bootstrap and preview flows.",
    )
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=cmd_init)

    attach_parser = subparsers.add_parser("attach-git", help="Attach the Overleaf Git remote.")
    attach_parser.add_argument("git_url")
    attach_parser.set_defaults(func=cmd_attach_git)

    doctor_parser = subparsers.add_parser("doctor", help="Validate config and export safety.")
    doctor_parser.set_defaults(func=cmd_doctor)

    push_parser = subparsers.add_parser("push", help="Export and push the canonical branch to Overleaf.")
    push_parser.add_argument("--message", help="Custom Git commit message for the bridge repo.")
    push_parser.set_defaults(func=cmd_push)

    pull_parser = subparsers.add_parser("pull", help="Fetch Overleaf and import two_way files.")
    pull_parser.set_defaults(func=cmd_pull)

    sync_parser = subparsers.add_parser("sync", help="Pull then push on the canonical branch.")
    sync_parser.add_argument("--message", help="Custom Git commit message for the bridge repo.")
    sync_parser.set_defaults(func=cmd_sync)

    bootstrap_parser = subparsers.add_parser(
        "bootstrap-api",
        help="Create a local HTML form that posts a project snapshot to Overleaf /docs.",
    )
    bootstrap_parser.add_argument("--output-html", help="Write the HTML form to this path.")
    bootstrap_parser.add_argument("--no-open", action="store_true")
    bootstrap_parser.set_defaults(func=cmd_bootstrap_api)

    preview_parser = subparsers.add_parser(
        "preview",
        help="Create a disposable Overleaf preview project from the current branch.",
    )
    preview_parser.add_argument("--output-html", help="Write the HTML form to this path.")
    preview_parser.add_argument("--no-open", action="store_true")
    preview_parser.set_defaults(func=cmd_preview)

    status_parser = subparsers.add_parser("status", help="Show bridge status.")
    status_parser.add_argument("--fetch", action="store_true", help="Fetch Overleaf before reporting status.")
    status_parser.set_defaults(func=cmd_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except BridgeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        message = stderr or str(exc)
        print(f"ERROR: command failed: {message}", file=sys.stderr)
        return exc.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
