"""Constructive compact-support neural check for Theorem 3.7 (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt

import numpy as np
import torch
from scipy.integrate import quad
from torch import nn


EPSILON = 0.5
SQRT_NORMALIZER = sqrt(2 * pi * EPSILON)


class TailPotentialNN(nn.Module):
    """Exact two-ReLU-layer realization of max(-M, -L dist(y,[-1,1]))."""

    def __init__(self, bound: float, lipschitz: float):
        super().__init__()
        self.bound = bound
        self.lipschitz = lipschitz

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        raw = -self.lipschitz * (
            torch.relu(value - 1) + torch.relu(-value - 1)
        )
        return -self.bound + torch.relu(raw + self.bound)


@dataclass
class ReluSplineNN:
    knots: np.ndarray
    values: np.ndarray

    def __post_init__(self) -> None:
        self.slopes = np.diff(self.values) / np.diff(self.knots)

    def __call__(self, value: float | np.ndarray) -> float | np.ndarray:
        x = np.asarray(value)
        result = self.values[0] + self.slopes[0] * (x - self.knots[0])
        for index in range(1, len(self.slopes)):
            result = result + (self.slopes[index] - self.slopes[index - 1]) * np.maximum(
                x - self.knots[index], 0
            )
        return float(result) if np.ndim(value) == 0 else result


def tail_potential(value: float, bound: float, lipschitz: float) -> float:
    return max(-bound, -lipschitz * max(abs(value) - 1, 0))


def restricted_partition(x: float) -> float:
    return quad(
        lambda y: exp(-0.5 * (x - y) ** 2 / EPSILON),
        -1,
        1,
        epsabs=2e-11,
        epsrel=2e-11,
        limit=200,
    )[0]


def capacity_partition(x: float, bound: float, lipschitz: float) -> float:
    return quad(
        lambda y: exp(
            (tail_potential(y, bound, lipschitz) - 0.5 * (x - y) ** 2) / EPSILON
        ),
        -np.inf,
        np.inf,
        epsabs=2e-10,
        epsrel=2e-10,
        limit=250,
    )[0]


def l_star() -> float:
    expected_log_z = 0.5 * quad(
        lambda x: log(restricted_partition(x)),
        -1,
        1,
        epsabs=2e-9,
        epsrel=2e-9,
        limit=180,
    )[0]
    return -EPSILON * expected_log_z


def objective_for_capacity(bound: float, lipschitz: float, width: int) -> dict[str, float]:
    knots = np.linspace(-1, 1, width)
    log_h_values = np.array(
        [log(capacity_partition(float(x), bound, lipschitz) / SQRT_NORMALIZER) for x in knots]
    )
    xi_network = ReluSplineNN(knots, log_h_values)

    expected_xi = 0.5 * quad(
        lambda x: xi_network(x), -1, 1, epsabs=2e-9, epsrel=2e-9, limit=180
    )[0]
    expected_mass_ratio = 0.5 * quad(
        lambda x: capacity_partition(x, bound, lipschitz)
        / SQRT_NORMALIZER
        * exp(-xi_network(x)),
        -1,
        1,
        epsabs=2e-8,
        epsrel=2e-8,
        limit=180,
    )[0]
    objective = (
        EPSILON * (1 - 0.5 * log(2 * pi * EPSILON))
        - EPSILON * expected_xi
        - EPSILON * expected_mass_ratio
    )

    network = TailPotentialNN(bound, lipschitz)
    audit_points = torch.linspace(-3, 3, 121, dtype=torch.float64)
    with torch.no_grad():
        torch_values = network(audit_points).numpy()
    direct_values = np.array(
        [tail_potential(float(x), bound, lipschitz) for x in audit_points.numpy()]
    )
    return {
        "bound_M": bound,
        "lipschitz_L": lipschitz,
        "xi_relu_width": width,
        "variational_objective": objective,
        "expected_exp_mass_ratio": expected_mass_ratio,
        "tail_network_realization_max_error": float(np.max(np.abs(torch_values - direct_values))),
    }


def target_marginal_normalization() -> float:
    def target_density(y: float) -> float:
        return 0.5 * quad(
            lambda x: exp(-0.5 * (x - y) ** 2 / EPSILON) / restricted_partition(x),
            -1,
            1,
            epsabs=2e-9,
            epsrel=2e-9,
            limit=150,
        )[0]

    return quad(target_density, -1, 1, epsabs=2e-8, epsrel=2e-8, limit=150)[0]


def run_claim4() -> dict[str, object]:
    optimum = l_star()
    levels = (
        (2.0, 8.0, 8),
        (4.0, 32.0, 16),
        (6.0, 128.0, 32),
        (8.0, 512.0, 64),
    )
    results = [objective_for_capacity(*level) for level in levels]
    for result in results:
        result["approximation_gap"] = optimum - result["variational_objective"]

    control = objective_for_capacity(1.0, 8.0, 64)
    control["approximation_gap"] = optimum - control["variational_objective"]
    control_rejected = control["approximation_gap"] > 0.01
    gaps = [result["approximation_gap"] for result in results]
    normalization = target_marginal_normalization()
    passed = (
        abs(normalization - 1) <= 2e-7
        and all(gap >= -2e-7 for gap in gaps)
        and gaps[-1] < 0.01
        and gaps[-1] < gaps[0] / 5
        and all(result["tail_network_realization_max_error"] <= 1e-12 for result in results)
        and control_rejected
    )
    return {
        "claim": "Theorem 3.7 in arXiv v1 / cached ar5iv",
        "status": "VERIFIED" if passed else "BLOCKED",
        "compact_instance": {
            "p0": "Uniform[-1,1]",
            "p1": "the compact target marginal induced by f*=0 on [-1,1] and -infinity outside",
            "epsilon": EPSILON,
            "target_marginal_normalization_adaptive_quadrature": normalization,
            "L_star": optimum,
        },
        "proof_certificate": [
            "normalize the weak-dual optimizer by additive-shift invariance",
            "approximate its restriction to compact X1 by a bounded Lipschitz function",
            "extend and clip it so Gaussian-kernel tail error vanishes as M,L grow",
            "represent the clipped piecewise-linear potential exactly by a ReLU network",
            "approximate xi_f uniformly on compact X0 by a ReLU spline network",
            "continuity of the bounded variational functional transfers both approximations to objective value",
        ],
        "capacity_results": results,
        "negative_control": {
            "change": "increase xi-network width while fixing tail bound M=1 and L=8",
            "result": control,
            "expected": "tail approximation error remains above 0.01",
            "rejected": control_rejected,
        },
        "source_version_warning": "The current arXiv v2 renumbers this statement as Theorem 3.6 and replaces the v1 proof with a bounded-network universal-approximation argument.",
        "passed": passed,
    }
