# Verification run


---
<!-- trackio-cell
{"type": "code", "id": "cell_97d7705924a3", "created_at": "2026-07-31T15:41:53+00:00", "title": "verify all claims", "command": [".venv/bin/python", "repro/src/verify.py"], "exit_code": 0, "duration_s": 19.698}
-->
````bash
$ .venv/bin/python repro/src/verify.py
````
exit 0 · 19.7s


````python title=verify.py
"""verify.py - 5 anchored claims for DgRd1uu8dj (arXiv 2602.02241, VarEOT)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import core as C
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs"); os.makedirs(OUT, exist_ok=True)
v = {"paper": "DgRd1uu8dj", "arxiv": "2602.02241", "checks": {}}

r = C.claim0_thm32_variational_dual()
v["checks"]["C0_thm32_variational_dual"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Theorem 3.2 / [0]: EOT = sup_f L(f) = sup_{f,xi} L(f,xi) (variational dual replaces the intractable log-partition)",
 "precision": f"variational bound tight err L(f*,xi_f)-L*={r['variational_bound_tight_err_Lfstar_xif_minus_Lstar']:.2e}; L(f,xi)<=L(f) for all xi (excess {r['max_Lfxi_excess_over_Lf_for_random_xi']:.2e})"}

r = C.claim1_thm33_gap_equals_kl()
v["checks"]["C1_thm33_gap_equals_scaled_KL"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Theorem 3.3 / [1]: optimality gap = scaled KL, eps*KL(pi*||pi_{f,xi}) = L* - L(f,xi)",
 "precision": f"EXACT identity eps*KL(pi*||pi_f)=L*-L(f), max err {r['max_abs_err_epsKL_pi_f_eq_Lstar_minus_Lf']:.2e}; with-xi variant err {r['max_abs_err_epsKL_pi_fxi_eq_Lstar_minus_Lfxi']:.2e}"}

r = C.claim2_thm35_finite_sample_rate()
v["checks"]["C2_thm35_finite_sample_rate"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Theorem 3.5 / [2]: finite-sample estimation error E sup[L-L_hat] = O(N^{-1/2})+O(M^{-1/2})",
 "precision": f"estimation error by N {r['Ns']}: {[e for e in r['estimation_error']]}; log-log slope {r['loglog_slope']:.3f} (~ -1/2)"}

r = C.claim3_thm36_capacity_vanishes()
v["checks"]["C3_thm36_approx_error_vanishes"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Theorem 3.6 / [3]: approximation error L*-sup_{class}L -> 0 as network capacity grows",
 "precision": f"approx error by #features {r['capacities_n_features']}: {[e for e in r['approx_error_Lstar_minus_Lclass']]} (->0)"}

r = C.claim4_algo1_recovers_plan()
v["checks"]["C4_algo1_recovers_plan_simfree"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Algorithm 1 / [4]: simulation-free variational solve jointly over (f,xi) recovers the EOT plan pi*",
 "precision": f"KL(pi*||pi_f_hat)={r['KL_pi_star_vs_recovered_pi_f']:.4f}; L_var-L*={r['recovered_L_var_minus_Lstar']:.4f}; simfree-noise MC rel-err by K {r['simfree_MC_mean_rel_err_by_K']}"}

v["n_claims_passed"] = sum(1 for c in v["checks"].values() if c["status"] == "PASS")
v["n_claims_total"] = 5
v["all_passed"] = all(c["status"] == "PASS" for c in v["checks"].values())
json.dump(v, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print(json.dumps(v, indent=2))
print(f"\nSUMMARY: {v['n_claims_passed']}/{v['n_claims_total']} passed, all_passed={v['all_passed']}")

````


````output
{
  "paper": "DgRd1uu8dj",
  "arxiv": "2602.02241",
  "checks": {
    "C0_thm32_variational_dual": {
      "status": "PASS",
      "anchor": "Theorem 3.2 / [0]: EOT = sup_f L(f) = sup_{f,xi} L(f,xi) (variational dual replaces the intractable log-partition)",
      "precision": "variational bound tight err L(f*,xi_f)-L*=0.00e+00; L(f,xi)<=L(f) for all xi (excess 0.00e+00)"
    },
    "C1_thm33_gap_equals_scaled_KL": {
      "status": "PASS",
      "anchor": "Theorem 3.3 / [1]: optimality gap = scaled KL, eps*KL(pi*||pi_{f,xi}) = L* - L(f,xi)",
      "precision": "EXACT identity eps*KL(pi*||pi_f)=L*-L(f), max err 1.85e-12; with-xi variant err 2.20e-04"
    },
    "C2_thm35_finite_sample_rate": {
      "status": "PASS",
      "anchor": "Theorem 3.5 / [2]: finite-sample estimation error E sup[L-L_hat] = O(N^{-1/2})+O(M^{-1/2})",
      "precision": "estimation error by N [64, 128, 256, 512, 1024]: [0.27285, 0.17804, 0.17685, 0.05574, 0.04529]; log-log slope -0.686 (~ -1/2)"
    },
    "C3_thm36_approx_error_vanishes": {
      "status": "PASS",
      "anchor": "Theorem 3.6 / [3]: approximation error L*-sup_{class}L -> 0 as network capacity grows",
      "precision": "approx error by #features [4, 8, 16, 32, 64, 128]: [0.26879, 0.03321, 0.00112, 5e-05, 0.0, 0.0] (->0)"
    },
    "C4_algo1_recovers_plan_simfree": {
      "status": "PASS",
      "anchor": "Algorithm 1 / [4]: simulation-free variational solve jointly over (f,xi) recovers the EOT plan pi*",
      "precision": "KL(pi*||pi_f_hat)=0.0053; L_var-L*=-0.0040; simfree-noise MC rel-err by K {4: 0.02, 16: 0.006, 64: 0.0025, 256: 0.001}"
    }
  },
  "n_claims_passed": 5,
  "n_claims_total": 5,
  "all_passed": true
}

SUMMARY: 5/5 passed, all_passed=True

````
