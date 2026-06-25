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


ARTIFACT_ROOT = Path("/tmp/agentic/claude-ce")
DEFAULT_TMUX_TIMEOUT_SECONDS = 7200.0
DEFAULT_TMUX_STARTUP_WAIT_SECONDS = 5.0
DEFAULT_TMUX_SHUTDOWN = os.environ.get("CLAUDE_CE_TMUX_SHUTDOWN", "on-complete")
FORBIDDEN_BILLING_ENV_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN")
CODEX_THREAD_ENV_VAR = "CODEX_THREAD_ID"

ROUTES: dict[str, dict[str, str]] = {
    "ideate": {
        "slash": "/compound-engineering:ce-ideate",
        "noun": "ideation",
        "artifact_hint": "docs/ideation/ or the CE scratch path",
    },
    "brainstorm": {
        "slash": "/compound-engineering:ce-brainstorm",
        "noun": "requirements brainstorm",
        "artifact_hint": "docs/brainstorms/",
    },
    "plan": {
        "slash": "/compound-engineering:ce-plan",
        "noun": "plan",
        "artifact_hint": "docs/plans/",
    },
}


class ClaudeCEError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def new_run_id() -> str:
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{os.urandom(3).hex()}"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_jsonl(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(data, sort_keys=True) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_dir(run_id_value: str) -> Path:
    return ARTIFACT_ROOT / run_id_value


def latest_path() -> Path:
    return ARTIFACT_ROOT / "latest"


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
            raise ClaudeCEError(
                f"no latest claude-ce run found for current Codex thread "
                f"({CODEX_THREAD_ENV_VAR}={scope.get('id')}); use an explicit --run-id for another thread"
            )
        raise ClaudeCEError("no latest claude-ce run found")
    resolved = path.read_text(encoding="utf-8").strip()
    if not resolved:
        if scope.get("type") == "codex_thread":
            raise ClaudeCEError(
                f"latest claude-ce run for current Codex thread is empty "
                f"({CODEX_THREAD_ENV_VAR}={scope.get('id')})"
            )
        raise ClaudeCEError("latest claude-ce run is empty")
    return resolved


def command_output(args: list[str], cwd: Path, *, check: bool = True) -> str:
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise ClaudeCEError(f"{args[0]} failed: {detail}")
    return proc.stdout.strip()


def repo_root(repo_arg: str | None) -> Path:
    start = Path(repo_arg or os.getcwd()).expanduser().resolve()
    output = command_output(["git", "rev-parse", "--show-toplevel"], start, check=False)
    return Path(output).resolve() if output else start


def require_tool(name: str) -> None:
    if subprocess.run(["/usr/bin/env", "which", name], capture_output=True).returncode != 0:
        raise ClaudeCEError(f"required tool not found on PATH: {name}")


def require_executable(command: str) -> None:
    expanded = Path(command).expanduser()
    if "/" in command:
        if not expanded.exists() or not os.access(expanded, os.X_OK):
            raise ClaudeCEError(f"required executable not found or not executable: {expanded}")
        return
    require_tool(command)


def claudet_bin(explicit: str | None) -> str:
    if explicit:
        return explicit
    local = Path.home() / ".local/bin/claudet"
    if local.exists():
        return str(local)
    return "claudet"


def ensure_no_billing_env_vars() -> None:
    present = [name for name in FORBIDDEN_BILLING_ENV_VARS if os.environ.get(name)]
    if present:
        joined = ", ".join(present)
        raise ClaudeCEError(
            f"refusing tmux runner while billing/auth env vars are set: {joined}; "
            "unset them so claudet uses the normal interactive Claude Code login"
        )

    if subprocess.run(["/usr/bin/env", "which", "tmux"], capture_output=True).returncode != 0:
        return
    for name in FORBIDDEN_BILLING_ENV_VARS:
        proc = subprocess.run(["tmux", "show-environment", "-g", name], text=True, capture_output=True)
        if proc.returncode == 0 and proc.stdout.startswith(f"{name}="):
            raise ClaudeCEError(
                f"refusing tmux runner because tmux global environment contains {name}; "
                f"run `tmux set-environment -gu {name}` or restart tmux before using claudet"
            )


def env_without_billing_vars() -> dict[str, str]:
    env = dict(os.environ)
    for name in FORBIDDEN_BILLING_ENV_VARS:
        env.pop(name, None)
    return env


