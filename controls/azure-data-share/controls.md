# Azure Data Share — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Data Share governs cross-subscription and cross-tenant sharing of data assets. The baseline is centered on outbound sharing control, tenant boundaries, and traceability.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ADS-001 | NS-1 | NS | Cross-tenant sharing limited to approved scenarios | Must | Partial | business approval + config review |
| ADS-002 | IM-1 | IM | Access governed by RBAC | Must | Partial | role assignments |
| ADS-003 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | share account diagnostics |
| ADS-004 | DP-2 | DP | Shared datasets classified before publication | Must | No | process/evidence control |
| ADS-005 | DP-8 | DP | Revocation process defined for active shares | Should | No | operational control |

## Implementation Notes

- Use Data Share only with explicit data owner approval.
- Keep sharing relationships documented, especially when crossing tenant boundaries.
- Log invitations, share activity, and revocation events for audit.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Data Share security baseline
