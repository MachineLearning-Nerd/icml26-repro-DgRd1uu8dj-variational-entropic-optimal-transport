# Claim 2 — Theorem 3.3 — VERIFIED

**Exact claim.** For every admissible `(f,ξ)`, `L* - L(f,ξ) = ε KL(pi* || pi_(f,ξ))`, where Definition A.1 uses generalized KL for finite, possibly non-normalized measures. Assumptions: required absolute continuity, finite generalized KL/objectives, probability marginals, and `ε>0`. Source: Theorem 3.3 / Eq. 14 and Definition A.1 in the [audited source](https://ar5iv.labs.arxiv.org/html/2602.02241#S3.Thmtheorem3).

The checker deliberately uses non-optimal quadratic potentials and nonconstant normalizer shifts on two continuous Gaussian EOT instances. Candidate masses were `0.620518` and `0.819714`, so ordinary probability KL is inapplicable. Direct objective gaps and generalized KL agreed to at most `5.83e-16`; an independent adaptive-integration implementation agreed exactly at displayed precision.

The negative control removes the finite-measure mass correction. It misses the identity by `0.265637` and `0.198315`, and is rejected.

- [Executable and independent checker](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/vareot_repro/claim2.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim2/claim_contract.json)
- [Raw run evidence](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/frozen_precision_run.json)

**Limit.** The analytical Radon–Nikodym derivation is general; numerical corroboration is scoped to two continuous Gaussian instances. Confidence: **HIGH**.
