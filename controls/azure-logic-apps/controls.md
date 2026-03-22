# Azure Logic Apps — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Logic Apps automates integrations and often handles credentials and business data flows. The baseline prioritizes managed identity, connector secret protection, and network restriction where supported.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| LGA-001 | IM-1 | IM | Managed identity enabled | Must | Yes | identity block present |
| LGA-002 | IM-3 | IM | Connector secrets stored in Key Vault | Must | Partial | secure parameter references |
| LGA-003 | NS-2 | NS | Standard Logic Apps use private networking where required | Should | Partial | App Service or VNet pattern |
| LGA-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | workflow diagnostics |
| LGA-005 | DP-3 | DP | Secure transport to downstream systems | Must | Partial | connector and endpoint review |

## Control Detail Highlights

- `LGA-001`: Managed identity should be the default for connectors and downstream Azure access.
- `LGA-002`: Workflow definitions and parameters should not carry plaintext connector credentials.
- `LGA-003`: Standard Logic Apps should use stronger network controls when the workflow handles sensitive systems or data.
- `LGA-004`: Workflow runs, trigger history, and failures should be logged because Logic Apps often orchestrate privileged operations.
- `LGA-005`: Downstream endpoints and connectors must maintain encrypted transport and approved trust boundaries.

## Agent Notes

- Logic Apps are integration control planes and should be treated like privileged automation, not just business workflow glue.
- Review both the workflow definition and the connectors it uses; the connector surface is often the real risk.
- Standard and Consumption models have different network-control options, so document which model is assumed.

## Suggested Validation Cases

- Secure: managed identity, Key Vault-backed secrets, diagnostics enabled, private networking where needed.
- Insecure: embedded connector credentials, opaque downstream endpoints, no run-history telemetry.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Logic Apps security baseline
