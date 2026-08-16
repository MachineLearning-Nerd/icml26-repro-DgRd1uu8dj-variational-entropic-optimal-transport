#!/usr/bin/env python3
"""Fail-closed verification for the published Variational EOT audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = "MachineLearning-Nerd/icml26-variational-entropic-optimal-transport"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_COMMIT_COUNT = 18
EXPECTED_STATUSES = {"C1": "VERIFIED", "C2": "VERIFIED", "C3": "VERIFIED", "C4": "VERIFIED", "C5": "VERIFIED"}


def command(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures: list[str] = []

    origin = command("git", "config", "--get", "remote.origin.url").strip()
    if EXPECTED_REPOSITORY not in origin:
        failures.append(f"unexpected origin: {origin}")

    local_branches = set(command("git", "for-each-ref", "--format=%(refname)", "refs/heads").splitlines())
    if local_branches != {"refs/heads/main"}:
        failures.append(f"local branches are {sorted(local_branches)}")

    remote_branches = set(command("git", "for-each-ref", "--format=%(refname)", "refs/remotes/origin").splitlines())
    allowed_remote = {"refs/remotes/origin/HEAD", "refs/remotes/origin/main"}
    if remote_branches - allowed_remote:
        failures.append(f"unexpected remote branches: {sorted(remote_branches)}")

    backup_refs = command("git", "for-each-ref", "--format=%(refname)", "refs/original").splitlines()
    if backup_refs:
        failures.append(f"backup refs remain: {backup_refs}")

    commits = command("git", "rev-list", "main").splitlines()
    if len(commits) != EXPECTED_COMMIT_COUNT:
        failures.append(f"expected {EXPECTED_COMMIT_COUNT} commits, found {len(commits)}")
    if command("git", "rev-parse", "main") != command("git", "rev-parse", "origin/main"):
        failures.append("main and origin/main differ")

    for commit in commits:
        identity = command("git", "show", "-s", "--format=%an%n%ae%n%cn%n%ce", commit).splitlines()
        if identity != [CANONICAL_NAME, CANONICAL_EMAIL, CANONICAL_NAME, CANONICAL_EMAIL]:
            failures.append(f"non-canonical identity at {commit[:12]}")
            break

    if "co-authored-by:" in command("git", "log", "main", "--format=%B").lower():
        failures.append("co-author trailer found")

    manifest = json.loads((ROOT / "EVIDENCE_MANIFEST.json").read_text())
    for relative in manifest["required_audit_files"]:
        if not (ROOT / relative).is_file():
            failures.append(f"missing audit file: {relative}")

    claims = json.loads((ROOT / "claims.json").read_text())
    statuses = {claim["id"]: claim["status"] for claim in claims["claims"]}
    if statuses != EXPECTED_STATUSES:
        failures.append(f"unexpected claim statuses: {statuses}")
    if len(claims["claims"]) != 5:
        failures.append("claim ledger does not contain five claims")

    frozen = json.loads((ROOT / ".openresearch/artifacts/frozen_precision_run.json").read_text())
    expected_frozen = {f"claim_{index}": "VERIFIED" for index in range(1, 6)}
    if frozen["statuses"] != expected_frozen:
        failures.append(f"frozen evidence statuses are {frozen['statuses']}")
    if frozen["claim_5"]["model_distribution_samples"] != 0:
        failures.append("frozen Claim 5 evidence reports model-distribution samples")

    for item in manifest["content_addressed_artifacts"]:
        path = ROOT / item["path"]
        if not path.is_file():
            failures.append(f"missing evidence artifact: {item['path']}")
        elif sha256(path) != item["sha256"]:
            failures.append(f"evidence hash mismatch: {item['path']}")

    for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"publication manifest path missing: {relative}")
        elif sha256(path) != expected:
            failures.append(f"publication manifest hash mismatch: {relative}")

    branch_rows = [line for line in (ROOT / "BRANCH_AUDIT.md").read_text().splitlines() if line.startswith("| `orx/")]
    if len(branch_rows) != 7:
        failures.append(f"branch audit has {len(branch_rows)} retired orx rows, expected 7")
    if "| `publication/evaluator-visible-release` |" not in (ROOT / "BRANCH_AUDIT.md").read_text():
        failures.append("publication branch row missing")

    readme = (ROOT / "README.md").read_text()
    for marker in ["CLAIM_EVIDENCE.md", "SOURCE_AUDIT.md", "BRANCH_AUDIT.md", "CITATION.cff", "AUTHOR_THANK_YOU.md", "verify_final.py"]:
        if marker not in readme:
            failures.append(f"README missing dossier marker: {marker}")

    state = json.loads((ROOT / "AUTONOMOUS_STATE.json").read_text())
    if state.get("phase") != "published_and_verified":
        failures.append(f"unexpected autonomous phase: {state.get('phase')}")
    if state.get("canonical_identity", {}).get("email") != CANONICAL_EMAIL:
        failures.append("autonomous state does not record canonical email")

    result = {
        "passed": not failures,
        "failures": failures,
        "repository": EXPECTED_REPOSITORY,
        "commit_count": len(commits),
        "claim_statuses": statuses,
        "retired_experiment_branches": len(branch_rows),
        "evidence_artifacts": len(manifest["content_addressed_artifacts"]),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
