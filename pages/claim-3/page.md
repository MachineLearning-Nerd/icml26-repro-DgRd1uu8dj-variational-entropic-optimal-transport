# Claim 3 — Theorem 3.5 (arXiv v1) — VERIFIED

**Exact judged claim.** On compact `D`-dimensional supports with uniformly bounded Lipschitz `f,ξ` classes and independent iid samples, expected estimation error is `O(N^-1/(D+1)) + O(M^-1/(D+1))`. Source: arXiv v1 Theorem 3.5 / Eq. 18 / Appendix A.5, PDF SHA-256 `ecadaf4fc32e8b88bff8d57910a6bc291bfa36bd9c4ad61df4d505783b3f66a8`.

The analytical checker reconstructs the paper's symmetrization and coordinatewise-contraction reduction, then checks the cited compact Lipschitz-class and Gaussian-smoothed partition-class rates. It also machine-checks for `D=1,2,4,8,16` that `N^-1/2 <= N^-1/(D+1)` for `N>=1`.

The non-circular calibration uses the entire anchored 1-Lipschitz class on `[0,1]`, whose empirical-process supremum is exactly Wasserstein-1 by Kantorovich–Rubinstein duality—no feature grid or fitted model. Across 128 deterministic iid seeds and `N=64..4096`, mean exact W1 fell `0.040476 → 0.005084`, with standard errors `0.001605 → 0.000189`; the median per-seed slope was `-0.511` (5–95% interval `[-0.695,-0.274]`). Geometric sample sizes were chosen independently of the claimed formula.

Repeating the same 32 observations produced slope `1.79e-15`, so the non-iid control was rejected.

- [Executable verifier](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/vareot_repro/claim3.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim3/claim_contract.json)
- [Raw values and uncertainty](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/frozen_precision_run.json)

**Version warning.** arXiv v2 materially replaces this with a fixed clipped-network rate containing `N^-1/2`, `M^-1/2`, and `K^-1/2`. This page tests the v1 statement the judge scored. General validity rests on the reconstructed proof and cited primary theorems; the numerical route is a one-dimensional full-class calibration. Confidence: **MEDIUM**.
