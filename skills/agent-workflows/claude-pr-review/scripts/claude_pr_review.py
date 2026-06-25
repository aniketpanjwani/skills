#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ARTIFACT_ROOT = Path("/tmp/agentic/claude-pr-review")
JSON_START = "<CLAUDE_PR_REVIEW_JSON>"
JSON_END = "</CLAUDE_PR_REVIEW_JSON>"
SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
DEFAULT_INLINE_LIMIT = 30
MAX_BODY_CHARS = 60000
MAX_COMMENT_CHARS = 12000
STREAM_STATE_INTERVAL_SECONDS = 2.0
STREAM_PROGRESS_INTERVAL_SECONDS = 30.0
DEFAULT_RUNNER = os.environ.get("CLAUDE_PR_REVIEW_RUNNER", "tmux")
DEFAULT_TMUX_TIMEOUT_SECONDS = 7200.0
DEFAULT_TMUX_STARTUP_WAIT_SECONDS = 5.0
DEFAULT_TMUX_SHUTDOWN = os.environ.get("CLAUDE_PR_REVIEW_TMUX_SHUTDOWN", "on-complete")
FORBIDDEN_BILLING_ENV_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN")
CODEX_THREAD_ENV_VAR = "CODEX_THREAD_ID"


class ReviewError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def run_id() -> str:
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M%S")
    suffix = os.urandom(3).hex()
    return f"{timestamp}-{suffix}"


def artifact_dir(run_id_value: str) -> Path:
    return ARTIFACT_ROOT / run_id_value


def latest_path() -> Path:
    return ARTIFACT_ROOT / "latest"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_utc_timestamp(value: Any) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.UTC)
    return parsed.astimezone(dt.UTC)


def elapsed_since(value: Any) -> str | None:
    parsed = parse_utc_timestamp(value)
    if parsed is None:
        return None
    seconds = max(0, int((dt.datetime.now(dt.UTC) - parsed).total_seconds()))
    if seconds < 60:
        return f"{seconds}s"
    minutes, remaining_seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"
    hours, remaining_minutes = divmod(minutes, 60)
    return f"{hours}h {remaining_minutes}m"


def safe_scope_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.=-]+", "_", value).strip("_") or "unknown"


def current_latest_scope() -> dict[str, str]:
    thread_id = os.environ.get(CODEX_THREAD_ENV_VAR)
    if thread_id:
        return {"type": "codex_thread", "id": thread_id}
    return {"type": "global"}


def scoped_latest_path(scope: dict[str, str]) -> Path:
    if scope.get("type") == "codex_thread":
        return ARTIFACT_ROOT / "latest-by-thread" / safe_scope_filename(str(scope.get("id") or ""))
    return latest_path()


def set_latest(run_id_value: str) -> dict[str, str]:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    latest_path().write_text(run_id_value + "\n", encoding="utf-8")
    scope = current_latest_scope()
    if scope.get("type") != "global":
        scoped_path = scoped_latest_path(scope)
        scoped_path.parent.mkdir(parents=True, exist_ok=True)
        scoped_path.write_text(run_id_value + "\n", encoding="utf-8")
    return scope


def resolve_run_id(value: str) -> str:
    if value != "latest":
        return value
    scope = current_latest_scope()
    path = scoped_latest_path(scope)
    if not path.is_file():
        if scope.get("type") == "codex_thread":
            raise ReviewError(
                f"no latest claude-pr-review run found for current Codex thread "
                f"({CODEX_THREAD_ENV_VAR}={scope.get('id')}); use an explicit --run-id for another thread"
            )
        raise ReviewError("no latest claude-pr-review run found")
    resolved = path.read_text(encoding="utf-8").strip()
    if not resolved:
        if scope.get("type") == "codex_thread":
            raise ReviewError(
                f"latest claude-pr-review run for current Codex thread is empty "
                f"({CODEX_THREAD_ENV_VAR}={scope.get('id')})"
            )
        raise ReviewError("latest claude-pr-review run is empty")
    return resolved


def command_output(
    args: list[str],
    cwd: Path,
    *,
    check: bool = True,
    input_text: str | None = None,
) -> str:
    proc = subprocess.run(
        args,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
    )
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise ReviewError(f"{args[0]} failed: {detail}")
    return proc.stdout.strip()


def require_tool(name: str) -> None:
    if subprocess.run(["/usr/bin/env", "which", name], capture_output=True).returncode != 0:
        raise ReviewError(f"required tool not found on PATH: {name}")


def repo_root(repo_arg: str | None) -> Path:
    start = Path(repo_arg or os.getcwd()).expanduser().resolve()
    output = command_output(["git", "rev-parse", "--show-toplevel"], start)
    return Path(output).resolve()


def git_status(repo: Path) -> str:
    return command_output(["git", "status", "--porcelain"], repo)


def current_head(repo: Path) -> str:
    return command_output(["git", "rev-parse", "HEAD"], repo)


def current_branch(repo: Path) -> str:
    branch = command_output(["git", "branch", "--show-current"], repo, check=False)
    return branch or "(detached)"


def gh_json(repo: Path, args: list[str]) -> Any:
    output = command_output(["gh", *args], repo)
    return json.loads(output)


def pr_metadata(repo: Path) -> dict[str, Any]:
    return gh_json(
        repo,
        [
            "pr",
            "view",
            "--json",
            "number,url,title,baseRefName,headRefName,headRefOid",
        ],
    )


def repo_name_with_owner(repo: Path) -> str:
    return command_output(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], repo)


