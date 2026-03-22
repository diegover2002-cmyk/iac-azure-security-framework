# Azure Private Link — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Private Link and private endpoints provide private access to PaaS services. The baseline concentrates on subnet placement, DNS correctness, and reduction of public data-plane exposure.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| PLS-001 | NS-2 | NS | Private endpoint used for sensitive PaaS services | Must | Partial | service-by-service linkage |
| PLS-002 | NS-1 | NS | Private endpoint subnet governed by NSG or policy as applicable | Must | Partial | subnet review |
| PLS-003 | NS-2 | NS | Public network access disabled on paired service where feasible | Must | Partial | paired service configuration |
| PLS-004 | LT-3 | LT | Private endpoint connection events monitored | Should | Partial | activity and diagnostic logs |
| PLS-005 | NS-1 | NS | Private DNS zones linked correctly | Must | Partial | zone group and VNet links |

## Control Detail Highlights

- `PLS-001`: Private endpoints should be the default pattern for sensitive PaaS services that would otherwise remain public.
- `PLS-002`: Endpoint subnets still need governance. Treat them as part of the network security model, not as invisible plumbing.
- `PLS-003`: Private Link is incomplete if the paired service still accepts broad public access without restriction.
- `PLS-004`: Connection approvals, rejections, and lifecycle events should be visible in logs to support change review and troubleshooting.
- `PLS-005`: DNS is part of the control. Incorrect zone linkage causes silent drift back to public routing.

## Agent Notes

- Private Link is a correlated control spanning the endpoint, the target service, DNS, and the consumer network.
- When documenting a private-link pattern, include the DNS dependency in the same baseline narrative.
- Watch for endpoint sprawl that creates unmanaged trust paths between application segments.

## Suggested Validation Cases

- Secure: private endpoint plus public access reduction, correct private DNS linkage, monitored connection lifecycle.
- Insecure: endpoint created but service remains public, no DNS linkage, unmanaged endpoint subnet.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Private Link security baseline
