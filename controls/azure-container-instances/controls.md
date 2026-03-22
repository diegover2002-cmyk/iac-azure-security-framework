# Azure Container Instances — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Container Instances provides lightweight container execution. The main risks are uncontrolled public exposure, weak secret handling, and ungoverned image sources.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ACI-001 | NS-2 | NS | Public IP disabled unless required | Must | Yes | `ip_address_type` / network profile |
| ACI-002 | IM-1 | IM | Managed identity enabled where supported | Should | Partial | identity configuration |
| ACI-003 | IM-3 | IM | Registry credentials not embedded in code | Must | Partial | secure image pull secret pattern |
| ACI-004 | PV-5 | PV | Images pulled from approved registry | Must | Partial | ACR or trusted registry only |
| ACI-005 | LT-3 | LT | Logs exported to centralized monitoring | Must | Partial | diagnostics / workspace linkage |

## Implementation Notes

- Avoid using ACI for long-lived sensitive workloads without strong network boundaries.
- Prefer private image registries and short-lived credentials.
- Route stdout/stderr and control-plane events to Log Analytics.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Container Instances security baseline
