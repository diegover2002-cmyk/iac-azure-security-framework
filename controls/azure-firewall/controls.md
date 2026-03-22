# Azure Firewall — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
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
| AFW-005 | NS-2 | NS | Forced tunneling or egress inspection used where required | Should | Partial | topology-specific |
| AFW-006 | PV-1 | PV | Premium TLS inspection considered for high-risk workloads | Should | Partial | SKU and policy capabilities |

## Control Detail Highlights

- `AFW-001`: Centralized Firewall Policy keeps rule logic portable, reviewable, and consistent across hubs and landing zones.
- `AFW-002`: The effective model should be explicit allow with deny by default. Broad any-any rules should be treated as structural exceptions.
- `AFW-003`: Azure Firewall is often the main evidence source for network investigation, so logging gaps undermine both security and troubleshooting.
- `AFW-004`: Threat intelligence mode should be enabled to add platform-backed detection and blocking where the risk profile justifies it.
- `AFW-005`: Egress-sensitive environments should not assume inbound filtering is enough. Outbound routing and inspection are often the real control objective.
- `AFW-006`: Premium features such as TLS inspection should be evaluated for internet egress or regulated workloads where encrypted traffic visibility matters.

## Agent Notes

- Evaluate Azure Firewall together with route tables, hub-spoke topology, and the workloads whose traffic should traverse it.
- A firewall deployment without deterministic routing is not an effective control.
- Prefer one centralized policy model over resource-local rule drift.

## Suggested Validation Cases

- Secure: shared Firewall Policy, diagnostics enabled, no broad allow-any collections, routing forces intended traffic through the firewall.
- Insecure: local unmanaged rules, no logs, public egress paths bypassing the firewall entirely.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Firewall security baseline
