"""A deliberately non-optimal potential that the Claim 1 verifier must reject."""

import json

from .claim1 import CASES, run_case, verify_results


def main() -> None:
    results = [run_case(case, q_scale=1.15) for case in CASES]
    passed, failures = verify_results(results)
    print(json.dumps({"control": "q_scaled_by_1.15", "passed": passed, "failures": failures}, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