def ensure_base_ref(repo: Path, base_ref_name: str, explicit_base: str | None) -> str:
    if explicit_base:
        return explicit_base

    origin_ref = f"origin/{base_ref_name}"
    if subprocess.run(["git", "rev-parse", "--verify", "--quiet", origin_ref], cwd=repo).returncode == 0:
        return origin_ref

    subprocess.run(
        ["git", "fetch", "--no-tags", "origin", f"{base_ref_name}:refs/remotes/origin/{base_ref_name}"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    if subprocess.run(["git", "rev-parse", "--verify", "--quiet", origin_ref], cwd=repo).returncode == 0:
        return origin_ref
    return base_ref_name


def claude_bin(explicit: str | None) -> str:
    if explicit:
        return explicit
    local = Path.home() / ".local/bin/claude"
    if local.exists():
        return str(local)
    return "claude"


def claudet_bin(explicit: str | None) -> str:
    if explicit:
        return explicit
    local = Path.home() / ".local/bin/claudet"
    if local.exists():
        return str(local)
    return "claudet"


def require_executable(command: str) -> None:
    expanded = Path(command).expanduser()
    if "/" in command:
        if not expanded.exists() or not os.access(expanded, os.X_OK):
            raise ReviewError(f"required executable not found or not executable: {expanded}")
        return
    require_tool(command)


def detect_claude_skill(repo: Path, claude: str, explicit: str | None) -> str:
    if explicit:
        return explicit

    del repo, claude

    cache_root = Path.home() / ".claude/plugins/cache"
    for skill_dir, slash_name in [
        ("ce-code-review", "/compound-engineering:ce-code-review"),
        ("ce-review", "/compound-engineering:ce-review"),
    ]:
        if any(cache_root.glob(f"*/compound-engineering/*/skills/{skill_dir}/SKILL.md")):
            return slash_name

    # Current installed Claude plugin uses this name. Keep the fallback explicit so
    # the wrapper still works when skill discovery is noisy or expensive.
    return "/compound-engineering:ce-review"


def review_skill_invocation(skill_name: str, base_ref: str) -> str:
    if is_ce_code_review_skill(skill_name):
        return f"{skill_name} mode:agent base:{base_ref}"
    return f"{skill_name} mode:report-only base:{base_ref}"


def is_ce_code_review_skill(skill_name: str) -> bool:
    return (
        skill_name.endswith(":ce-code-review")
        or skill_name.endswith("/ce-code-review")
        or skill_name == "ce-code-review"
    )


def review_prompt(skill_name: str, base_ref: str, pr: dict[str, Any]) -> str:
    skill_invocation = review_skill_invocation(skill_name, base_ref)
    if is_ce_code_review_skill(skill_name):
        return f"""You are Claude Code running as a delegated PR reviewer for Codex.

Task:
1. Invoke `{skill_invocation}` to review the current checkout.
2. Do not edit files, commit, push, create branches, create a PR, or post to GitHub.
3. Preserve the native `ce-code-review mode:agent` JSON object as the review result. It must be one raw JSON object, not markdown and not a fenced code block.
4. Make sure the native JSON preserves CE reviewer provenance, confidence, routing, evidence, actionable findings, triage groups, testing gaps, residual risks, and verification notes.
5. Prefer semantic bugs, regressions, missing tests, contract breaks, security issues, reliability problems, and agent-native gaps over style comments.
6. Codex owns validation, line mapping, duplicate avoidance, GitHub posting, and follow-on fixes.

PR context:
- Title: {pr.get("title", "")}
- URL: {pr.get("url", "")}
- Base: {pr.get("baseRefName", "")}
- Head: {pr.get("headRefName", "")}
"""

    return f"""You are Claude Code running as a delegated PR reviewer for Codex.

Task:
1. Invoke `{skill_invocation}` to review the current checkout.
2. Do not edit files, commit, push, create branches, or create a PR.
3. Produce a very detailed review. Do not compress important reasoning into terse nits.
4. Maintain your own suggested severity ranking for every finding using P0, P1, P2, or P3. Preserve that ranking in the final JSON even if the prose report groups things differently.
5. For every finding, include a severity rationale, concrete evidence, why it matters, and a suggested fix when one exists.
6. Prefer semantic bugs, regressions, missing tests, contract breaks, security issues, reliability problems, and agent-native gaps over style comments.
7. Preserve the Compound Engineering report's reviewer/team context, route decisions, confidence, testing gaps, residual risks, and any agent-native/deployment/requirements notes. Codex needs enough detail to fix or consciously skip each item without rereading the entire chat transcript.
8. Do not post to GitHub. Codex owns validation, line mapping, duplicate avoidance, GitHub posting, and follow-on fixes.

PR context:
- Title: {pr.get("title", "")}
- URL: {pr.get("url", "")}
- Base: {pr.get("baseRefName", "")}
- Head: {pr.get("headRefName", "")}

At the end of your response, print exactly one machine-readable JSON object between these markers:
{JSON_START}
{{
  "verdict": "Ready to merge | Ready with fixes | Not ready",
  "summary": "Detailed prose summary of the review",
  "severity_ranking_note": "How you calibrated P0-P3 for this review",
  "findings": [
    {{
      "title": "Short actionable title",
      "severity": "P0 | P1 | P2 | P3",
      "severity_rationale": "Why this severity is appropriate",
      "file": "path/to/file.ext",
      "line": 123,
      "reviewers": ["correctness", "testing"],
      "confidence": 75,
      "body": "Detailed review comment with evidence and why it matters",
      "evidence": [
        "Specific code-grounded evidence with file/line/function context"
      ],
      "suggested_fix": "Concrete suggested fix, or null",
      "autofix_class": "safe_auto | gated_auto | manual | advisory | null",
      "owner": "review-fixer | downstream-resolver | human | release | null",
      "codex_action": "Exact next action Codex should take, or why Codex should not auto-fix this finding",
      "verification": "Targeted verification command or manual check needed after a fix, or null",
      "requires_verification": true,
      "pre_existing": false
    }}
  ],
  "testing_gaps": ["..."],
  "residual_risks": ["..."]
}}
{JSON_END}

JSON rules:
- Use null for unknown file, line, suggested_fix, or confidence.
- Preserve your own severity ranking. Do not omit severity_rationale.
- Preserve CE routing (`autofix_class`, `owner`) and reviewer provenance when available.
- Every substantive finding must include at least one evidence item and a self-contained `codex_action`.
- Use repository-relative file paths.
- Use current file line numbers when possible.
- Include all substantive findings, even if they cannot be mapped to an inline GitHub comment.
"""


def tmux_review_prompt(base_prompt: str, out_dir: Path, *, native_json: bool = False) -> str:
    result_path = out_dir / "claude-result.md"
    done_path = out_dir / "done.json"
    if native_json:
        return f"""{base_prompt}

Interactive tmux runner instructions:
- You are running in a normal interactive Claude Code session launched by `claudet`.
- Do not invoke `claude -p`, the Agent SDK, API keys, Console billing, or usage credits.
- If Claude Code asks to enable API/usage-credit billing, do not consent. Stop and write a failure `done.json` if possible.
- The artifact files below are the source of truth. Do not rely on the visible chat transcript as the final handoff.
- Write the single raw JSON object returned by `ce-code-review mode:agent` to:
  `{result_path}`
- The file must start with `{{` and contain no markdown code fence.
- Do not write `done.json` until the review artifact contains a complete JSON object with `"status": "complete"` or an explicit non-complete status.
- After the review artifact has been fully written and verified, write this JSON object to:
  `{done_path}`

```json
{{
  "status": "complete",
  "message": "Claude PR review artifacts are ready"
}}
```

If you cannot complete the review, write `done.json` with `"status": "failed"` and a concise `"message"` explaining why.
"""

    return f"""{base_prompt}

Interactive tmux runner instructions:
- You are running in a normal interactive Claude Code session launched by `claudet`.
- Do not invoke `claude -p`, the Agent SDK, API keys, Console billing, or usage credits.
- If Claude Code asks to enable API/usage-credit billing, do not consent. Stop and write a failure `done.json` if possible.
- The artifact files below are the source of truth. Do not rely on the visible chat transcript as the final handoff.
- Write the full final review, including the `{JSON_START}` / `{JSON_END}` machine-readable envelope, to:
  `{result_path}`
- Do not write `done.json` until the review artifact contains the full prose review and the complete JSON envelope.
- After the review artifact has been fully written and verified, write this JSON object to:
  `{done_path}`

```json
{{
  "status": "complete",
  "message": "Claude PR review artifacts are ready"
}}
```

If you cannot complete the review, write `done.json` with `"status": "failed"` and a concise `"message"` explaining why.
"""


def ensure_no_billing_env_vars() -> None:
    present = [name for name in FORBIDDEN_BILLING_ENV_VARS if os.environ.get(name)]
    if present:
        joined = ", ".join(present)
        raise ReviewError(
            f"refusing tmux runner while billing/auth env vars are set: {joined}; "
            "unset them so claudet uses the normal interactive Claude Code login"
        )

    if subprocess.run(["/usr/bin/env", "which", "tmux"], capture_output=True).returncode != 0:
        return
    for name in FORBIDDEN_BILLING_ENV_VARS:
        proc = subprocess.run(
            ["tmux", "show-environment", "-g", name],
            text=True,
            capture_output=True,
        )
        if proc.returncode == 0 and proc.stdout.startswith(f"{name}="):
            raise ReviewError(
                f"refusing tmux runner because tmux global environment contains {name}; "
                f"run `tmux set-environment -gu {name}` or restart tmux before using claudet"
            )


def env_without_billing_vars() -> dict[str, str]:
    env = dict(os.environ)
    for name in FORBIDDEN_BILLING_ENV_VARS:
        env.pop(name, None)
    return env


def capture_tmux_pane(session_name: str, out_dir: Path) -> str:
    proc = subprocess.run(
        ["tmux", "capture-pane", "-p", "-S", "-2000", "-t", f"{session_name}:0"],
        text=True,
        capture_output=True,
    )
    text = proc.stdout if proc.returncode == 0 else (proc.stderr or "")
    write_text(out_dir / "claude-pane.log", text)
    return text


def summarize_pane_activity(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "Claude interactive session is open"
    tail = lines[-1]
    return f"Claude tmux pane: {tail[:160]}"


def paste_message_into_tmux(session_name: str, message_path: Path, out_dir: Path) -> None:
    buffer_name = f"claude-pr-review-{out_dir.name}"
    target = f"{session_name}:0"
    for command in [
        ["tmux", "load-buffer", "-b", buffer_name, str(message_path)],
        ["tmux", "paste-buffer", "-b", buffer_name, "-t", target],
        ["tmux", "send-keys", "-t", target, "Enter"],
        ["tmux", "delete-buffer", "-b", buffer_name],
    ]:
        proc = subprocess.run(command, text=True, capture_output=True)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout).strip()
            raise ReviewError(f"tmux command failed: {' '.join(command)}: {detail}")


def run_claude_tmux_review(
    repo: Path,
    claudet: str,
    prompt: str,
    out_dir: Path,
    *,
    timeout: float,
    startup_wait: float,
) -> str:
    require_tool("tmux")
    require_executable(claudet)
    ensure_no_billing_env_vars()

    result_path = out_dir / "claude-result.md"
    done_path = out_dir / "done.json"
    prompt_path = out_dir / "prompt.md"
    message_path = out_dir / "tmux-message.txt"
    write_text(prompt_path, prompt)
    write_text(
        message_path,
        f"Read and follow exactly: {prompt_path}. Write completion status to {done_path}.\n",
    )

    update_state(
        out_dir,
        {
            "runner": "tmux",
            "claude_output_format": "interactive-tmux",
            "claude_prompt_path": str(prompt_path),
            "claude_done_path": str(done_path),
            "claude_result_path": str(result_path),
            "claude_pane_log_path": str(out_dir / "claude-pane.log"),
            "last_activity": "starting Claude Code through claudet",
            "last_event_at": utc_now(),
        },
    )

    proc = subprocess.run(
        [claudet, "--detach", "--new"],
        cwd=repo,
        text=True,
        capture_output=True,
        env=env_without_billing_vars(),
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise ReviewError(f"claudet failed: {detail}")

    session_name = ""
    for line in proc.stdout.splitlines():
        if line.strip():
            session_name = line.strip()
    if not session_name:
        raise ReviewError("claudet did not print a tmux session name")

    update_state(
        out_dir,
        {
            "claude_tmux_session": session_name,
            "last_activity": f"Claude Code tmux session started: {session_name}",
            "last_event_at": utc_now(),
        },
    )

    if startup_wait > 0:
        time.sleep(startup_wait)
    paste_message_into_tmux(session_name, message_path, out_dir)
    update_state(
        out_dir,
        {
            "last_activity": "sent review instructions to Claude Code tmux session",
            "last_event_at": utc_now(),
        },
    )

    deadline = time.time() + timeout
    last_state_write = 0.0
    while True:
        pane_text = capture_tmux_pane(session_name, out_dir)
        now = time.time()
        if now - last_state_write >= STREAM_PROGRESS_INTERVAL_SECONDS:
            update_state(
                out_dir,
                {
                    "last_activity": summarize_pane_activity(pane_text),
                    "last_event_at": utc_now(),
                },
            )
            last_state_write = now

        if done_path.is_file():
            try:
                done = read_json(done_path)
            except json.JSONDecodeError as exc:
                raise ReviewError(f"Claude wrote malformed done.json: {exc}") from exc
            status = str(done.get("status") or "").lower()
            if status != "complete":
                raise ReviewError(f"Claude tmux review failed: {done.get('message') or done}")
            if not result_path.is_file():
                raise ReviewError(f"Claude marked complete but did not write {result_path}")
            result = result_path.read_text(encoding="utf-8")
            if not result.strip():
                raise ReviewError(f"Claude wrote an empty review artifact: {result_path}")
            update_state(
                out_dir,
                {
                    "last_activity": "Claude tmux review artifacts are complete",
                    "last_event_at": utc_now(),
                },
            )
            return result

        if time.time() > deadline:
            raise ReviewError(
                f"timed out waiting for Claude tmux review; attach with `tmux attach -t {session_name}` "
                f"or inspect {out_dir / 'claude-pane.log'}"
            )
        time.sleep(10.0)


def maybe_shutdown_tmux_session(out_dir: Path, policy: str, *, successful: bool) -> dict[str, Any] | None:
    if policy == "never" or (policy == "on-complete" and not successful):
        return None

    state_path = out_dir / "state.json"
    state = read_json(state_path) if state_path.is_file() else {}
    session_name = state.get("claude_tmux_session")
    if not session_name:
        return update_state(
            out_dir,
            {
                "claude_tmux_shutdown": {
                    "policy": policy,
                    "status": "skipped",
                    "reason": "no tmux session recorded",
                    "at": utc_now(),
                },
            },
        )

    has_session = subprocess.run(
        ["tmux", "has-session", "-t", str(session_name)],
        text=True,
        capture_output=True,
    )
    if has_session.returncode != 0:
        return update_state(
            out_dir,
            {
                "claude_tmux_shutdown": {
                    "policy": policy,
                    "status": "already_gone",
                    "session": session_name,
                    "at": utc_now(),
                },
            },
        )

    proc = subprocess.run(
        ["tmux", "kill-session", "-t", str(session_name)],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return update_state(
            out_dir,
            {
                "claude_tmux_shutdown": {
                    "policy": policy,
                    "status": "failed",
                    "session": session_name,
                    "error": (proc.stderr or proc.stdout).strip(),
                    "at": utc_now(),
                },
            },
        )

    return update_state(
        out_dir,
        {
            "claude_tmux_shutdown": {
                "policy": policy,
                "status": "killed",
                "session": session_name,
                "successful_run": successful,
                "at": utc_now(),
            },
        },
    )


def describe_claude_stream_event(
    payload: dict[str, Any],
    current_tool: str | None,
) -> tuple[str, dict[str, Any], str | None, bool]:
    event_type = str(payload.get("type") or "unknown")
    subtype = payload.get("subtype")
    event_label = event_type if not subtype else f"{event_type}/{subtype}"
    updates: dict[str, Any] = {"last_event_type": event_label}
    activity = f"Claude emitted {event_label}"
    force = event_type != "stream_event"

    session_id = payload.get("session_id")
    if session_id:
        updates["claude_session_id"] = session_id

    if event_type == "system":
        if subtype == "init":
            activity = "Claude session initialized"
            for key in ("model", "tools", "mcp_servers", "plugins", "plugin_errors"):
                if key in payload:
                    updates[f"claude_{key}"] = payload.get(key)
        elif subtype == "api_retry":
            attempt = payload.get("attempt")
            max_retries = payload.get("max_retries")
            delay_ms = payload.get("retry_delay_ms")
            error = payload.get("error") or "unknown error"
            retry_label = f"{attempt}/{max_retries}" if attempt and max_retries else "scheduled"
            activity = f"Claude API retry {retry_label}: {error}"
            if delay_ms is not None:
                activity += f" after {delay_ms}ms"
            updates["claude_last_retry"] = {
                "attempt": attempt,
                "max_retries": max_retries,
                "retry_delay_ms": delay_ms,
                "error_status": payload.get("error_status"),
                "error": payload.get("error"),
            }
        elif subtype == "plugin_install":
            status = payload.get("status") or "progress"
            name = payload.get("name")
            activity = f"Claude plugin install {status}"
            if name:
                activity += f": {name}"

    elif event_type == "stream_event":
        event = payload.get("event") if isinstance(payload.get("event"), dict) else {}
        api_event_type = str(event.get("type") or "unknown")
        updates["last_event_type"] = f"stream_event/{api_event_type}"
        force = api_event_type in {"content_block_start", "content_block_stop", "message_stop"}

        if api_event_type == "message_start":
            activity = "Claude started an assistant turn"
        elif api_event_type == "message_delta":
            activity = "Claude updated assistant turn metadata"
        elif api_event_type == "message_stop":
            activity = "Claude finished an assistant turn"
        elif api_event_type == "content_block_start":
            block = event.get("content_block") if isinstance(event.get("content_block"), dict) else {}
            if block.get("type") == "tool_use":
                current_tool = str(block.get("name") or "tool")
                updates["current_tool"] = current_tool
                activity = f"Claude started tool {current_tool}"
            else:
                activity = "Claude started drafting review text"
        elif api_event_type == "content_block_delta":
            delta = event.get("delta") if isinstance(event.get("delta"), dict) else {}
            delta_type = delta.get("type")
            if delta_type == "text_delta":
                activity = "Claude is drafting review text"
            elif delta_type == "input_json_delta":
                activity = (
                    f"Claude is preparing input for {current_tool}"
                    if current_tool
                    else "Claude is preparing tool input"
                )
            else:
                activity = f"Claude streamed {delta_type or 'content'}"
        elif api_event_type == "content_block_stop":
            if current_tool:
                activity = f"Claude finished tool {current_tool}"
                updates["current_tool"] = None
                current_tool = None
            else:
                activity = "Claude finished a content block"
        else:
            activity = f"Claude streamed {api_event_type}"

    elif event_type == "assistant":
        activity = "Claude completed an assistant message"
    elif event_type == "user":
        activity = "Claude received a tool result"
    elif event_type == "result":
        activity = "Claude returned the final review"
        for key in ("subtype", "duration_ms", "duration_api_ms", "num_turns", "cost_usd", "is_error"):
            if key in payload:
                updates[f"claude_result_{key}"] = payload.get(key)

    updates["last_activity"] = activity
    return activity, updates, current_tool, force


def run_claude_review(repo: Path, claude: str, prompt: str, out_dir: Path) -> str:
    stream_path = out_dir / "claude-output.ndjson"
    raw_path = out_dir / "claude-output.json"
    result_path = out_dir / "claude-result.md"
    stderr_path = out_dir / "claude-stderr.log"
    update_state(
        out_dir,
        {
            "claude_output_format": "stream-json",
            "claude_stream_path": str(stream_path),
            "last_activity": "starting Claude Code review",
            "last_event_at": utc_now(),
        },
    )

    command = [
        claude,
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
        "--permission-mode",
        "bypassPermissions",
        prompt,
    ]

    result_payload: dict[str, Any] | None = None
    streamed_text_parts: list[str] = []
    current_tool: str | None = None
    last_state_write = 0.0
    last_progress_write = 0.0
    last_activity: str | None = None

    def maybe_record_event(payload: dict[str, Any], *, force: bool = False) -> None:
        nonlocal current_tool, last_state_write, last_progress_write, last_activity

        activity, updates, current_tool, event_force = describe_claude_stream_event(payload, current_tool)
        now = time.monotonic()
        should_write_state = (
            force
            or event_force
            or activity != last_activity
            or now - last_state_write >= STREAM_STATE_INTERVAL_SECONDS
        )
        if should_write_state:
            updates["last_event_at"] = utc_now()
            update_state(out_dir, updates)
            last_state_write = now

        should_emit_progress = (
            activity != last_activity
            or now - last_progress_write >= STREAM_PROGRESS_INTERVAL_SECONDS
        )
        if should_emit_progress:
            print(f"claude-pr-review: {activity}", file=sys.stderr, flush=True)
            last_progress_write = now
        last_activity = activity

    with stream_path.open("w", encoding="utf-8") as stream_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        proc = subprocess.Popen(
            command,
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=stderr_file,
            bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            stream_file.write(line)
            stream_file.flush()
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                maybe_record_event({"type": "unknown", "subtype": "non_json_stdout"}, force=True)
                continue

            if payload.get("type") == "stream_event":
                event = payload.get("event") if isinstance(payload.get("event"), dict) else {}
                delta = event.get("delta") if isinstance(event.get("delta"), dict) else {}
                if event.get("type") == "content_block_delta" and delta.get("type") == "text_delta":
                    streamed_text_parts.append(str(delta.get("text") or ""))
            if payload.get("type") == "result":
                result_payload = payload
            maybe_record_event(payload)

        proc.stdout.close()
        returncode = proc.wait()

    if result_payload is not None:
        write_json(raw_path, result_payload)
    else:
        write_json(raw_path, {"type": "result", "subtype": "missing_result", "result": "".join(streamed_text_parts)})

    stderr_text = stderr_path.read_text(encoding="utf-8") if stderr_path.is_file() else ""
    if returncode != 0:
        detail = (
            stderr_text.strip()
            or (result_payload or {}).get("result")
            or stream_path.read_text(encoding="utf-8")[-4000:]
        )
        raise ReviewError(f"claude review failed: {str(detail).strip()}")

    if result_payload and result_payload.get("is_error"):
        detail = result_payload.get("result") or result_payload.get("subtype") or "Claude returned an error result"
        raise ReviewError(f"claude review failed: {detail}")

    result = (result_payload or {}).get("result") or "".join(streamed_text_parts)
    if not result:
        raise ReviewError(f"claude review did not return a final result; inspect {stream_path}")

    update_state(
        out_dir,
        {
            "last_activity": "Claude review stream complete",
            "last_event_at": utc_now(),
            "claude_result_path": str(result_path),
        },
    )
    write_text(result_path, result)
    return result


def adapt_native_ce_review(payload: dict[str, Any]) -> dict[str, Any]:
    findings = payload.get("findings") if isinstance(payload.get("findings"), list) else []
    actionable_ids = {
        item.get("#")
        for item in payload.get("actionable_findings", [])
        if isinstance(item, dict) and item.get("#") is not None
    }
    adapted_findings: list[dict[str, Any]] = []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        adapted = dict(finding)
        why_it_matters = str(adapted.get("why_it_matters") or adapted.get("body") or "").strip()
        severity = normalize_severity(adapted.get("severity"))
        confidence = adapted.get("confidence")
        adapted.setdefault("body", why_it_matters or str(adapted.get("title") or "Code review finding"))
        adapted.setdefault(
            "severity_rationale",
            f"Compound Engineering assigned {severity}"
            + (f" with confidence {confidence}" if confidence is not None else "")
            + (f": {why_it_matters}" if why_it_matters else "."),
        )
        if not adapted.get("codex_action"):
            if adapted.get("#") in actionable_ids or adapted.get("owner") == "downstream-resolver":
                adapted["codex_action"] = "Codex should validate this CE actionable finding, apply the smallest defensible fix, and run targeted verification."
            else:
                adapted["codex_action"] = "Codex should surface this CE finding as report context and only fix it if it remains actionable in the requested scope."
        if adapted.get("requires_verification") and not adapted.get("verification"):
            adapted["verification"] = "Run targeted tests or a focused verification pass for the touched behavior after any fix."
        adapted_findings.append(adapted)

    reviewers = payload.get("reviewers") if isinstance(payload.get("reviewers"), list) else []
    scope = payload.get("scope") if isinstance(payload.get("scope"), dict) else {}
    summary_parts = [
        "Compound Engineering code review completed in mode:agent.",
        f"Verdict: {payload.get('verdict') or 'Ready with fixes'}.",
    ]
    if payload.get("intent"):
        summary_parts.append(f"Intent: {payload['intent']}")
    if reviewers:
        summary_parts.append(f"Reviewers: {', '.join(str(item) for item in reviewers)}.")
    if scope:
        summary_parts.append(
            f"Scope: {scope.get('branch') or 'current branch'} at {scope.get('head_sha') or 'unknown HEAD'}; "
            f"{scope.get('files_changed', 'unknown')} files changed."
        )

    return {
        "verdict": payload.get("verdict") or "Ready with fixes",
        "summary": " ".join(summary_parts),
        "severity_ranking_note": (
            "Native ce-code-review mode:agent P0-P3 severities, confidence anchors, "
            "reviewer provenance, routing, and validation results are preserved in this payload."
        ),
        "findings": adapted_findings,
        "testing_gaps": payload.get("testing_gaps") or [],
        "residual_risks": payload.get("residual_risks") or [],
        "triage_groups": payload.get("triage_groups") or [],
        "pre_existing_findings": payload.get("pre_existing_findings") or [],
        "requirements_completeness": payload.get("requirements_completeness"),
        "learnings": payload.get("learnings") or [],
        "agent_native_gaps": payload.get("agent_native_gaps") or [],
        "deployment_notes": payload.get("deployment_notes") or [],
        "coverage": payload.get("coverage") or {},
        "native_ce_review": payload,
    }


def extract_review_json(text: str, *, require_envelope: bool = False) -> dict[str, Any]:
    match = re.search(
        re.escape(JSON_START) + r"\s*(\{.*?\})\s*" + re.escape(JSON_END),
        text,
        flags=re.DOTALL,
    )
    if not match:
        stripped = text.strip()
        if stripped.startswith("{"):
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ReviewError(f"claude returned malformed native review JSON: {exc}") from exc
            if isinstance(payload, dict) and ("actionable_findings" in payload or "triage_groups" in payload):
                status = str(payload.get("status") or "complete").lower()
                if status not in {"complete", "degraded"}:
                    raise ReviewError(f"native ce-code-review returned {status}: {payload.get('reason') or payload}")
                return adapt_native_ce_review(payload)
            if isinstance(payload, dict):
                return payload
        if require_envelope:
            raise ReviewError(
                f"Claude review artifact is missing the required {JSON_START} / {JSON_END} JSON envelope"
            )
        return {
            "verdict": "Ready with fixes",
            "summary": text,
            "severity_ranking_note": "Claude did not return the requested JSON envelope.",
            "findings": [],
            "testing_gaps": [],
            "residual_risks": [],
        }
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ReviewError(f"claude returned malformed review JSON: {exc}") from exc


def validate_review_contract(review: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    errors: list[str] = []

    summary = str(review.get("summary") or "").strip()
    if len(summary) < 80:
        errors.append("summary is missing or too short")

    severity_note = str(review.get("severity_ranking_note") or "").strip()
    if len(severity_note) < 20:
        errors.append("severity_ranking_note is missing or too short")

    raw_findings = review.get("findings")
    if not isinstance(raw_findings, list):
        errors.append("findings must be a JSON list")
    elif len(raw_findings) != len(findings):
        errors.append("one or more findings could not be normalized")
    else:
        for index, finding in enumerate(raw_findings, start=1):
            if not isinstance(finding, dict):
                errors.append(f"finding {index} is not an object")
                continue
            title = str(finding.get("title") or "").strip()
            severity = str(finding.get("severity") or "").strip().upper()
            body = str(finding.get("body") or finding.get("why_it_matters") or "").strip()
            rationale = str(finding.get("severity_rationale") or "").strip()
            evidence = normalize_string_list(finding.get("evidence"))
            codex_action = str(finding.get("codex_action") or "").strip()
            if not title:
                errors.append(f"finding {index} is missing title")
            if severity not in SEVERITY_ORDER:
                errors.append(f"finding {index} has invalid severity")
            if len(body) < 40:
                errors.append(f"finding {index} body is missing or too short")
            if len(rationale) < 20:
                errors.append(f"finding {index} severity_rationale is missing or too short")
            if not evidence:
                errors.append(f"finding {index} evidence is missing")
            if len(codex_action) < 20:
                errors.append(f"finding {index} codex_action is missing or too short")

    if errors:
        raise ReviewError("Claude review artifact is not detailed enough for Codex action: " + "; ".join(errors))


def normalize_severity(value: Any) -> str:
    severity = str(value or "P3").strip().upper()
    if severity not in SEVERITY_ORDER:
        return "P3"
    return severity


def normalize_line(value: Any) -> int | None:
    if value in (None, "", "null"):
        return None
    try:
        line = int(value)
    except (TypeError, ValueError):
        return None
    return line if line > 0 else None


def normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, "", "null"):
        return []
    return [str(value).strip()]


def normalize_findings(review: dict[str, Any]) -> list[dict[str, Any]]:
    findings = review.get("findings") or []
    normalized: list[dict[str, Any]] = []
    if not isinstance(findings, list):
        return normalized

    for index, finding in enumerate(findings, start=1):
        if not isinstance(finding, dict):
            continue
        title = str(finding.get("title") or f"Finding {index}").strip()
        severity = normalize_severity(finding.get("severity"))
        file_value = finding.get("file")
        file_path = str(file_value).strip() if file_value not in (None, "") else None
        body = str(finding.get("body") or finding.get("why_it_matters") or title).strip()
        normalized.append(
            {
                "id": index,
                "title": title,
                "severity": severity,
                "severity_rationale": str(finding.get("severity_rationale") or "").strip() or None,
                "file": file_path,
                "line": normalize_line(finding.get("line")),
                "reviewers": normalize_string_list(finding.get("reviewers") or finding.get("reviewer")),
                "confidence": finding.get("confidence"),
                "body": body,
                "evidence": normalize_string_list(finding.get("evidence")),
                "suggested_fix": finding.get("suggested_fix") or None,
                "autofix_class": finding.get("autofix_class") or None,
                "owner": finding.get("owner") or None,
                "codex_action": str(finding.get("codex_action") or "").strip() or None,
                "verification": finding.get("verification") or None,
                "requires_verification": bool(finding.get("requires_verification", False)),
                "pre_existing": bool(finding.get("pre_existing", False)),
            }
        )

    normalized.sort(
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 99),
            str(item.get("file") or ""),
            item.get("line") or 0,
            item["id"],
        )
    )
    return normalized


def pr_patch(repo: Path) -> str:
    return command_output(["gh", "pr", "diff", "--patch"], repo, check=False)


def diff_line_map(patch: str) -> dict[str, set[int]]:
    allowed: dict[str, set[int]] = {}
    current_file: str | None = None
    new_line: int | None = None

    for raw_line in patch.splitlines():
        if raw_line.startswith("+++ b/"):
            current_file = raw_line[6:]
            allowed.setdefault(current_file, set())
            new_line = None
            continue
        if raw_line.startswith("+++ /dev/null"):
            current_file = None
            new_line = None
            continue
        if raw_line.startswith("@@ "):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw_line)
            new_line = int(match.group(1)) if match else None
            continue
        if current_file is None or new_line is None:
            continue
        if raw_line.startswith("-"):
            continue
        if raw_line.startswith("\\"):
            continue
        allowed[current_file].add(new_line)
        if raw_line.startswith("+") or raw_line.startswith(" "):
            new_line += 1

    return allowed


def trim_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    marker = "\n\n[Trimmed for GitHub length limit.]"
    return value[: max(0, limit - len(marker))].rstrip() + marker


def list_of_strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value)]


