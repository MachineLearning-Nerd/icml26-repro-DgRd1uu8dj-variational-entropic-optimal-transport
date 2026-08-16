# Historical branch audit

Before normalization, this repository had one publication branch and eight remote experiment or release branches. Every former branch tip was an ancestor of the pre-normalization main tip 96aa3a381ff18e0b6a0c78e444979e784827b6e4. The experiment history therefore remains reachable through main after the branch pointers are retired.

| Former branch | Pre-normalization tip | Purpose and recorded outcome | Disposition |
| --- | --- | --- | --- |
| main | 96aa3a381ff18e0b6a0c78e444979e784827b6e4 | Final publication surface, current five-claim evidence, historical baseline archive, and release artifacts. | Keep as canonical main |
| orx/baseline-exact-claim-contract | 03460f11bc71d2d71a89d955d6ecb6bfa2db8d30 | Replace the original grid proxy with the continuous exact Claim 1 baseline. | Retire pointer; history retained |
| orx/exact-theorem-certificates | a3ea38b9ae77fd723c54ef27cf68aad489fd2b25 | Add exact certificates and independent checks for Claims 1–4. | Retire pointer; history retained |
| orx/algorithm-1-cpu-profile | 8da1cdc54e933e2ae4e9753078a2a852aff35581 | Profile the official Algorithm 1 tensor scale before paying for the full run. | Retire pointer; history retained |
| orx/full-official-algorithm-1 | e87cf0a259b627e892e2fd82e39545c7b9c45c97 | Execute the first full 5,000-step Algorithm 1 run; the initial checker tolerance was later rejected. | Retire pointer; history retained |
| orx/precision-certified-algorithm-1 | 7ee3d8e5e21f4f59fd5025e3c2df8f80f584db86 | Add the a-priori mixed-precision certificate and complete the accepted five-claim scientific run. | Retire pointer; history retained |
| orx/evaluator-visible-release-candidate | efde861d15da4b670a0050c2aeac9ae99665526e | Assemble evaluator-visible claim pages and the first release gate; packaging blockers were recorded. | Retire pointer; history retained |
| orx/pinned-marimo-release-validation | e3ea13f631fc74ba3e178126f613693995e4401c | Use the pinned marimo export fallback and corrected non-self-matching secret scan. | Retire pointer; history retained |
| publication/evaluator-visible-release | 96aa3a381ff18e0b6a0c78e444979e784827b6e4 | Final publication surface; same tip as main. | Retire duplicate pointer; history retained |

The orx/* and publication/* names were generated experiment or release labels, not stable public APIs. The normalized public surface uses only main; claim pages, raw evidence, commit history, and this audit preserve the decision path and outcomes.

Before normalization, the branch tips used the numeric MachineLearning-Nerd noreply identity. The final history rewrite sets both author and committer to MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com> for every reachable commit.
