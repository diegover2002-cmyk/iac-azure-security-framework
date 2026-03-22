# Azure Container Apps — Security Controls

> **Status:** Regenerated scaffold on 2026-03-22 from current repo conventions. No prior committed version was found in `git` history.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Container Apps hosts containerized workloads with managed ingress and revision support. The baseline focuses on ingress restriction, managed identity, secret handling, and telemetry.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ACA-001 | NS-2 | NS | External ingress disabled unless explicitly required | Must | Yes | ingress `external_enabled = false` by default |
| ACA-002 | IM-1 | IM | Managed identity enabled | Must | Yes | identity block present |
| ACA-003 | IM-3 | IM | Secrets not hardcoded in template/env | Must | Partial | secret refs / Key Vault integration |
| ACA-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | environment/app diagnostics |
| ACA-005 | NS-2 | NS | Environment integrated with private networking where needed | Should | Partial | managed environment VNet pattern |
| ACA-006 | PV-5 | PV | Images sourced from approved registry | Must | Partial | ACR allowlist / image provenance |

## Implementation Notes

- Default to internal-only ingress for APIs and backends.
- Use managed identity for downstream Azure access and ACR pulls.
- Keep secrets in Key Vault or managed secret stores, not inline environment variables.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Container Apps security baseline
