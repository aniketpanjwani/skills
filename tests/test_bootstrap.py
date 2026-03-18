from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "bootstrap.sh"
PDF_SKILL_MD = REPO_ROOT / "skills" / "general" / "pdf-reading" / "SKILL.md"


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    shutil.copy2(BOOTSTRAP_SCRIPT, repo / "scripts" / "bootstrap.sh")
    return repo


def _run_bootstrap(repo: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    return subprocess.run(
        ["bash", str(repo / "scripts" / "bootstrap.sh"), *args],
        cwd=repo,
        env=merged_env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_bootstrap_rejects_duplicate_skill_names(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _write_text(repo / "skills" / "type-a" / "shared" / "SKILL.md", "# skill a\n")
    _write_text(repo / "skills" / "type-b" / "shared" / "SKILL.md", "# skill b\n")

    result = _run_bootstrap(repo, "--list")

    assert result.returncode != 0
    assert "duplicate skill directory names" in result.stderr
    assert "shared" in result.stderr


def test_bootstrap_tool_specific_install_keeps_shared_assets(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path)
    _write_text(repo / "skills" / "general" / "demo" / "SKILL.md", "# root skill\n")
    _write_text(repo / "skills" / "general" / "demo" / "scripts" / "helper.sh", "echo shared\n")
    _write_text(repo / "skills" / "general" / "demo" / "gemini" / "SKILL.md", "# gemini override\n")

    home = tmp_path / "home"
    home.mkdir()

    result = _run_bootstrap(
        repo,
        "--target",
        "gemini",
        "--scope",
        "global",
        "--skills",
        "demo",
        env={"HOME": str(home)},
    )

    assert result.returncode == 0, result.stderr

    installed = home / ".gemini" / "skills" / "demo"
    assert installed.exists()
    assert (installed / "scripts" / "helper.sh").read_text(encoding="utf-8") == "echo shared\n"
    assert (installed / "SKILL.md").read_text(encoding="utf-8") == "# gemini override\n"
    assert not (installed / "gemini").exists()


def test_pdf_reading_skill_uses_install_relative_script_path() -> None:
    skill_text = PDF_SKILL_MD.read_text(encoding="utf-8")

    assert "python3 scripts/pdf_extract.py /path/to/paper.pdf" in skill_text
    assert "skills/general/pdf-reading/scripts/pdf_extract.py" not in skill_text
