# Azure Event Hubs — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Event Hubs is a high-throughput ingestion service. The baseline emphasizes private networking, identity-based access, encryption, and activity logging.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| EVH-001 | NS-2 | NS | Public network access disabled or restricted | Must | Yes | namespace network settings |
| EVH-002 | NS-2 | NS | Private endpoint configured for production | Must | Partial | `azurerm_private_endpoint` |
| EVH-003 | IM-1 | IM | Local/SAS auth minimized in favor of RBAC | Must | Partial | authorization rule review |
| EVH-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | namespace/hub diagnostics |
| EVH-005 | DP-5 | DP | Customer-managed keys where required | Should | Partial | CMK configuration |
| EVH-006 | DP-8 | DP | Capture/retention configured for recovery requirements | Should | Partial | capture settings |

## Implementation Notes

- Prefer Entra ID and RBAC for producers and consumers.
- Use private endpoints for critical telemetry pipelines.
- Audit authorization rules because SAS keys can become long-lived shared secrets.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Event Hubs security baseline
