# Claim 5 evaluation contract

Run the inherited command `uv sync --frozen && .venv/bin/python -m vareot_repro.run_all` on HF `cpu-upgrade`. The frozen parent measured `1.34562` seconds per step at the exact tensor shape and projected `6728.08` training seconds. This node changes only committed `steps=5000`, `profile_only=false`, and the CPU estimate, then reruns Claims 1–4 and the final Claim 5 gate.
