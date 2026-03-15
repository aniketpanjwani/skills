from __future__ import annotations

import importlib.util
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tomllib

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    REPO_ROOT
    / "skills"
    / "economists"
    / "overleaf-git-bridge"
    / "scripts"
    / "overleaf_bridge.py"
)


def load_bridge_module():
    spec = importlib.util.spec_from_file_location("overleaf_bridge", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


bridge = load_bridge_module()


def run_command(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        joined = " ".join(args)
        raise AssertionError(
            f"command failed ({joined})\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run_command("git", *args, cwd=cwd, check=check)


def run_cli(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run_command(sys.executable, str(SCRIPT_PATH), "--repo", str(repo), *args, cwd=repo, check=check)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def configure_identity(repo: Path) -> None:
    git(repo, "config", "user.name", "Test User")
    git(repo, "config", "user.email", "test@example.com")


def make_paper_repo(
    tmp_path: Path,
    *,
    include_generated: bool = True,
    include_intro: bool = True,
) -> Path:
    repo = tmp_path / "paper-repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    configure_identity(repo)

    if include_intro:
        write_file(repo / "paper" / "sections" / "intro.tex", "Intro section.\n")
        intro_line = "\\input{sections/intro}\n"
    else:
        intro_line = ""

    write_file(
        repo / "paper" / "main.tex",
        "\\documentclass{article}\n\\begin{document}\n"
        + intro_line
        + "Hello bridge.\n\\end{document}\n",
    )

    if include_generated:
        write_file(repo / "results" / "tables" / "table1.tex", "% generated table\n")

    git(repo, "add", ".")
    git(repo, "commit", "-m", "init")
    return repo


def init_bridge(repo: Path, *, include_generated: bool = True) -> Path:
    args = [
        "init",
        "--paper-dir",
        "paper",
        "--main-document",
        "paper/main.tex",
    ]
    if include_generated:
        args.extend(["--generated-mapping", "results/tables:generated/tables"])
    run_cli(repo, *args)
    bridge_repo = repo / ".overleaf" / "paper" / "mirror"
    configure_identity(bridge_repo)
    return bridge_repo


def create_fake_overleaf_remote(tmp_path: Path) -> Path:
    remote = tmp_path / "fake-overleaf.com-remote.git"
    git(tmp_path, "init", "--bare", str(remote))
    return remote


def load_config(path: Path) -> dict:
    return tomllib.loads(path.read_text())


def test_validate_config_rejects_overlapping_two_way_mappings() -> None:
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="pdflatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", ".", "two_way", tuple(), True),
            bridge.Mapping("paper/sections", "sections", "two_way", tuple(), True),
        ),
    )
    with pytest.raises(bridge.BridgeError, match="must not overlap"):
        bridge.validate_config(config)


def test_mapped_main_document_respects_overleaf_prefix(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path, include_generated=False)
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="xelatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", "manuscript", "two_way", tuple(), True),
        ),
    )
    assert bridge.mapped_main_document(config, repo) == PurePosixPath("manuscript/main.tex")


def test_collect_export_warns_for_missing_export_only_mapping(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path, include_generated=False)
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="pdflatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", ".", "two_way", tuple(), True),
            bridge.Mapping("results/tables", "generated/tables", "export_only", tuple(), False),
        ),
    )
    exported, warnings = bridge.collect_export(
        repo,
        config,
        allow_missing_export_only=True,
    )
    assert {item.dest.as_posix() for item in exported} == {"main.tex", "sections/intro.tex"}
    assert warnings == ["Skipping missing export_only mapping: results/tables"]


def test_collect_export_rejects_main_document_when_excluded(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path, include_generated=False)
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="pdflatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", ".", "two_way", ("main.tex",), True),
        ),
    )
    with pytest.raises(bridge.BridgeError, match="main_document is excluded"):
        bridge.collect_export(repo, config, allow_missing_export_only=True)


def test_collect_export_rejects_git_lfs_pointer(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path, include_generated=False)
    write_file(
        repo / "paper" / "figure.pdf",
        "version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 42\n",
    )
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="pdflatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", ".", "two_way", tuple(), True),
        ),
    )
    with pytest.raises(bridge.BridgeError, match="Git LFS pointer"):
        bridge.collect_export(repo, config, allow_missing_export_only=True)


def test_collect_export_rejects_large_editable_file(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path, include_generated=False)
    write_file(repo / "paper" / "appendix.tex", "a" * (bridge.MAX_EDITABLE_FILE_BYTES + 1))
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="pdflatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", ".", "two_way", tuple(), True),
        ),
    )
    with pytest.raises(bridge.BridgeError, match="exceed the recommended 2 MB limit"):
        bridge.collect_export(repo, config, allow_missing_export_only=True)


def test_validate_export_limits_rejects_excess_file_count() -> None:
    exported = [
        bridge.ExportedFile(
            source=Path(f"/tmp/{index}.tex"),
            dest=PurePosixPath(f"{index}.tex"),
            size=1,
            is_text=True,
            mapping=bridge.Mapping("paper", ".", "two_way", tuple(), True),
        )
        for index in range(bridge.MAX_FILE_COUNT + 1)
    ]
    with pytest.raises(bridge.BridgeError, match="above the 2000 file limit"):
        bridge.validate_export_limits(exported)


