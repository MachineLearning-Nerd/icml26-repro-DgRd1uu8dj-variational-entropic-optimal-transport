# ICML 2026 — Variational Entropic Optimal Transport

Independent, claim-by-claim reproduction of [Variational Entropic Optimal Transport](https://arxiv.org/abs/2602.02241), also called VarEOT.

> Status: all five claim contracts are verified in the current evidence surface. Claims 3 and 4 are explicitly the arXiv v1 contracts used by the historical judge; arXiv v2 changes their statement or numbering.

This repository replaces the earlier grid-discretized smoke test with continuous measures, exact theorem certificates, a complete one-dimensional Lipschitz-class calibration, explicit ReLU capacity witnesses, and the authors' executable-scale Algorithm 1 training loop. The final scientific evidence reports 5/5 verified claims. This is a reproduction verdict, not a new live-judge score; the last recorded live score remains 5/10.

## Paper

| Item | Record |
| --- | --- |
| Title | Variational Entropic Optimal Transport |
| Authors | Roman Dyachenko, Nikita Gushchin, Kirill Sokolov, Petr Mokrov, Evgeny Burnaev, and Alexander Korotin |
| Paper | [arXiv:2602.02241](https://arxiv.org/abs/2602.02241) |
| Paper publication record | [Author publication list](https://akorotin.netlify.app/publication/) |
| OpenReview record | [DgRd1uu8dj](https://openreview.net/forum?id=DgRd1uu8dj) |
| Current paper source | arXiv v2, PDF SHA-256 257689c36d4d589942660667e880211ab18c6de37d9c643adacd571beaf1949b |
| v1 source used for judged Claims 3 and 4 | PDF SHA-256 ecadaf4fc32e8b88bff8d57910a6bc291bfa36bd9c4ad61df4d505783b3f66a8 |
| Audited HTML source | ar5iv HTML, retrieved 2026-08-02, SHA-256 50f2161eea8428c71e455b7412cd020157a3450f7c60dd6271a8bfe6c6f08261 |
| Current repository | [MachineLearning-Nerd/icml26-variational-entropic-optimal-transport](https://github.com/MachineLearning-Nerd/icml26-variational-entropic-optimal-transport) |
| Former repository name | icml26-repro-DgRd1uu8dj-variational-entropic-optimal-transport |
| Canonical branch | main |

## Standardized audit dossier

The paper-first audit is split into small, reviewable records:

| Record | Purpose |
| --- | --- |
| [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) | Claim contracts, producers, controls, evidence paths, verdicts, and scope boundaries |
| [SOURCE_AUDIT.md](SOURCE_AUDIT.md) | Paper versions, source hashes, OpenReview record, and official implementation provenance |
| [BRANCH_AUDIT.md](BRANCH_AUDIT.md) | Final branch policy and the purpose/outcome of every retired branch |
| [ENVIRONMENT.md](ENVIRONMENT.md) | Fixed command, pinned environment, run provenance, and compute boundary |
| [REPORT.md](REPORT.md) | Scientific interpretation, limitations, and publication boundary |
| [CITATION.cff](CITATION.cff) | Machine-readable paper citation |
| [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) | Thank-you note to the paper authors |
| [claims.json](claims.json) | Machine-readable claim ledger |
| [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) | Hash-pinned evidence and required audit records |
| [verify_final.py](verify_final.py) | Fail-closed final-state verifier; it does not rerun the expensive training job |

The reproduction uses the paper's public theorem statements and the executable Swiss-roll notebook configuration recorded in the source audit. This repository is an independent implementation and verification record, not an official author code release.

## What the paper is doing

Entropic optimal transport with quadratic cost has a weak-dual objective containing an intractable log-partition term. VarEOT introduces an auxiliary positive normalizer, represented by a second learned function, and uses an exact variational reformulation of that term. The resulting objective is differentiable and can be optimized with stochastic gradients without sampling from the current transport plan during training.

The paper's theory covers four related questions: whether the variational dual is exact, whether the objective gap is a generalized KL divergence, how empirical error scales for bounded Lipschitz classes, and whether neural approximation error vanishes with capacity. Algorithm 1 then jointly trains the potential and normalizer from source samples, target samples, and independent Gaussian noise.

## Claim ledger

| Claim | Paper statement | Production path in this repository | Evidence and verdict |
| --- | --- | --- | --- |
| 1 / Theorem 3.2 | The EOT value equals the supremum of the weak dual and the variational dual; for fixed potential, the optimal auxiliary normalizer makes the bound tight. | Symbolically substitute the normalizer perturbation; evaluate the primal, semidual, and variational objectives on continuous Gaussian instances; independently integrate the quantities; reject a wrong precision control. | Maximum continuous agreement error 4.44e-16; adaptive quadrature error 4.44e-16; control exits 1. **VERIFIED, high confidence.** |
| 2 / Theorem 3.3 | The objective gap equals epsilon times generalized KL between the optimal plan and the candidate finite measure, including the finite-measure mass correction. | Derive the Radon–Nikodym identity; evaluate non-optimal potentials and nonconstant normalizer shifts on two continuous Gaussian instances; reject ordinary KL without mass correction. | Maximum identity error 5.83e-16; ordinary-KL control errors 0.265637 and 0.198315. **VERIFIED, high confidence.** |
| 3 / Theorem 3.5, arXiv v1 | For bounded Lipschitz classes on compact supports, expected estimation error has the stated N and M rate. | Reconstruct the proof chain; calibrate the complete anchored one-dimensional 1-Lipschitz class via exact Wasserstein-1 duality over 128 iid seeds; reject repeated observations. | Median per-seed log-log slope -0.511; repeated-data slope 1.79e-15. **VERIFIED for the v1 contract, medium confidence.** |
| 4 / Theorem 3.7, arXiv v1 | Over increasing universal bounded-Lipschitz neural classes, the approximation error tends to zero on compact-support EOT problems. | Reconstruct the universal-approximation argument; realize capacity-growing potentials with exact ReLU pieces and normalizers with ReLU splines; independently integrate a continuous compact witness; reject widening only the normalizer. | Gaps 0.022732, 0.005575, 0.001404, 0.000352 at capacities 8, 16, 32, 64; fixed-tail control remains 0.039799. **VERIFIED for the v1 contract, medium confidence.** |
| 5 / Algorithm 1 | Each training step uses source samples, target samples, and independent Gaussian noise, jointly updating the potential and normalizer without current-plan simulation. | Run the official executable Swiss-roll configuration for 5,000 steps; audit samples, gradients, updates, independent float64 aggregation, mixed-precision error, and a detached-potential control. | Held-out objective improves -0.996558 to 0.217951; 327,680,000 Gaussian proposals; 0 model-distribution samples; control rejects zero potential gradient. **VERIFIED, high confidence.** |

The v1/v2 distinction is part of the claim contract. The current v2 paper changes the finite-sample statement to a clipped-network rate containing N, M, and K terms, and renumbers the approximation result as Theorem 3.6. The v1 verdicts are not silently presented as a separate proof of the v2 formulations.

## How each claim is produced

1. Pin the ar5iv HTML and both relevant arXiv PDF versions with retrieval times and SHA-256 values.
2. Write an explicit contract for each claim: statement, assumptions, quantifiers, source anchors, machine checks, negative control, and failure policy.
3. For Theorems 3.2 and 3.3, use symbolic identities plus independent adaptive quadrature on continuous Gaussian instances.
4. For the v1 statistical claim, use the entire anchored 1-Lipschitz class in one dimension, whose empirical-process supremum is exact Wasserstein-1 rather than a selected feature proxy.
5. For the v1 approximation claim, construct an absolutely continuous compact EOT instance with a known optimizer and evaluate explicit capacity-growing ReLU functions.
6. For Algorithm 1, use the executable notebook schedule, preserve the paper's tensor scale, count every sample source, and audit both network gradients.
7. Run a deliberate negative control for every claim. A claim passes only when the positive evidence passes and its control is rejected.
8. Store raw results, independent-checker output, controls, source audits, and limitations beside the executable code. The cumulative verifier exits nonzero if any contract fails.

The fixed reproduction command is:

    uv sync --frozen && .venv/bin/python -m vareot_repro.run_all

The pinned environment is Python 3.12 with NumPy 2.3.2, SciPy 1.16.1, Torch 2.8.0 CPU, and marimo 0.15.2 resolved by uv.lock. The canonical scientific run used Hugging Face cpu-upgrade, estimated 32 cores, observed 64 CPU-affinity cores, 32 Torch threads, no CUDA, 5,750.05 seconds of scientific runtime, and 2h16m wall time. No local or GPU research run was used.

The earlier release-candidate record marked packaging BLOCKED because marimo 0.15.2 has no check subcommand and a secret scanner matched its own marker literal. The subsequent pinned-marimo release validation used the available export command and a non-self-matching scan; the outer provider job timed out after the final certificate was printed. That infrastructure event is preserved as provenance and is not relabeled as a scientific failure.

## Repository map

| Path | Purpose |
| --- | --- |
| vareot_repro/ | Fixed cumulative verifier and five claim implementations |
| .openresearch/artifacts/claim1/ through claim5/ | Contracts, methods, source audits, raw results, independent checkers, controls, and limitations |
| .openresearch/artifacts/frozen_precision_run.json | Canonical 5/5 scientific evidence and compute record |
| .openresearch/artifacts/claim5/training_trace.csv | Full Algorithm 1 training trace |
| pages/current/page.md | Canonical evaluator entrypoint |
| pages/claim-1/ through claim-5/ | Claim-specific explanations and raw evidence links |
| pages/source-audit/page.md | Version and source boundary record |
| pages/release-audit/page.md | Evaluator-blind visibility and publication checks |
| reports/variational-eot-reproduction/report.md | Illustrated scientific report |
| notebooks/variational_eot.py | Tutorial notebook; it does not rerun expensive training |
| historical/judged-7b762ad/ | Byte-preserved earlier judged artifact |
| branch-audit.md | Former branch names, tips, purposes, and cleanup decisions |
| STATUS.md | Current paper, claim, source, and publication status |
| AUTONOMOUS_STATE.json | Machine-readable continuation state |

Start with [Current verification](pages/current/page.md), then read [Claim 1](pages/claim-1/page.md), [Claim 2](pages/claim-2/page.md), [Claim 3](pages/claim-3/page.md), [Claim 4](pages/claim-4/page.md), and [Claim 5](pages/claim-5/page.md). The [release audit](pages/release-audit/page.md) explains how every claim is visible from the canonical entrypoint.

## Branch policy

The normalized public repository uses one stable branch: main. The former orx/* and publication/* names were experiment or release labels, not public interfaces. Every former branch tip was an ancestor of the pre-normalization main tip, so retiring those pointers preserves the complete history through main. Their purposes and outcomes are recorded in [branch-audit.md](branch-audit.md).

The normalized history uses `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>` as both author and committer for every reachable commit. The older numeric noreply identity was rewritten with a recovery bundle preserved before publication.

## Citation

Please cite the paper when using this reproduction:

    @article{dyachenko2026variational,
      title = {Variational Entropic Optimal Transport},
      author = {Dyachenko, Roman and Gushchin, Nikita and Sokolov, Kirill and Mokrov, Petr and Burnaev, Evgeny and Korotin, Alexander},
      journal = {arXiv preprint arXiv:2602.02241},
      year = {2026},
      doi = {10.48550/arXiv.2602.02241}
    }

## Thank you

Thank you to Roman Dyachenko, Nikita Gushchin, Kirill Sokolov, Petr Mokrov, Evgeny Burnaev, and Alexander Korotin for presenting the VarEOT objective, proof structure, and training procedure clearly enough for independent reconstruction. The explicit separation between the variational theorem, finite-measure KL identity, approximation claims, and Algorithm 1 made it possible to test each layer with its own checker and control. This repository is intended as a respectful reproducibility record and a contribution to transparent scientific discussion.

## Scope and limitations

- The numerical checks for Claims 1 and 2 use continuous one-dimensional Gaussian instances; the symbolic derivations carry the general theorem contracts.
- Claim 3 uses the complete one-dimensional anchored Lipschitz class and a reconstructed proof chain, not a proof assistant or an all-dimensional finite experiment.
- Claim 4 uses an explicit continuous compact witness and analytical universal-approximation reasoning; a finite capacity sweep alone does not prove the universal limit.
- Claim 5 validates simulation-free training, not simulation-free inference. The paper's Algorithm 2 may use Langevin sampling at inference.
- Algorithm 1 follows the authors' executable notebook configuration of 5,000 steps at learning rate 3e-4, while Appendix B.1 states 10,000 steps at 1e-4. Both records are preserved.
- The historical score and all release-gate/provider statuses are provenance, not a new judge result.
