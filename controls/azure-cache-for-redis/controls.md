# Azure Cache for Redis — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Cache for Redis is a sensitive in-memory data store commonly used for sessions, tokens, and transient application state. The baseline prioritizes transport security, network isolation, and access minimization.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| RED-001 | DP-3 | DP | Non-TLS port disabled | Must | Yes | `enable_non_ssl_port = false` |
| RED-002 | NS-2 | NS | Private endpoint or restricted network access | Must | Partial | private endpoint / firewall rules |
| RED-003 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| RED-004 | DP-5 | DP | Customer-managed key where required | Should | Partial | enterprise/CMK configuration |
| RED-005 | IM-3 | IM | Access keys rotated and minimized | Should | Partial | operational evidence |
| RED-006 | PV-1 | PV | Defender recommendations monitored | Should | Partial | Defender for Cloud posture |

## Implementation Notes

- Disable the plaintext port in every environment.
- Prefer private connectivity for production caches storing session or authentication data.
- Treat Redis access keys as secrets and rotate them through controlled processes.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Cache for Redis security baseline
