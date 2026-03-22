# Azure Bastion — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Bastion provides managed RDP/SSH access to virtual machines. The baseline centers on replacing direct management exposure, enforcing segmentation, and preserving session visibility.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| BAS-001 | NS-2 | NS | Bastion used instead of public RDP/SSH on VMs | Must | Partial | correlated VM/public IP review |
| BAS-002 | NS-1 | NS | Dedicated `AzureBastionSubnet` with correct sizing | Must | Yes | subnet naming and CIDR |
| BAS-003 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| BAS-004 | IM-1 | IM | Access governed by RBAC/PIM | Must | Partial | role assignments outside resource code path |
| BAS-005 | NS-2 | NS | Standard SKU used for production | Should | Yes | `sku = "Standard"` |

## Implementation Notes

- Remove direct internet exposure for administrative ports when Bastion is present.
- Keep Bastion isolated in its dedicated subnet and monitor session activity.
- Pair with JIT or PIM-based privileged workflows where applicable.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Bastion security baseline
