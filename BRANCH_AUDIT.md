# Branch audit

The final public repository has one branch: `main`. The former branch names below were experiment or publication labels. Their tips were reachable from the pre-normalization main history, so retiring the pointers preserves their contents through the canonical history.

| Former branch | Pre-normalization tip | Purpose and outcome | Disposition |
| --- | --- | --- | --- |
| `orx/baseline-exact-claim-contract` | `03460f11bc71d2d71a89d955d6ecb6bfa2db8d30` | Replaced the original grid proxy with the continuous exact Claim 1 baseline. | Retire pointer; history retained |
| `orx/exact-theorem-certificates` | `a3ea38b9ae77fd723c54ef27cf68aad489fd2b25` | Added exact certificates and independent checks for Claims 1–4. | Retire pointer; history retained |
| `orx/algorithm-1-cpu-profile` | `8da1cdc54e933e2ae4e9753078a2a852aff35581` | Profiled the official Algorithm 1 tensor scale before the full run. | Retire pointer; history retained |
| `orx/full-official-algorithm-1` | `e87cf0a259b627e892e2fd82e39545c7b9c45c97` | Executed the first full 5,000-step Algorithm 1 run; its initial checker tolerance was later rejected. | Retire pointer; history retained |
| `orx/precision-certified-algorithm-1` | `7ee3d8e5e21f4f59fd5025e3c2df8f80f584db86` | Added the mixed-precision certificate and completed the accepted five-claim scientific run. | Retire pointer; history retained |
| `orx/evaluator-visible-release-candidate` | `efde861d15da4b670a0050c2aeac9ae99665526e` | Assembled evaluator-visible claim pages and recorded packaging blockers. | Retire pointer; history retained |
| `orx/pinned-marimo-release-validation` | `e3ea13f631fc74ba3e178126f613693995e4401c` | Used the pinned marimo export fallback and corrected non-self-matching secret scan. | Retire pointer; history retained |
| `publication/evaluator-visible-release` | `96aa3a381ff18e0b6a0c78e444979e784827b6e4` | Duplicate final publication surface at the same content as main. | Retire pointer; history retained |

The old branch tips are provenance from the pre-identity-normalization repository. The current remote and local ref layout is intentionally only `main`; `verify_final.py` fails if any additional public branch pointer appears.

All reachable final commits use `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>` for both author and committer. A complete recovery bundle was created before this identity rewrite; its SHA-256 is recorded in the working audit log rather than published as scientific evidence.
