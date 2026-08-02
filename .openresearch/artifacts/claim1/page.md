# Current verification: Claim 1 / Theorem 3.2

Status: **VERIFIED** by immutable HF run `0f29450d-5b73-4214-ae3e-10d47608a377` at commit `7ee3d8e5e21f4f59fd5025e3c2df8f80f584db86`.

This page supersedes the grid-discretized historical verifier for Claim 1. It tests the exact variational identity with a symbolic reconstruction and a continuous Gaussian EOT instance. The executable entrypoint is `vareot_repro/run_all.py`; the independent implementation is in `vareot_repro/claim1.py`; the deliberately wrong-potential control is `vareot_repro/negative_control.py`.

The frozen aggregate is `../frozen_precision_run.json`. The maximum continuous equality and adaptive-quadrature errors were `4.44e-16`; the wrong-potential control exited `1`.

The claim contract, exact source quantifiers, assumptions, method, and limitations are adjacent to this page.
