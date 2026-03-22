# Azure Public IP — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Public IP resources are direct internet exposure indicators. The baseline is intentionally restrictive and treats public IP allocation as a reviewed exception.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| PIP-001 | NS-2 | NS | Public IP used only when justified | Must | Yes | resource presence review |
| PIP-002 | NS-3 | NS | Standard SKU required | Must | Yes | `sku = "Standard"` |
| PIP-003 | NS-1 | NS | Resource associated with protected ingress control | Must | Partial | linked LB/AppGW/Firewall/WAF |
| PIP-004 | LT-3 | LT | Changes and associations monitored | Must | Partial | activity logs |
| PIP-005 | PV-1 | PV | Idle/unattached public IPs removed | Should | Partial | inventory/governance |

## Implementation Notes

- A public IP should trigger a security review by default.
- Prefer Standard SKU and pair it with NSGs, Firewall, WAF, or Application Gateway as appropriate.
- Unattached public IPs are low-value assets with unnecessary attack surface.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure networking security baseline
