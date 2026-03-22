# Azure Application Gateway — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Application Gateway is a Layer 7 ingress component frequently used for public web entry points, internal HTTP routing, and WAF-backed application publishing. The baseline focuses on WAF posture, TLS hygiene, backend trust boundaries, and operational visibility.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| AGW-001 | NS-2 | NS | WAF tier enabled for internet-facing workloads | Must | Yes | `sku.tier = "WAF_v2"` |
| AGW-002 | DP-3 | DP | TLS 1.2+ enforced on listeners and policy | Must | Partial | SSL policy / listener protocol |
| AGW-003 | NS-1 | NS | Backend pool restricted to approved targets | Must | Partial | backend pools reference intended services only |
| AGW-004 | LT-3 | LT | Diagnostic and access logs enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| AGW-005 | IM-3 | IM | Certificates sourced from Key Vault | Must | Partial | Key Vault secret or certificate reference |
| AGW-006 | NS-2 | NS | Public frontend only when explicitly required | Should | Yes | public IP presence justified |

## Control Detail Highlights

- `AGW-001`: Public HTTP workloads should use `WAF_v2`, not Standard tiers, so that inspection and managed rules are part of the baseline rather than an add-on.
- `AGW-002`: The gateway should terminate TLS with modern policies and avoid legacy listener or backend TLS behavior that weakens the edge posture.
- `AGW-003`: Backend pools should only contain the intended application targets. Mixing unrelated services in one gateway increases blast radius and makes routing mistakes harder to audit.
- `AGW-004`: Access, performance, and firewall logs should be exported to central monitoring because Application Gateway is often the main evidence source for web ingress incidents.
- `AGW-005`: Certificates should come from Key Vault, not inline PFX blobs or unmanaged manual rotation paths.
- `AGW-006`: A public frontend should be treated as an explicit architectural decision. Internal-only gateways should remain private.

## Agent Notes

- Correlate Application Gateway posture with NSGs, subnets, Key Vault, and the protected backend service.
- For internet-facing workloads, review WAF association and prevention mode together rather than as separate controls.
- If the backend is AKS or App Service, verify that direct origin access is also limited so traffic cannot bypass the gateway.

## Suggested Validation Cases

- Secure: `WAF_v2`, modern SSL policy, diagnostics enabled, certificate from Key Vault, private frontend where possible.
- Insecure: Standard tier on a public web app, unmanaged certificate material, missing diagnostics, broad backend pool membership.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Application Gateway security baseline
- AKS ingress guidance already referenced in this repo
