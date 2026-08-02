---
title: "Repro - Variational Entropic Optimal Transport"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-DgRd1uu8dj
---

# Variational Entropic Optimal Transport — claim-by-claim reproduction

![Five-claim evidence summary](reports/variational-eot-reproduction/images/headline.svg)

This is the current reproduction of [arXiv:2602.02241](https://arxiv.org/abs/2602.02241). It replaces the judged grid proxy with continuous distributions, exact theorem certificates, actual ReLU function classes, and a full 5,000-step neural implementation of Algorithm 1. The cumulative verifier reports **VERIFIED for all five claim contracts**. This is a reproduction verdict, not a new live-judge score; the last live score remains **5/10**.

The strongest experimental result is Algorithm 1 on the authors' continuous Gaussian-to-Swiss-roll task: the fixed held-out variational objective rose from `-0.996558` to `0.217951` over 5,000 joint updates, while consuming `327,680,000` independent Gaussian proposals and exactly `0` samples from the learned model. The run used Hugging Face `cpu-upgrade` only: 32 estimated cores, 64 allocated CPU-affinity cores, 32 Torch threads, no CUDA, and 2h16m wall time.

The paper's Appendix B.1 says 10,000 steps at `1e-4`, while the authors' executable Swiss-roll notebook uses 5,000 at `3e-4`; this reproduction follows the executable notebook and reports the discrepancy. The historical judge claim also follows arXiv v1 for Theorems 3.5/3.7; v2 changes the rate and numbering.

[Current evaluator entrypoint](#/current) · [Illustrated report](reports/variational-eot-reproduction/report.md) · [Tutorial notebook](notebooks/variational_eot.py) · [Open in molab](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/blob/main/notebooks/variational_eot.py)

## Headline results

| Claim | Paper statement | Observed evidence | Assessment |
| --- | --- | --- | --- |
| 1 / Thm. 3.2 | exact variational dual | general pointwise certificate; continuous Gaussian primal/dual error `4.44e-16` | VERIFIED |
| 2 / Thm. 3.3 | gap = scaled generalized KL | two non-normalized continuous cases; max error `5.83e-16` | VERIFIED |
| 3 / Thm. 3.5 v1 | bounded-Lipschitz rate | exact full 1-Lipschitz class, 128 seeds; slope `-0.511` | VERIFIED, analytical certificate plus scoped calibration |
| 4 / Thm. 3.7 v1 | neural approximation gap vanishes | actual ReLU sequence; gap `0.02273 → 0.000352` | VERIFIED, analytical certificate plus continuous witness |
| 5 / Algorithm 1 | simulation-free joint neural training | full official 5,000-step task; objective gain `1.21451`; model samples `0` | VERIFIED |

## Experiment log

All formal nodes inherited this exact command: `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | Baseline source only | — |
| [`orx/baseline-exact-claim-contract`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/baseline-exact-claim-contract) | Claim 1 continuous/symbolic baseline | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | VERIFIED Claim 1 | HF `cpu-upgrade`, 26s wall |
| [`orx/exact-theorem-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/exact-theorem-certificates) | Claims 2–4 exact contracts | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | VERIFIED Claims 1–4 | HF `cpu-upgrade`, 1m19s wall |
| [`orx/algorithm-1-cpu-profile`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/algorithm-1-cpu-profile) | Exact tensor-scale CPU profile | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | PROFILE_ONLY; justified full run | HF `cpu-upgrade`, 1m51s successful wall |
| [`orx/full-official-algorithm-1`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/full-official-algorithm-1) | First 5,000-step run | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | Training completed; checker tolerance was invalid, so BLOCKED | HF `cpu-upgrade`, 1h42m wall |
| [`orx/precision-certified-algorithm-1`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/precision-certified-algorithm-1) | A-priori mixed-precision certificate | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | VERIFIED Claims 1–5 | HF `cpu-upgrade`, 2h16m wall |
| [`orx/evaluator-visible-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/evaluator-visible-release-candidate) | Cumulative release and visibility gate | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | Science passed; packaging gate rejected unavailable pinned-marimo command and a scanner self-match | HF `cpu-upgrade`, 14,066.31s scientific runtime |
| [`orx/pinned-marimo-release-validation`](https://github.com/MachineLearning-Nerd/icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport/tree/orx/pinned-marimo-release-validation) | Pinned-marimo execution fallback and non-self-matching secret scan | `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` | VERIFIED Claims 1–5; release gate passed before outer job timeout | HF `cpu-upgrade`, 5h57m scientific runtime / 5h58m wall |

## Reproduce

The environment is Python 3.12 with exact dependencies in `uv.lock`. The only accepted command is:

```bash
uv sync --frozen && .venv/bin/python -m vareot_repro.run_all
```

Formal results were generated only on Hugging Face `cpu-upgrade`, never locally and never on GPU. For an interactive explanation with embedded evidence, run `uv run marimo edit notebooks/variational_eot.py` or `uv run marimo run notebooks/variational_eot.py`; the notebook does not rerun the expensive training.
