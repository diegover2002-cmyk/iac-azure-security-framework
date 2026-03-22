# Azure Service Bus — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
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
| ASB-006 | DP-8 | DP | Geo-disaster recovery or resilience pattern defined | Should | Partial | alias or replication strategy |

## Control Detail Highlights

- `ASB-001`: Messaging namespaces should not be left broadly public when they carry internal or regulated message flows.
- `ASB-002`: Private endpoints are the preferred production access pattern for internal messaging fabrics.
- `ASB-003`: SAS rules are shared credentials with broad blast radius and should be minimized in favor of identity-based access.
- `ASB-004`: Diagnostic logs should capture authentication failures, namespace operations, and message-plane issues relevant to investigation.
- `ASB-005`: CMK remains a conditional control for workloads with stronger encryption governance requirements.
- `ASB-006`: Messaging resilience should be explicit. Recovery aliasing, failover strategy, or equivalent design should not be left implicit.

## Agent Notes

- Review Service Bus together with sender and receiver authentication patterns.
- Namespace auth rules and queue or topic ownership boundaries are part of the security baseline.
- For critical workflows, resilience and security controls interact closely because message loss and compromise can have similar business impact.

## Suggested Validation Cases

- Secure: restricted network path, private endpoints, RBAC-first auth model, diagnostics enabled, resilience design documented.
- Insecure: open namespace, unmanaged SAS proliferation, no logging, no defined failover pattern.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Service Bus security baseline
