# Claim 5 — Algorithm 1 — VERIFIED

**Exact claim.** Each Algorithm 1 training iteration samples only source data, target data, and independent standard Gaussian noise, evaluates Equation 15, and jointly updates neural `f_theta` and `xi_psi`; no current model-plan simulation is used during training. This does not claim simulation-free inference. Source: v2 Section 3.2, Algorithm 1, Eq. 15, Table 1, and Appendix B.1, PDF SHA-256 `257689c36d4d589942660667e880211ab18c6de37d9c643adacd571beaf1949b`.

The full CPU run uses continuous 2D Gaussian and noisy Swiss-roll marginals, two independent `2→256→256→256→1` SiLU MLPs, batch 256, Monte Carlo `K=256`, AdamW, EMA, clipping, and 5,000 joint steps. The fixed held-out maximized objective improved from `-0.996558` to `0.217951` (`+1.214509`). First-step gradient norms were `0.300385` for the potential and `0.014266` for the normalizer; update norms were `17.9652` and `8.71017`.

The sample ledger records `1,280,000` source samples, `1,280,000` target samples, `327,680,000` independent Gaussian proposals, and **0 model-distribution samples**. Training took 5,719.53s.

An independent NumPy float64 recombination exactly matched Torch float64 (`0` error). The actual mixed-precision discrepancy was `6.54e-7`, below the a-priori IEEE scale bound `1.41e-5`. Detaching all potential outputs forced its gradient to `0` while the normalizer gradient remained `0.01394`; the joint-training control was rejected.

- [Algorithm 1 implementation](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/vareot_repro/claim5.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim5/claim_contract.json)
- [Raw results](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim5/raw_results.json)
- [Training trace CSV](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim5/training_trace.csv)
- [Independent checker](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim5/independent_checker_output.json) · [negative control](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/.openresearch/artifacts/claim5/negative_control_output.json)

**Deviation.** The authors' executable Swiss-roll notebook at `fd1b2f93b89fd1d8be8ddf32aa30807fc5fafb26` runs 5,000 steps at `3e-4`; Appendix B.1 says 10,000 at `1e-4`. We follow the executable notebook and do not conceal the conflict. Swiss-roll plan KL is not analytically available, so the acceptance contract audits the exact training objective and sampling mechanism rather than inventing a ground truth. Confidence: **HIGH**.