def comment_body(finding: dict[str, Any], run_id_value: str) -> str:
    parts = [
        f"**[{finding['severity']}] {finding['title']}**",
        finding["body"],
    ]
    if finding.get("reviewers"):
        parts.append(f"Reviewers: {', '.join(finding['reviewers'])}")
    if finding.get("severity_rationale"):
        parts.append(f"Severity rationale: {finding['severity_rationale']}")
    if finding.get("evidence"):
        evidence = "\n".join(f"- {item}" for item in finding["evidence"][:3])
        parts.append(f"Evidence:\n{evidence}")
    route = " -> ".join(str(value) for value in [finding.get("autofix_class"), finding.get("owner")] if value)
    if route:
        parts.append(f"Route: `{route}`")
    if finding.get("codex_action"):
        parts.append(f"Codex action: {finding['codex_action']}")
    if finding.get("suggested_fix"):
        parts.append(f"Suggested fix: {finding['suggested_fix']}")
    if finding.get("verification"):
        parts.append(f"Verification: {finding['verification']}")
    if finding.get("requires_verification"):
        parts.append("Requires verification after fixing.")
    parts.append(f"_Claude Code review run `{run_id_value}`._")
    return trim_text("\n\n".join(part for part in parts if part), MAX_COMMENT_CHARS)


