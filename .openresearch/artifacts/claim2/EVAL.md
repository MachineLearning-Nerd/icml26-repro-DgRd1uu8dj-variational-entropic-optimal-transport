# Claim 2 evaluation contract

Run the inherited command:

```bash
uv sync --frozen && .venv/bin/python -m vareot_repro.run_all
```

The cumulative process writes `raw_results.json`, `independent_checker_output.json`, and `negative_control_output.json`. It exits nonzero if the exact generalized-KL identity, independent integral, inequality, or negative control fails.
