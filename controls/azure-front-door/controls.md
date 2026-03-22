# Azure Front Door — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Front Door is a global entry point for HTTP and HTTPS traffic. The baseline is driven by WAF association, HTTPS posture, origin protection, and access telemetry.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| AFD-001 | NS-2 | NS | WAF policy associated with each public route | Must | Partial | route-to-policy linkage |
| AFD-002 | DP-3 | DP | HTTPS enforced and HTTP redirected or disabled | Must | Partial | route configuration |
| AFD-003 | NS-1 | NS | Origins locked down to Front Door only | Must | Partial | origin ACL, header, or private link |
| AFD-004 | LT-3 | LT | Access and WAF logs enabled | Must | Partial | diagnostic settings |
| AFD-005 | IM-3 | IM | Certificates managed securely | Must | Partial | managed cert or Key Vault |

## Control Detail Highlights

- `AFD-001`: Every public route should be attached to a WAF policy. Unprotected routes become bypass paths at the global edge.
- `AFD-002`: HTTP should be redirected or disabled so that the edge posture stays consistently encrypted.
- `AFD-003`: Backend origins should reject direct access where feasible. Front Door should be the intended ingress path, not just one of several.
- `AFD-004`: Access and WAF telemetry should be exported together to support investigation of abusive traffic, rules, and origin errors.
- `AFD-005`: Certificates should be managed through approved platform paths, ideally managed certificates or Key Vault-backed material.

## Agent Notes

- Front Door is only part of the control story; the origin must also be protected against direct bypass.
- Review route-to-domain and route-to-origin mappings because exposure mistakes often happen in configuration joins rather than in a single resource.
- For high-value web apps, correlate Front Door with App Gateway, WAF, or private origin patterns.

## Suggested Validation Cases

- Secure: WAF on all public routes, HTTPS enforced, origin isolated from direct traffic, diagnostics enabled.
- Insecure: public route without WAF, HTTP left open, origin still internet-reachable directly, missing logs.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Front Door security baseline
