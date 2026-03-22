# Azure Service Bus — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Service Bus brokers queues and topics that often carry business-critical messages. The baseline focuses on network isolation, RBAC over shared keys, encryption, and diagnostic visibility.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ASB-001 | NS-2 | NS | Public network access disabled or restricted | Must | Yes | namespace network settings |
| ASB-002 | NS-2 | NS | Private endpoint configured for production | Must | Partial | `azurerm_private_endpoint` |
| ASB-003 | IM-1 | IM | RBAC preferred over long-lived SAS keys | Must | Partial | auth rule review |
| ASB-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | namespace diagnostics |
| ASB-005 | DP-5 | DP | Customer-managed keys where required | Should | Partial | CMK configuration |
| ASB-006 | DP-8 | DP | Geo-disaster recovery or resilience pattern defined | Should | Partial | alias/replication strategy |

## Implementation Notes

- Review SAS policies carefully because they are shared credentials with broad blast radius.
- Use private endpoints for internal integration fabrics.
- Log send/receive/auth errors and administrative changes.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Service Bus security baseline