def test_build_overleaf_html_contains_expected_fields() -> None:
    html = bridge.build_overleaf_html(
        b"zip-bytes",
        main_document="manuscript/main.tex",
        engine="xelatex",
        visual_editor=True,
        title="Preview",
    )
    assert "https://www.overleaf.com/docs" in html
    assert 'name="main_document" value="manuscript/main.tex"' in html
    assert 'name="engine" value="xelatex"' in html
    assert 'name="visual_editor" value="true"' in html


def test_detect_risky_layout_changes_blocks_rename(tmp_path: Path) -> None:
    bridge_repo = tmp_path / "bridge"
    bridge_repo.mkdir()
    git(bridge_repo, "init", "-b", "master")
    configure_identity(bridge_repo)
    write_file(bridge_repo / "main.tex", "hello\n")
    git(bridge_repo, "add", ".")
    git(bridge_repo, "commit", "-m", "initial")

    git(bridge_repo, "mv", "main.tex", "renamed.tex")
    config = bridge.Config(
        canonical_branch="main",
        main_document="paper/main.tex",
        engine="pdflatex",
        visual_editor=False,
        overleaf_git_url="",
        bridge_repo_path=".overleaf/paper/mirror",
        mappings=(
            bridge.Mapping("paper", ".", "two_way", tuple(), True),
        ),
    )
    with pytest.raises(bridge.BridgeError, match="renamed or moved"):
        bridge.detect_risky_layout_changes(bridge_repo, config)


def test_init_creates_config_and_nested_bridge_repo(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path)
    bridge_repo = init_bridge(repo)
    config_path = repo / ".overleaf-bridge.toml"
    config = load_config(config_path)

    assert config_path.exists()
    assert bridge.is_git_repo_root(bridge_repo)
    assert config["main_document"] == "paper/main.tex"
    assert config["bridge_repo_path"] == ".overleaf/paper/mirror"
    assert ".overleaf/" in (repo / ".gitignore").read_text()


def test_stage_export_preserves_nested_bridge_repo_metadata(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path)
    bridge_repo = init_bridge(repo)
    export_root, _, _, tempdir = bridge.export_snapshot(
        repo,
        bridge.load_config(repo / ".overleaf-bridge.toml"),
        allow_missing_export_only=True,
    )
    try:
        bridge.stage_export_in_bridge(bridge_repo, export_root)
        assert bridge.is_git_repo_root(bridge_repo)
        assert "On branch master" in git(bridge_repo, "status").stdout
    finally:
        tempdir.cleanup()


def test_preview_writes_html_from_feature_branch(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path)
    init_bridge(repo)
    git(repo, "checkout", "-b", "draft")
    output_html = repo / "preview.html"

    run_cli(repo, "preview", "--no-open", "--output-html", str(output_html))

    content = output_html.read_text()
    assert output_html.exists()
    assert "Overleaf Preview" in content
    assert 'name="main_document" value="main.tex"' in content


def test_push_and_pull_round_trip_with_fake_remote(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path)
    init_bridge(repo)
    remote = create_fake_overleaf_remote(tmp_path)
    run_cli(repo, "attach-git", str(remote))

    push_result = run_cli(repo, "push")
    assert "Pushed bridge repo to overleaf/master" in push_result.stdout

    overleaf_work = tmp_path / "overleaf-work"
    git(tmp_path, "clone", str(remote), str(overleaf_work))
    configure_identity(overleaf_work)
    write_file(overleaf_work / "main.tex", "Remote revised main.\n")
    write_file(overleaf_work / "generated" / "tables" / "remote-only.tex", "% remote generated\n")
    intro = overleaf_work / "sections" / "intro.tex"
    if intro.exists():
        intro.unlink()
    git(overleaf_work, "add", "-A")
    git(overleaf_work, "commit", "-m", "remote edits")
    git(overleaf_work, "push", "origin", "master")

    pull_result = run_cli(repo, "pull")
    assert "Imported two_way mappings" in pull_result.stdout
    assert (repo / "paper" / "main.tex").read_text() == "Remote revised main.\n"
    assert not (repo / "paper" / "sections" / "intro.tex").exists()
    assert not (repo / "results" / "tables" / "remote-only.tex").exists()


def test_push_is_blocked_on_non_canonical_branch(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path)
    init_bridge(repo)
    git(repo, "checkout", "-b", "draft")

    result = run_cli(repo, "push", check=False)

    assert result.returncode != 0
    assert "canonical branch 'main'" in result.stderr


def test_doctor_rejects_symlink_in_exported_content(tmp_path: Path) -> None:
    repo = make_paper_repo(tmp_path, include_generated=False)
    init_bridge(repo, include_generated=False)
    (repo / "paper" / "linked.tex").symlink_to(repo / "paper" / "main.tex")

    result = run_cli(repo, "doctor", check=False)

    assert result.returncode != 0
    assert "Symlinks are not supported in exported content" in result.stderr