def build_summary(
    run_id_value: str,
    pr: dict[str, Any],
    review: dict[str, Any],
    findings: list[dict[str, Any]],
    inline_comments: list[dict[str, Any]],
    non_inline: list[dict[str, Any]],
    warnings: list[str],
) -> str:
    lines = [
        f"<!-- claude-pr-review:{run_id_value} -->",
        "## Claude Code Review",
        "",
        f"Run: `{run_id_value}`",
        f"Verdict: **{review.get('verdict') or 'Ready with fixes'}**",
        f"PR: {pr.get('url', '')}",
        "",
        "### Severity Calibration",
        "",
        str(review.get("severity_ranking_note") or "Claude's own P0-P3 severity ranking is preserved below."),
        "",
        "### Summary",
        "",
        str(review.get("summary") or "Claude completed the review."),
        "",
        "### Findings",
        "",
    ]

    if not findings:
        lines.append("No substantive findings were returned in the machine-readable review envelope.")
    for finding in findings:
        location = f"{finding.get('file')}:{finding.get('line')}" if finding.get("file") and finding.get("line") else "not inline-mappable"
        lines.extend(
            [
                f"- **[{finding['severity']}] {finding['title']}** ({location})",
                f"  Severity rationale: {finding.get('severity_rationale') or 'not provided'}",
            ]
        )
        if finding.get("reviewers"):
            lines.append(f"  Reviewers: {', '.join(finding['reviewers'])}")
        if finding.get("autofix_class") or finding.get("owner"):
            route = " -> ".join(str(value) for value in [finding.get("autofix_class"), finding.get("owner")] if value)
            lines.append(f"  Route: `{route}`")
        if finding.get("codex_action"):
            lines.append(f"  Codex action: {finding['codex_action']}")
        if finding.get("evidence"):
            lines.append(f"  Evidence: {finding['evidence'][0]}")
        if finding.get("suggested_fix"):
            lines.append(f"  Suggested fix: {finding['suggested_fix']}")
        if finding.get("verification"):
            lines.append(f"  Verification: {finding['verification']}")

    testing_gaps = list_of_strings(review.get("testing_gaps"))
    residual_risks = list_of_strings(review.get("residual_risks"))

    if testing_gaps:
        lines.extend(["", "### Testing Gaps", ""])
        lines.extend(f"- {gap}" for gap in testing_gaps)

    if residual_risks:
        lines.extend(["", "### Residual Risks", ""])
        lines.extend(f"- {risk}" for risk in residual_risks)

    lines.extend(
        [
            "",
            "### Posting Coverage",
            "",
            f"- Inline comments prepared: {len(inline_comments)}",
            f"- Findings included in summary only: {len(non_inline)}",
        ]
    )
    if warnings:
        lines.extend(["", "### Warnings", ""])
        lines.extend(f"- {warning}" for warning in warnings)

    return trim_text("\n".join(lines).strip() + "\n", MAX_BODY_CHARS)


