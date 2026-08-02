# Claim 1 — Theorem 3.2 — VERIFIED

**Exact claim.** For admissible EOT instances, `EOTε(p0,p1) = sup_f L(f) = sup_(f,ξ) L(f,ξ)`; for fixed admissible `f`, `ξ_f` makes the auxiliary bound tight. Assumptions: absolutely continuous Borel probability marginals on `R^D`, `ε>0`, admissible/integrable functions, and finite displayed quantities. Source: Theorem 3.2 / Eq. 13 in the [audited ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2602.02241#S3.Thmtheorem2).

The verifier substitutes `ξ=ξ_f+δ` and independently reconstructs

`L(f)-L(f,ξ) = ε E[δ + exp(-δ) - 1] >= 0`,

using `exp(-δ) >= 1-δ`, with equality only at `δ=0`. Two continuous Gaussian EOT instances then check that the analytic primal, semidual, and variational values agree. The largest discrepancy was `4.44e-16`; independent adaptive quadrature also had maximum error `4.44e-16`.

The negative control multiplies the analytic precision by `1.15`; it violates the target marginal and exited `1` as required.

- [Executable verifier](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/vareot_repro/claim1.py)
- [Independent checker and failing control](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/vareot_repro/negative_control.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim1/claim_contract.json)
- [Raw results](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim1/raw_results.json) · [checker output](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim1/independent_checker_output.json) · [control output](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim1/negative_control_output.json)

**Limit.** The symbolic reduction addresses the general auxiliary identity; the numerical non-vacuity checks are continuous one-dimensional Gaussians, not an exhaustive numerical proof over distributions. Confidence: **HIGH**.
