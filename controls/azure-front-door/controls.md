# Azure Front Door — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Front Door is a global entry point for HTTP/HTTPS traffic. The baseline is driven by WAF, origin protection, TLS posture, and access telemetry.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| AFD-001 | NS-2 | NS | WAF policy associated with each public route | Must | Partial | route-to-policy linkage |
| AFD-002 | DP-3 | DP | HTTPS enforced and HTTP redirected or disabled | Must | Partial | route configuration |
| AFD-003 | NS-1 | NS | Origins locked down to Front Door only | Must | Partial | origin ACL / header / private link |
| AFD-004 | LT-3 | LT | Access and WAF logs enabled | Must | Partial | diagnostic settings |
| AFD-005 | IM-3 | IM | Certificates managed securely | Must | Partial | managed cert or Key Vault |

## Implementation Notes

- Front Door should not be the only control; origin services must reject direct bypass traffic.
- Associate WAF policies with all internet-facing domains and routes.
- Capture both access logs and WAF logs for investigations.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Front Door security baseline