def split_inline_comments(
    findings: list[dict[str, Any]],
    allowed_lines: dict[str, set[int]],
    run_id_value: str,
    limit: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    inline: list[dict[str, Any]] = []
    non_inline: list[dict[str, Any]] = []

    for finding in findings:
        file_path = finding.get("file")
        line = finding.get("line")
        if (
            file_path
            and line
            and file_path in allowed_lines
            and line in allowed_lines[file_path]
            and len(inline) < limit
        ):
            inline.append(
                {
                    "path": file_path,
                    "line": line,
                    "side": "RIGHT",
                    "body": comment_body(finding, run_id_value),
                }
            )
        else:
            non_inline.append(finding)
    return inline, non_inline


def post_review(
    repo: Path,
    repo_full_name: str,
    pr_number: int,
    summary: str,
    inline_comments: list[dict[str, Any]],
    out_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    summary_path = out_dir / "summary.md"
    payload_path = out_dir / "review-payload.json"
    write_text(summary_path, summary)

    payload: dict[str, Any] = {"event": "COMMENT", "body": summary}
    if inline_comments:
        payload["comments"] = inline_comments
    write_json(payload_path, payload)

    if dry_run:
        return {"posted": False, "dry_run": True, "inline_comment_count": len(inline_comments)}

    endpoint = f"repos/{repo_full_name}/pulls/{pr_number}/reviews"
    try:
        output = command_output(["gh", "api", "--method", "POST", endpoint, "--input", str(payload_path)], repo)
        response = json.loads(output) if output else {}
        return {
            "posted": True,
            "inline_comment_count": len(inline_comments),
            "review_url": response.get("html_url"),
            "api_response": response,
        }
    except Exception as exc:
        fallback_error = str(exc)
        command_output(["gh", "pr", "review", str(pr_number), "--comment", "--body-file", str(summary_path)], repo)
        return {
            "posted": True,
            "inline_comment_count": 0,
            "fallback_summary_only": True,
            "fallback_reason": fallback_error,
        }


def initial_state(run_id_value: str, repo: Path) -> dict[str, Any]:
    return {
        "run_id": run_id_value,
        "status": "pending",
        "repo": str(repo),
        "artifact_dir": str(artifact_dir(run_id_value)),
        "started_at": utc_now(),
    }


def update_state(out_dir: Path, updates: dict[str, Any]) -> dict[str, Any]:
    state_path = out_dir / "state.json"
    state = read_json(state_path) if state_path.is_file() else {}
    state.update(updates)
    write_json(state_path, state)
    return state


def run_review(args: argparse.Namespace) -> int:
    require_tool("git")
    require_tool("gh")

    repo = repo_root(args.repo)
    rid = args.run_id or run_id()
    out_dir = artifact_dir(rid)
    out_dir.mkdir(parents=True, exist_ok=True)
    latest_scope = set_latest(rid)
    state = initial_state(rid, repo)
    state["latest_scope"] = latest_scope
    write_json(out_dir / "state.json", state)

    if args.detach and not args.worker:
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "run",
            "--repo",
            str(repo),
            "--run-id",
            rid,
            "--worker",
        ]
        for flag, enabled in [
            ("--dry-run", args.dry_run),
            ("--allow-dirty", args.allow_dirty),
            ("--allow-head-mismatch", args.allow_head_mismatch),
        ]:
            if enabled:
                command.append(flag)
        if args.base:
            command.extend(["--base", args.base])
        if args.claude_bin:
            command.extend(["--claude-bin", args.claude_bin])
        if args.claude_skill:
            command.extend(["--claude-skill", args.claude_skill])
        if args.claudet_bin:
            command.extend(["--claudet-bin", args.claudet_bin])
        command.extend(["--runner", args.runner])
        command.extend(["--tmux-timeout", str(args.tmux_timeout)])
        command.extend(["--tmux-startup-wait", str(args.tmux_startup_wait)])
        command.extend(["--tmux-shutdown", args.tmux_shutdown])
        command.extend(["--max-inline-comments", str(args.max_inline_comments)])

        log_path = out_dir / "runner.log"
        with log_path.open("w", encoding="utf-8") as log_file:
            proc = subprocess.Popen(command, cwd=repo, stdout=log_file, stderr=subprocess.STDOUT)
        update_state(out_dir, {"status": "running", "pid": proc.pid, "detached": True})
        print(json.dumps({"run_id": rid, "status": "running", "artifact_dir": str(out_dir)}, indent=2))
        return 0

    try:
        update_state(out_dir, {"status": "running", "detached": bool(args.worker)})
        dirty = git_status(repo)
        if dirty and not args.allow_dirty:
            raise ReviewError("worktree is dirty; commit/stash changes or rerun with --allow-dirty")

        pr = pr_metadata(repo)
        local_head = current_head(repo)
        pr_head = pr.get("headRefOid")
        warnings: list[str] = []
        if pr_head and local_head != pr_head:
            message = f"local HEAD {local_head[:12]} does not match PR head {pr_head[:12]}"
            if not args.allow_head_mismatch:
                raise ReviewError(message + "; push/sync the branch or rerun with --allow-head-mismatch")
            warnings.append(message)

        full_name = repo_name_with_owner(repo)
        base_ref = ensure_base_ref(repo, pr["baseRefName"], args.base)
        claude = claude_bin(args.claude_bin)
        skill = detect_claude_skill(repo, claude, args.claude_skill)

        update_state(
            out_dir,
            {
                "pr_number": pr.get("number"),
                "pr_url": pr.get("url"),
                "branch": current_branch(repo),
                "head_sha": local_head,
                "base_ref": base_ref,
                "claude_skill": skill,
                "runner": args.runner,
                "dry_run": bool(args.dry_run),
            },
        )

        prompt = review_prompt(skill, base_ref, pr)
        native_ce_json = is_ce_code_review_skill(skill)
        if args.runner == "tmux":
            prompt = tmux_review_prompt(prompt, out_dir, native_json=native_ce_json)
        write_text(out_dir / "prompt.md", prompt)
        if args.runner == "tmux":
            result = run_claude_tmux_review(
                repo,
                claudet_bin(args.claudet_bin),
                prompt,
                out_dir,
                timeout=args.tmux_timeout,
                startup_wait=args.tmux_startup_wait,
            )
        elif args.runner == "claude-p":
            result = run_claude_review(repo, claude, prompt, out_dir)
        else:
            raise ReviewError(f"unsupported runner: {args.runner}")
        review = extract_review_json(result, require_envelope=args.runner == "tmux" and not native_ce_json)
        findings = normalize_findings(review)
        if args.runner == "tmux":
            validate_review_contract(review, findings)
        write_json(out_dir / "findings.json", {"review": review, "findings": findings})

        allowed_lines = diff_line_map(pr_patch(repo))
        inline_comments, non_inline = split_inline_comments(findings, allowed_lines, rid, args.max_inline_comments)
        summary = build_summary(rid, pr, review, findings, inline_comments, non_inline, warnings)
        post_result = post_review(
            repo,
            full_name,
            int(pr["number"]),
            summary,
            inline_comments,
            out_dir,
            args.dry_run,
        )
        state = update_state(
            out_dir,
            {
                "status": "complete",
                "completed_at": utc_now(),
                "finding_count": len(findings),
                "inline_comment_count": len(inline_comments) if not post_result.get("fallback_summary_only") else 0,
                "summary_only_finding_count": len(non_inline)
                + (len(inline_comments) if post_result.get("fallback_summary_only") else 0),
                "post_result": post_result,
                "warnings": warnings,
            },
        )
        if args.runner == "tmux":
            state = maybe_shutdown_tmux_session(out_dir, args.tmux_shutdown, successful=True) or state
        print(json.dumps(state, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        state = update_state(out_dir, {"status": "failed", "completed_at": utc_now(), "error": str(exc)})
        if getattr(args, "runner", None) == "tmux":
            state = maybe_shutdown_tmux_session(out_dir, args.tmux_shutdown, successful=False) or state
        print(f"claude-pr-review failed: {exc}", file=sys.stderr)
        return 1


def status_command(args: argparse.Namespace) -> int:
    rid = resolve_run_id(args.run_id)
    state_path = artifact_dir(rid) / "state.json"
    if not state_path.is_file():
        raise ReviewError(f"state not found for run {rid}: {state_path}")
    state = read_json(state_path)
    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True))
    else:
        print(f"{state.get('run_id')} {state.get('status')} {state.get('artifact_dir')}")
        if state.get("pr_url"):
            print(f"PR: {state['pr_url']}")
        if state.get("last_activity"):
            print(f"Activity: {state['last_activity']}")
        if state.get("last_event_at"):
            age = elapsed_since(state.get("last_event_at"))
            suffix = f" ({age} ago)" if age else ""
            print(f"Last Claude event: {state['last_event_at']}{suffix}")
        if state.get("current_tool"):
            print(f"Current Claude tool: {state['current_tool']}")
        if state.get("runner"):
            print(f"Runner: {state['runner']}")
        if state.get("claude_tmux_session"):
            print(f"Tmux session: {state['claude_tmux_session']}")
        if state.get("claude_pane_log_path"):
            print(f"Pane log: {state['claude_pane_log_path']}")
        if state.get("claude_tmux_shutdown"):
            shutdown = state["claude_tmux_shutdown"]
            if isinstance(shutdown, dict):
                print(f"Tmux shutdown: {shutdown.get('status')} ({shutdown.get('policy')})")
        if state.get("claude_session_id"):
            print(f"Claude session: {state['claude_session_id']}")
        if state.get("claude_stream_path"):
            print(f"Stream: {state['claude_stream_path']}")
        if state.get("finding_count") is not None:
            print(f"Findings: {state['finding_count']}")
        if state.get("error"):
            print(f"Error: {state['error']}")
    return 0


def watch_command(args: argparse.Namespace) -> int:
    rid = resolve_run_id(args.run_id)
    deadline = time.time() + args.timeout
    last_status = None
    last_progress_report = 0.0
    while True:
        state_path = artifact_dir(rid) / "state.json"
        if state_path.is_file():
            state = read_json(state_path)
            status = state.get("status")
            now = time.time()
            should_print_progress = (
                status == "running"
                and not args.json
                and now - last_progress_report >= args.progress_interval
            )
            if (status != last_status or should_print_progress) and not args.json:
                line = f"{rid}: {status}"
                if state.get("last_activity"):
                    line += f" - {state['last_activity']}"
                age = elapsed_since(state.get("last_event_at"))
                if age:
                    line += f" (last Claude event {age} ago)"
                print(line)
                last_status = status
                last_progress_report = now
            if status in {"complete", "failed"}:
                if args.json:
                    print(json.dumps(state, indent=2, sort_keys=True))
                elif status == "complete":
                    print(f"Artifacts: {state.get('artifact_dir')}")
                    print(f"Findings: {state.get('finding_count', 0)}")
                else:
                    print(f"Error: {state.get('error')}", file=sys.stderr)
                return 0 if status == "complete" else 1
        if time.time() > deadline:
            raise ReviewError(f"timed out waiting for run {rid}")
        time.sleep(args.interval)


def load_findings_for_run(run_id_value: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    out_dir = artifact_dir(run_id_value)
    findings_path = out_dir / "findings.json"
    if not findings_path.is_file():
        raise ReviewError(f"findings not found for run {run_id_value}: {findings_path}")
    payload = read_json(findings_path)
    review = payload.get("review") if isinstance(payload, dict) else {}
    findings = payload.get("findings") if isinstance(payload, dict) else []
    if not isinstance(review, dict):
        review = {}
    if not isinstance(findings, list):
        findings = []
    return review, [finding for finding in findings if isinstance(finding, dict)]


def action_queue(findings: list[dict[str, Any]], include_pre_existing: bool = False) -> list[dict[str, Any]]:
    queue = []
    for finding in findings:
        if finding.get("pre_existing") and not include_pre_existing:
            continue
        queue.append(
            {
                "id": finding.get("id"),
                "severity": normalize_severity(finding.get("severity")),
                "title": finding.get("title"),
                "file": finding.get("file"),
                "line": normalize_line(finding.get("line")),
                "reviewers": finding.get("reviewers") or [],
                "severity_rationale": finding.get("severity_rationale"),
                "body": finding.get("body"),
                "evidence": finding.get("evidence") or [],
                "suggested_fix": finding.get("suggested_fix"),
                "autofix_class": finding.get("autofix_class"),
                "owner": finding.get("owner"),
                "codex_action": finding.get("codex_action"),
                "verification": finding.get("verification"),
                "requires_verification": bool(finding.get("requires_verification", False)),
                "confidence": finding.get("confidence"),
            }
        )
    queue.sort(
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 99),
            str(item.get("file") or ""),
            item.get("line") or 0,
            item.get("id") or 0,
        )
    )
    return queue


