# Azure Load Balancer — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Load Balancer distributes Layer 4 traffic. The baseline focuses on limiting public exposure, constraining backend pools, and pairing with NSG controls.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ALB-001 | NS-2 | NS | Public load balancer used only when required | Must | Yes | public frontend config review |
| ALB-002 | NS-1 | NS | Backend pool limited to intended workloads | Must | Partial | backend pool membership |
| ALB-003 | NS-2 | NS | NSGs enforce inbound restrictions on backend subnets/NICs | Must | Partial | correlated network review |
| ALB-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | load balancer diagnostics |
| ALB-005 | NS-3 | NS | DDoS protection considered for public ingress VNets | Should | Partial | VNet-level control |

## Implementation Notes

- Treat public frontends as an explicit exception, not the default.
- Load Balancer is not a security boundary by itself; NSGs remain mandatory.
- Monitor health probe anomalies and frontend rule changes.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Load Balancer security baseline
