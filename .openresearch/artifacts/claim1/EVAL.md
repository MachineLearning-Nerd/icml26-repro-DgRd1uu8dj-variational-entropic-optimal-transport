# Claim 1 evaluation contract

Run exactly:

```bash
uv sync --frozen && .venv/bin/python -m vareot_repro.run_all
```

The command must print the selected backend/flavor, actual CPU allocation, resolved versions, raw results, independent-checker result, negative-control exit code, runtime, and final status. Any failed numerical identity, source-marginal audit, or control causes a nonzero exit.
