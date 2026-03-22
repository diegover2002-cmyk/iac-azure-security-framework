# Azure App Configuration — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure App Configuration stores application settings and feature flags. The primary security goals are restricting data-plane access, protecting secrets-by-reference patterns, and enabling auditability.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ACF-001 | NS-2 | NS | Public network access disabled | Must | Yes | `public_network_access` or equivalent private access pattern |
| ACF-002 | NS-2 | NS | Private endpoint configured | Must | Partial | `azurerm_private_endpoint` plus store linkage |
| ACF-003 | IM-1 | IM | Local auth disabled where supported | Should | Partial | disable access keys in favor of Entra ID and RBAC |
| ACF-004 | DP-5 | DP | Customer-managed key where required | Should | Partial | CMK configuration for regulated workloads |
| ACF-005 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| ACF-006 | IM-3 | IM | Key Vault references used for secrets | Must | Partial | no secret values stored directly in config |

## Control Detail Highlights

- `ACF-001`: Configuration stores should not remain broadly reachable from the internet when they hold application-critical settings.
- `ACF-002`: Private endpoints are the preferred production access path for internal applications and regulated workloads.
- `ACF-003`: Local or key-based access should be minimized so applications consume configuration through managed identity and RBAC.
- `ACF-004`: CMK is a conditional hardening control for workloads with stricter key ownership requirements.
- `ACF-005`: Request and audit logs should be exported because configuration changes often explain downstream application incidents.
- `ACF-006`: App Configuration should hold references to secrets, not the secrets themselves.

## Agent Notes

- Treat App Configuration and Key Vault as a paired pattern for secure settings and secret delivery.
- Review both data-plane exposure and application authentication model when documenting this service.
- Feature flags can materially alter application behavior; configuration changes should therefore be treated as security-relevant events.

## Suggested Validation Cases

- Secure: private endpoint, diagnostics enabled, managed identity consumers, Key Vault references for secret values.
- Insecure: public store access, local auth dependence, plaintext secrets or tokens stored as configuration values.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure App Configuration security baseline
- Existing repo patterns under `controls/azure-storage` and `controls/azure-key-vault`
