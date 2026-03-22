# Azure DNS — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure DNS provides public and private name resolution. The main security goals are change control, least privilege over zones, and protection of records that steer traffic.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| DNS-001 | IM-1 | IM | Zone management restricted with RBAC | Must | Partial | role assignments |
| DNS-002 | LT-3 | LT | Activity logging enabled and retained | Must | Partial | subscription/activity log coverage |
| DNS-003 | NS-1 | NS | Private DNS used for private endpoint resolution | Should | Partial | private DNS zone linkage |
| DNS-004 | DP-3 | DP | DNSSEC or equivalent integrity protection where available | Should | Partial | service capability dependent |
| DNS-005 | PV-1 | PV | Critical public records protected by change review | Must | No | workflow/evidence control |

## Implementation Notes

- DNS records are security-sensitive because they redirect client traffic.
- Separate public and private DNS responsibilities and permissions.
- Use IaC plus review gates for high-impact records such as MX, TXT, CNAME, and apex A records.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure DNS security baseline
