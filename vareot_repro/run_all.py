"""Fixed cumulative entrypoint for every experiment node."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import scipy
import torch

from .claim1 import CASES, pointwise_variational_penalty, run_case, verify_results


ARTIFACTS = Path(".openresearch/artifacts/claim1")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def cpu_info() -> dict[str, object]:
    affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    return {
        "estimated_cores_required": 2,
        "selected_backend": "hf",
        "selected_flavor": "cpu-upgrade",
        "os_cpu_count": os.cpu_count(),
        "cpu_affinity_count": affinity,
        "torch_threads": torch.get_num_threads(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
    }


def main() -> None:
    started = time.perf_counter()
    system = cpu_info()
    if system["cuda_available"]:
        raise SystemExit("GPU detected: this campaign is CPU-only")

    results = [run_case(case) for case in CASES]
    passed, failures = verify_results(results)
    penalties = {str(delta): pointwise_variational_penalty(delta) for delta in (-2, -0.5, 0, 0.5, 2)}
    certificate_ok = min(penalties.values()) >= -1e-15 and penalties["0"] == 0

    control = subprocess.run(
        [sys.executable, "-m", "vareot_repro.negative_control"],
        check=False,
        capture_output=True,
        text=True,
    )
    control_ok = control.returncode != 0
    final_pass = passed and certificate_ok and control_ok
    runtime = time.perf_counter() - started

    raw = {
        "claim": "Theorem 3.2",
        "scope": "continuous one-dimensional Gaussian distributions; exact quadratic optimal potential",
        "results": results,
        "pointwise_penalty_delta_plus_exp_minus_delta_minus_one": penalties,
        "symbolic_certificate": {
            "identity": "L(f)-L(f,xi_f+delta)=epsilon*E[delta+exp(-delta)-1]",
            "global_nonnegativity_basis": "exp(-delta) >= 1-delta for every real delta",
            "equality_condition": "delta=0",
            "passed": certificate_ok,
        },
        "verifier_failures": failures,
        "negative_control": {
            "command": f"{sys.executable} -m vareot_repro.negative_control",
            "expected_exit_nonzero": True,
            "actual_exit_code": control.returncode,
            "stdout": control.stdout,
            "stderr": control.stderr,
            "passed": control_ok,
        },
        "system": system,
        "runtime_seconds": runtime,
        "status": "VERIFIED" if final_pass else "BLOCKED",
        "limitation": "The exact symbolic reduction is general, while the numerical non-vacuity check is a continuous Gaussian special case rather than an exhaustive test over all distributions.",
    }
    write_json(ARTIFACTS / "raw_results.json", raw)
    write_json(
        ARTIFACTS / "independent_checker_output.json",
        {"passed": passed, "failures": failures, "results": results},
    )
    write_json(
        ARTIFACTS / "negative_control_output.json",
        raw["negative_control"],
    )

    print("=== SYSTEM ===")
    print(json.dumps(system, indent=2, sort_keys=True))
    print("=== CLAIM 1 RAW RESULTS ===")
    print(json.dumps(raw, indent=2, sort_keys=True))
    print("=== EVAL ===")
    print(
        json.dumps(
            {
                "claim_1": raw["status"],
                "independent_checker": passed,
                "negative_control_rejected": control_ok,
                "runtime_seconds": runtime,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not final_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
