# Checkov Coverage Audit

> Audit date: 2026-03-23  
> Audit scope: `controls/MCSB-control-matrix.md`, `controls/MCSB-service-control-catalog.md`, the official Checkov documentation at `checkov.io`, and the local mirror of `bridgecrewio/checkov` under `checkov/`

## Executive Summary

This audit treats the official Checkov documentation and the `bridgecrewio/checkov` codebase as complementary sources of truth:

- `checkov.io`: product scope, supported IaC types, policy model, and documented scanning behavior
- `bridgecrewio/checkov`: concrete rule IDs, supported resources, and implementable rule logic

For rule-level verification, this audit uses the repository code as the decisive source because it exposes the exact check identifiers and supported resources.

This repository remains the source of truth for:

- which MCSB-derived controls the framework expects per Azure service
- which controls are `Must`, `Should`, or `Nice`
- which controls require custom or manual validation when Checkov does not cover them

### Current State

| Metric | Result | Interpretation |
|---|---:|---|
| Matrix controls audited | 218 | Deployable-service controls currently defined in the matrix |
| Normalized catalog rows | 118 | Rows currently normalized for export and CI/CD design |
| Matrix rows referencing an extant Checkov rule ID | 75 | Rule ID exists in the current Checkov repo, but semantic review is still needed in some cases |
| Matrix rows referencing Checkov plus custom logic | 6 | Partial Checkov coverage plus manual or custom validation remains required |
| Matrix rows with no Checkov rule referenced | 124 | No explicit Checkov traceability is currently documented in the matrix |
| Manual or inherited controls | 7 | Platform-managed or process controls not expected to be enforced directly in Checkov |
| Broken Checkov references detected | 6 | Matrix points to rule IDs not found in the current Checkov repo |

### Primary Findings

1. The repository already has meaningful Checkov traceability, but it is incomplete and unevenly maintained.
2. Several matrix and service baseline documents still reference legacy or incorrect Checkov IDs.
3. The normalized catalog is not yet complete enough to act as the only export surface for all deployable services.
4. A sizable portion of the control set still depends on `Custom`, `Needs verification`, or process evidence.

## Service Inventory Status

This section measures structural alignment between the deployable matrix and the normalized catalog. It does not imply that every Checkov mapping is semantically correct.

| Status | Services |
|---|---|
| `Aligned between matrix and catalog` | Azure Storage Account, Azure Key Vault, Azure Virtual Network, Azure App Service, Azure Kubernetes Service, Azure SQL Database, Azure API Management, Azure Event Grid, Azure Logic Apps, Azure Private Link |
| `Count mismatch between matrix and catalog` | Azure Backup, Azure Cosmos DB, Azure Functions |
| `Present in matrix but not yet normalized in catalog` | Azure Bastion, Azure App Configuration, Azure Cache for Redis, Azure Container Apps, Azure Container Instances, Azure Container Registry, Azure Data Factory, Azure Data Share, Azure DNS, Azure Event Hubs, Azure Firewall, Azure Front Door, Azure Application Gateway, Azure Load Balancer, Azure Monitor, Azure Public IP, Azure Service Bus, Azure Web Application Firewall |

### Structural Inconsistencies

| Area | Finding | Impact |
|---|---|---|
| Cosmos DB | `CO-010` exists in the normalized catalog but not in the matrix | Catalog and matrix disagree on control inventory |
| Backup | `BK-009` exists in the normalized catalog but not in the matrix | Catalog and matrix disagree on control inventory |
| Functions | Matrix defines 9 controls while the normalized catalog currently carries 7 | Export surface is incomplete |

## Broken Checkov References

These matrix references point to IDs not found in the current local mirror of `bridgecrewio/checkov`.

| Control ID | Service | Current Matrix Validation | Audit Result | Recommended Action |
|---|---|---|---|---|
| ST-004 | Azure Storage Account | `CKV_AZURE_256` | Rule not found | Downgrade to `Needs verification` and validate with custom policy or evidence |
| SQ-001 | Azure SQL Database | `CKV_AZURE_46` | Rule not found | Replace with verified current rule |
| SQ-002 | Azure SQL Database | `CKV2_AZURE_18` | Rule not found | Replace with verified current rule or custom graph validation |
| CO-002 | Azure Cosmos DB | `CKV2_AZURE_18` | Rule not found | Mark `Needs verification` until a verified Cosmos private endpoint rule is confirmed |
| CO-003 | Azure Cosmos DB | `CKV2_AZURE_68` | Rule not found | Replace with custom validation; no verified current direct rule was confirmed in this audit |
| BK-007 | Azure Backup | `CKV2_AZURE_18` | Rule not found | Mark `Needs verification` or implement custom graph policy |

## High-Confidence Current Checkov Mappings

The following mappings were confirmed directly against the local `checkov/` source and should be treated as current high-confidence candidates for documentation normalization.