def initial_state(run_id_value: str, repo: Path, route: str, args_text: str, out_dir: Path) -> dict[str, Any]:
    return {
        "run_id": run_id_value,
        "status": "created",
        "created_at": utc_now(),
        "repo": str(repo),
        "route": route,
        "arguments": args_text,
        "artifact_dir": str(out_dir),
    }


def update_state(out_dir: Path, updates: dict[str, Any]) -> dict[str, Any]:
    state_path = out_dir / "state.json"
    state = read_json(state_path) if state_path.is_file() else {}
    state.update(updates)
    write_json(state_path, state)
    return state


def route_for(name: str) -> dict[str, str]:
    if name not in ROUTES:
        choices = ", ".join(sorted(ROUTES))
        raise ClaudeCEError(f"unsupported route: {name}. Choose one of: {choices}")
    return ROUTES[name]


def build_prompt(route: str, args_text: str, out_dir: Path) -> str:
    config = route_for(route)
    slash = config["slash"]
    result_path = out_dir / "result.md"
    done_path = out_dir / "done.json"
    pending_question_path = out_dir / "pending-question.json"
    answer_path = out_dir / "answer.json"
    answers_path = out_dir / "answers.jsonl"
    artifact_hint = config["artifact_hint"]

    arg_suffix = f" {args_text}" if args_text else ""
    return f"""You are running in a normal interactive Claude Code session launched by `claudet`.

Invoke this Compound Engineering workflow now:

```text
{slash}{arg_suffix}
```

Use Claude Code's native skill, tools, AskUserQuestion support, and sub-agents. Do not invoke `claude -p`, the Agent SDK, API keys, Console billing, or usage credits. If Claude Code asks to enable API/usage-credit billing, do not consent.

Codex is the outer operator for this run. Artifact files are the source of truth.

Question bridge:
- Before any user question, including before calling `AskUserQuestion`, write a JSON object to `{pending_question_path}`.
- Use this shape:

```json
{{
  "id": "q1",
  "status": "pending",
  "kind": "single_select",
  "question": "Question text",
  "options": [
    {{"label": "First option", "description": "What this chooses"}},
    {{"label": "Second option", "description": "What this chooses"}}
  ],
  "free_text_allowed": true
}}
```

- `options` may be an empty array for open-ended questions.
- After writing `{pending_question_path}`, ask the user through Claude Code normally.
- Codex will ask the user outside this tmux session, write the latest answer to `{answer_path}`, append it to `{answers_path}`, and paste the same answer into this tmux pane.
- Continue from that answer. If useful, read `{answer_path}` after the prompt unblocks.

Completion contract:
- When the {config["noun"]} workflow is complete, write a concise final handoff to `{result_path}`.
- Include the CE-produced artifact path(s), expected under {artifact_hint} when applicable.
- Then write this JSON object to `{done_path}`:

```json
{{
  "status": "complete",
  "message": "Claude CE workflow complete",
  "route": "{route}",
  "result_path": "{result_path}",
  "artifacts": []
}}
```

If you cannot complete the workflow, write `{done_path}` with `"status": "failed"` and a concise `"message"`.
"""


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
    return f"Claude tmux pane: {lines[-1][:160]}"


def paste_message_into_tmux(session_name: str, message: str, out_dir: Path, *, buffer_prefix: str = "claude-ce") -> None:
    message_path = out_dir / "tmux-paste.txt"
    write_text(message_path, message)
    buffer_name = f"{buffer_prefix}-{out_dir.name}"
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
            raise ClaudeCEError(f"tmux command failed: {' '.join(command)}: {detail}")


def pending_question(out_dir: Path) -> dict[str, Any] | None:
    path = out_dir / "pending-question.json"
    if not path.is_file():
        return None
    try:
        question = read_json(path)
    except json.JSONDecodeError as exc:
        raise ClaudeCEError(f"Claude wrote malformed pending-question.json: {exc}") from exc
    if str(question.get("status") or "pending").lower() in {"answered", "cancelled", "complete"}:
        return None
    return question


