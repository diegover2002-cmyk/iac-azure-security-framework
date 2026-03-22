# Azure Monitor — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Monitor, Log Analytics, and related workspaces collect operational and security telemetry. The baseline focuses on data retention, private ingestion where needed, and access governance.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| MON-001 | LT-3 | LT | Central Log Analytics workspace configured | Must | Partial | workspace association |
| MON-002 | IM-1 | IM | Workspace access restricted with RBAC | Must | Partial | role assignments |
| MON-003 | NS-2 | NS | Private Link used for sensitive telemetry ingestion/query | Should | Partial | AMPLS/private endpoint |
| MON-004 | LT-4 | LT | Retention aligned to incident response requirements | Must | Yes | retention configuration |
| MON-005 | DP-2 | DP | Sensitive logs protected and export controlled | Must | Partial | export rules and destination review |
| MON-006 | PV-1 | PV | Alerting enabled for critical posture signals | Should | Partial | alerts/workbooks/rules |

## Implementation Notes

- Logging is a dependency for most other controls in this repo.
- Separate readers, operators, and contributors through RBAC.
- Review diagnostic export paths because they can become data exfiltration channels.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Monitor / Log Analytics security baseline
