# Azure Container Registry — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Container Registry is the software supply-chain anchor for container images and artifacts. The baseline emphasizes private access, trusted pulls, image integrity, and logging.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ACR-001 | NS-2 | NS | Public network access disabled | Must | Yes | `public_network_access_enabled = false` |
| ACR-002 | IM-1 | IM | Admin user disabled | Must | Yes | `admin_enabled = false` |
| ACR-003 | NS-2 | NS | Private endpoint configured for production | Must | Partial | `azurerm_private_endpoint` |
| ACR-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| ACR-005 | PV-5 | PV | Image scanning / Defender enabled | Should | Partial | Defender for Containers / registry posture |
| ACR-006 | IM-3 | IM | Pull access via managed identity/RBAC | Must | Partial | AcrPull role assignments |

## Implementation Notes

- Disable the legacy admin account and move all consumers to Entra ID plus RBAC.
- Use private endpoints for production registries.
- Monitor push/pull/delete activity because registry compromise affects all dependent workloads.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Container Registry security baseline