def format_question(question: dict[str, Any]) -> str:
    lines = [str(question.get("question") or "Claude is asking for input.")]
    options = question.get("options") or []
    if isinstance(options, list) and options:
        lines.append("")
        for index, option in enumerate(options, 1):
            if isinstance(option, dict):
                label = option.get("label") or f"Option {index}"
                description = option.get("description")
                suffix = f" - {description}" if description else ""
                lines.append(f"{index}. {label}{suffix}")
            else:
                lines.append(f"{index}. {option}")
    if question.get("free_text_allowed", True):
        lines.append("")
        lines.append("Reply with a number, or provide free text.")
    else:
        lines.append("")
        lines.append("Reply with one of the numbers above.")
    return "\n".join(lines)


def completion_state(out_dir: Path) -> dict[str, Any] | None:
    done_path = out_dir / "done.json"
    if not done_path.is_file():
        return None
    try:
        done = read_json(done_path)
    except json.JSONDecodeError as exc:
        raise ClaudeCEError(f"Claude wrote malformed done.json: {exc}") from exc
    status = str(done.get("status") or "").lower()
    if status not in {"complete", "failed"}:
        raise ClaudeCEError(f"Claude wrote unsupported done status: {done}")
    updates: dict[str, Any] = {
        "status": "complete" if status == "complete" else "failed",
        "completed_at": utc_now(),
        "done": done,
        "last_activity": "Claude CE workflow complete" if status == "complete" else "Claude CE workflow failed",
        "last_event_at": utc_now(),
    }
    result_path = out_dir / "result.md"
    if result_path.is_file():
        updates["result_path"] = str(result_path)
    if done.get("artifacts") is not None:
        updates["artifacts"] = done.get("artifacts")
    if status == "failed":
        updates["error"] = done.get("message") or "Claude CE workflow failed"
    return update_state(out_dir, updates)


def monitor_run(out_dir: Path, *, timeout: float, interval: float, stop_on_question: bool, json_output: bool) -> int:
    deadline = time.time() + timeout
    last_progress = 0.0
    while True:
        state = read_json(out_dir / "state.json")
        session_name = state.get("claude_tmux_session")
        if session_name:
            pane_text = capture_tmux_pane(str(session_name), out_dir)
            now = time.time()
            if now - last_progress >= 30.0:
                update_state(
                    out_dir,
                    {
                        "last_activity": summarize_pane_activity(pane_text),
                        "last_event_at": utc_now(),
                    },
                )
                last_progress = now

        completed = completion_state(out_dir)
        if completed:
            if json_output:
                print(json.dumps(completed, indent=2, sort_keys=True))
            elif completed["status"] == "complete":
                print(f"Complete: {completed.get('result_path', out_dir / 'result.md')}")
                print(f"Artifacts: {completed.get('artifact_dir')}")
            else:
                print(f"Failed: {completed.get('error')}", file=sys.stderr)
            return 0 if completed["status"] == "complete" else 1

        question = pending_question(out_dir)
        if question and stop_on_question:
            state = update_state(
                out_dir,
                {
                    "status": "waiting_for_user",
                    "pending_question": question,
                    "last_activity": "Claude is waiting for user input",
                    "last_event_at": utc_now(),
                },
            )
            if json_output:
                print(json.dumps(state, indent=2, sort_keys=True))
            else:
                print(f"Run id: {state.get('run_id')}")
                print(format_question(question))
            return 2

        if time.time() > deadline:
            raise ClaudeCEError(f"timed out waiting for run {state.get('run_id')}")
        time.sleep(interval)


