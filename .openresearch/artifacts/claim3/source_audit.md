# Claim 3 source audit

The judge contract refers to arXiv v1, SHA-256 `ecadaf4fc32e8b88bff8d57910a6bc291bfa36bd9c4ad61df4d505783b3f66a8`: Theorem 3.5, Equation 18, proof A.5. The proof applies symmetrization to both empirical marginals, coordinatewise contraction to the bounded quotient class, the compact-metric Lipschitz rate from Gottlieb et al. (2016, Theorem 4.3), and the Gaussian-smoothed partition-class rate from Kolesov et al. (2024, Theorem 4.5).

The current v2 PDF, SHA-256 `257689c36d4d589942660667e880211ab18c6de37d9c643adacd571beaf1949b`, materially changes the statement to `O(N^-1/2)+O(M^-1/2)+O(K^-1/2)` for fixed clipped neural-network classes. The two claims must not be conflated; this verifier targets the historical claim the judge actually scored.
