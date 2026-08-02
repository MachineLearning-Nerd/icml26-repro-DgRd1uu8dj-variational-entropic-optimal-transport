"""Evaluator-visible release checks run after the cumulative science suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def run_release_gate(generated: dict[str, object]) -> dict[str, object]:
    failures: list[str] = []
    frozen = json.loads(
        (ROOT / ".openresearch/artifacts/frozen_precision_run.json").read_text()
    )
    require(
        all(status == "VERIFIED" for status in frozen["statuses"].values()),
        "frozen evidence does not verify every claim",
        failures,
    )
    require(
        generated["statuses"] == frozen["statuses"],
        "fresh cumulative statuses differ from frozen evidence",
        failures,
    )

    claim5 = generated["claim5"]
    expected5 = frozen["claim_5"]
    require(
        abs(claim5["heldout_objective_improvement"] - expected5["heldout_objective_improvement"]) < 1e-8,
        "fresh Algorithm 1 objective differs from frozen evidence",
        failures,
    )
    require(
        claim5["training_sample_audit"]["model_distribution_samples"] == 0,
        "Algorithm 1 sampled its model distribution",
        failures,
    )
    require(
        claim5["independent_equation_checker"]["passed"],
        "independent Algorithm 1 equation checker failed",
        failures,
    )
    require(claim5["negative_control"]["rejected"], "Claim 5 control survived", failures)

    required_paths = [
        "README.md",
        "logbook.json",
        "pages/index.md",
        "pages/current/page.md",
        "pages/claim-1/page.md",
        "pages/claim-2/page.md",
        "pages/claim-3/page.md",
        "pages/claim-4/page.md",
        "pages/claim-5/page.md",
        "pages/source-audit/page.md",
        "pages/release-audit/page.md",
        "pages/historical/page.md",
        "reports/variational-eot-reproduction/report.md",
        "reports/variational-eot-reproduction/images/headline.svg",
        "reports/variational-eot-reproduction/images/identities.svg",
        "reports/variational-eot-reproduction/images/finite_sample.svg",
        "reports/variational-eot-reproduction/images/capacity.svg",
        "reports/variational-eot-reproduction/images/training.svg",
        "notebooks/variational_eot.py",
        ".openresearch/artifacts/frozen_precision_run.json",
        ".openresearch/artifacts/claim5/training_trace.csv",
        "publication_allowlist.txt",
        "MANIFEST.sha256",
    ]
    for claim in range(1, 6):
        required_paths.extend(
            [
                f".openresearch/artifacts/claim{claim}/raw_results.json",
                f".openresearch/artifacts/claim{claim}/independent_checker_output.json",
                f".openresearch/artifacts/claim{claim}/negative_control_output.json",
            ]
        )
    for relative in required_paths:
        require((ROOT / relative).is_file(), f"missing evaluator file: {relative}", failures)

    logbook = json.loads((ROOT / "logbook.json").read_text())
    children = logbook["root"]["children"]
    require(children[0]["slug"] == "current", "current verification is not first", failures)
    require(
        children[1]["title"] == "Historical rejected baseline",
        "historical navigation label is not exact",
        failures,
    )
    current = (ROOT / "pages/current/page.md").read_text()
    for claim in range(1, 6):
        require(f"| {claim} |" in current, f"visibility row {claim} missing", failures)
    for heading in ("Code visible", "Data inline", "Raw link", "Checker", "Control", "Exact claim tested", "Reviewer verdict"):
        require(heading in current, f"visibility column missing: {heading}", failures)

    historical = ["overview", "claims", "evidence", "verification-run", "conclusion"]
    for slug in historical:
        require((ROOT / f"pages/{slug}/page.md").is_file(), f"lost historical page {slug}", failures)

    for image in (ROOT / "reports/variational-eot-reproduction/images").glob("*.svg"):
        text = image.read_text()
        require(text.startswith("<svg") and "</svg>" in text, f"invalid SVG: {image.name}", failures)

    notebook = subprocess.run(
        [sys.executable, "-m", "marimo", "check", "notebooks/variational_eot.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    require(notebook.returncode == 0, "marimo check failed", failures)

    allowlist = [
        line.strip()
        for line in (ROOT / "publication_allowlist.txt").read_text().splitlines()
        if line.strip()
    ]
    require(len(allowlist) == len(set(allowlist)), "duplicate upload allowlist path", failures)
    for relative in allowlist:
        require((ROOT / relative).is_file(), f"allowlisted file missing: {relative}", failures)
    forbidden = ("HF_TOKEN=", "HUGGING_FACE_HUB_TOKEN=", "BEGIN PRIVATE KEY", "api_key =")
    for relative in allowlist:
        body = (ROOT / relative).read_text(errors="replace")
        require(not any(marker in body for marker in forbidden), f"secret marker in {relative}", failures)

    return {
        "passed": not failures,
        "failures": failures,
        "marimo_check_exit_code": notebook.returncode,
        "marimo_check_stdout": notebook.stdout,
        "marimo_check_stderr": notebook.stderr,
        "allowlist_file_count": len(allowlist),
        "historical_pages_preserved": historical,
    }
