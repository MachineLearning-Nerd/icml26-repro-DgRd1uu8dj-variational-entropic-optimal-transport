# Current verification: Claim 1 / Theorem 3.2

Status before execution: **PENDING BASELINE RUN**.

This page supersedes the grid-discretized historical verifier for Claim 1. It tests the exact variational identity with a symbolic reconstruction and a continuous Gaussian EOT instance. The executable entrypoint is `vareot_repro/run_all.py`; the independent implementation is in `vareot_repro/claim1.py`; the deliberately wrong-potential control is `vareot_repro/negative_control.py`.

Run the fixed command from `EVAL.md`. On success, the run prints and writes `raw_results.json`, `independent_checker_output.json`, and `negative_control_output.json`. Those generated files are not pre-populated: a descendant evidence-freeze node will commit the exact outputs from the immutable baseline run and rerun the cumulative suite against them.

The claim contract, exact source quantifiers, assumptions, method, and limitations are adjacent to this page.
