"""Generalized-KL certificate for Theorem 3.3."""

from __future__ import annotations

from math import exp, log

import numpy as np
from scipy.integrate import quad

from .claim1 import CASES, GaussianCase, log_partition, normal_pdf, optimal_parameters


def semidual(case: GaussianCase, params: dict[str, float]) -> float:
    ef = params["a"] * (case.std1**2 + case.mean1**2) + params["b"] * case.mean1
    elogz = 0.5 * log(2 * np.pi * case.epsilon / params["q"]) + (
        (case.std0**2 + (case.mean0 + params["b"]) ** 2) / params["q"]
        - (case.std0**2 + case.mean0**2)
    ) / (2 * case.epsilon)
    return ef - case.epsilon * elogz


def conditional_kl_coefficients(
    case: GaussianCase,
    star: dict[str, float],
    candidate: dict[str, float],
) -> tuple[float, float, float, float]:
    variance_star = case.epsilon / star["q"]
    variance_candidate = case.epsilon / candidate["q"]
    slope = 1 / star["q"] - 1 / candidate["q"]
    intercept = star["b"] / star["q"] - candidate["b"] / candidate["q"]
    return variance_star, variance_candidate, slope, intercept


def run_case(case: GaussianCase) -> dict[str, float]:
    star = optimal_parameters(case)
    candidate = dict(star)
    candidate["q"] *= 1.22
    candidate["a"] = (1 - candidate["q"]) / 2
    candidate["b"] = candidate["q"] * case.mean1 - case.mean0 + 0.25

    l_star = semidual(case, star)
    l_f = semidual(case, candidate)
    d0, d1 = 0.35, -0.2
    expected_delta = d0 + d1 * case.mean0
    mass = exp(-d0 - d1 * case.mean0 + 0.5 * d1**2 * case.std0**2)
    penalty = expected_delta + mass - 1
    l_f_xi = l_f - case.epsilon * penalty

    var_star, var_candidate, slope, intercept = conditional_kl_coefficients(
        case, star, candidate
    )
    expected_mean_difference_sq = (
        slope**2 * (case.std0**2 + case.mean0**2)
        + 2 * slope * intercept * case.mean0
        + intercept**2
    )
    normalized_kl = 0.5 * (
        log(var_candidate / var_star)
        + (var_star + expected_mean_difference_sq) / var_candidate
        - 1
    )
    generalized_kl = normalized_kl + expected_delta + mass - 1

    def conditional_kl_at_x(x: float) -> float:
        mean_difference = slope * x + intercept
        return 0.5 * (
            log(var_candidate / var_star)
            + (var_star + mean_difference**2) / var_candidate
            - 1
        )

    normalized_kl_quad = quad(
        lambda x: conditional_kl_at_x(x) * normal_pdf(x, case.mean0, case.std0),
        -np.inf,
        np.inf,
        epsabs=1e-11,
        epsrel=1e-11,
        limit=250,
    )[0]
    mass_quad = quad(
        lambda x: exp(-(d0 + d1 * x)) * normal_pdf(x, case.mean0, case.std0),
        -np.inf,
        np.inf,
        epsabs=1e-11,
        epsrel=1e-11,
        limit=250,
    )[0]
    generalized_kl_quad = normalized_kl_quad + expected_delta + mass_quad - 1
    ordinary_kl_without_mass_correction = normalized_kl + expected_delta

    return {
        "name": case.name,
        "epsilon": case.epsilon,
        "candidate_q": candidate["q"],
        "candidate_b": candidate["b"],
        "delta_intercept": d0,
        "delta_slope": d1,
        "pi_f_xi_total_mass": mass,
        "L_star": l_star,
        "L_f": l_f,
        "L_f_xi": l_f_xi,
        "normalized_KL_pi_star_pi_f": normalized_kl,
        "generalized_KL_pi_star_pi_f_xi": generalized_kl,
        "generalized_KL_adaptive_quadrature": generalized_kl_quad,
        "gap_identity_abs_error": abs(case.epsilon * generalized_kl - (l_star - l_f_xi)),
        "independent_checker_abs_error": abs(generalized_kl - generalized_kl_quad),
        "kl_inequality_margin": generalized_kl - normalized_kl,
        "ordinary_KL_without_mass_correction": ordinary_kl_without_mass_correction,
        "ordinary_KL_false_identity_abs_error": abs(
            case.epsilon * ordinary_kl_without_mass_correction - (l_star - l_f_xi)
        ),
    }


def run_claim2() -> dict[str, object]:
    results = [run_case(case) for case in CASES]
    failures: list[str] = []
    for result in results:
        if result["gap_identity_abs_error"] > 1e-10:
            failures.append(f"{result['name']}: generalized KL identity")
        if result["independent_checker_abs_error"] > 1e-10:
            failures.append(f"{result['name']}: adaptive checker")
        if result["kl_inequality_margin"] < -1e-12:
            failures.append(f"{result['name']}: KL inequality")
        if result["ordinary_KL_false_identity_abs_error"] < 0.05:
            failures.append(f"{result['name']}: negative control was not rejected")
    return {
        "claim": "Theorem 3.3",
        "status": "VERIFIED" if not failures else "BLOCKED",
        "results": results,
        "failures": failures,
        "symbolic_certificate": {
            "radon_nikodym_ratio": "log(d pi*/d pi_f,xi) = log(d pi*/d pi_f) + delta(x0)",
            "mass_correction": "KL_generalized(P||Q)=int log(dP/dQ)dP-P(Omega)+Q(Omega)",
            "objective_gap": "L*-L(f,xi)=epsilon*KL_generalized(pi*||pi_f,xi)",
        },
        "negative_control": {
            "change": "omit -P(Omega)+Q(Omega) from Definition A.1",
            "expected": "identity fails because pi_f,xi is not normalized",
            "rejected": all(r["ordinary_KL_false_identity_abs_error"] >= 0.05 for r in results),
        },
    }
