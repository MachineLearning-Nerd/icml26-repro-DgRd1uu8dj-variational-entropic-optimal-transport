# Claim 1 method

The verifier reconstructs the variational step independently. Writing `xi=xi_f+delta` yields

`L(f)-L(f,xi) = epsilon E[delta + exp(-delta) - 1]`.

The elementary inequality `exp(-delta) >= 1-delta` proves nonnegativity for every real `delta`, with equality only at zero. This proves the auxiliary optimization is exact whenever the original semidual is admissible.

For a non-vacuous continuous check, the verifier solves EOT between two one-dimensional Gaussian distributions. The optimal quadratic potential induces a Gaussian conditional whose target marginal is checked analytically. The primal conditional-entropy objective, weak semidual, and variational objective are then compared. A separate adaptive-integration implementation checks the partition function and expectations without discretizing the transport problem.

The negative control scales the analytic precision parameter by 1.15. It no longer produces the target marginal and must make the verifier exit nonzero.
