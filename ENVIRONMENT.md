# Environment and run provenance

## Reproduction command

    uv sync --frozen && .venv/bin/python -m vareot_repro.run_all

The command above is the repository's fixed cumulative verifier. The final-state checker in `verify_final.py` validates the stored evidence and does not rerun this expensive job.

## Canonical scientific run

| Field | Value |
| --- | --- |
| Evidence run | `0f29450d-5b73-4214-ae3e-10d47608a377` |
| Evidence revision | `7ee3d8e5e21f4f59fd5025e3c2df8f80f584db86` |
| Backend | Hugging Face `cpu-upgrade` |
| GPU | unavailable; `cuda_available=false` |
| Estimated cores | 32 |
| CPU affinity observed | 64 |
| Torch threads | 32 |
| Scientific runtime | 5750.050501372001 seconds |
| Wall-time record | 2h16m |
| Claim statuses | 5/5 `VERIFIED` |

## Resolved environment

The pinned project environment is Python 3.12 with NumPy 2.3.2, SciPy 1.16.1, Torch 2.8.0 CPU, and marimo 0.15.2 resolved by `uv.lock`. The expensive training evidence was produced on the historical CPU job above; no new paid, remote, GPU, or scientific rerun was started for repository cleanup.

## Evidence pointers

- Aggregate evidence: `.openresearch/artifacts/frozen_precision_run.json`
- Claim-specific raw results, independent checkers, controls, and source audits: `.openresearch/artifacts/claim1/` through `.openresearch/artifacts/claim5/`
- Algorithm 1 trace: `.openresearch/artifacts/claim5/training_trace.csv`
- Historical judged artifact: `historical/judged-7b762ad/`
- Original evaluator manifest: `MANIFEST.sha256`
- Standardized selected-evidence manifest: `EVIDENCE_MANIFEST.json`

The old release record's marimo `check` command was unavailable in the pinned version, so its export fallback and provider timeout are retained as infrastructure provenance, not scientific failures.
