# Azure Data Factory — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Data Factory orchestrates data movement and transformation. Its baseline focuses on managed identities, linked-service secret protection, private integration runtimes, and audit logging.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ADF-001 | IM-1 | IM | Managed identity enabled | Must | Yes | identity block present |
| ADF-002 | IM-3 | IM | Linked service secrets stored in Key Vault | Must | Partial | Key Vault reference instead of plaintext |
| ADF-003 | NS-2 | NS | Managed virtual network / private endpoints used where needed | Must | Partial | private connectivity pattern |
| ADF-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | factory diagnostics |
| ADF-005 | DP-3 | DP | Secure transport to sources and sinks | Must | Partial | connector configuration review |
| ADF-006 | PV-1 | PV | Defender recommendations monitored | Should | Partial | Defender posture evidence |

## Implementation Notes

- Treat linked services as a high-risk area because they often carry credentials to downstream systems.
- Prefer managed VNet and private endpoints for internal data movement.
- Capture pipeline runs, activity runs, and integration runtime telemetry centrally.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Data Factory security baseline
