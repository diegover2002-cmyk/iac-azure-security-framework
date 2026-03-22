# Azure API Management — Security Controls

> **MCSB Mapping** | **Severity:** 4 High / 6 Medium / 0 Low
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Controls Summary

| Control ID | MCSB | Domain | Control Name | Severity | Priority | IaC Checkable | Checkov Rule |
|---|---|---|---|---|---|---|---|
| AP-001 | NS-1 | NS | VNet integration | Medium | Should | Partial | Custom |
| AP-002 | NS-2 | NS | Private Link enabled | Medium | Should | Partial | Custom |
| AP-003 | NS-2 | NS | Public network access disabled or restricted | High | Must | Partial | Custom |
| AP-004 | IM-1 | IM | Entra ID authentication | Medium | Should | Partial | Custom |
| AP-005 | PA-1 | PA | Local accounts restricted | Medium | Should | No | Manual evidence |
| AP-006 | DP-3 | DP | Encrypted protocols only | High | Must | Partial | Gateway config |
| AP-007 | DP-4 | DP | Encryption at rest with platform keys | Medium | Must | No | Platform-managed |
| AP-008 | DP-6 | DP | Key Vault integration for secrets and certificates | High | Must | Partial | Custom |
| AP-009 | LT-1 | LT | Defender for APIs enabled | Medium | Should | Partial | Defender plan |
| AP-010 | LT-4 | LT | Resource logging enabled | High | Must | Partial | Diagnostic settings |

---

## Implementation Notes

`AP-003`, `AP-006`, `AP-008`, and `AP-010` are the operational minimum for public API exposure.

```hcl
resource "azurerm_api_management" "compliant" {
  name                = "apim-compliant"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  publisher_name      = "Security Team"
  publisher_email     = "security@example.com"
  sku_name            = "Premium_1"

  public_network_access_enabled = false

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_monitor_diagnostic_setting" "apim_diag" {
  name                       = "diag-apim"
  target_resource_id         = azurerm_api_management.compliant.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_log { category = "GatewayLogs" }
  enabled_log { category = "WebSocketConnectionLogs" }
}
```

Use Key Vault for certificates, named values, and other sensitive APIM material. Avoid local account dependency except for controlled break-glass scenarios.
