# Visibility and release audit

## Evaluator-blind traversal

The reviewer was restricted to the candidate artifact and began at `README.md`, without OpenResearch logs or repository history. Files opened, in order:

1. `README.md`
2. `pages/current/page.md`
3. `pages/claim-1/page.md` through `pages/claim-5/page.md`
4. `pages/source-audit/page.md`
5. each claim's `raw_results.json`, `independent_checker_output.json`, and `negative_control_output.json`
6. `.openresearch/artifacts/frozen_precision_run.json` and `.openresearch/artifacts/claim5/training_trace.csv`
7. each linked `claim_contract.json`, `vareot_repro/claim*.py`, `run_all.py`, `pyproject.toml`, and `uv.lock`
8. `reports/variational-eot-reproduction/report.md` and its five SVG figures
9. this release-audit page and `publication_allowlist.txt`

The reviewer could locate the current verifier without being told a hidden path. Every claim exposed its exact statement, assumptions, scope, inline number, raw download, executable source, independent check, negative control, limitations, evidence SHA/run, fixed command, and CPU/runtime record. No conclusion required unpublished logs. The v1/v2 statement difference and Algorithm 1 notebook/appendix discrepancy were visible before the verdicts.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `#/claim-1` | yes | yes | yes | yes | yes | yes | complete |
| 2 | `#/claim-2` | yes | yes | yes | yes | yes | yes | complete |
| 3 | `#/claim-3` | yes | yes | yes | yes | yes | yes | complete |
| 4 | `#/claim-4` | yes | yes | yes | yes | yes | yes | complete |
| 5 | `#/claim-5` | yes | yes | yes | yes | yes | yes | complete |

## Historical subset safety

Judged revision `7b762ad0a9b67bef76040075929c4cbb3eb8f3b3` contains 17 protected files. The candidate upload is additive: it does not delete any path. The five historical claim/evidence pages remain byte-identical at their original paths and appear only under navigation titled exactly **Historical rejected baseline**. Because the current `README.md`, `logbook.json`, and `pages/index.md` must change to expose the new verifier, their exact judged bytes are additionally archived under `historical/judged-7b762ad/`. The original 17-file hash list is `historical/judged-7b762ad/MANIFEST.sha256`.

A fresh-clone prepublication audit reported old-path inclusion `17/17`: the upload contains no delete operation, 14 protected paths are untouched, and the three replaced evaluator entrypoints are archived byte-for-byte. Binary Trackio assets are untouched. The same `17/17` check is required again after publication.

## Publication controls

- Upload destination: existing Space `DineshAI/DgRd1uu8dj`; no second Space.
- Transport: text-only Hugging Face commit API.
- Exact upload paths: `publication_allowlist.txt`.
- SHA-256 values: `MANIFEST.sha256` (the manifest intentionally excludes its own self-referential hash).
- Secret scan: every allowlisted text file; token values are never printed.
- Scientific source: commit `7ee3d8e5e21f4f59fd5025e3c2df8f80f584db86`, run `0f29450d-5b73-4214-ae3e-10d47608a377`.
- Pinned `marimo==0.15.2` does not expose the later `marimo check` subcommand. The exact requested command was executed on HF and returned the documented “No such command” exit `2`. The same pinned release is therefore required to execute every notebook cell via `marimo export html --no-sandbox`; any cell error makes that command nonzero. Both results are printed in the release evidence, and the lockfile is unchanged.
- Publication occurs only after the corrective child reruns the cumulative scientific suite, frozen-evidence comparison, exact marimo-command audit, executable notebook export, visibility checks, controls, and secret scan on HF `cpu-upgrade`.
