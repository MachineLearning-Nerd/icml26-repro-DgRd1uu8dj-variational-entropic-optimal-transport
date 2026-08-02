# Claim 5 method

The implementation mirrors the authors' Swiss-roll notebook: continuous two-dimensional standard-Gaussian source, continuous noisy Swiss-roll target, two independent four-linear-layer width-256 SiLU networks, batch 256, K=256, AdamW, exponential clipping, gradient clipping, and EMA.

The audit counts every training sample source. The only stochastic inputs are `p0`, `p1`, and independent Gaussian noise. A fixed held-out batch measures Equation 15 before and after training. An independent NumPy implementation recombines frozen network outputs and checks the Torch loss. Both first-step gradients and total parameter updates must be nonzero.

The negative control detaches every potential output before Equation 15. Its potential gradient is then exactly zero while the normalizer gradient remains nonzero; the joint-update checker must reject it.
