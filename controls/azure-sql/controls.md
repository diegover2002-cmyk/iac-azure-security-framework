# Azure SQL Database — Security Controls

> **MCSB Mapping** | **Severity:** 4 High / 5 Medium / 0 Low
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Controls Summary

| Control ID | MCSB | Domain | Control Name | Severity | Priority | IaC Checkable | Checkov Rule |
|---|---|---|---|---|---|---|---|
| SQ-001 | NS-1 | NS | Virtual network integration | Medium | Should | Partial | Custom |
| SQ-002 | NS-2 | NS | Private Link enabled | High | Must | Partial | Custom |
| SQ-003 | IM-1 | IM | Entra ID authentication for data plane | High | Must | Partial | Custom |
| SQ-004 | IM-7 | IM | Conditional access for data plane | Medium | Should | No | Manual evidence |
| SQ-005 | DP-3 | DP | Encryption in transit | High | Must | No | Platform / client standard |
| SQ-006 | DP-4 | DP | Encryption at rest with platform keys | Medium | Must | No | Platform-managed |
| SQ-007 | DP-5 | DP | Customer-managed keys for TDE | Medium | Should | Partial | Custom |
| SQ-008 | LT-1 | LT | Defender for Azure SQL enabled | Medium | Should | Partial | Defender plan |
| SQ-009 | LT-4 | LT | Resource and audit logging enabled | High | Must | Partial | Diagnostic settings + auditing |

---

## SQ-001 — Virtual Network Integration

| Field | Detail |
|---|---|
| **MCSB** | NS-1 — Establish network segmentation boundaries |
| **Severity** | Medium |
| **Priority** | Should |
| **Applies** | Conditional — required for internal application data paths |
| **Justification** | SQL data access should traverse private, governed network paths whenever the workload is not intended for broad internet access |
| **Checkov** | Custom — assert server and database access patterns are paired with private connectivity design |

```hcl
resource "azurerm_mssql_virtual_network_rule" "sql_vnet" {
  name      = "sql-vnet-rule"
  server_id = azurerm_mssql_server.sql.id
  subnet_id = azurerm_subnet.data.id
}
```

---

## SQ-002 — Private Link Enabled

| Field | Detail |
|---|---|
| **MCSB** | NS-2 — Secure cloud services with network controls |
| **Severity** | High |
| **Priority** | Must |
| **Applies** | Yes — production SQL servers and sensitive workloads |
| **Justification** | Private Link removes dependence on publicly reachable SQL endpoints and aligns data-plane access to enterprise private networking |
| **Checkov** | Custom — assert `azurerm_private_endpoint` targets the SQL server |

```hcl
resource "azurerm_private_endpoint" "sql_pe" {
  name                = "pe-sql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.private.id

  private_service_connection {
    name                           = "psc-sql"
    private_connection_resource_id = azurerm_mssql_server.sql.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }
}
```

---

## SQ-003 — Entra ID Authentication For Data Plane

| Field | Detail |
|---|---|
| **MCSB** | IM-1 — Use centralized identity and authentication system |
| **Severity** | High |
| **Priority** | Must |
| **Applies** | Yes — all enterprise SQL estates |
| **Justification** | Centralized identity reduces SQL login sprawl, supports MFA and Conditional Access, and improves auditability |
| **Checkov** | Custom — assert SQL server has Entra administrator configured |

```hcl
resource "azurerm_mssql_server" "sql" {
  name                         = "sql-example"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "localadmin"
  administrator_login_password = var.sql_admin_password

  azuread_administrator {
    login_username = "sql-admins"
    object_id      = var.sql_admin_group_object_id
  }
}
```

---

## SQ-004 — Conditional Access For Data Plane

| Field | Detail |
|---|---|
| **MCSB** | IM-7 — Restrict access to resources based on conditions |
| **Severity** | Medium |
| **Priority** | Should |
| **Applies** | Conditional — where user access to SQL is performed through Entra ID |
| **Justification** | Database access should be constrained by user risk, trusted location, and device posture when interactive access is permitted |
| **Checkov** | No — policy and identity evidence review |

> Validate through Entra Conditional Access policy evidence rather than Terraform alone.

---

## SQ-005 — Encryption In Transit

| Field | Detail |
|---|---|
| **MCSB** | DP-3 — Encrypt data in transit |
| **Severity** | High |
| **Priority** | Must |
| **Applies** | Yes |
| **Justification** | SQL traffic often carries regulated and business-critical data that must not transit in clear text |
| **Checkov** | No — platform plus client configuration standard |

> Treat encrypted SQL connections as mandatory in application standards and connection policy.

---

## SQ-006 — Encryption At Rest With Platform Keys

| Field | Detail |
|---|---|
| **MCSB** | DP-4 — Enable data at rest encryption by default |
| **Severity** | Medium |
| **Priority** | Must |
| **Applies** | Yes |
| **Justification** | Azure SQL encrypts data at rest by default and this inherited control must remain documented in the baseline |
| **Checkov** | No — platform-managed |

---

## SQ-007 — Customer-Managed Keys For TDE

| Field | Detail |
|---|---|
| **MCSB** | DP-5 — Use customer-managed key option when required |
| **Severity** | Medium |
| **Priority** | Should |
| **Applies** | Conditional — regulated or specially classified databases |
| **Justification** | Some workloads require customer ownership of encryption keys and revocation lifecycle |
| **Checkov** | Custom — assert transparent data encryption protector uses Key Vault key |

```hcl
resource "azurerm_mssql_server_transparent_data_encryption" "sql_tde" {
  server_id        = azurerm_mssql_server.sql.id
  key_vault_key_id = azurerm_key_vault_key.sql_tde.id
}
```

---

## SQ-008 — Defender For Azure SQL Enabled

| Field | Detail |
|---|---|
| **MCSB** | LT-1 — Enable threat detection capabilities |
| **Severity** | Medium |
| **Priority** | Should |
| **Applies** | Yes — production subscriptions |
| **Justification** | Defender adds anomalous activity detection, vulnerability insight, and attack telemetry for database workloads |
| **Checkov** | Partial — subscription/service configuration evidence |

---

## SQ-009 — Resource And Audit Logging Enabled

| Field | Detail |
|---|---|
| **MCSB** | LT-4 — Enable logging for security investigation |
| **Severity** | High |
| **Priority** | Must |
| **Applies** | Yes |
| **Justification** | Audit trails are required for privileged access review, incident investigation, and regulated retention |
| **Checkov** | Partial — diagnostic settings and auditing configuration |

```hcl
resource "azurerm_monitor_diagnostic_setting" "sql_diag" {
  name                       = "diag-sql"
  target_resource_id         = azurerm_mssql_server.sql.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_log { category = "SQLSecurityAuditEvents" }
  enabled_log { category = "DevOpsOperationsAudit" }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
```

---

## Secure Azure SQL — Full Reference

```hcl
resource "azurerm_mssql_server" "compliant" {
  name                         = "sql-compliant"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "localadmin"
  administrator_login_password = var.sql_admin_password

  azuread_administrator {
    login_username = "sql-admins"
    object_id      = var.sql_admin_group_object_id
  }
}

resource "azurerm_private_endpoint" "sql" {
  name                = "pe-sql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.private.id

  private_service_connection {
    name                           = "psc-sql"
    private_connection_resource_id = azurerm_mssql_server.compliant.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }
}
```
