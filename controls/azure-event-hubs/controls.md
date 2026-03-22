# Azure Event Hubs — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Event Hubs is a high-throughput ingestion service. The baseline emphasizes private networking, identity-based access, encryption, and activity logging.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| EVH-001 | NS-2 | NS | Public network access disabled or restricted | Must | Yes | namespace network settings |
| EVH-002 | NS-2 | NS | Private endpoint configured for production | Must | Partial | `azurerm_private_endpoint` |
| EVH-003 | IM-1 | IM | Local or SAS auth minimized in favor of RBAC | Must | Partial | authorization rule review |
| EVH-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | namespace or hub diagnostics |
| EVH-005 | DP-5 | DP | Customer-managed keys where required | Should | Partial | CMK configuration |
| EVH-006 | DP-8 | DP | Capture or retention configured for recovery requirements | Should | Partial | capture settings |

## Control Detail Highlights

- `EVH-001`: Event Hubs namespaces should not remain broadly public unless the architecture explicitly requires it.
- `EVH-002`: Private endpoints are the preferred production path for ingestion services carrying internal telemetry or business events.
- `EVH-003`: SAS rules are convenient but become long-lived shared credentials. Prefer Entra ID and RBAC where supported.
- `EVH-004`: Namespace activity and diagnostics are required to investigate delivery issues, abuse, and administrative changes.
- `EVH-005`: CMK is a conditional control for workloads that need stronger customer control over encryption material.
- `EVH-006`: Capture and retention settings should align with operational recovery and incident evidence requirements.

## Agent Notes

- Review Event Hubs together with producer and consumer authentication design.
- Namespace authorization rules should be treated as high-risk objects because they can grant broad send or listen capability.
- If Event Hubs is part of the security telemetry path, diagnostics and resilience controls become more important, not less.

## Suggested Validation Cases

- Secure: restricted network access, private endpoints, RBAC-first auth, diagnostics enabled.
- Insecure: broad public access, unmanaged SAS use, no visibility into namespace activity.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Event Hubs security baseline
