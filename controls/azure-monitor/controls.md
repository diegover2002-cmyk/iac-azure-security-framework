# Azure Monitor — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Monitor, Log Analytics, and related workspaces collect operational and security telemetry. The baseline focuses on data retention, private ingestion where needed, and access governance.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| MON-001 | LT-3 | LT | Central Log Analytics workspace configured | Must | Partial | workspace association |
| MON-002 | IM-1 | IM | Workspace access restricted with RBAC | Must | Partial | role assignments |
| MON-003 | NS-2 | NS | Private Link used for sensitive telemetry ingestion or query | Should | Partial | AMPLS or private endpoint |
| MON-004 | LT-4 | LT | Retention aligned to incident response requirements | Must | Yes | retention configuration |
| MON-005 | DP-2 | DP | Sensitive logs protected and export controlled | Must | Partial | export rules and destination review |
| MON-006 | PV-1 | PV | Alerting enabled for critical posture signals | Should | Partial | alerts, workbooks, or rules |

## Control Detail Highlights

- `MON-001`: A central workspace pattern reduces telemetry fragmentation and makes cross-service investigation more reliable.
- `MON-002`: Workspace permissions should separate readers, operators, and contributors to avoid unnecessary access to sensitive log data.
- `MON-003`: Sensitive telemetry paths may require private ingestion or query access rather than broad public endpoints.
- `MON-004`: Retention should align to real incident response and audit needs, not arbitrary defaults.
- `MON-005`: Log export paths are security-sensitive because they can leak data or create secondary storage surfaces.
- `MON-006`: Alerts and posture signals should be wired for actual response rather than treated as passive dashboards.

## Agent Notes

- Logging is a dependency for most other controls in this repository, so Monitor is foundational rather than optional.
- Review workspace RBAC and export destinations whenever sensitive logs are present.
- If data is exported, document where it goes and who can read it.

## Suggested Validation Cases

- Secure: central workspace, controlled RBAC, retention defined, export paths reviewed, critical alerts configured.
- Insecure: fragmented workspaces, overly broad reader access, short retention, uncontrolled log exports.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Monitor and Log Analytics security baseline
