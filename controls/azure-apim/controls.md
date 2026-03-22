# MCSB Controls for Azure API Management

**Category:** Integration / API
**Service:** `Microsoft.ApiManagement/service`

## 1. Control Summary

This document outlines the Microsoft Cloud Security Benchmark (MCSB) controls for Azure API Management (APIM). It focuses on securing the API gateway, protecting backend services, and ensuring secure consumption of APIs.

| Control ID | MCSB | Domain | Control Name | Priority | IaC Checkable | Validation (Checkov) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AP-001** | NS-1 | NS | Use virtual network (Internal mode) | **Should** | Yes | `CKV_AZURE_33` |
| **AP-002** | DP-3 | DP | Encrypt communication with backend | **Must** | Yes | `CKV_AZURE_104` |
| **AP-003** | DP-6 | DP | Use certificates from Key Vault | **Must** | Yes | `CKV_AZURE_105` |
| **AP-004** | IM-1 | IM | Use Managed Identity | **Must** | Yes | `CKV_AZURE_106` |
| **AP-005** | IM-1 | IM | Authenticate with Azure AD | **Should** | Partial | Custom |
| **AP-006** | LT-1 | LT | Defender for APIs enabled | **Should** | Yes | `CKV_AZURE_65` |
| **AP-007** | LT-4 | LT | API Management logging enabled | **Must** | Yes | `CKV_AZURE_103` |
| **AP-008** | DP-3 | DP | Enforce minimum TLS 1.2 | **Must** | Yes | `CKV2_AZURE_3` |
| **AP-009** | DP-3 | DP | Disable weak ciphers and protocols | **Must** | Yes | `CKV2_AZURE_2` |
| **AP-010** | IM-3 | IM | Use Named Values from Key Vault | **Must** | Yes | `CKV2_AZURE_6` |

---

## 2. Control Details

### AP-001: Use virtual network (Internal mode)

- **MCSB:** NS-1 (Network Segmentation)
- **Priority:** **Should**
- **Relevance:** For APIs that are not meant for public consumption, deploying APIM in a VNet (Internal mode) provides network-level isolation, making it accessible only from within the private network.
- **Implementation:** Set the `virtual_network_type` to `Internal`.
- **Validation:** `CKV_AZURE_33: "Ensure that the API Management service is deployed in a VNet"`

### AP-002: Encrypt communication with backend

- **MCSB:** DP-3 (Data Protection)
- **Priority:** **Must**
- **Relevance:** APIM must use HTTPS to communicate with backend services to protect data in transit between the gateway and the API implementation.
- **Implementation:** Ensure backend URLs use the `https` scheme.
- **Validation:** `CKV_AZURE_104: "Ensure that communication with API backends is secured"`

### AP-003: Use certificates from Key Vault

- **MCSB:** DP-6 (Data Protection / Key Management)
- **Priority:** **Must**
- **Relevance:** Client certificates and custom domain TLS certificates should be stored and managed securely in Azure Key Vault, not embedded in code or APIM configuration.
- **Implementation:** Certificates should be sourced from `azurerm_key_vault_certificate`.
- **Validation:** `CKV_AZURE_105: "Ensure that certificates are managed in Key Vault"`

### AP-004: Use Managed Identity

- **MCSB:** IM-1 (Identity Management)
- **Priority:** **Must**
- **Relevance:** The APIM instance should use a Managed Identity (System or User-assigned) to authenticate to other Azure services (like Key Vault or backend APIs) without needing to store credentials.
- **Implementation:** The `identity` block on the `azurerm_api_management` resource must be configured.
- **Validation:** `CKV_AZURE_106: "Ensure that the API Management service is using a managed identity"`

### AP-005: Authenticate with Azure AD

- **MCSB:** IM-1 (Identity Management)
- **Priority:** **Should**
- **Relevance:** Protect APIs by using Azure AD for authentication and authorization, leveraging OAuth 2.0 and OpenID Connect policies. This centralizes access control.
- **Implementation:** Configure `validate-jwt` policies within the APIM service.
- **Validation:** Custom policy check required; not easily detectable via static IaC analysis.

### AP-006: Defender for APIs enabled

- **MCSB:** LT-1 (Logging and Threat Detection)
- **Priority:** **Should**
- **Relevance:** Defender for APIs provides security recommendations, anomaly detection, and threat intelligence for your API inventory.
- **Implementation:** The `azurerm_security_center_subscription_pricing` resource should be configured for `Api`.
- **Validation:** `CKV_AZURE_65: "Ensure that Advanced Threat Protection is enabled"` (Applies to APIM when the `Api` plan is enabled).

### AP-007: API Management logging enabled

- **MCSB:** LT-4 (Logging and Threat Detection)
- **Priority:** **Must**
- **Relevance:** Diagnostic logs are essential for monitoring API usage, troubleshooting, and investigating security incidents.
- **Implementation:** An `azurerm_monitor_diagnostic_setting` must be configured to send `GatewayLogs` and other relevant categories to a Log Analytics workspace.
- **Validation:** `CKV_AZURE_103: "Ensure that logging is enabled for API Management"`

### AP-008: Enforce minimum TLS 1.2

- **MCSB:** DP-3 (Data Protection)
- **Priority:** **Must**
- **Relevance:** Disables older, insecure TLS versions (1.0, 1.1) for client-to-gateway communication, protecting against known vulnerabilities.
- **Implementation:** Configure the `min_api_version` and custom domain settings to enforce TLS 1.2.
- **Validation:** `CKV2_AZURE_3: "Ensure API Management disables backend SSL/TLS certificate validation"` (Note: this check's name is counterintuitive, it checks for a disabled validation which is bad. The fix is to *not* disable it). The primary control is via policy. A better direct check is `CKV2_AZURE_2`.

### AP-009: Disable weak ciphers and protocols

- **MCSB:** DP-3 (Data Protection)
- **Priority:** **Must**
- **Relevance:** Reduces the attack surface by explicitly disabling weak cryptographic ciphers (like 3DES) and protocols (like TLS 1.0/1.1).
- **Implementation:** The `security` block should be used to disable insecure protocols and ciphers.
- **Validation:** `CKV2_AZURE_2: "Ensure API Management disables weak ciphers and protocols"`

### AP-010: Use Named Values from Key Vault

- **MCSB:** IM-3 (Identity Management)
- **Priority:** **Must**
- **Relevance:** Secrets (like backend keys or tokens) should never be stored directly in APIM policies or as plain text named values. They must be sourced from Key Vault.
- **Implementation:** The `azurerm_api_management_named_value` resource should have its `value_from_key_vault` property set.
- **Validation:** `CKV2_AZURE_6: "Ensure API Management named values are not plain text"`