def launch_run(
    repo: Path,
    run_id_value: str,
    route: str,
    args_text: str,
    *,
    claudet: str,
    startup_wait: float,
) -> Path:
    require_tool("tmux")
    require_executable(claudet)
    ensure_no_billing_env_vars()

    out_dir = artifact_dir(run_id_value)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "state.json", initial_state(run_id_value, repo, route, args_text, out_dir))
    latest_scope = set_latest(run_id_value)

    prompt = build_prompt(route, args_text, out_dir)
    prompt_path = out_dir / "prompt.md"
    write_text(prompt_path, prompt)
    message = f"Read and follow exactly: {prompt_path}\n"
    write_text(out_dir / "tmux-message.txt", message)

    update_state(
        out_dir,
        {
            "status": "starting",
            "claude_prompt_path": str(prompt_path),
            "claude_done_path": str(out_dir / "done.json"),
            "claude_result_path": str(out_dir / "result.md"),
            "claude_pane_log_path": str(out_dir / "claude-pane.log"),
            "latest_scope": latest_scope,
            "runner": "tmux",
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
        raise ClaudeCEError(f"claudet failed: {detail}")
    session_name = ""
    for line in proc.stdout.splitlines():
        if line.strip():
            session_name = line.strip()
    if not session_name:
        raise ClaudeCEError("claudet did not print a tmux session name")

    update_state(
        out_dir,
        {
            "status": "running",
            "claude_tmux_session": session_name,
            "last_activity": f"Claude Code tmux session started: {session_name}",
            "last_event_at": utc_now(),
        },
    )
    if startup_wait > 0:
        time.sleep(startup_wait)
    paste_message_into_tmux(session_name, message, out_dir)
    update_state(
        out_dir,
        {
            "last_activity": "sent CE workflow instructions to Claude Code tmux session",
            "last_event_at": utc_now(),
        },
    )
    return out_dir


def maybe_shutdown_tmux_session(out_dir: Path, policy: str, *, successful: bool) -> None:
    if policy == "never" or (policy == "on-complete" and not successful):
        return
    state = read_json(out_dir / "state.json")
    session_name = state.get("claude_tmux_session")
    if not session_name:
        return
    exists = subprocess.run(["tmux", "has-session", "-t", str(session_name)], text=True, capture_output=True)
    if exists.returncode != 0:
        return
    proc = subprocess.run(["tmux", "kill-session", "-t", str(session_name)], text=True, capture_output=True)
    update_state(
        out_dir,
        {
            "claude_tmux_shutdown": {
                "policy": policy,
                "status": "killed" if proc.returncode == 0 else "failed",
                "at": utc_now(),
            }
        },
    )


def run_command(args: argparse.Namespace) -> int:
    repo = repo_root(args.repo)
    run_id_value = args.run_id or new_run_id()
    route_for(args.route)
    args_text = " ".join(args.workflow_args).strip()

    out_dir = launch_run(
        repo,
        run_id_value,
        args.route,
        args_text,
        claudet=claudet_bin(args.claudet_bin),
        startup_wait=args.tmux_startup_wait,
    )
    if args.detach:
        state = read_json(out_dir / "state.json")
        print(json.dumps(state, indent=2, sort_keys=True) if args.json else f"{run_id_value} running\nArtifacts: {out_dir}")
        return 0

    code = monitor_run(
        out_dir,
        timeout=args.tmux_timeout,
        interval=args.interval,
        stop_on_question=True,
        json_output=args.json,
    )
    if code == 0:
        maybe_shutdown_tmux_session(out_dir, args.tmux_shutdown, successful=True)
    return code


def status_command(args: argparse.Namespace) -> int:
    run_id_value = resolve_run_id(args.run_id)
    out_dir = artifact_dir(run_id_value)
    state_path = out_dir / "state.json"
    if not state_path.is_file():
        raise ClaudeCEError(f"state not found for run {run_id_value}: {state_path}")
    state = read_json(state_path)
    question = pending_question(out_dir)
    if question:
        state["pending_question"] = question
    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True))
    else:
        print(f"{state.get('run_id')} {state.get('status')} {state.get('route')}")
        print(f"Artifacts: {state.get('artifact_dir')}")
        if state.get("claude_tmux_session"):
            print(f"Tmux session: {state['claude_tmux_session']}")
        if state.get("last_activity"):
            print(f"Activity: {state['last_activity']}")
        if question:
            print("")
            print(format_question(question))
        if state.get("result_path"):
            print(f"Result: {state['result_path']}")
        if state.get("error"):
            print(f"Error: {state['error']}")
    return 0


def watch_command(args: argparse.Namespace) -> int:
    run_id_value = resolve_run_id(args.run_id)
    out_dir = artifact_dir(run_id_value)
    return monitor_run(
        out_dir,
        timeout=args.timeout,
        interval=args.interval,
        stop_on_question=not args.ignore_questions,
        json_output=args.json,
    )


