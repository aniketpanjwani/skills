#!/usr/bin/env python3
"""Verify that an approved PR head produced a recorded integration commit."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


OBJECT_ID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


class VerificationError(RuntimeError):
    """A fail-closed verification error."""


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise VerificationError(f"git {' '.join(args)}: {detail}")
    return result


def resolve_commit(repo: Path, value: str, label: str) -> str:
    result = git(repo, "rev-parse", "--verify", f"{value}^{{commit}}")
    object_id = result.stdout.strip()
    if not OBJECT_ID.fullmatch(object_id):
        raise VerificationError(f"{label} did not resolve to a commit object ID")
    return object_id


def tree(repo: Path, commit: str) -> str:
    object_id = git(repo, "rev-parse", "--verify", f"{commit}^{{tree}}").stdout.strip()
    if not OBJECT_ID.fullmatch(object_id):
        raise VerificationError(f"{commit} did not resolve to a tree object ID")
    return object_id


def parents(repo: Path, commit: str) -> list[str]:
    output = git(repo, "show", "-s", "--format=%P", commit).stdout.strip()
    return output.split() if output else []


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    result = git(repo, "merge-base", "--is-ancestor", older, newer, check=False)
    if result.returncode not in (0, 1):
        detail = result.stderr.strip() or "unable to determine ancestry"
        raise VerificationError(f"git merge-base --is-ancestor: {detail}")
    return result.returncode == 0


def expected_merge_tree(repo: Path, base: str, candidate: str) -> str:
    result = git(repo, "merge-tree", "--write-tree", base, candidate, check=False)
    if result.returncode != 0:
        raise VerificationError(
            "approved head does not integrate cleanly into the applicable base"
        )
    first_line = next((line.strip() for line in result.stdout.splitlines() if line.strip()), "")
    if not OBJECT_ID.fullmatch(first_line):
        raise VerificationError("git merge-tree did not return an expected tree object ID")
    return first_line


def verify(
    repo: Path,
    method: str,
    candidate_value: str,
    validated_base_value: str,
    integration_value: str,
) -> dict[str, object]:
    candidate = resolve_commit(repo, candidate_value, "candidate")
    validated_base = resolve_commit(repo, validated_base_value, "validated base")
    integration = resolve_commit(repo, integration_value, "integration")
    integration_parents = parents(repo, integration)

    if method == "merge":
        if len(integration_parents) != 2:
            raise VerificationError("merge integration must have exactly two parents")
        integration_base = integration_parents[0]
        if integration_parents[1] != candidate:
            raise VerificationError(
                "merge integration's second parent is not the exact approved head"
            )
        if not is_ancestor(repo, candidate, integration):
            raise VerificationError("exact approved head is not an integration ancestor")
        if not is_ancestor(repo, validated_base, integration_base):
            raise VerificationError(
                "actual integration base does not descend from the validated base"
            )
    elif method == "squash":
        if len(integration_parents) != 1:
            raise VerificationError("squash integration must have exactly one parent")
        integration_base = integration_parents[0]
        if not is_ancestor(repo, validated_base, integration_base):
            raise VerificationError(
                "actual integration base does not descend from the validated base"
            )
    else:
        integration_base = validated_base
        if not is_ancestor(repo, validated_base, integration):
            raise VerificationError(
                "rebase integration does not descend from the validated base"
            )

    expected_tree = expected_merge_tree(repo, integration_base, candidate)
    actual_tree = tree(repo, integration)
    if expected_tree != actual_tree:
        raise VerificationError(
            "recorded integration tree does not equal the expected integration tree"
        )

    return {
        "verified": True,
        "method": method,
        "candidate_head": candidate,
        "validated_base": validated_base,
        "integration_base": integration_base,
        "integration_commit": integration,
        "expected_tree": expected_tree,
        "actual_tree": actual_tree,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--method", choices=("merge", "squash", "rebase"), required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--validated-base", required=True)
    parser.add_argument("--integration", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = verify(
            args.repo.resolve(),
            args.method,
            args.candidate,
            args.validated_base,
            args.integration,
        )
    except VerificationError as error:
        print(json.dumps({"verified": False, "error": str(error)}, sort_keys=True))
        return 1

    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
