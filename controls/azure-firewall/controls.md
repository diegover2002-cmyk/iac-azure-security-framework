# Azure Firewall — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Firewall is a central network security control enforcing egress and ingress policy. The baseline focuses on deny-by-default policy, logging, segmentation, and centralized rule management.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| AFW-001 | NS-2 | NS | Firewall policy used instead of ad hoc local rules | Must | Yes | `firewall_policy_id` |
| AFW-002 | NS-1 | NS | Rule collections follow deny-by-default model | Must | Partial | policy review |
| AFW-003 | LT-3 | LT | Application, network, and threat logs enabled | Must | Partial | diagnostics |
| AFW-004 | NS-3 | NS | Threat intelligence mode enabled | Should | Yes | `threat_intel_mode` |
| AFW-005 | NS-2 | NS | Forced tunneling / egress inspection used where required | Should | Partial | topology-specific |
| AFW-006 | PV-1 | PV | Premium TLS inspection considered for high-risk workloads | Should | Partial | SKU and policy capabilities |

## Implementation Notes

- Keep rule management centralized through Firewall Policy.
- Export all log categories because Azure Firewall is often the main evidence source for network investigations.
- Review wide any-any allows as structural exceptions, not normal rules.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Firewall security baseline
