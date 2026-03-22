# Azure Functions — Security Controls

> **MCSB Mapping** | **Severity:** 4 High / 3 Medium / 0 Low
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Controls Summary

| Control ID | MCSB | Domain | Control Name | Severity | Priority | IaC Checkable | Checkov Rule |
|---|---|---|---|---|---|---|---|
| FN-001 | NS-1 | NS | VNet integration | Medium | Should | Partial | Custom |
| FN-002 | NS-2 | NS | Private Link enabled | Medium | Should | Partial | Custom |
| FN-003 | IM-1 | IM | Entra ID authentication for endpoints and deployment access | High | Must | Partial | Custom |
| FN-004 | IM-3 | IM | Managed identity enabled | High | Must | Yes | Function app identity |
| FN-005 | DP-3 | DP | HTTPS only and minimum TLS 1.2 | High | Must | Yes | Site config |
| FN-006 | LT-1 | LT | Defender for App Service enabled | Medium | Should | Partial | Defender plan |
| FN-007 | LT-4 | LT | Resource logging enabled | High | Must | Partial | Diagnostic settings |

---

## Secure Azure Functions — Full Reference

```hcl
resource "azurerm_windows_function_app" "compliant" {
  name                = "func-compliant"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.func.name
  storage_account_access_key = azurerm_storage_account.func.primary_access_key

  https_only = true

  identity {
    type = "SystemAssigned"
  }

  site_config {
    minimum_tls_version = "1.2"
  }
}

resource "azurerm_monitor_diagnostic_setting" "func_diag" {
  name                       = "diag-func"
  target_resource_id         = azurerm_windows_function_app.compliant.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_log { category = "FunctionAppLogs" }
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
```

Use VNet integration and Private Link when the function app depends on private services or should not expose public ingress. Restrict deployment access to centrally governed identity.
