# Azure Event Grid — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Event Grid routes events between publishers and subscribers. The baseline focuses on authenticated delivery, restricted endpoints, and monitoring of event flow.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| EVG-001 | IM-1 | IM | Managed identity or Entra auth used where supported | Must | Partial | subscription auth pattern |
| EVG-002 | NS-2 | NS | Webhook and destination endpoints restricted | Must | Partial | approved HTTPS destinations only |
| EVG-003 | DP-3 | DP | HTTPS-only event delivery | Must | Partial | endpoint scheme and TLS |
| EVG-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | topic/system topic diagnostics |
| EVG-005 | NS-1 | NS | Private Link used for sensitive event domains where supported | Should | Partial | private endpoint pattern |

## Implementation Notes

- Review every subscription target because it defines an outbound trust path.
- Avoid unauthenticated webhooks and enforce HTTPS for event delivery.
- Monitor dead-lettering and delivery failures for abuse or misconfiguration signals.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Event Grid security baseline
