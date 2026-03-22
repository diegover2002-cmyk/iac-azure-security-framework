# Azure Cache for Redis — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Cache for Redis is a sensitive in-memory data store commonly used for sessions, tokens, and transient application state. The baseline prioritizes transport security, network isolation, and access minimization.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| RED-001 | DP-3 | DP | Non-TLS port disabled | Must | Yes | `enable_non_ssl_port = false` |
| RED-002 | NS-2 | NS | Private endpoint or restricted network access | Must | Partial | private endpoint or firewall rules |
| RED-003 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| RED-004 | DP-5 | DP | Customer-managed key where required | Should | Partial | enterprise or CMK configuration |
| RED-005 | IM-3 | IM | Access keys rotated and minimized | Should | Partial | operational evidence |
| RED-006 | PV-1 | PV | Defender recommendations monitored | Should | Partial | Defender for Cloud posture |

## Control Detail Highlights

- `RED-001`: Plaintext Redis connectivity should be disabled in every environment because these caches frequently hold authentication or session material.
- `RED-002`: Production caches should prefer private connectivity or very restrictive network paths.
- `RED-003`: Cache diagnostics help correlate performance anomalies, failed auth, and abusive access patterns.
- `RED-004`: CMK is relevant for regulated data or stricter key ownership requirements.
- `RED-005`: Redis keys are high-risk shared secrets and should be rotated through controlled processes, not treated as static credentials.
- `RED-006`: Defender posture findings should be monitored because Redis misconfigurations can expose authentication and state data quickly.

## Agent Notes

- Redis often sits behind application layers, so exposure is easy to underestimate.
- Review application secret handling together with Redis authentication and key rotation.
- If the cache stores tokens, sessions, or authorization data, treat network isolation as a baseline control rather than optional hardening.

## Suggested Validation Cases

- Secure: non-SSL port disabled, private access path, diagnostics enabled, controlled key lifecycle.
- Insecure: plaintext port enabled, public access without restriction, stale keys reused across applications.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Cache for Redis security baseline