| Control ID | Service | Current Repo Mapping | Verified Current Checkov Mapping | Evidence in `checkov/` |
|---|---|---|---|---|
| SQ-001 | Azure SQL Database | `CKV_AZURE_46` | `CKV_AZURE_113` | `checkov/terraform/checks/resource/azure/SQLServerPublicAccessDisabled.py` |
| SQ-002 | Azure SQL Database | `CKV2_AZURE_18` | `CKV2_AZURE_45` | `checkov/terraform/checks/graph_checks/azure/AzureMSSQLserverConfigPrivEndpt.yaml` |
| SQ-003 | Azure SQL Database | `CKV_AZURE_192` | `CKV2_AZURE_27` | `checkov/arm/checks/resource/SQLServerUsesADAuth.py` and `checkov/terraform/checks/graph_checks/azure/AzureConfigMSSQLwithAD.yaml` |
| SQ-004 | Azure SQL Database | `CKV_AZURE_47` | `CKV_AZURE_69` | `checkov/terraform/checks/resource/azure/AzureDefenderOnSqlServers.py` |
| SQ-005 | Azure SQL Database | `CKV_AZURE_49`, `CKV_AZURE_21` | `CKV_AZURE_156` plus custom evidence | `checkov/terraform/checks/resource/azure/MSSQLServerAuditPolicyLogMonitor.py` |
| SQ-006 | Azure SQL Database | `CKV_AZURE_191` | `CKV_AZURE_52` | `checkov/terraform/checks/resource/azure/MSSQLServerMinTLSVersion.py` |
| CO-004 | Azure Cosmos DB | `CKV_AZURE_217` | `CKV_AZURE_140` | `checkov/terraform/checks/resource/azure/CosmosDBLocalAuthDisabled.py` |
| AP-001 | Azure API Management | `CKV_AZURE_33` | `CKV_AZURE_107` | `checkov/terraform/checks/resource/azure/APIServicesUseVirtualNetwork.py` |
| AP-002 | Azure API Management | `CKV_AZURE_104` | `CKV_AZURE_215` | `checkov/terraform/checks/resource/azure/APIManagementBackendHTTPS.py` |
| AP-008 | Azure API Management | `CKV2_AZURE_3` | `CKV_AZURE_173` | `checkov/terraform/checks/resource/azure/APIManagementMinTLS12.py` |
| ACF-001 | Azure App Configuration | `Custom` | `CKV_AZURE_185` | `checkov/terraform/checks/resource/azure/AppConfigPublicAccess.py` |
| ACF-003 | Azure App Configuration | `Custom` | `CKV_AZURE_184` | `checkov/terraform/checks/resource/azure/AppConfigLocalAuth.py` |
| ACF-004 | Azure App Configuration | `Custom` | `CKV_AZURE_186` | `checkov/terraform/checks/resource/azure/AppConfigEncryption.py` |
| RED-001 | Azure Cache for Redis | `Custom` | `CKV_AZURE_91` | `checkov/terraform/checks/resource/azure/RedisCacheEnableNonSSLPort.py` |
| RED-002 | Azure Cache for Redis | `Custom` | `CKV_AZURE_89` plus custom | `checkov/terraform/checks/resource/azure/RedisCachePublicNetworkAccessEnabled.py` |

## Controls Without Verified Automatic Coverage

The following are representative categories of controls that still lack a verified direct Checkov rule in this audit and should remain `Custom`, `Needs verification`, or manual evidence controls.

| Area | Example Controls | Recommended Validation Path |
|---|---|---|
| Storage infrastructure encryption | `ST-004` | Terraform plan review plus Azure Policy or custom static policy |
| Cosmos DB private endpoint and data-plane RBAC | `CO-002`, `CO-003` | Graph-based custom policy plus runtime architecture evidence |
| Backup vault private endpoint and CMK coverage | `BK-005`, `BK-007` | Custom graph policy plus deployment evidence |
| Logic Apps connector secret handling | `LGA-002`, `LGA-005` | Terraform plan review, secrets scanning, and policy-as-code for connector patterns |
| Private Link DNS correctness and lifecycle monitoring | `PLS-004`, `PLS-005` | Custom graph validation plus Azure Policy and operational evidence |
| Data classification or revocation controls | `ADS-004`, `ADS-005`, `WAF-005` | Process control, evidence review, and governance workflow |

## Recommended CI/CD Integration

1. Add a generated rule register step that extracts Checkov IDs and supported resources from the local `checkov/` mirror or from a pinned release of `bridgecrewio/checkov`.
2. Classify matrix controls into:
   - `Verified Checkov`
   - `Checkov + Custom`
   - `Custom`
   - `Manual / Inherited`
3. Block pull requests only on `Must` + `High` controls whose Checkov mapping is verified and current.
4. Route `Must` + `High` controls without Checkov coverage into custom graph checks, Azure Policy, or evidence review gates.
5. Store the mapping output as a build artifact so PR reviewers can see:
   - control ID
   - MCSB mapping
   - current Checkov rule ID if any
   - validation status
   - gap owner

## Next Remediation Waves

1. Normalize SQL, Cosmos DB, API Management, Backup, App Configuration, and Redis first. These have the highest signal-to-effort ratio because the audit already identified current Checkov rule candidates.
2. Reconcile the normalized catalog with the matrix for `CO-010`, `BK-009`, and the current Azure Functions mismatch.
3. Expand the normalized catalog to the matrix-only services before attempting executive export from the catalog alone.
4. Introduce a generated validation register so future documentation updates cannot silently drift from the Checkov rule set.
