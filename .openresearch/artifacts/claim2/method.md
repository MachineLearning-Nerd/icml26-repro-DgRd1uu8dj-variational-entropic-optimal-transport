# Claim 2 method

For each of the two continuous Gaussian baseline instances, the verifier perturbs both the curvature and linear term of the optimal quadratic potential. It then adds a nonconstant affine normalizer shift `delta(x)` so the candidate plan is deliberately not normalized.

The primary implementation evaluates the Gaussian conditional KL and log-normal moment analytically. The independent checker uses adaptive quadrature for both. The verifier compares their generalized KL with the direct objective gap.

The negative control drops the finite-measure mass correction and must miss the identity by at least `0.05`.
