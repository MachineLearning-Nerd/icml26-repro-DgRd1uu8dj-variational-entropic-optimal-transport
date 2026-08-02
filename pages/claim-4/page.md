# Claim 4 — Theorem 3.7 (arXiv v1) — VERIFIED

**Exact judged claim.** For compact-support EOT, an increasing sequence of universal bounded Lipschitz neural classes makes the best variational approximation gap tend to zero. The quantifier is a capacity limit, not monotonicity for every optimizer or architecture. Source: arXiv v1 Theorem 3.7 / Eq. 19 / Appendix A.6, PDF SHA-256 `ecadaf4fc32e8b88bff8d57910a6bc291bfa36bd9c4ad61df4d505783b3f66a8`.

The analytical certificate normalizes the weak-dual optimizer, approximates it on compact support, controls Gaussian-kernel tails after clipped Lipschitz extension, realizes the piecewise-linear potential exactly with ReLUs, approximates `ξ_f` by a ReLU spline, and transfers both uniform errors through continuity of the bounded functional.

For a non-vacuous continuous witness, `p0=Uniform[-1,1]`, `ε=0.5`, and `p1` is the absolutely continuous compact marginal induced by a known optimizer. Adaptive quadrature gave target mass `1.0`. Actual ReLU capacities `8,16,32,64` reduced the objective gap `0.022732, 0.005575, 0.001404, 0.000352`; direct-vs-network realization error was exactly `0`.

Increasing only the normalizer width while fixing insufficient potential-tail capacity left gap `0.039799`, so the negative control was rejected.

- [Executable ReLU verifier](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/vareot_repro/claim4.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim4/claim_contract.json)
- [Raw capacity data](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/frozen_precision_run.json)

**Version warning.** v2 renumbers this as Theorem 3.6 and changes the proof presentation. The capacity sweep is a scoped witness; the universal result rests on the reconstructed analytical certificate. Confidence: **MEDIUM**.
