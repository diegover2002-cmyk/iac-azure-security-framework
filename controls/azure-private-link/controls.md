# Azure Private Link — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Private Link and private endpoints provide private access to PaaS services. The baseline concentrates on subnet placement, DNS correctness, and reduction of public data-plane exposure.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| PLS-001 | NS-2 | NS | Private endpoint used for sensitive PaaS services | Must | Partial | service-by-service linkage |
| PLS-002 | NS-1 | NS | Private endpoint subnet governed by NSG/policy as applicable | Must | Partial | subnet review |
| PLS-003 | NS-2 | NS | Public network access disabled on paired service where feasible | Must | Partial | paired service configuration |
| PLS-004 | LT-3 | LT | Private endpoint connection events monitored | Should | Partial | activity/diagnostic logs |
| PLS-005 | NS-1 | NS | Private DNS zones linked correctly | Must | Partial | zone group and VNet links |

## Implementation Notes

- Private Link is only effective if public access is also closed or tightly restricted.
- DNS is part of the control; incorrect resolution silently bypasses intended private routing.
- Keep endpoint sprawl under review to avoid unmanaged east-west trust paths.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Private Link security baseline
