# Azure Event Grid — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Event Grid routes events between publishers and subscribers. The baseline focuses on authenticated delivery, restricted destination endpoints, and monitoring of event flow.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| EVG-001 | IM-1 | IM | Managed identity or Entra auth used where supported | Must | Partial | subscription auth pattern |
| EVG-002 | NS-2 | NS | Webhook and destination endpoints restricted | Must | Partial | approved HTTPS destinations only |
| EVG-003 | DP-3 | DP | HTTPS-only event delivery | Must | Partial | endpoint scheme and TLS |
| EVG-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | topic or system topic diagnostics |
| EVG-005 | NS-1 | NS | Private Link used for sensitive event domains where supported | Should | Partial | private endpoint pattern |

## Control Detail Highlights

- `EVG-001`: Authentication for publishers and subscribers should avoid weak shared-secret patterns where stronger identity models are available.
- `EVG-002`: Subscription destinations are outbound trust paths and should be restricted to approved endpoints.
- `EVG-003`: Event delivery should stay encrypted end to end; unauthenticated or non-HTTPS webhook patterns are not acceptable baselines.
- `EVG-004`: Delivery failures, dead-lettering, and topic operations should be observable through central diagnostics.
- `EVG-005`: Sensitive domains should prefer private connectivity where platform support makes it feasible.

## Agent Notes

- Review Event Grid subscriptions as security-relevant routing rules, not just event plumbing.
- Each subscription target changes trust boundaries and should be documented as part of the design.
- Dead-lettering and retry behavior are useful security signals, not only reliability features.

## Suggested Validation Cases

- Secure: authenticated delivery, approved HTTPS destinations, diagnostics enabled, private access where needed.
- Insecure: unauthenticated webhooks, unrestricted endpoints, opaque failure handling with no logs.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Event Grid security baseline
