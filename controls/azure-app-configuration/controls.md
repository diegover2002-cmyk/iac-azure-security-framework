# Azure App Configuration — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure App Configuration stores application settings and feature flags. The primary security goals are restricting data-plane access, protecting secrets-by-reference patterns, and enabling auditability.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ACF-001 | NS-2 | NS | Public network access disabled | Must | Yes | `public_network_access` / private access pattern |
| ACF-002 | NS-2 | NS | Private endpoint configured | Must | Partial | `azurerm_private_endpoint` + store linkage |
| ACF-003 | IM-1 | IM | Local auth disabled where supported | Should | Partial | disable access keys in favor of Entra ID/RBAC |
| ACF-004 | DP-5 | DP | Customer-managed key where required | Should | Partial | CMK configuration for regulated workloads |
| ACF-005 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| ACF-006 | IM-3 | IM | Key Vault references for secrets | Must | Partial | no secret values stored directly in config |

## Implementation Notes

- Prefer private endpoints for production App Configuration stores.
- Use Azure RBAC and managed identities for applications reading configuration.
- Keep secrets in Key Vault; App Configuration should hold references, not plaintext secrets.
- Send audit and request logs to Log Analytics.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure App Configuration security baseline
- Existing repo patterns under `controls/azure-storage` and `controls/azure-key-vault`
