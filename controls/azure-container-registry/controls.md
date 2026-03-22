# Azure Container Registry — Security Controls

> **Status:** Expanded baseline on 2026-03-23 from repository control conventions.
> **Back to matrix:** [MCSB-control-matrix.md](../MCSB-control-matrix.md)

---

## Service Scope

Azure Container Registry is the software supply-chain anchor for container images and artifacts. The baseline emphasizes private access, trusted pulls, image integrity, and logging.

## Recommended Baseline Controls

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|
| ACR-001 | NS-2 | NS | Public network access disabled | Must | Yes | `public_network_access_enabled = false` |
| ACR-002 | IM-1 | IM | Admin user disabled | Must | Yes | `admin_enabled = false` |
| ACR-003 | NS-2 | NS | Private endpoint configured for production | Must | Partial | `azurerm_private_endpoint` |
| ACR-004 | LT-3 | LT | Diagnostic logging enabled | Must | Partial | `azurerm_monitor_diagnostic_setting` |
| ACR-005 | PV-5 | PV | Image scanning or Defender enabled | Should | Partial | Defender for Containers or registry posture |
| ACR-006 | IM-3 | IM | Pull access via managed identity and RBAC | Must | Partial | `AcrPull` role assignments |

## Control Detail Highlights

- `ACR-001`: Production registries should not remain broadly public if private connectivity is available.
- `ACR-002`: The admin account is a legacy convenience path and should be disabled in favor of Entra ID and RBAC.
- `ACR-003`: Private endpoints are the preferred production pattern for internal image distribution.
- `ACR-004`: Push, pull, delete, and auth telemetry should be exported because registry compromise affects every dependent workload.
- `ACR-005`: Image scanning and Defender posture findings help identify supply-chain risk before deployment.
- `ACR-006`: Registry consumers should use managed identity and role assignments rather than shared username/password style access.

## Agent Notes

- Review ACR together with the services that pull from it; image trust and pull authorization are one control chain.
- A secure registry still needs secure deployment consumers. Do not stop at the registry resource alone.
- Artifact deletion and overwrite patterns can be operationally disruptive and should be monitored.

## Suggested Validation Cases

- Secure: admin user disabled, private access path, diagnostics enabled, managed identity pulls, scanning enabled.
- Insecure: public registry, admin account enabled, opaque image provenance, no artifact activity logs.

## Expansion Sources

- Microsoft Cloud Security Benchmark
- Azure Container Registry security baseline
