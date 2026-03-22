# Azure Cosmos DB — Security Controls

> **MCSB Mapping** | **Severity:** 4 High / 6 Medium / 0 Low
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Controls Summary

| Control ID | MCSB | Domain | Control Name | Severity | Priority | IaC Checkable | Checkov Rule |
|---|---|---|---|---|---|---|---|
| CO-001 | NS-1 | NS | Virtual network integration | Medium | Should | Partial | Custom |
| CO-002 | NS-2 | NS | Private Link enabled | High | Must | Partial | Custom |
| CO-003 | IM-1 | IM | Entra ID authentication for data plane | High | Must | Partial | Custom |
| CO-004 | IM-3 | IM | Managed identities for application access | Medium | Should | Partial | Custom |
| CO-005 | PA-7 | PA | Data plane RBAC enabled | High | Must | Partial | Custom |
| CO-006 | DP-3 | DP | Encryption in transit | High | Must | No | Platform / client standard |
| CO-007 | DP-4 | DP | Encryption at rest with platform keys | Medium | Must | No | Platform-managed |
| CO-008 | DP-5 | DP | Customer-managed keys when required | Medium | Should | Partial | Custom |
| CO-009 | LT-1 | LT | Defender for Azure Cosmos DB enabled | Medium | Should | Partial | Defender plan |
| CO-010 | LT-4 | LT | Resource logging enabled | High | Must | Partial | Diagnostic settings |

---

## CO-001 — Virtual Network Integration

Use VNet-restricted access patterns for internal workloads to reduce unnecessary public reachability.

## CO-002 — Private Link Enabled

Use private endpoints for production Cosmos DB accounts and keep name resolution aligned with private access.

## CO-003 — Entra ID Authentication For Data Plane

Prefer Entra ID and supported data-plane RBAC instead of key-only authentication models.

## CO-004 — Managed Identities For Application Access

Azure-hosted workloads should consume Cosmos DB through managed identity where the API and access pattern support it.

## CO-005 — Data Plane RBAC Enabled

Least privilege is required for applications and operators; avoid broad key distribution at account scope.

## CO-006 — Encryption In Transit

Treat TLS-secured transport as mandatory in client standards.

## CO-007 — Encryption At Rest With Platform Keys

Document platform encryption as inherited baseline.

## CO-008 — Customer-Managed Keys When Required

Use Key Vault-backed CMK for regulated or specially classified workloads.

## CO-009 — Defender For Azure Cosmos DB Enabled

Enable Defender in production subscriptions to improve anomaly and threat visibility.

## CO-010 — Resource Logging Enabled

```hcl
resource "azurerm_monitor_diagnostic_setting" "cosmos_diag" {
  name                       = "diag-cosmos"
  target_resource_id         = azurerm_cosmosdb_account.cosmos.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_log { category = "DataPlaneRequests" }
  enabled_log { category = "MongoRequests" }
  enabled_log { category = "QueryRuntimeStatistics" }
}
```

---

## Secure Azure Cosmos DB — Full Reference

```hcl
resource "azurerm_cosmosdb_account" "compliant" {
  name                = "cosmos-compliant"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  public_network_access_enabled = false
  local_authentication_disabled = true
}
```
