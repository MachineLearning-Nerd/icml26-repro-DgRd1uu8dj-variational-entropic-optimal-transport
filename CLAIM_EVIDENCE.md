# Claim-to-evidence ledger

This ledger states what each claim means, which code produces its evidence, which artifact records the result, and what the result does not establish. The verdicts are scoped reproductions, not a current external judge score.

## Claim 1 — Theorem 3.2 — VERIFIED

- Contract: the EOT value equals the weak and variational dual values; for a fixed potential, the optimal auxiliary normalizer makes the variational bound tight.
- Producer: `vareot_repro/claim1.py`, orchestrated by `vareot_repro/run_all.py`.
- Evidence: `.openresearch/artifacts/claim1/raw_results.json`, `.openresearch/artifacts/claim1/independent_checker_output.json`, and `.openresearch/artifacts/claim1/negative_control_output.json`.
- Method: symbolic reconstruction plus continuous one-dimensional Gaussian EOT instances and independent adaptive quadrature.
- Result: maximum continuous agreement error `4.440892098500626e-16`; maximum adaptive-quadrature error `4.440892098500626e-16`; deliberately wrong potential exits with code `1`.
- Boundary: the numerical instance is finite-dimensional; the general theorem conclusion comes from the reconstructed identity and source contract, not from one numerical case.

## Claim 2 — Theorem 3.3 — VERIFIED

- Contract: the objective gap equals epsilon times generalized KL between the optimal plan and the candidate finite measure, including the finite-measure mass correction.
- Producer: `vareot_repro/claim2.py`, orchestrated by `vareot_repro/run_all.py`.
- Evidence: `.openresearch/artifacts/claim2/raw_results.json`, `.openresearch/artifacts/claim2/independent_checker_output.json`, and `.openresearch/artifacts/claim2/negative_control_output.json`.
- Method: Radon–Nikodym identity, two continuous Gaussian instances, non-optimal potentials, nonconstant normalizer shifts, and an independent checker.
- Result: maximum identity error `5.828670879282072e-16`; independent checker error `0.0`; ordinary-KL control errors `0.26563711076027896` and `0.19831479832594923`.
- Boundary: the generalized-KL mass correction is part of the tested contract; ordinary normalized KL is intentionally not substituted for it.

## Claim 3 — Theorem 3.5 in arXiv v1 — VERIFIED, v1 contract

- Contract: on compact supports with uniformly bounded Lipschitz classes and independent iid samples, the expected estimation error has the v1 `N`/`M` rate.
- Producer: `vareot_repro/claim3.py`, orchestrated by `vareot_repro/run_all.py`.
- Evidence: `.openresearch/artifacts/claim3/raw_results.json`, `.openresearch/artifacts/claim3/independent_checker_output.json`, and `.openresearch/artifacts/claim3/negative_control_output.json`.
- Method: analytical proof-chain reconstruction plus the complete anchored one-dimensional 1-Lipschitz class, whose empirical supremum is evaluated by exact Wasserstein-1 duality over 128 seeds.
- Result: median per-seed log-log slope `-0.5111585503734187`; repeated-data control slope `1.7893076816262386e-15`.
- Boundary: this verdict is explicitly for the arXiv v1 judged contract. arXiv v2 replaces the statement with a clipped-network rate containing `N`, `M`, and `K` terms.

## Claim 4 — Theorem 3.7 in arXiv v1 — VERIFIED, v1 contract

- Contract: for compact-support EOT, an increasing sequence of universal bounded-Lipschitz neural classes has approximation gap tending to zero.
- Producer: `vareot_repro/claim4.py`, orchestrated by `vareot_repro/run_all.py`.
- Evidence: `.openresearch/artifacts/claim4/raw_results.json`, `.openresearch/artifacts/claim4/independent_checker_output.json`, and `.openresearch/artifacts/claim4/negative_control_output.json`.
- Method: continuous compact witness, explicit capacity-growing ReLU potential/normalizer realizations, independent integration, and a fixed-tail control.
- Result: gaps decrease from `0.022731969838272567` to `0.0003522071774274965` at capacities 8, 16, 32, and 64; fixed-tail control gap `0.0397988656519601` is rejected.
- Boundary: this verdict is explicitly for the arXiv v1 contract, where the result is Theorem 3.7. The current v2 paper renumbers the approximation result as Theorem 3.6 and changes the surrounding statement.

## Claim 5 — Algorithm 1 — VERIFIED

- Contract: every training step uses source samples, target samples, and independent Gaussian noise, jointly updating the potential and normalizer without sampling the current model distribution during training.
- Producer: `vareot_repro/claim5.py`, orchestrated by `vareot_repro/run_all.py`.
- Evidence: `.openresearch/artifacts/claim5/raw_results.json`, `.openresearch/artifacts/claim5/independent_checker_output.json`, `.openresearch/artifacts/claim5/negative_control_output.json`, and `.openresearch/artifacts/claim5/training_trace.csv`.
- Method: the authors' executable-scale Swiss-roll configuration with 5,000 steps, batch size 256, Monte Carlo `K=256`, two width-256 SiLU MLPs, independent NumPy/Torch aggregation, mixed-precision certificate, and a detached-potential control.
- Result: held-out objective improves from `-0.9965578028615594` to `0.21795134304479635`; `1,280,000` source samples, `1,280,000` target samples, `327,680,000` Gaussian proposals, and `0` model-distribution samples; both networks update and the detached-potential control is rejected.
- Boundary: this validates simulation-free training, not simulation-free inference. The paper's inference procedure may still use Langevin sampling. The notebook schedule is 5,000 steps at `3e-4`, while Appendix B.1 records 10,000 steps at `1e-4`; both are preserved in the source audit.

## Aggregate verdict

All five stored scientific contracts are `VERIFIED`, with Claims 3 and 4 explicitly scoped to the arXiv v1 judged statements. This repository does not claim that a finite check proves every universal quantifier by itself, and it does not claim a new live ICML score.
