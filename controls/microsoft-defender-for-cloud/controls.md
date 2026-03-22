# Microsoft Defender for Cloud — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Microsoft Defender for Cloud is a cross-cutting posture and threat-protection service. This file captures foundational controls for plan enablement, recommendation governance, and alert routing.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| MDC-001 | PV-1 | PV | Relevant Defender plans enabled for in-scope resources | Must | Partial | `azurerm_security_center_subscription_pricing` |
| MDC-002 | LT-1 | LT | Security alerts routed to monitored destination | Must | Partial | workflow automation / SIEM pattern |
| MDC-003 | PV-1 | PV | Secure Score and recommendations reviewed regularly | Must | No | operational evidence |
| MDC-004 | IM-1 | IM | Access to Defender findings restricted by RBAC | Must | Partial | role assignments |
| MDC-005 | LT-3 | LT | Continuous export configured where required | Should | Partial | export settings |
| MDC-006 | PV-5 | PV | Regulatory/compliance initiatives assigned where applicable | Should | Partial | policy initiative linkage |

## Implementation Notes

- Defender for Cloud is not a single-resource control; it is subscription and management-group scoped.
- Enable only the plans that map to actual deployed services, then verify alert routing and ownership.
- Treat recommendation review as an operating process, not a one-time setup step.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Microsoft Defender for Cloud security baseline
