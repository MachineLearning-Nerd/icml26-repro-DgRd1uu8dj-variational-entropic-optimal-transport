# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e47e390d0d63", "created_at": "2026-07-31T15:41:32+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Theorem 3.2 derives a variational dual form of entropic optimal transport, EOT_eps(p0,p1) = sup_f L(f) = sup_{f,xi} L(f,xi), replacing the intractable log-partition function with a tractable variational minimization over an auxiliary normalizer xi (Section 3, Theorem 3.2).
2. Theorem 3.3 shows the optimality gap equals a scaled KL divergence, eps*KL(pi* || pi_{f,xi}) = L* - L(f,xi), so optimizing the variational objective directly controls approximation of the ground-truth EOT plan (Section 3, Theorem 3.3).
3. Theorem 3.5 gives a finite-sample estimation error bound of order O(N^(-1/(1+D))) + O(M^(-1/(1+D))) for Lipschitz-constrained function classes on compact supports (Section 3.3, Theorem 3.5).
4. Theorem 3.7 proves the approximation error vanishes as neural network capacity grows under universal function approximation, giving a full generalization guarantee together with Theorem 3.5 (Section 3.3, Theorem 3.7).
5. Algorithm 1 trains VarEOT in a simulation-free manner by jointly optimizing the potential f_theta and auxiliary function xi_psi via stochastic gradient ascent, avoiding the MCMC simulations required by EgNOT (Section 3, Algorithm 1; Table 1).
