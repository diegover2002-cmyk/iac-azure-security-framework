# Azure Service to MCSB Control Catalog

> Purpose: normalized service-control catalog for internal security documentation and CI/CD security check design.
> Scope in this version: Azure services already modeled in this repository.
> Source of truth: Microsoft Learn MCSB overview and Azure service security baselines.
> Review date: 2026-03-22

## Method and scope

This document is designed to be exported to Excel or consumed directly as Markdown. Each row represents one applicable control for one Azure service.

Important note on source versions:

- The Microsoft Cloud Security Benchmark overview page currently presents **MCSB v2 (preview)** and was last updated on **2026-01-15**.
- The Azure service security baseline pages currently exposed in Microsoft Learn for the services used in this repository still state that they apply **MCSB version 1.0** and most were last updated on **2025-02-25**.
- For repository consistency, this catalog keeps the existing service-level control structure already modeled in the repo, while treating Microsoft Learn service baselines as the authoritative source for service applicability.

Official references:

- MCSB overview: https://learn.microsoft.com/es-es/security/benchmark/azure/overview
- Storage baseline: https://learn.microsoft.com/es-es/security/benchmark/azure/baselines/storage-security-baseline
- Key Vault baseline: https://learn.microsoft.com/es-es/security/benchmark/azure/baselines/key-vault-security-baseline
- Virtual Network baseline: https://learn.microsoft.com/es-es/security/benchmark/azure/baselines/virtual-network-security-baseline
- App Service baseline: https://learn.microsoft.com/es-es/security/benchmark/azure/baselines/app-service-security-baseline
- AKS baseline: https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-kubernetes-service-aks-security-baseline

## Normalized Catalog