def answer_payload(question: dict[str, Any] | None, *, choice: int | None, text: str | None) -> dict[str, Any]:
    if choice is None and text is None:
        raise ClaudeCEError("provide --choice N or --text TEXT")
    if choice is not None and text is not None:
        raise ClaudeCEError("provide only one of --choice or --text")
    if choice is not None:
        options = question.get("options") if question else None
        if isinstance(options, list) and options and not (1 <= choice <= len(options)):
            raise ClaudeCEError(f"choice {choice} is outside the available range 1-{len(options)}")
        selected = options[choice - 1] if isinstance(options, list) and options else None
        label = selected.get("label") if isinstance(selected, dict) else selected
        return {
            "type": "choice",
            "choice": choice,
            "label": label,
            "text_to_paste": str(choice),
        }
    assert text is not None
    if question and question.get("free_text_allowed") is False:
        raise ClaudeCEError("pending question does not allow free text")
    return {"type": "text", "text": text, "text_to_paste": text}


def answer_command(args: argparse.Namespace) -> int:
    run_id_value = resolve_run_id(args.run_id)
    out_dir = artifact_dir(run_id_value)
    state = read_json(out_dir / "state.json")
    session_name = state.get("claude_tmux_session")
    if not session_name:
        raise ClaudeCEError("run has no recorded Claude tmux session")
    question = pending_question(out_dir)
    payload = answer_payload(question, choice=args.choice, text=args.text)
    event = {
        "answered_at": utc_now(),
        "run_id": run_id_value,
        "question_id": question.get("id") if question else None,
        **payload,
    }
    write_json(out_dir / "answer.json", event)
    append_jsonl(out_dir / "answers.jsonl", event)
    if question:
        question["status"] = "answered"
        question["answer"] = payload
        question["answered_at"] = event["answered_at"]
        write_json(out_dir / "pending-question.json", question)

    paste_message_into_tmux(str(session_name), str(payload["text_to_paste"]), out_dir, buffer_prefix="claude-ce-answer")
    state = update_state(
        out_dir,
        {
            "status": "running",
            "last_answer": event,
            "pending_question": None,
            "last_activity": "pasted user answer into Claude tmux session",
            "last_event_at": utc_now(),
        },
    )
    print(json.dumps(state, indent=2, sort_keys=True) if args.json else f"Answered {run_id_value}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Compound Engineering workflows in interactive Claude Code.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Start a Claude CE workflow")
    run_parser.add_argument("route", choices=sorted(ROUTES))
    run_parser.add_argument("workflow_args", nargs="*")
    run_parser.add_argument("--repo", help="Repo/path to run from. Defaults to cwd.")
    run_parser.add_argument("--run-id", help="Explicit run id.")
    run_parser.add_argument("--detach", action="store_true", help="Start and return immediately.")
    run_parser.add_argument("--json", action="store_true", help="Print JSON state.")
    run_parser.add_argument("--claudet-bin", help="Path to claudet. Defaults to ~/.local/bin/claudet or PATH.")
    run_parser.add_argument("--tmux-timeout", type=float, default=DEFAULT_TMUX_TIMEOUT_SECONDS)
    run_parser.add_argument("--tmux-startup-wait", type=float, default=DEFAULT_TMUX_STARTUP_WAIT_SECONDS)
    run_parser.add_argument("--tmux-shutdown", choices=["never", "on-complete", "always"], default=DEFAULT_TMUX_SHUTDOWN)
    run_parser.add_argument("--interval", type=float, default=5.0)
    run_parser.set_defaults(func=run_command)

    status_parser = subparsers.add_parser("status", help="Show run status")
    status_parser.add_argument("--run-id", default="latest")
    status_parser.add_argument("--json", action="store_true")
    status_parser.set_defaults(func=status_command)

    watch_parser = subparsers.add_parser("watch", help="Watch until complete or user input is needed")
    watch_parser.add_argument("--run-id", default="latest")
    watch_parser.add_argument("--timeout", type=float, default=DEFAULT_TMUX_TIMEOUT_SECONDS)
    watch_parser.add_argument("--interval", type=float, default=5.0)
    watch_parser.add_argument("--ignore-questions", action="store_true", help="Keep waiting even if pending-question.json exists.")
    watch_parser.add_argument("--json", action="store_true")
    watch_parser.set_defaults(func=watch_command)

    answer_parser = subparsers.add_parser("answer", help="Answer a pending Claude question")
    answer_parser.add_argument("--run-id", default="latest")
    answer_group = answer_parser.add_mutually_exclusive_group(required=True)
    answer_group.add_argument("--choice", type=int)
    answer_group.add_argument("--text")
    answer_parser.add_argument("--json", action="store_true")
    answer_parser.set_defaults(func=answer_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ClaudeCEError as exc:
        print(f"claude-ce: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
