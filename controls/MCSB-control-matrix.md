# MCSB Control Matrix — Azure Services

> **Purpose:** Maps Azure services to MCSB controls. Used as the foundation for CI/CD security checks, security documentation, and compliance tracking.
> **Last updated:** 2026-03-22
> **Source of truth:** [Microsoft Cloud Security Benchmark](https://learn.microsoft.com/en-us/security/benchmark/azure/)
> **Normalized catalog:** [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md)

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
| 6 | [Azure SQL Database](#6-azure-sql-database) | Database | 9 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 7 | [Azure Cosmos DB](#7-azure-cosmos-db) | Database | 10 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 8 | [Azure API Management](#8-azure-api-management) | Integration | 10 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 9 | [Azure Functions](#9-azure-functions) | Compute | 7 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 10 | [Azure Backup](#10-azure-backup) | Backup/Recovery | 9 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 11 | [Azure Event Hubs](#11-azure-event-hubs) | Messaging | 7 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 12 | [Azure Monitor](#12-azure-monitor) | Monitoring | 9 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 13 | [Azure Load Balancer](#13-azure-load-balancer) | Networking | 2 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 14 | [Azure Public IP](#14-azure-public-ip) | Networking | 4 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 15 | [Azure Private Link](#15-azure-private-link) | Networking | 3 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 16 | [Microsoft Defender for Cloud](#16-microsoft-defender-for-cloud) | Security | 7 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 17 | [Azure Service Bus](#17-azure-service-bus) | Messaging | 6 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 18 | [Azure Event Grid](#18-azure-event-grid) | Messaging | 4 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 19 | [Azure Container Registry](#19-azure-container-registry) | Containers | 8 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 20 | [Azure Application Gateway](#20-azure-application-gateway) | Networking | 4 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 21 | [Azure Front Door](#21-azure-front-door) | Edge | 3 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 22 | [Azure Firewall](#22-azure-firewall) | Networking/Security | 5 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 23 | [Azure DNS](#23-azure-dns) | Networking | 3 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 24 | [Azure Bastion](#24-azure-bastion) | Networking/Admin Access | 4 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 25 | [Azure Web Application Firewall](#25-azure-web-application-firewall) | Security | 3 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 26 | [Azure Container Instances](#26-azure-container-instances) | Containers | 3 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 27 | [Azure Container Apps](#27-azure-container-apps) | Containers | 4 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 28 | [Azure App Configuration](#28-azure-app-configuration) | Developer Tools | 6 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 29 | [Azure Data Factory](#29-azure-data-factory) | Data Integration | 6 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 30 | [Azure Logic Apps](#30-azure-logic-apps) | Integration | 6 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 31 | [Azure Cache for Redis](#31-azure-cache-for-redis) | Database/Cache | 4 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 32 | [Azure Data Share](#32-azure-data-share) | Data Sharing | 3 | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 33 | [Endpoint Security](#33-endpoint-security) | Cross-cutting Domain | Domain catalog | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 34 | [DevOps Security](#34-devops-security) | Cross-cutting Domain | Domain catalog | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |
| 35 | [AI Security](#35-ai-security) | Cross-cutting Domain | Domain catalog | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

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
| SQ-001 | NS-1 | NS | Virtual network integration | Conditional | Medium | Should | Partial | Custom |
| SQ-002 | NS-2 | NS | Private Link enabled | Yes | High | Must | Partial | Custom |
| SQ-003 | IM-1 | IM | Entra ID authentication for data plane | Yes | High | Must | Partial | Custom |
| SQ-004 | IM-7 | IM | Conditional access for data plane | Conditional | Medium | Should | No | Manual evidence |
| SQ-005 | DP-3 | DP | Encryption in transit | Yes | High | Must | No | Platform / client standard |
| SQ-006 | DP-4 | DP | Encryption at rest with platform keys | Yes | Medium | Must | No | Platform-managed |
| SQ-007 | DP-5 | DP | Customer-managed keys for TDE | Conditional | Medium | Should | Partial | Custom |
| SQ-008 | LT-1 | LT | Defender for Azure SQL enabled | Yes | Medium | Should | Partial | Defender plan |
| SQ-009 | LT-4 | LT | Resource and audit logging enabled | Yes | High | Must | Partial | Diagnostic settings + auditing |

# 7. Azure Cosmos DB

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| CO-001 | NS-1 | NS | Virtual network integration | Conditional | Medium | Should | Partial | Custom |
| CO-002 | NS-2 | NS | Private Link enabled | Yes | High | Must | Partial | Custom |
| CO-003 | IM-1 | IM | Entra ID authentication for data plane | Yes | High | Must | Partial | Custom |
| CO-004 | IM-3 | IM | Managed identities for application access | Conditional | Medium | Should | Partial | Custom |
| CO-005 | PA-7 | PA | Data plane RBAC enabled | Yes | High | Must | Partial | Custom |
| CO-006 | DP-3 | DP | Encryption in transit | Yes | High | Must | No | Platform / client standard |
| CO-007 | DP-4 | DP | Encryption at rest with platform keys | Yes | Medium | Must | No | Platform-managed |
| CO-008 | DP-5 | DP | Customer-managed keys when required | Conditional | Medium | Should | Partial | Custom |
| CO-009 | LT-1 | LT | Defender for Azure Cosmos DB enabled | Yes | Medium | Should | Partial | Defender plan |
| CO-010 | LT-4 | LT | Resource logging enabled | Yes | High | Must | Partial | Diagnostic settings |

# 8. Azure API Management

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| AP-001 | NS-1 | NS | VNet integration | Conditional | Medium | Should | Partial | Custom |
| AP-002 | NS-2 | NS | Private Link enabled | Conditional | Medium | Should | Partial | Custom |
| AP-003 | NS-2 | NS | Public network access disabled or restricted | Yes | High | Must | Partial | Custom |
| AP-004 | IM-1 | IM | Entra ID authentication | Yes | Medium | Should | Partial | Custom |
| AP-005 | PA-1 | PA | Local accounts restricted | Yes | Medium | Should | No | Manual evidence |
| AP-006 | DP-3 | DP | Encrypted protocols only | Yes | High | Must | Partial | Gateway config |
| AP-007 | DP-4 | DP | Encryption at rest with platform keys | Yes | Medium | Must | No | Platform-managed |
| AP-008 | DP-6 | DP | Key Vault integration for secrets and certificates | Yes | High | Must | Partial | Custom |
| AP-009 | LT-1 | LT | Defender for APIs enabled | Yes | Medium | Should | Partial | Defender plan |
| AP-010 | LT-4 | LT | Resource logging enabled | Yes | High | Must | Partial | Diagnostic settings |

# 9. Azure Functions

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| FN-001 | NS-1 | NS | VNet integration | Conditional | Medium | Should | Partial | Custom |
| FN-002 | NS-2 | NS | Private Link enabled | Conditional | Medium | Should | Partial | Custom |
| FN-003 | IM-1 | IM | Entra ID authentication for endpoints and deployment access | Yes | High | Must | Partial | Custom |
| FN-004 | IM-3 | IM | Managed identity enabled | Yes | High | Must | Yes | Function app identity |
| FN-005 | DP-3 | DP | HTTPS only and minimum TLS 1.2 | Yes | High | Must | Yes | Site config |
| FN-006 | LT-1 | LT | Defender for App Service enabled | Yes | Medium | Should | Partial | Defender plan |
| FN-007 | LT-4 | LT | Resource logging enabled | Yes | High | Must | Partial | Diagnostic settings |

# 10. Azure Backup

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| BK-001 | NS-2 | NS | Private Link enabled | Conditional | Medium | Should | Partial | Custom |
| BK-002 | NS-2 | NS | Public network access disabled | Yes | High | Must | Partial | Custom |
| BK-003 | IM-8 | IM | Key Vault for credentials and secret storage | Conditional | Medium | Should | Partial | Custom |
| BK-004 | DP-2 | DP | Immutable and anti-deletion protections | Yes | High | Must | Partial | Vault config |
| BK-005 | DP-3 | DP | Encryption in transit | Yes | High | Must | No | Platform-managed |
| BK-006 | DP-4 | DP | Encryption at rest with platform keys | Yes | Medium | Must | No | Platform-managed |
| BK-007 | DP-5 | DP | Customer-managed keys when required | Conditional | Medium | Should | Partial | Custom |
| BK-008 | DP-6 | DP | Key lifecycle in Key Vault | Conditional | Medium | Should | Partial | Process / custom |
| BK-009 | BR-1 | BR | Automated backup protection enabled | Yes | High | Must | Partial | Policy + protected items |

# 11. Azure Event Hubs

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 12. Azure Monitor

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 13. Azure Load Balancer

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 14. Azure Public IP

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 15. Azure Private Link

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 16. Microsoft Defender for Cloud

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 17. Azure Service Bus

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 18. Azure Event Grid

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 19. Azure Container Registry

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 20. Azure Application Gateway

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 21. Azure Front Door

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 22. Azure Firewall

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 23. Azure DNS

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 24. Azure Bastion

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 25. Azure Web Application Firewall

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 26. Azure Container Instances

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 27. Azure Container Apps

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 28. Azure App Configuration

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 29. Azure Data Factory

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 30. Azure Logic Apps

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 31. Azure Cache for Redis

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 32. Azure Data Share

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| See normalized catalog | Multiple | Multiple | Refer to normalized service catalog | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 33. Endpoint Security

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| Domain catalog | ES | ES | Cross-cutting endpoint controls | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 34. DevOps Security

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| Domain catalog | DS | DS | Cross-cutting DevOps controls | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

# 35. AI Security

| Control ID | MCSB | Domain | Control Name | Applies | Severity | Priority | IaC Checkable | Validation |
|---|---|---|---|---|---|---|---|---|
| Domain catalog | IA | IA | Cross-cutting AI security controls | Yes | Mixed | Mixed | Mixed | [MCSB-service-control-catalog.md](MCSB-service-control-catalog.md) |

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
