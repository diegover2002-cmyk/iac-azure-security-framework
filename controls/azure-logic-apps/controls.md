# Azure Logic Apps — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Logic Apps automates integrations and often handles credentials and business data flows. The baseline prioritizes managed identity, connector secret protection, and network restriction where supported.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| LGA-001 | IM-1 | IM | Managed identity enabled | Must | Yes | identity block present |
| LGA-002 | IM-3 | IM | Connector secrets stored in Key Vault | Must | Partial | secure parameter references |
| LGA-003 | NS-2 | NS | Standard Logic Apps use private networking where required | Should | Partial | App Service/VNet pattern |
| LGA-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | workflow diagnostics |
| LGA-005 | DP-3 | DP | Secure transport to downstream systems | Must | Partial | connector and endpoint review |

## Implementation Notes

- Prefer Standard plan for stronger network control when workflows process sensitive data.
- Avoid embedding connector credentials in definitions or parameters.
- Log workflow runs, trigger history, and failures for forensics.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Logic Apps security baseline
