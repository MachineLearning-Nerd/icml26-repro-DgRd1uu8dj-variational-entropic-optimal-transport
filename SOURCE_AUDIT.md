# Source and paper audit

## Paper identity

- Title: *Variational Entropic Optimal Transport*
- Authors: Roman Dyachenko, Nikita Gushchin, Kirill Sokolov, Petr Mokrov, Evgeny Burnaev, and Alexander Korotin
- arXiv: [2602.02241](https://arxiv.org/abs/2602.02241)
- OpenReview: [DgRd1uu8dj](https://openreview.net/forum?id=DgRd1uu8dj)
- arXiv v1: submitted 2026-02-02; used for the judged Theorem 3.5 and Theorem 3.7 contracts
- arXiv v2: revised 2026-06-04; current source for the stable theorem statements and Algorithm 1

The arXiv abstract describes VarEOT as an exact variational reformulation of the log-partition term in continuous quadratic-cost EOT. It introduces an auxiliary positive normalizer, produces a differentiable stochastic-gradient objective, avoids MCMC during training, and supplies generalization and approximation guarantees.

## Pinned source records

| Source | Retrieval/provenance | SHA-256 |
| --- | --- | --- |
| arXiv v2 PDF | current paper source used for Claims 1, 2, and 5 | `257689c36d4d589942660667e880211ab18c6de37d9c643adacd571beaf1949b` |
| arXiv v1 PDF | historical judged source for Claims 3 and 4 | `ecadaf4fc32e8b88bff8d57910a6bc291bfa36bd9c4ad61df4d505783b3f66a8` |
| ar5iv HTML | retrieved 2026-08-02T03:20:39Z from `https://ar5iv.labs.arxiv.org/html/2602.02241` | `50f2161eea8428c71e455b7412cd020157a3450f7c60dd6271a8bfe6c6f08261` |

The version boundary is material: v2 changes the finite-sample statement and renumbers the approximation theorem. The claim ledger keeps those contracts separate rather than silently translating a v1 verdict into a v2 verdict.

## Official implementation provenance

The arXiv record links the authors' public implementation [DrEternity/VarEOT](https://github.com/DrEternity/VarEOT). The current public `main` tip observed through the GitHub API on 2026-08-17 is `fd1b2f93e1b5606feafaf46e34da61066c844e83`. The existing scientific record also preserves an earlier executable-source identifier beginning `fd1b2f93`; this audit treats the current API-resolved tip as the current upstream pin and does not claim that upstream history is immutable.

This repository is an independent audit and does not vendor or modify the authors' repository. The local `vareot_repro/` implementation is the claim producer; the external repository is source provenance for the Algorithm 1 configuration.

## Source boundaries

- Claims 1 and 2 use source theorem statements plus independent continuous instances.
- Claims 3 and 4 report the arXiv v1 contracts that were judged; the v2 changes are recorded as a limitation.
- Claim 5 follows the authors' executable Swiss-roll schedule and records its disagreement with Appendix B.1.
- The historical judge score `5/10` is provenance only; no current judge result is asserted.
