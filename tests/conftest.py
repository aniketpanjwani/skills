from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_SCRIPTS_DIR = REPO_ROOT / "tests" / "pdf-reading" / "scripts"
RUNTIME_SCRIPTS_DIR = REPO_ROOT / "skills" / "general" / "pdf-reading" / "scripts"

for scripts_dir in (BENCHMARK_SCRIPTS_DIR, RUNTIME_SCRIPTS_DIR):
    scripts_dir_str = str(scripts_dir)
    if scripts_dir_str not in sys.path:
        sys.path.insert(0, scripts_dir_str)
