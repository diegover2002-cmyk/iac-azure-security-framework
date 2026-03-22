# Azure Web Application Firewall — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

This document covers Azure WAF deployments attached to Application Gateway or Front Door. The baseline concentrates on prevention mode, managed rule sets, logging, and exception governance.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| WAF-001 | NS-2 | NS | WAF enabled in prevention mode for production | Must | Yes | `firewall_mode = "Prevention"` |
| WAF-002 | NS-2 | NS | OWASP managed rule set enabled and current | Must | Yes | rule set type/version |
| WAF-003 | LT-3 | LT | WAF logs enabled | Must | Partial | diagnostics |
| WAF-004 | NS-1 | NS | Custom rules and exclusions reviewed and minimal | Must | Partial | policy review |
| WAF-005 | PV-1 | PV | Rule tuning process documented to avoid silent bypass | Should | No | process/evidence control |

## Implementation Notes

- Detection mode is acceptable only during controlled tuning windows.
- Every exclusion or disabled rule should have a traceable justification.
- WAF logs are mandatory if the service is meant to provide attack visibility.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure WAF security baseline
