# Claim 5 limitations and deviations

- This route follows the executable official notebook's 5,000-step schedule; the paper appendix's conflicting 10,000-step schedule is reported rather than hidden.
- The training claim is tested directly. Langevin inference quality is outside the exact simulation-free-training quantifier and is not used to make the verifier pass.
- Swiss-roll transport quality has no analytic ground-truth plan. The acceptance gate therefore uses the exact held-out training objective and structural sampling contract, not an invented KL target.
