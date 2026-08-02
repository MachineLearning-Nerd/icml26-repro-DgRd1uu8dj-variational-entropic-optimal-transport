# Current verification

This is the canonical evaluator entrypoint. It supersedes the historical grid verifier with commit `7ee3d8e5e21f4f59fd5025e3c2df8f80f584db86` and immutable HF run `0f29450d-5b73-4214-ae3e-10d47608a377`. The fixed command was:

```bash
uv sync --frozen && .venv/bin/python -m vareot_repro.run_all
```

The run selected HF `cpu-upgrade`; 32 cores were estimated, 64 CPU-affinity cores and 32 Torch threads were observed, CUDA was false, scientific runtime was 5,750.05s, and wall time was 2h16m. Exact versions are pinned in [pyproject.toml](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/pyproject.toml) and [uv.lock](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/uv.lock).

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Thm. 3.2](#/claim-1) | `claim1.py` | `4.44e-16` max equality error | [JSON](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim1/raw_results.json) | adaptive quadrature | wrong potential exits 1 | general auxiliary identity + continuous non-vacuity case | VERIFIED / HIGH |
| 2 | [Thm. 3.3](#/claim-2) | `claim2.py` | `5.83e-16` max gap error | [JSON](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim2/raw_results.json) | independent generalized KL | ordinary KL rejected | every admissible finite candidate measure | VERIFIED / HIGH |
| 3 | [Thm. 3.5 v1](#/claim-3) | `claim3.py` | slope `-0.511`, 128 seeds | [JSON](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim3/raw_results.json) | proof chain + exact W1 | repeated non-iid data rejected | v1 bounded-Lipschitz rate | VERIFIED / MEDIUM |
| 4 | [Thm. 3.7 v1](#/claim-4) | `claim4.py` | gap `0.02273→0.000352` | [JSON](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim4/raw_results.json) | adaptive integration + exact ReLU realization | fixed potential tail rejected | v1 universal neural capacity limit | VERIFIED / MEDIUM |
| 5 | [Algorithm 1](#/claim-5) | `claim5.py` | objective gain `1.21451`; model samples `0` | [JSON](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim5/raw_results.json) / [CSV](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/resolve/main/.openresearch/artifacts/claim5/training_trace.csv) | NumPy/Torch float64 equality | detached potential rejected | official full neural training loop | VERIFIED / HIGH |

No finite experiment is presented as proof of a universal statement. Claims 1–4 pair machine-checked special cases with independently reconstructed analytical certificates. Claim 5 implements the named algorithm directly. [Read the illustrated report](https://huggingface.co/spaces/DineshAI/DgRd1uu8dj/blob/main/reports/variational-eot-reproduction/report.md).
