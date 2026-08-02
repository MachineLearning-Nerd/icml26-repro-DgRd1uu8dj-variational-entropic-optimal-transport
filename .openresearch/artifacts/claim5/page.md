# Current verification: Claim 5 / Algorithm 1

This candidate supersedes the grid optimizer with the actual continuous, neural, joint-gradient Algorithm 1 at the official batch, Monte Carlo, network, and 5,000-step executable scale. It receives a final verdict only if the held-out objective, joint updates, sample audit, independent checker, and negative control all pass.

It also supersedes the frozen full-run parent's unscaled `2e-7` checker: the current checker reports exact float64 NumPy/Torch agreement and audits the mixed-precision training reduction against an IEEE-epsilon scale bound.

The source contract, exact implementation, raw JSON, NumPy checker, detached-potential control, CPU accounting, and deviations are adjacent.
