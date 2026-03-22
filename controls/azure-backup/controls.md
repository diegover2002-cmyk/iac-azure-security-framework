# Azure Backup — Security Controls

> **MCSB Mapping** | **Severity:** 4 High / 5 Medium / 0 Low
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Controls Summary

| Control ID | MCSB | Domain | Control Name | Severity | Priority | IaC Checkable | Checkov Rule |
|---|---|---|---|---|---|---|---|
| BK-001 | NS-2 | NS | Private Link enabled | Medium | Should | Partial | Custom |
| BK-002 | NS-2 | NS | Public network access disabled | High | Must | Partial | Custom |
| BK-003 | IM-8 | IM | Key Vault for credentials and secret storage | Medium | Should | Partial | Custom |
| BK-004 | DP-2 | DP | Immutable and anti-deletion protections | High | Must | Partial | Vault config |
| BK-005 | DP-3 | DP | Encryption in transit | High | Must | No | Platform-managed |
| BK-006 | DP-4 | DP | Encryption at rest with platform keys | Medium | Must | No | Platform-managed |
| BK-007 | DP-5 | DP | Customer-managed keys when required | Medium | Should | Partial | Custom |
| BK-008 | DP-6 | DP | Key lifecycle in Key Vault | Medium | Should | Partial | Process / custom |
| BK-009 | BR-1 | BR | Automated backup protection enabled | High | Must | Partial | Policy + protected items |

---

## Implementation Notes

Azure Backup must be treated as ransomware-resilience infrastructure, not only as an operational recovery service.

```hcl
resource "azurerm_recovery_services_vault" "compliant" {
  name                = "rsv-compliant"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
  soft_delete_enabled = true
}
```

Baseline expectations:

- use Private Link for vault access in production environments with private networking standards;
- enable soft delete, immutability, and anti-deletion protections where supported;
- manage CMK material in Key Vault when customer-managed encryption is required;
- ensure protected items are actually onboarded and bound to approved backup policy.
