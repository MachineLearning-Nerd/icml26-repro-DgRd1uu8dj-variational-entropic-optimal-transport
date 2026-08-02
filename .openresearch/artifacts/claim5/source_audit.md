# Claim 5 source audit

- Current v2 source: Section 3.2, Algorithm 1, Equation 15, Table 1, and Appendix B.1; PDF SHA-256 `257689c36d4d589942660667e880211ab18c6de37d9c643adacd571beaf1949b`.
- Algorithm 1 samples minibatches from `p0` and `p1` plus iid standard Gaussian `z`, evaluates Equation 15, and updates both `theta` and `psi` in one loop.
- “Simulation-free” is specifically a training claim: no samples from the learned conditional are required to estimate the training objective. Algorithm 2 does use Langevin dynamics at inference and is not relabeled simulation-free.
- Appendix B.1 specifies 10,000 steps and learning rate `1e-4`. The authors' official Swiss-roll notebook at commit `fd1b2f93b89fd1d8be8ddf32aa30807fc5fafb26` instead executes 5,000 steps at `3e-4`; both use batch 256, K=256, width 256, AdamW betas `(0.7,0.8)`, weight decay `1e-4`, EMA `0.999`, and simultaneous updates. The executable notebook contract is used and the discrepancy remains visible.