def actions_command(args: argparse.Namespace) -> int:
    rid = resolve_run_id(args.run_id)
    review, findings = load_findings_for_run(rid)
    queue = action_queue(findings, include_pre_existing=args.include_pre_existing)
    payload = {
        "run_id": rid,
        "artifact_dir": str(artifact_dir(rid)),
        "verdict": review.get("verdict"),
        "severity_ranking_note": review.get("severity_ranking_note"),
        "action_count": len(queue),
        "actions": queue,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print(f"Claude PR review actions for run {rid}")
    print(f"Artifact: {payload['artifact_dir']}")
    if payload.get("verdict"):
        print(f"Verdict: {payload['verdict']}")
    if payload.get("severity_ranking_note"):
        print()
        print("Severity ranking:")
        print(payload["severity_ranking_note"])
    if not queue:
        print()
        print("No actionable findings.")
        return 0
    print()
    for item in queue:
        location = f"{item.get('file')}:{item.get('line')}" if item.get("file") and item.get("line") else "no file:line"
        print(f"- [{item['severity']}] #{item.get('id')} {item.get('title')} ({location})")
        if item.get("reviewers"):
            print(f"  Reviewers: {', '.join(item['reviewers'])}")
        if item.get("autofix_class") or item.get("owner"):
            route = " -> ".join(str(value) for value in [item.get("autofix_class"), item.get("owner")] if value)
            print(f"  Route: {route}")
        if item.get("severity_rationale"):
            print(f"  Severity rationale: {item['severity_rationale']}")
        if item.get("codex_action"):
            print(f"  Codex action: {item['codex_action']}")
        if item.get("evidence"):
            print(f"  Evidence: {item['evidence'][0]}")
        if item.get("suggested_fix"):
            print(f"  Suggested fix: {item['suggested_fix']}")
        if item.get("verification"):
            print(f"  Verification: {item['verification']}")
        if item.get("requires_verification"):
            print("  Requires verification after fixing.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Delegate current PR review to Claude Code and post GitHub comments.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run Claude PR review")
    run_parser.add_argument("--repo", help="Repository path. Defaults to current working directory.")
    run_parser.add_argument("--base", help="Diff base ref to pass to the Claude review skill.")
    run_parser.add_argument("--detach", action="store_true", help="Run in the background and return the run id.")
    run_parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    run_parser.add_argument("--run-id", help="Internal run id. Mostly used by --detach worker.")
    run_parser.add_argument("--dry-run", action="store_true", help="Write artifacts but do not post to GitHub.")
    run_parser.add_argument("--allow-dirty", action="store_true", help="Allow a dirty worktree.")
    run_parser.add_argument(
        "--allow-head-mismatch",
        action="store_true",
        help="Allow local HEAD to differ from the PR head.",
    )
    run_parser.add_argument("--claude-bin", help="Path to Claude Code CLI.")
    run_parser.add_argument("--claude-skill", help="Slash skill to invoke, e.g. /compound-engineering:ce-review.")
    run_parser.add_argument("--claudet-bin", help="Path to claudet. Defaults to ~/.local/bin/claudet or PATH.")
    run_parser.add_argument(
        "--runner",
        choices=["tmux", "claude-p"],
        default=DEFAULT_RUNNER,
        help="Claude runner. Default: tmux (or CLAUDE_PR_REVIEW_RUNNER).",
    )
    run_parser.add_argument(
        "--tmux-timeout",
        type=float,
        default=DEFAULT_TMUX_TIMEOUT_SECONDS,
        help=f"Timeout in seconds for the tmux runner. Default: {int(DEFAULT_TMUX_TIMEOUT_SECONDS)}.",
    )
    run_parser.add_argument(
        "--tmux-startup-wait",
        type=float,
        default=DEFAULT_TMUX_STARTUP_WAIT_SECONDS,
        help=f"Seconds to wait after claudet starts before pasting instructions. Default: {DEFAULT_TMUX_STARTUP_WAIT_SECONDS}.",
    )
    run_parser.add_argument(
        "--tmux-shutdown",
        choices=["on-complete", "always", "never"],
        default=DEFAULT_TMUX_SHUTDOWN,
        help="Whether to kill the Claude tmux session after the run. Default: on-complete.",
    )
    run_parser.add_argument(
        "--max-inline-comments",
        type=int,
        default=DEFAULT_INLINE_LIMIT,
        help=f"Maximum inline comments to post. Default: {DEFAULT_INLINE_LIMIT}.",
    )
    run_parser.set_defaults(func=run_review)

    status_parser = subparsers.add_parser("status", help="Show run status")
    status_parser.add_argument("--run-id", default="latest", help="Run id or 'latest'.")
    status_parser.add_argument("--json", action="store_true", help="Print full state JSON.")
    status_parser.set_defaults(func=status_command)

    watch_parser = subparsers.add_parser("watch", help="Wait for a run to complete")
    watch_parser.add_argument("--run-id", default="latest", help="Run id or 'latest'.")
    watch_parser.add_argument("--interval", type=float, default=10.0, help="Polling interval in seconds.")
    watch_parser.add_argument(
        "--progress-interval",
        type=float,
        default=30.0,
        help="While running, print live Claude activity at this interval in seconds.",
    )
    watch_parser.add_argument("--timeout", type=float, default=3600.0, help="Timeout in seconds.")
    watch_parser.add_argument("--json", action="store_true", help="Print final state JSON.")
    watch_parser.set_defaults(func=watch_command)

    actions_parser = subparsers.add_parser("actions", help="Print actionable findings for Codex to resolve")
    actions_parser.add_argument("--run-id", default="latest", help="Run id or 'latest'.")
    actions_parser.add_argument("--json", action="store_true", help="Print action queue as JSON.")
    actions_parser.add_argument(
        "--include-pre-existing",
        action="store_true",
        help="Include findings Claude marked as pre-existing.",
    )
    actions_parser.set_defaults(func=actions_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if not argv:
        argv = ["run"]
    elif argv[0].startswith("-") and argv[0] not in {"-h", "--help"}:
        argv = ["run", *argv]
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ReviewError as exc:
        print(f"claude-pr-review: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
