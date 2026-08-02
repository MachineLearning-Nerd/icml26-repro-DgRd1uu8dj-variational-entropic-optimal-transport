"""Continuous-Gaussian certificate for Theorem 3.2."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, log, pi, sqrt

import numpy as np
from scipy.integrate import quad


@dataclass(frozen=True)
class GaussianCase:
    name: str
    mean0: float
    std0: float
    mean1: float
    std1: float
    epsilon: float


CASES = (
    GaussianCase("shift_and_scale", -0.7, 0.8, 1.2, 1.35, 0.7),
    GaussianCase("reverse_scale", 0.5, 1.6, -0.4, 0.65, 1.1),
)


def normal_pdf(x: float, mean: float, std: float) -> float:
    return exp(-0.5 * ((x - mean) / std) ** 2) / (std * sqrt(2 * pi))


def optimal_parameters(case: GaussianCase, q_scale: float = 1.0) -> dict[str, float]:
    s0_sq = case.std0**2
    s1_sq = case.std1**2
    q = (
        case.epsilon + sqrt(case.epsilon**2 + 4 * s0_sq * s1_sq)
    ) / (2 * s1_sq)
    q *= q_scale
    return {"q": q, "a": (1 - q) / 2, "b": q * case.mean1 - case.mean0}


def f_value(y: float, params: dict[str, float]) -> float:
    return params["a"] * y * y + params["b"] * y


def log_partition(x: float, case: GaussianCase, params: dict[str, float]) -> float:
    q = params["q"]
    b = params["b"]
    return 0.5 * log(2 * pi * case.epsilon / q) + (
        (x + b) ** 2 / q - x * x
    ) / (2 * case.epsilon)


def xi_value(x: float, case: GaussianCase, params: dict[str, float]) -> float:
    return log_partition(x, case, params) - 0.5 * log(2 * pi * case.epsilon)


def analytic_values(case: GaussianCase, q_scale: float = 1.0) -> dict[str, float]:
    params = optimal_parameters(case, q_scale)
    q = params["q"]
    b = params["b"]
    ef_target = params["a"] * (case.std1**2 + case.mean1**2) + b * case.mean1
    elogz_source = 0.5 * log(2 * pi * case.epsilon / q) + (
        (case.std0**2 + (case.mean0 + b) ** 2) / q
        - (case.std0**2 + case.mean0**2)
    ) / (2 * case.epsilon)
    semidual = ef_target - case.epsilon * elogz_source

    conditional_variance = case.epsilon / q
    recovered_mean = (case.mean0 + b) / q
    recovered_variance = case.std0**2 / q**2 + conditional_variance
    difference_mean = case.mean0 - recovered_mean
    difference_variance = (1 - 1 / q) ** 2 * case.std0**2 + conditional_variance
    primal = 0.5 * (difference_variance + difference_mean**2) - 0.5 * case.epsilon * log(
        2 * pi * np.e * conditional_variance
    )

    exi_source = elogz_source - 0.5 * log(2 * pi * case.epsilon)
    variational = (
        case.epsilon * (1 - 0.5 * log(2 * pi * case.epsilon))
        + ef_target
        - case.epsilon * exi_source
        - case.epsilon
    )
    return {
        **asdict(case),
        **params,
        "recovered_target_mean": recovered_mean,
        "recovered_target_variance": recovered_variance,
        "target_variance": case.std1**2,
        "primal_eot": primal,
        "semidual": semidual,
        "variational": variational,
        "primal_semidual_abs_error": abs(primal - semidual),
        "semidual_variational_abs_error": abs(semidual - variational),
        "target_mean_abs_error": abs(recovered_mean - case.mean1),
        "target_variance_abs_error": abs(recovered_variance - case.std1**2),
    }


def independent_checker(case: GaussianCase, params: dict[str, float]) -> dict[str, float]:
    ef_numeric = quad(
        lambda y: f_value(y, params) * normal_pdf(y, case.mean1, case.std1),
        -np.inf,
        np.inf,
        epsabs=1e-11,
        epsrel=1e-11,
        limit=250,
    )[0]
    elogz_numeric = quad(
        lambda x: log_partition(x, case, params) * normal_pdf(x, case.mean0, case.std0),
        -np.inf,
        np.inf,
        epsabs=1e-11,
        epsrel=1e-11,
        limit=250,
    )[0]
    semidual_numeric = ef_numeric - case.epsilon * elogz_numeric

    anchor_errors = []
    for x in (case.mean0 - case.std0, case.mean0, case.mean0 + case.std0):
        numerical_z = quad(
            lambda y: exp(
                (f_value(y, params) - 0.5 * (x - y) ** 2) / case.epsilon
            ),
            -np.inf,
            np.inf,
            epsabs=1e-11,
            epsrel=1e-11,
            limit=250,
        )[0]
        anchor_errors.append(abs(log(numerical_z) - log_partition(x, case, params)))
    return {
        "semidual_adaptive_quadrature": semidual_numeric,
        "max_log_partition_adaptive_quadrature_error": max(anchor_errors),
    }


def run_case(case: GaussianCase, q_scale: float = 1.0) -> dict[str, float]:
    result = analytic_values(case, q_scale)
    result.update(independent_checker(case, optimal_parameters(case, q_scale)))
    result["analytic_numeric_semidual_abs_error"] = abs(
        result["semidual"] - result["semidual_adaptive_quadrature"]
    )
    return result


def verify_results(results: list[dict[str, float]]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    for result in results:
        name = result["name"]
        checks = {
            "primal=semidual": result["primal_semidual_abs_error"] <= 1e-10,
            "semidual=variational": result["semidual_variational_abs_error"] <= 1e-12,
            "target mean": result["target_mean_abs_error"] <= 1e-12,
            "target variance": result["target_variance_abs_error"] <= 1e-12,
            "independent semidual": result["analytic_numeric_semidual_abs_error"] <= 1e-9,
            "independent partition": result[
                "max_log_partition_adaptive_quadrature_error"
            ]
            <= 1e-9,
        }
        failures.extend(f"{name}: {label}" for label, passed in checks.items() if not passed)
    return not failures, failures


def pointwise_variational_penalty(delta: float) -> float:
    """L(f)-L(f, xi_f+delta), divided by epsilon."""
    return delta + exp(-delta) - 1
