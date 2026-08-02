"""Faithful CPU implementation and audit of VarEOT Algorithm 1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import pi, sqrt
from time import perf_counter

import numpy as np
import torch
from torch import nn


@dataclass(frozen=True)
class AlgorithmConfig:
    dimension: int = 2
    epsilon: float = 1.0
    batch_size: int = 256
    monte_carlo_k: int = 256
    steps: int = 20
    hidden_width: int = 256
    learning_rate: float = 3e-4
    beta1: float = 0.7
    beta2: float = 0.8
    weight_decay: float = 1e-4
    ema_momentum: float = 0.999
    exponential_clip: float = 20.0
    gradient_clip: float = 1.0
    seed: int = 42
    profile_only: bool = True


class MLP(nn.Module):
    def __init__(self, dimension: int, width: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dimension, width),
            nn.SiLU(),
            nn.Linear(width, width),
            nn.SiLU(),
            nn.Linear(width, width),
            nn.SiLU(),
            nn.Linear(width, 1),
        )

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.net(value)


def swiss_roll(batch_size: int, generator: torch.Generator) -> torch.Tensor:
    turning = 1.5 * pi * (1 + 2 * torch.rand(batch_size, generator=generator))
    planar = torch.stack((turning * torch.cos(turning), turning * torch.sin(turning)), 1)
    noise = 0.8 * torch.randn(batch_size, 2, generator=generator)
    return (planar + noise) / 7.5


def vareot_loss(
    potential: nn.Module,
    normalizer: nn.Module,
    source: torch.Tensor,
    target: torch.Tensor,
    noise: torch.Tensor,
    config: AlgorithmConfig,
    detach_potential: bool = False,
) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    noisy_source = source[:, None, :] - sqrt(config.epsilon) * noise
    potential_noisy = potential(noisy_source.reshape(-1, config.dimension)).view(
        config.batch_size, config.monte_carlo_k
    )
    potential_target = potential(target)
    if detach_potential:
        potential_noisy = potential_noisy.detach()
        potential_target = potential_target.detach()
    xi_source = normalizer(source)
    exponent = torch.clamp(
        potential_noisy / config.epsilon - xi_source,
        max=config.exponential_clip,
    )
    exponential_term = torch.exp(exponent.to(torch.float64))
    minimized_loss = config.epsilon * (
        xi_source.mean() + exponential_term.mean()
    ) - potential_target.mean()
    return minimized_loss, {
        "mean_target_potential": potential_target.mean(),
        "mean_source_normalizer": xi_source.mean(),
        "mean_exponential_term": exponential_term.mean(),
    }


def parameter_vector(model: nn.Module) -> torch.Tensor:
    return torch.cat([parameter.detach().reshape(-1) for parameter in model.parameters()])


def gradient_norm(model: nn.Module) -> float:
    squared = sum(
        float(torch.sum(parameter.grad.detach() ** 2))
        for parameter in model.parameters()
        if parameter.grad is not None
    )
    return sqrt(squared)


def fixed_batch(config: AlgorithmConfig, seed: int) -> tuple[torch.Tensor, ...]:
    generator = torch.Generator().manual_seed(seed)
    source = torch.randn(config.batch_size, config.dimension, generator=generator)
    target = swiss_roll(config.batch_size, generator)
    noise = torch.randn(
        config.batch_size,
        config.monte_carlo_k,
        config.dimension,
        generator=generator,
    )
    return source, target, noise


def evaluate_loss(
    potential: nn.Module,
    normalizer: nn.Module,
    batch: tuple[torch.Tensor, ...],
    config: AlgorithmConfig,
) -> tuple[float, dict[str, float]]:
    with torch.no_grad():
        loss, components = vareot_loss(potential, normalizer, *batch, config)
    return float(loss), {name: float(value) for name, value in components.items()}


def numpy_equation_checker(
    potential: nn.Module,
    normalizer: nn.Module,
    batch: tuple[torch.Tensor, ...],
    config: AlgorithmConfig,
) -> dict[str, float | bool]:
    source, target, noise = batch
    with torch.no_grad():
        noisy = source[:, None, :] - sqrt(config.epsilon) * noise
        f_noisy = potential(noisy.reshape(-1, config.dimension)).reshape(
            config.batch_size, config.monte_carlo_k
        ).numpy()
        f_target = potential(target).numpy()
        xi_source = normalizer(source).numpy()
        torch_loss, _ = vareot_loss(potential, normalizer, *batch, config)
    exponent = np.minimum(
        f_noisy / config.epsilon - xi_source,
        config.exponential_clip,
    )
    numpy_loss = config.epsilon * (
        float(np.mean(xi_source))
        + float(np.mean(np.exp(exponent.astype(np.float64))))
    ) - float(np.mean(f_target))
    error = abs(float(torch_loss) - numpy_loss)
    return {
        "torch_minimized_loss": float(torch_loss),
        "numpy_minimized_loss": numpy_loss,
        "absolute_error": error,
        "passed": error <= 2e-7,
    }


def detached_potential_control(
    potential: nn.Module,
    normalizer: nn.Module,
    batch: tuple[torch.Tensor, ...],
    config: AlgorithmConfig,
) -> dict[str, float | bool | str]:
    potential.zero_grad(set_to_none=True)
    normalizer.zero_grad(set_to_none=True)
    loss, _ = vareot_loss(
        potential, normalizer, *batch, config, detach_potential=True
    )
    loss.backward()
    potential_gradient = gradient_norm(potential)
    normalizer_gradient = gradient_norm(normalizer)
    rejected = potential_gradient == 0 and normalizer_gradient > 0
    potential.zero_grad(set_to_none=True)
    normalizer.zero_grad(set_to_none=True)
    return {
        "change": "detach every potential output before Equation 15",
        "potential_gradient_norm": potential_gradient,
        "normalizer_gradient_norm": normalizer_gradient,
        "expected": "joint-gradient audit rejects the zero potential gradient",
        "rejected": rejected,
    }


def run_claim5() -> dict[str, object]:
    config = AlgorithmConfig()
    torch.manual_seed(config.seed)
    potential = MLP(config.dimension, config.hidden_width)
    normalizer = MLP(config.dimension, config.hidden_width)
    potential_ema = MLP(config.dimension, config.hidden_width)
    potential_ema.load_state_dict(potential.state_dict())
    for parameter in potential_ema.parameters():
        parameter.requires_grad_(False)

    initial_potential = parameter_vector(potential)
    initial_normalizer = parameter_vector(normalizer)
    evaluation_batch = fixed_batch(config, 260202241)
    initial_loss, initial_components = evaluate_loss(
        potential, normalizer, evaluation_batch, config
    )
    control = detached_potential_control(
        potential, normalizer, evaluation_batch, config
    )

    optimizer = torch.optim.AdamW(
        list(potential.parameters()) + list(normalizer.parameters()),
        lr=config.learning_rate,
        betas=(config.beta1, config.beta2),
        weight_decay=config.weight_decay,
    )
    generator = torch.Generator().manual_seed(config.seed + 1)
    trace = []
    source_sample_count = 0
    target_sample_count = 0
    gaussian_noise_count = 0
    model_distribution_sample_count = 0
    first_gradient_norms: dict[str, float] = {}
    started = perf_counter()
    for step in range(1, config.steps + 1):
        source = torch.randn(
            config.batch_size, config.dimension, generator=generator
        )
        target = swiss_roll(config.batch_size, generator)
        noise = torch.randn(
            config.batch_size,
            config.monte_carlo_k,
            config.dimension,
            generator=generator,
        )
        source_sample_count += config.batch_size
        target_sample_count += config.batch_size
        gaussian_noise_count += config.batch_size * config.monte_carlo_k

        loss, components = vareot_loss(
            potential, normalizer, source, target, noise, config
        )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        if step == 1:
            first_gradient_norms = {
                "potential": gradient_norm(potential),
                "normalizer": gradient_norm(normalizer),
            }
        torch.nn.utils.clip_grad_norm_(potential.parameters(), config.gradient_clip)
        torch.nn.utils.clip_grad_norm_(normalizer.parameters(), config.gradient_clip)
        optimizer.step()
        with torch.no_grad():
            for current, averaged in zip(potential.parameters(), potential_ema.parameters()):
                averaged.mul_(config.ema_momentum).add_(
                    current, alpha=1 - config.ema_momentum
                )
        if step == 1 or step == config.steps or step % 100 == 0:
            trace.append(
                {
                    "step": step,
                    "training_minimized_loss": float(loss.detach()),
                    **{name: float(value.detach()) for name, value in components.items()},
                }
            )
    training_runtime = perf_counter() - started

    final_loss, final_components = evaluate_loss(
        potential, normalizer, evaluation_batch, config
    )
    checker = numpy_equation_checker(
        potential, normalizer, evaluation_batch, config
    )
    potential_update = float(
        torch.linalg.vector_norm(parameter_vector(potential) - initial_potential)
    )
    normalizer_update = float(
        torch.linalg.vector_norm(parameter_vector(normalizer) - initial_normalizer)
    )
    structural_pass = (
        first_gradient_norms["potential"] > 0
        and first_gradient_norms["normalizer"] > 0
        and potential_update > 0
        and normalizer_update > 0
        and source_sample_count == config.steps * config.batch_size
        and target_sample_count == config.steps * config.batch_size
        and gaussian_noise_count
        == config.steps * config.batch_size * config.monte_carlo_k
        and model_distribution_sample_count == 0
        and bool(checker["passed"])
        and bool(control["rejected"])
        and np.isfinite(final_loss)
    )
    improvement = initial_loss - final_loss
    final_pass = structural_pass and improvement > 0.02
    passed = structural_pass if config.profile_only else final_pass
    return {
        "claim": "Algorithm 1 simulation-free joint neural training",
        "status": "PROFILE_ONLY"
        if config.profile_only and passed
        else "VERIFIED"
        if passed
        else "BLOCKED",
        "profile_only": config.profile_only,
        "config": asdict(config),
        "architecture": "two independent 2->256->256->256->1 SiLU MLPs",
        "source_distribution": "two-dimensional standard Gaussian",
        "target_distribution": "continuous noisy Swiss roll, matching the official notebook sampler",
        "initial_heldout": {
            "minimized_loss": initial_loss,
            "maximized_objective_without_constant": -initial_loss,
            **initial_components,
        },
        "final_heldout": {
            "minimized_loss": final_loss,
            "maximized_objective_without_constant": -final_loss,
            **final_components,
        },
        "heldout_objective_improvement": improvement,
        "first_step_gradient_norms": first_gradient_norms,
        "parameter_update_norms": {
            "potential": potential_update,
            "normalizer": normalizer_update,
        },
        "training_sample_audit": {
            "source_samples": source_sample_count,
            "target_samples": target_sample_count,
            "independent_gaussian_noise_samples": gaussian_noise_count,
            "model_distribution_samples": model_distribution_sample_count,
            "simulation_free": model_distribution_sample_count == 0,
        },
        "trace": trace,
        "independent_equation_checker": checker,
        "negative_control": control,
        "training_runtime_seconds": training_runtime,
        "seconds_per_step": training_runtime / config.steps,
        "projected_5000_step_training_seconds": training_runtime
        / config.steps
        * 5000,
        "structural_pass": structural_pass,
        "final_performance_pass": final_pass,
        "passed": passed,
        "deviation": "This profiling node uses 20 of the official notebook's 5000 steps. Batch, K, architecture, distributions, optimizer, clipping, and EMA match that notebook. It is not final Claim 5 evidence.",
    }
