# MCSB Control Matrix — Azure Services

> **Purpose:** Maps Azure services to MCSB controls. Used as the foundation for CI/CD security checks, security documentation, and compliance tracking.
> **Last updated:** 2025
> **Source of truth:** [Microsoft Cloud Security Benchmark](https://learn.microsoft.com/en-us/security/benchmark/azure/)

---

## How to read this matrix

| Column | Description |
|---|---|
| **Control ID** | Internal ID (service prefix + number) |
| **MCSB** | MCSB control ID |
| **Domain** | MCSB domain (NS, IM, DP, LT, PA, PV, AM, IR, ES, BR, DS, IA) |
| **Control Name** | Short name |
| **Applies** | Yes / No / Conditional |
| **Severity** | High / Medium / Low |
| **Priority** | Must / Should / Nice |
| **IaC Checkable** | Yes / Partial / No |
| **Validation** | How to detect in code |

---

## Services Index

| # | Service | Category | Controls | Detail |
|---|---|---|---|---|
| 1 | [Azure Storage Account](#1-azure-storage-account) | Storage | 12 | [controls.md](azure-storage/controls.md) |
| 2 | [Azure Key Vault](#2-azure-key-vault) | Security | 11 | [controls.md](azure-key-vault/controls.md) |
| 3 | [Azure Virtual Network](#3-azure-virtual-network) | Networking | 10 | [controls.md](azure-vnet/controls.md) |
| 4 | [Azure App Service](#4-azure-app-service) | Compute | 12 | [controls.md](azure-app-service/controls.md) |
| 5 | [Azure Kubernetes Service](#5-azure-kubernetes-service-aks) | Compute | 13 | [controls.md](azure-aks/controls.md) |
| 6 | [Azure SQL Database](#6-azure-sql-database) | Database | TBD | [controls.md](azure-sql/controls.md) |
| 7 | [Azure Cosmos DB](#7-azure-cosmos-db) | Database | TBD | [controls.md](azure-cosmosdb/controls.md) |
| 8 | [Azure API Management](#8-azure-api-management) | Integration | TBD | [controls.md](azure-apim/controls.md) |
| 9 | [Azure Functions](#9-azure-functions) | Compute | TBD | [controls.md](azure-functions/controls.md) |
| 10 | [Azure Backup](#10-azure-backup) | Backup/Recovery | TBD | [controls.md](azure-backup/controls.md) |
| 11 | [Endpoint Security (Defender)](#11-endpoint-security-defender) | Endpoint Security | TBD | [controls.md](endpoint-security/controls.md) |
| 12 | [DevOps Security](#12-devops-security) | DevOps | TBD | [controls.md](devops-security/controls.md) |
| 13 | [AI Security](#13-ai-security) | AI | TBD | [controls.md](ai-security/controls.md) |
| 14 | [Azure Application Gateway](#14-azure-application-gateway) | Networking | 6 | [controls.md](azure-application-gateway/controls.md) |
| 15 | [Azure Bastion](#15-azure-bastion) | Networking | 5 | [controls.md](azure-bastion/controls.md) |

---

## 1. Azure Storage Account

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| ST-001 | NS-1 | NS | Public blob access disabled | Yes | High | Must | Yes | `CKV_AZURE_59` |
| ST-002 | DP-3 | DP | HTTPS only (secure transfer) | Yes | High | Must | Yes | `CKV_AZURE_3` |
| ST-003 | DP-3 | DP | Minimum TLS 1.2 | Yes | High | Must | Yes | `CKV_AZURE_44` |
| ST-004 | DP-4 | DP | Infrastructure encryption | Yes | Medium | Should | Yes | `CKV_AZURE_256` |
| ST-005 | DP-5 | DP | Customer-managed keys (CMK) | Conditional | Medium | Should | Partial | `CKV_AZURE_206` |
| ST-006 | NS-2 | NS | Network firewall default deny | Yes | High | Must | Yes | `CKV_AZURE_35` |
| ST-007 | NS-2 | NS | Public network access disabled | Conditional | High | Must | Yes | `CKV_AZURE_190` |
| ST-008 | LT-3 | LT | Diagnostic logging enabled | Yes | Medium | Must | Partial | Custom |
| ST-009 | DP-8 | DP | Soft delete ≥ 7 days | Yes | Medium | Should | Yes | `CKV_AZURE_111` |
| ST-010 | DP-8 | DP | Blob versioning enabled | Yes | Low | Nice | Yes | `CKV_AZURE_119` |
| ST-011 | IM-1 | IM | Shared key access disabled | Yes | High | Must | Yes | `CKV2_AZURE_40` |
| ST-012 | NS-1 | NS | Cross-tenant replication disabled | Yes | High | Must | Yes | `CKV_AZURE_92` |

---

## 2. Azure Key Vault

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| KV-001 | NS-2 | NS | Public network access disabled | Yes | High | Must | Yes | `CKV_AZURE_109` |
| KV-002 | NS-2 | NS | Private endpoint configured | Conditional | High | Must | Partial | `CKV_AZURE_109` + custom |
| KV-003 | NS-1 | NS | Network default action deny | Yes | High | Must | Yes | `CKV_AZURE_109` |
| KV-004 | LT-3 | LT | Diagnostic logging enabled | Yes | Medium | Must | Partial | Custom |
| KV-005 | DP-7 | DP | Soft delete enabled | Yes | High | Must | Yes | `CKV_AZURE_42` |
| KV-006 | DP-7 | DP | Purge protection enabled | Yes | High | Must | Yes | `CKV_AZURE_110` |
| KV-007 | IM-1 | IM | RBAC authorization model | Yes | High | Must | Yes | `CKV2_AZURE_38` |
| KV-008 | DP-6 | DP | Key rotation policy defined | Yes | Medium | Should | Partial | Custom |
| KV-009 | DP-6 | DP | Key expiration date set | Yes | Medium | Should | Yes | `CKV_AZURE_112` |
| KV-010 | DP-6 | DP | Secret expiration date set | Yes | Medium | Should | Yes | `CKV_AZURE_114` |
| KV-011 | PV-1 | PV | Defender for Key Vault enabled | Yes | Medium | Should | Partial | `CKV_AZURE_234` |

---

## 3. Azure Virtual Network

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| VN-001 | NS-1 | NS | Subnets associated with NSG | Yes | High | Must | Yes | `CKV2_AZURE_31` |
| VN-002 | NS-1 | NS | NSG default deny inbound | Yes | High | Must | Yes | Custom |
| VN-003 | NS-2 | NS | No unrestricted inbound SSH (22) | Yes | High | Must | Yes | `CKV_AZURE_10` |
| VN-004 | NS-2 | NS | No unrestricted inbound RDP (3389) | Yes | High | Must | Yes | `CKV_AZURE_9` |
| VN-005 | NS-3 | NS | DDoS protection enabled | Yes | Medium | Should | Yes | `CKV_AZURE_182` |
| VN-006 | NS-4 | NS | Network Watcher enabled | Yes | Medium | Must | Partial | Custom |
| VN-007 | LT-3 | LT | NSG flow logs enabled | Yes | Medium | Must | Partial | `CKV_AZURE_12` |
| VN-008 | NS-2 | NS | No wildcard inbound rules (any/any) | Yes | High | Must | Yes | Custom |
| VN-009 | NS-7 | NS | Service endpoints scoped to subnet | Conditional | Medium | Should | Yes | Custom |
| VN-010 | NS-1 | NS | Subnets not overly broad (/8, /16) | Yes | Low | Nice | Partial | Custom |

---

## 4. Azure App Service

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| AS-001 | DP-3 | DP | HTTPS only enabled | Yes | High | Must | Yes | `CKV_AZURE_14` |
| AS-002 | DP-3 | DP | Minimum TLS 1.2 | Yes | High | Must | Yes | `CKV_AZURE_154` |
| AS-003 | NS-2 | NS | Public network access restricted | Conditional | High | Must | Yes | `CKV_AZURE_222` |
| AS-004 | NS-2 | NS | VNet integration configured | Conditional | High | Should | Partial | Custom |
| AS-005 | IM-1 | IM | Managed identity enabled | Yes | High | Must | Yes | `CKV_AZURE_16` |
| AS-006 | IM-3 | IM | No credentials in app settings | Yes | High | Must | Partial | Custom / Checkov secrets |
| AS-007 | LT-3 | LT | Diagnostic logging enabled | Yes | Medium | Must | Partial | `CKV_AZURE_13` |
| AS-008 | LT-3 | LT | HTTP logging enabled | Yes | Medium | Must | Yes | `CKV_AZURE_13` |
| AS-009 | PV-5 | PV | Latest runtime version | Yes | Medium | Should | Yes | Custom |
| AS-010 | DP-4 | DP | Data encryption at rest | Yes | Medium | Must | No | Platform-managed |
| AS-011 | NS-1 | NS | IP restrictions configured | Conditional | Medium | Should | Yes | `CKV_AZURE_17` |
| AS-012 | PV-1 | PV | Defender for App Service enabled | Yes | Medium | Should | Partial | `CKV_AZURE_65` |

---

## 5. Azure Kubernetes Service (AKS)

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| AK-001 | NS-2 | NS | API server authorized IP ranges | Yes | High | Must | Yes | `CKV_AZURE_6` |
| AK-002 | NS-2 | NS | Private cluster enabled | Conditional | High | Should | Yes | `CKV_AZURE_115` |
| AK-003 | IM-1 | IM | Azure AD integration enabled | Yes | High | Must | Yes | `CKV_AZURE_5` |
| AK-004 | IM-1 | IM | Local accounts disabled | Yes | High | Must | Yes | `CKV_AZURE_141` |
| AK-005 | PA-7 | PA | RBAC enabled | Yes | High | Must | Yes | `CKV_AZURE_5` |
| AK-006 | NS-1 | NS | Network policy enabled (Calico/Azure) | Yes | High | Must | Yes | `CKV_AZURE_7` |
| AK-007 | PV-2 | PV | Auto-upgrade channel configured | Yes | Medium | Should | Yes | `CKV_AZURE_170` |
| AK-008 | PV-5 | PV | Node OS auto-patching enabled | Yes | Medium | Should | Yes | `CKV_AZURE_141` |
| AK-009 | LT-3 | LT | Diagnostic logging enabled | Yes | Medium | Must | Partial | Custom |
| AK-010 | LT-1 | LT | Defender for Containers enabled | Yes | Medium | Must | Yes | `CKV_AZURE_117` |
| AK-011 | DP-4 | DP | Disk encryption at rest | Yes | Medium | Must | Yes | `CKV_AZURE_226` |
| AK-012 | NS-2 | NS | Ingress with WAF / App Gateway | Conditional | Medium | Should | Partial | Custom |
| AK-013 | PV-1 | PV | Azure Policy add-on enabled | Yes | Medium | Should | Yes | `CKV_AZURE_116` |

---

## Applicability Notes

### Conditional controls

| Control | Condition |
|---|---|
| ST-005 (CMK) | Required for storage accounts handling sensitive/regulated data |
| ST-007 (No public network) | Required when storage is accessed only from private networks |
| KV-002 (Private endpoint) | Required in production environments |
| VN-009 (Service endpoints) | Only when PaaS services are accessed from VNet |
| AS-003 (Public access restricted) | Required unless the app is a public-facing web application |
| AS-004 (VNet integration) | Required when app needs access to private resources |
| AK-002 (Private cluster) | Required in production; dev clusters may be public with IP restrictions |
| AK-012 (WAF/Ingress) | Required when AKS exposes public HTTP endpoints |

### Controls that do NOT apply (and why)

| Service | MCSB Control | Reason Not Applicable |
|---|---|---|
| Azure VNet | DP-3 (Encrypt in transit) | VNet is a network construct, not a data service — transit encryption is enforced at the workload level |
| Azure VNet | IM-1 (Centralized identity) | VNet has no authentication surface — identity controls apply to resources within the VNet |
| Azure Key Vault | NS-5 (DDoS) | Key Vault is a PaaS service — DDoS protection is handled at the platform level, not configurable per vault |
| Azure Storage | PA-7 (RBAC) | Covered by ST-011 (shared key disabled) — RBAC is the implicit result of disabling shared keys |

---

## MCSB Domain Reference

| Domain | Full Name | Focus |
|---|---|---|
| NS | Network Security | Network segmentation, firewall, private endpoints |
| IM | Identity Management | Authentication, authorization, managed identities |
| PA | Privileged Access | Admin access, JIT, RBAC |
| DP | Data Protection | Encryption at rest/transit, key management, backup |
| AM | Asset Management | Inventory, tagging, lifecycle, governance |
| LT | Logging & Threat Detection | Diagnostics, SIEM, Defender |
| IR | Incident Response | Detection, containment, recovery |
| PV | Posture & Vulnerability Mgmt | Patching, scanning, Defender for Cloud |
| ES | Endpoint Security | EDR, antimalware, endpoint protection |
| BR | Backup & Recovery | Data/config backup, validation, protection |
| DS | DevOps Security | Secure DevOps, supply chain, SAST, threat modeling |
| IA | AI Security | Secure AI platform, model, monitoring |

# 6. Azure SQL Database

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 7. Azure Cosmos DB

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 8. Azure API Management

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 9. Azure Functions

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 10. Azure Backup

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 11. Endpoint Security (Defender)

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 12. DevOps Security

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

# 13. AI Security

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

---

## 14. Azure Application Gateway

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| AGW-001 | NS-2 | NS | WAF enabled | Yes | High | Must | Yes | `CKV_AZURE_120` |
| AGW-002 | NS-2 | NS | WAF in Prevention mode | Yes | High | Must | Yes | `CKV_AZURE_122` |
| AGW-003 | DP-3 | DP | TLS 1.2+ enforced | Yes | High | Must | Partial | Custom |
| AGW-004 | LT-3 | LT | Diagnostic and access logs enabled | Yes | Medium | Must | Partial | Custom |
| AGW-005 | IM-3 | IM | Certificates sourced from Key Vault | Yes | High | Must | Partial | Custom |
| AGW-006 | NS-2 | NS | Public frontend only when required | Conditional | Medium | Should | Yes | Custom |

---

## 15. Azure Bastion

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| BAS-001 | NS-2 | NS | Bastion used instead of public RDP/SSH | Yes | High | Must | Partial | Custom |
| BAS-002 | NS-1 | NS | Dedicated `AzureBastionSubnet` | Yes | High | Must | Yes | Custom |
| BAS-003 | LT-3 | LT | Diagnostic logging enabled | Yes | Medium | Must | Partial | Custom |
| BAS-004 | IM-1 | IM | Access governed by RBAC/PIM | Yes | High | Must | Partial | Not Applicable |
| BAS-005 | NS-2 | NS | Standard SKU used for production | Conditional | Medium | Should | Yes | Custom |

---

## Usage

### Generate CI/CD checks

Each row where `IaC Checkable = Yes` maps directly to a Checkov rule or custom check.
Filter by `Priority = Must` + `Severity = High` to define the blocking gate in PRs.

### Standardize across repositories

Use this matrix as the contract between the security team and development teams.
Each service module in Terraform must pass all `Must` controls before merge.

### Scale to new services

1. Add a new row block to this file
2. Create `controls/<service>/controls.md` with full control detail
3. Add custom Checkov checks to `.checkov/custom_checks/` for any gaps
