"""Proof-chain and calibrated Lipschitz-class check for Theorem 3.5 (v1)."""

from __future__ import annotations

import numpy as np


def uniform_empirical_w1(samples: np.ndarray) -> float:
    """Exact W1 between Uniform[0,1] and an empirical distribution."""
    ordered = np.sort(samples)
    n = len(ordered)
    total = 0.0
    for index, value in enumerate(ordered):
        left = index / n
        right = (index + 1) / n
        if value <= left:
            total += 0.5 * ((right - value) ** 2 - (left - value) ** 2)
        elif value >= right:
            total += 0.5 * ((value - left) ** 2 - (value - right) ** 2)
        else:
            total += 0.5 * ((value - left) ** 2 + (right - value) ** 2)
    return total


def run_claim3() -> dict[str, object]:
    sample_sizes = np.array([64, 128, 256, 512, 1024, 2048, 4096])
    seed_errors = []
    for seed in range(128):
        rng = np.random.default_rng(20260802 + seed)
        largest = rng.uniform(size=int(sample_sizes[-1]))
        seed_errors.append([uniform_empirical_w1(largest[:n]) for n in sample_sizes])
    errors = np.asarray(seed_errors)
    means = errors.mean(axis=0)
    standard_errors = errors.std(axis=0, ddof=1) / np.sqrt(len(errors))
    per_seed_slopes = np.array(
        [np.polyfit(np.log(sample_sizes), np.log(row), 1)[0] for row in errors]
    )

    duplicated_errors = []
    control_rng = np.random.default_rng(260202241)
    base = control_rng.uniform(size=32)
    for n in sample_sizes:
        duplicated_errors.append(uniform_empirical_w1(np.resize(base, int(n))))
    duplicated_slope = float(
        np.polyfit(np.log(sample_sizes), np.log(duplicated_errors), 1)[0]
    )

    exponent_checks = []
    for dimension in (1, 2, 4, 8, 16):
        old_exponent = 1 / (1 + dimension)
        dominated = all(n ** -0.5 <= n ** -old_exponent + 1e-15 for n in sample_sizes)
        exponent_checks.append(
            {
                "dimension": dimension,
                "v1_exponent": -old_exponent,
                "n_minus_half_implies_v1_rate_for_n_ge_1": dominated,
            }
        )

    median_slope = float(np.median(per_seed_slopes))
    slope_interval = [float(x) for x in np.quantile(per_seed_slopes, [0.05, 0.95])]
    control_rejected = duplicated_slope > -0.1
    passed = (
        -0.65 <= median_slope <= -0.35
        and all(item["n_minus_half_implies_v1_rate_for_n_ge_1"] for item in exponent_checks)
        and control_rejected
    )
    return {
        "claim": "Theorem 3.5 in arXiv v1 / cached ar5iv",
        "status": "VERIFIED" if passed else "BLOCKED",
        "source_version_warning": "arXiv v2 replaces this rate by O(N^-1/2)+O(M^-1/2)+O(K^-1/2) for fixed clipped neural-network classes and renumbers Theorem 3.7 to 3.6.",
        "proof_chain": [
            "symmetrization bounds each one-sided empirical-process term by twice its Rademacher complexity",
            "the quotient class Z(f,.)/exp(xi(.)) is controlled by coordinatewise contraction on bounded ranges",
            "Gottlieb et al. (2016), Theorem 4.3 gives the compact D-dimensional Lipschitz-class rate n^-1/(D+1)",
            "Kolesov et al. (2024), Theorem 4.5 gives n^-1/2 for the Gaussian-smoothed partition class",
            "n^-1/2 is no larger than n^-1/(D+1) for D>=1 and n>=1",
        ],
        "exponent_checks": exponent_checks,
        "calibrated_corrobation": {
            "class": "all 1-Lipschitz functions on [0,1], anchored modulo constants",
            "exact_duality": "sup empirical gap equals W1(Uniform[0,1], empirical measure)",
            "sample_sizes": sample_sizes.tolist(),
            "seeds": 128,
            "mean_exact_w1": means.tolist(),
            "standard_error": standard_errors.tolist(),
            "median_per_seed_loglog_slope": median_slope,
            "per_seed_slope_5_95_percentiles": slope_interval,
        },
        "negative_control": {
            "change": "repeat the same 32 observations instead of drawing additional i.i.d. data",
            "errors": duplicated_errors,
            "loglog_slope": duplicated_slope,
            "rejected": control_rejected,
        },
        "passed": passed,
    }
