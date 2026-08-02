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
from .claim2 import run_claim2
from .claim3 import run_claim3
from .claim4 import run_claim4
from .claim5 import run_claim5


ARTIFACTS = Path(".openresearch/artifacts")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def cpu_info() -> dict[str, object]:
    affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    return {
        "estimated_cores_required": 32,
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

    claim1 = {
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
    write_json(ARTIFACTS / "claim1/raw_results.json", claim1)
    write_json(
        ARTIFACTS / "claim1/independent_checker_output.json",
        {"passed": passed, "failures": failures, "results": results},
    )
    write_json(
        ARTIFACTS / "claim1/negative_control_output.json",
        claim1["negative_control"],
    )

    claim2 = run_claim2()
    write_json(ARTIFACTS / "claim2/raw_results.json", claim2)
    write_json(
        ARTIFACTS / "claim2/independent_checker_output.json",
        {
            "passed": not claim2["failures"],
            "adaptive_quadrature_abs_errors": [
                result["independent_checker_abs_error"] for result in claim2["results"]
            ],
        },
    )
    write_json(
        ARTIFACTS / "claim2/negative_control_output.json", claim2["negative_control"]
    )

    claim3 = run_claim3()
    write_json(ARTIFACTS / "claim3/raw_results.json", claim3)
    write_json(
        ARTIFACTS / "claim3/independent_checker_output.json",
        {
            "proof_chain": claim3["proof_chain"],
            "exponent_checks": claim3["exponent_checks"],
            "calibrated_corroboration": claim3["calibrated_corroboration"],
            "passed": claim3["passed"],
        },
    )
    write_json(
        ARTIFACTS / "claim3/negative_control_output.json", claim3["negative_control"]
    )

    claim4 = run_claim4()
    write_json(ARTIFACTS / "claim4/raw_results.json", claim4)
    write_json(
        ARTIFACTS / "claim4/independent_checker_output.json",
        {
            "proof_certificate": claim4["proof_certificate"],
            "compact_instance": claim4["compact_instance"],
            "passed": claim4["passed"],
        },
    )
    write_json(
        ARTIFACTS / "claim4/negative_control_output.json", claim4["negative_control"]
    )

    claim5 = run_claim5()
    write_json(ARTIFACTS / "claim5/raw_results.json", claim5)
    write_json(
        ARTIFACTS / "claim5/independent_checker_output.json",
        claim5["independent_equation_checker"],
    )
    write_json(
        ARTIFACTS / "claim5/negative_control_output.json", claim5["negative_control"]
    )

    cumulative_runtime = time.perf_counter() - started
    statuses = {
        "claim_1": claim1["status"],
        "claim_2": claim2["status"],
        "claim_3": claim3["status"],
        "claim_4": claim4["status"],
        "claim_5": claim5["status"],
    }
    cumulative_pass = all(
        status == "VERIFIED" for name, status in statuses.items() if name != "claim_5"
    ) and bool(claim5["passed"])
    run_summary = {
        "system": system,
        "statuses": statuses,
        "cumulative_pass": cumulative_pass,
        "runtime_seconds": cumulative_runtime,
    }
    write_json(ARTIFACTS / "run_summary.json", run_summary)

    print("=== SYSTEM ===")
    print(json.dumps(system, indent=2, sort_keys=True))
    print("=== CLAIM 1 RAW RESULTS ===")
    print(json.dumps(claim1, indent=2, sort_keys=True))
    print("=== CLAIM 2 RAW RESULTS ===")
    print(json.dumps(claim2, indent=2, sort_keys=True))
    print("=== CLAIM 3 RAW RESULTS ===")
    print(json.dumps(claim3, indent=2, sort_keys=True))
    print("=== CLAIM 4 RAW RESULTS ===")
    print(json.dumps(claim4, indent=2, sort_keys=True))
    print("=== CLAIM 5 RAW RESULTS ===")
    print(json.dumps(claim5, indent=2, sort_keys=True))
    print("=== EVAL ===")
    print(json.dumps(run_summary, indent=2, sort_keys=True))
    if not cumulative_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
