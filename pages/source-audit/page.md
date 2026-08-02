# Source and version audit

The primary HTML was retrieved with User-Agent `OpenResearch-Reproduction/1.0 (paper-source-audit)` on `2026-08-02T03:20:39Z` from `https://ar5iv.labs.arxiv.org/html/2602.02241`; SHA-256: `50f2161eea8428c71e455b7412cd020157a3450f7c60dd6271a8bfe6c6f08261`.

| Claim | Source anchor | Exact quantifier / assumption focus |
| --- | --- | --- |
| 1 | Thm. 3.2, Eqs. 11–13 | every admissible EOT instance; exact auxiliary maximizer for each fixed admissible potential |
| 2 | Thm. 3.3, Eq. 14, Def. A.1 | every admissible candidate pair; generalized KL for finite measures |
| 3 | v1 Thm. 3.5, Eq. 18, App. A.5 | expected error over iid empirical samples; compact support and bounded Lipschitz classes |
| 4 | v1 Thm. 3.7, Eq. 19, App. A.6 | capacity limit for universal neural classes on compact supports |
| 5 | v2 Sec. 3.2, Alg. 1, Eq. 15, Table 1 | each training step's sampling sources and joint parameter update |

The arXiv v1 PDF SHA-256 is `ecadaf4fc32e8b88bff8d57910a6bc291bfa36bd9c4ad61df4d505783b3f66a8`. The current v2 PDF SHA-256 is `257689c36d4d589942660667e880211ab18c6de37d9c643adacd571beaf1949b`. Claims 1–2 are stable in substance. V2 changes Claim 3's rate to `O(N^-1/2)+O(M^-1/2)+O(K^-1/2)` for fixed clipped networks and renumbers Claim 4 to Theorem 3.6. The judged contracts are explicitly v1.

The official code audit used author commit `fd1b2f93b89fd1d8be8ddf32aa30807fc5fafb26`. Its executable Swiss-roll notebook conflicts with Appendix B.1 on steps and learning rate; both configurations are stated on the Claim 5 page.