| Azure Service | Category | Control ID | MCSB | Control Name | Relevance | Recommendation / Implementation Note | Priority | IaC Checkable | Primary Source |
|---|---|---|---|---|---|---|---|---|---|
| Azure Storage Account | Storage | ST-001 | NS-1 | Public blob access disabled | Prevents anonymous exposure of containers and blobs. | Set `allow_nested_items_to_be_public = false` and block any public container pattern by default. | Must | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-002 | DP-3 | HTTPS only | Ensures clients cannot use clear-text transport. | Set `enable_https_traffic_only = true`; treat any exception as non-compliant. | Must | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-003 | DP-3 | Minimum TLS 1.2 | Reduces downgrade and legacy protocol exposure. | Enforce `min_tls_version = "TLS1_2"` in all storage modules. | Must | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-004 | DP-4 | Infrastructure encryption | Adds defense in depth for regulated data sets. | Enable `infrastructure_encryption_enabled = true` for sensitive and production workloads. | Should | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-005 | DP-5 | Customer-managed keys | Required where customer control over key lifecycle is mandated. | Use CMK backed by Key Vault when workload classification or regulation requires it. | Should | Partial | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-006 | NS-2 | Network firewall default deny | Prevents unrestricted public network reachability. | Enforce `default_action = "Deny"` and explicitly allow only trusted IPs or subnets. | Must | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-007 | NS-2 | Public network access disabled | Removes internet exposure for internal-only storage workloads. | Use `public_network_access_enabled = false` with private endpoints for private access patterns. | Must | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-008 | LT-3 | Diagnostic logging enabled | Required for auditability and incident investigation of data operations. | Configure diagnostic settings for blob services to Log Analytics or approved sink. | Must | Partial | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-009 | DP-8 | Soft delete enabled | Supports recovery after accidental or malicious deletion. | Configure blob and container retention; use 30 days in production unless a stronger standard exists. | Should | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-010 | DP-8 | Blob versioning enabled | Preserves prior object states and reduces overwrite risk. | Enable versioning when workload needs recovery of overwritten data or ransomware resilience. | Nice | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-011 | IM-1 | Shared key access disabled | Forces identity-based access and removes anonymous-like key sprawl risk. | Set `shared_access_key_enabled = false` and move consumers to Entra ID and RBAC. | Must | Yes | Repo matrix + Storage baseline |
| Azure Storage Account | Storage | ST-012 | NS-1 | Cross-tenant replication disabled | Reduces uncontrolled data replication to external tenants. | Set `cross_tenant_replication_enabled = false` unless a formally approved B2B scenario exists. | Must | Yes | Repo matrix + Storage baseline |
| Azure Key Vault | Security / Secrets | KV-001 | NS-2 | Public network access disabled | Key Vault is a high-value target and should not be internet-exposed. | Set `public_network_access_enabled = false` by default in production patterns. | Must | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-002 | NS-2 | Private endpoint configured | Keeps secret retrieval on private address space. | Pair public access disablement with a private endpoint in trusted VNets. | Must | Partial | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-003 | NS-1 | Network default action deny | Ensures only explicitly trusted paths can reach the vault. | Use `network_acls.default_action = "Deny"` and restrict by subnet/IP as needed. | Must | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-004 | LT-3 | Diagnostic logging enabled | Required to track secret, key, and certificate access. | Send `AuditEvent` and related logs to centralized monitoring. | Must | Partial | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-005 | DP-7 | Soft delete enabled | Prevents irreversible loss from accidental deletion. | Set high retention, typically 90 days, in standard enterprise modules. | Must | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-006 | DP-7 | Purge protection enabled | Blocks permanent deletion before retention expires. | Set `purge_protection_enabled = true` and treat it as baseline mandatory. | Must | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-007 | IM-1 | RBAC authorization model | Aligns access management with centralized Entra ID and auditable role assignments. | Use `enable_rbac_authorization = true` and avoid legacy access policies except documented exceptions. | Must | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-008 | DP-6 | Key rotation policy defined | Limits exposure window for cryptographic key compromise. | Require `rotation_policy` for customer-managed keys used by applications or encryption services. | Should | Partial | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-009 | DP-6 | Key expiration date set | Ensures keys do not remain valid indefinitely. | Set expiration on all managed keys and align with rotation cadence. | Should | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-010 | DP-6 | Secret expiration date set | Reduces long-lived credential risk. | Require expiration dates on secrets and connect renewal to application lifecycle. | Should | Yes | Repo matrix + Key Vault baseline |
| Azure Key Vault | Security / Secrets | KV-011 | PV-1 | Defender for Key Vault enabled | Adds anomaly detection for suspicious vault access. | Enable Defender plan at subscription scope for production subscriptions. | Should | Partial | Repo matrix + Key Vault baseline |
| Azure Virtual Network | Networking | VN-001 | NS-1 | Subnets associated with NSG | Establishes segmentation and subnet-level traffic control. | Require NSG association on every workload subnet except justified platform subnets. | Must | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-002 | NS-1 | NSG default deny inbound | Prevents implicit broad exposure through permissive rule design. | Use explicit allow rules only where needed and ensure deny-all inbound remains effective. | Must | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-003 | NS-2 | No unrestricted inbound SSH | Removes one of the most common external attack paths. | Disallow `0.0.0.0/0` on port 22; use Bastion or approved management ranges. | Must | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-004 | NS-2 | No unrestricted inbound RDP | Prevents ransomware-oriented exposure on management endpoints. | Disallow `0.0.0.0/0` on port 3389 and prefer Bastion or JIT access. | Must | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-005 | NS-3 | DDoS protection enabled | Required for VNets hosting public-facing critical services. | Associate DDoS Network Protection plan to internet-facing production VNets. | Should | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-006 | NS-4 | Network Watcher enabled | Enables troubleshooting and some network forensics capabilities. | Deploy Network Watcher in each active region used by the landing zone. | Must | Partial | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-007 | LT-3 | NSG flow logs enabled | Provides evidence of allowed and denied network flows. | Enable flow logs with retention and traffic analytics for sensitive environments. | Must | Partial | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-008 | NS-2 | No wildcard inbound rules | Prevents segmentation collapse caused by any-any allows. | Reject NSG rules that use wildcards for source, destination, and port with `Allow`. | Must | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-009 | NS-7 | Service endpoints scoped to subnet | Reduces reliance on public routing for PaaS consumption from VNets. | Use service endpoints only where private endpoints are not the selected pattern and scope them per subnet. | Should | Yes | Repo matrix + Virtual Network baseline |
| Azure Virtual Network | Networking | VN-010 | NS-1 | Subnets not overly broad | Better segmentation limits lateral movement blast radius. | Avoid large flat subnets for workload tiers; design CIDR per application boundary. | Nice | Partial | Repo matrix + Virtual Network baseline |
| Azure App Service | Compute / PaaS Web | AS-001 | DP-3 | HTTPS only enabled | Prevents clear-text application traffic. | Set `https_only = true` on every app and slot. | Must | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-002 | DP-3 | Minimum TLS 1.2 | Blocks legacy protocol negotiation. | Enforce `min_tls_version = "1.2"` in all web app modules. | Must | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-003 | NS-2 | Public network access restricted | Internal APIs and admin apps should not be broadly reachable. | Apply IP restrictions or private access pattern unless the service is intentionally public-facing. | Must | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-004 | NS-2 | VNet integration configured | Allows secure outbound access to private dependencies. | Use VNet integration when the app consumes private endpoints, internal APIs, or restricted PaaS services. | Should | Partial | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-005 | IM-1 | Managed identity enabled | Eliminates stored credentials for Azure resource access. | Enable system- or user-assigned managed identity and use RBAC for downstream services. | Must | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-006 | IM-3 | No credentials in app settings | Prevents secret leakage in Terraform state, portal configuration, and CI logs. | Store secrets in Key Vault and use references instead of plaintext app settings. | Must | Partial | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-007 | LT-3 | Diagnostic logging enabled | Centralized telemetry is needed for investigation and platform monitoring. | Configure diagnostics to Log Analytics for app, audit, console, and HTTP telemetry. | Must | Partial | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-008 | LT-3 | HTTP logging enabled | Supports attack analysis, abuse detection, and troubleshooting. | Enable HTTP access logging with retention aligned to incident response needs. | Must | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-009 | PV-5 | Latest runtime version | Outdated runtimes introduce known CVEs and unsupported components. | Standardize on supported runtime versions and fail builds for EOL runtimes. | Should | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-010 | DP-4 | Data encryption at rest | Data is platform-encrypted by default and must be documented as inherited control. | Record as platform-managed baseline; no Terraform assertion unless service mode changes. | Must | No | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-011 | NS-1 | IP restrictions configured | Limits inbound exposure to trusted paths. | Use allowlists for internal or administrative apps and propagate the same policy to SCM. | Should | Yes | Repo matrix + App Service baseline |
| Azure App Service | Compute / PaaS Web | AS-012 | PV-1 | Defender for App Service enabled | Improves posture visibility and attack detection for web workloads. | Enable Defender plan in production subscriptions and track recommendations centrally. | Should | Partial | Repo matrix + App Service baseline |
| Azure Kubernetes Service | Containers | AK-001 | NS-2 | API server authorized IP ranges | The control plane is a high-value interface and must not be world-reachable. | Restrict API server access to corporate egress or trusted administration networks. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-002 | NS-2 | Private cluster enabled | Removes the API endpoint from the public internet. | Use private cluster mode for production unless there is a formally accepted exception. | Should | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-003 | IM-1 | Azure AD integration enabled | Centralizes cluster authentication and supports enterprise identity controls. | Use managed Entra integration and avoid certificate-only access patterns. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-004 | IM-1 | Local accounts disabled | Prevents bypass of centralized identity and weakens shared admin credential use. | Set `local_account_disabled = true` for all enterprise clusters. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-005 | PA-7 | RBAC enabled | Enforces least privilege on cluster administration and workload operations. | Require Kubernetes RBAC and prefer Azure RBAC integration where supported. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-006 | NS-1 | Network policy enabled | Limits east-west traffic and pod lateral movement. | Require `network_policy` with Azure or Calico in every cluster network profile. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-007 | PV-2 | Auto-upgrade channel configured | Reduces lag on critical control-plane security patches. | Use `patch` in production by default and document stricter cadence for non-prod if needed. | Should | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-008 | PV-5 | Node OS auto-patching enabled | Keeps node image vulnerabilities under control. | Enforce node OS upgrade channel such as `NodeImage` unless a managed exception exists. | Should | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-009 | LT-3 | Diagnostic logging enabled | Captures audit and control plane logs required for incident response. | Send `kube-audit`, `kube-audit-admin`, and control plane categories to Log Analytics. | Must | Partial | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-010 | LT-1 | Defender for Containers enabled | Adds runtime threat detection and image security posture. | Enable Defender for Containers at subscription level and onboard all production clusters. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-011 | DP-4 | Disk encryption at rest | Protects node and attached disk data, especially in regulated workloads. | Use platform encryption as baseline and CMK-backed Disk Encryption Set where required. | Must | Yes | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-012 | NS-2 | Ingress with WAF / App Gateway | Public HTTP exposure needs a web application protection layer. | Front internet-facing clusters with Application Gateway WAF or equivalent approved control. | Should | Partial | Repo matrix + AKS baseline |
| Azure Kubernetes Service | Containers | AK-013 | PV-1 | Azure Policy add-on enabled | Enforces preventive guardrails on cluster objects. | Enable Azure Policy add-on and map required Gatekeeper constraints to platform standards. | Should | Yes | Repo matrix + AKS baseline |

## Use in CI/CD documentation

Recommended documentation columns for Excel export:

1. `Azure Service`
2. `Category`
3. `Control ID`
4. `MCSB`
5. `Control Name`
6. `Relevance`
7. `Recommendation / Implementation Note`
8. `Priority`
9. `IaC Checkable`
10. `Primary Source`
11. `Planned Validation Rule`
12. `Exception Criteria`

Recommended interpretation for pipeline design:

- `Must` + `IaC Checkable = Yes`: candidate for blocking PR gate.
- `Must` + `IaC Checkable = Partial`: candidate for combined IaC + evidence review.
- `Should`: candidate for non-blocking advisory gate or backlog control.
- `No` or platform-managed: document as inherited or manual evidence control.

## Current gap versus full Azure service catalog

This repository still lacks completed per-service control catalogs for:

- Azure SQL Database
- Azure Cosmos DB
- Azure API Management
- Azure Functions
- Azure Backup

The corresponding Microsoft Learn security baseline pages do exist and should be used to extend this catalog in the next iteration. Cross-cutting areas such as Endpoint Security and DevOps Security should be handled as domain catalogs, not as a single Azure service row set.
