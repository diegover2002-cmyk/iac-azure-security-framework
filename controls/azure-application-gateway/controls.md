# Azure Application Gateway — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Application Gateway is a Layer 7 load balancer frequently used as the HTTP ingress point for web workloads. The baseline focuses on WAF enforcement, TLS hygiene, network exposure, and observability.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| AGW-001 | NS-2 | NS | WAF tier enabled for internet-facing workloads | Must | Yes | `sku.tier = "WAF_v2"` |
| AGW-002 | DP-3 | DP | TLS 1.2+ enforced on listeners and policy | Must | Partial | SSL policy / listener protocol |
| AGW-003 | NS-1 | NS | Backend pool restricted to approved targets | Must | Partial | backend pools reference intended services only |
| AGW-004 | LT-3 | LT | Diagnostic and access logs enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| AGW-005 | IM-3 | IM | Certificates sourced from Key Vault | Must | Partial | Key Vault secret/certificate reference |
| AGW-006 | NS-2 | NS | Public frontend only when explicitly required | Should | Yes | public IP presence justified |

## Implementation Notes

- Use `WAF_v2` in prevention mode for public web entry points.
- Terminate TLS with modern policies and rotate certificates from Key Vault.
- Restrict backend membership and avoid mixing unrelated applications on one gateway.
- Export access, performance, and firewall logs to central monitoring.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Application Gateway security baseline
- AKS ingress guidance already referenced in this repo
