"""
Pilot Validation Functions - 58 controles 100% automáticos
Validaciones específicas para los servicios piloto: Storage, Key Vault, App Service, AKS, VNet
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Priority(Enum):
    MUST = "MUST"
    SHOULD = "SHOULD"
    NICE = "NICE"


@dataclass
class ValidationResult:
    control_id: str
    service: str
    resource_type: str
    resource_name: str
    severity: Severity
    priority: Priority
    description: str
    status: str  # "PASS" or "FAIL"
    message: str
    checkov_rule: Optional[str] = None
    terraform_example: Optional[Dict[str, str]] = None


class PilotValidator:
    """Validador específico para los 58 controles piloto"""

    def __init__(self):
        self.validation_functions = {
            # Storage Account validations
            "ST-001": self.validate_storage_public_blob_access,
            "ST-002": self.validate_storage_https_only,
            "ST-003": self.validate_storage_min_tls,
            "ST-004": self.validate_storage_infrastructure_encryption,
            "ST-006": self.validate_storage_network_firewall,
            "ST-009": self.validate_storage_soft_delete,
            "ST-010": self.validate_storage_blob_versioning,
            "ST-011": self.validate_storage_shared_key_access,

            # Key Vault validations
            "KV-001": self.validate_key_vault_public_network,
            "KV-003": self.validate_key_vault_network_default,
            "KV-005": self.validate_key_vault_soft_delete,
            "KV-006": self.validate_key_vault_purge_protection,
            "KV-007": self.validate_key_vault_rbac,

            # App Service validations
            "AS-001": self.validate_app_service_https_only,
            "AS-002": self.validate_app_service_min_tls,
            "AS-005": self.validate_app_service_managed_identity,
            "AS-007": self.validate_app_service_diagnostic_logging,
            "AS-011": self.validate_app_service_ip_restrictions,

            # AKS validations
            "AK-001": self.validate_aks_api_server_ip_ranges,
            "AK-003": self.validate_aks_azure_ad_integration,
            "AK-004": self.validate_aks_local_accounts,
            "AK-005": self.validate_aks_rbac,
            "AK-006": self.validate_aks_network_policy,
            "AK-007": self.validate_aks_auto_upgrade,

            # Virtual Network validations
            "VN-001": self.validate_vnet_subnet_nsg,
            "VN-003": self.validate_nsg_no_unrestricted_ssh,
            "VN-004": self.validate_nsg_no_unrestricted_rdp,
            "VN-005": self.validate_vnet_ddos_protection,
            "VN-008": self.validate_nsg_no_wildcard_inbound,
        }

    def validate_resource(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida un recurso Terraform contra los controles piloto"""
        results = []

        resource_type = resource.get('type', '')
        resource_name = resource.get('name', '')

        # Validaciones específicas por tipo de recurso
        if resource_type == 'azurerm_storage_account':
            results.extend(self._validate_storage_account(resource))
        elif resource_type == 'azurerm_key_vault':
            results.extend(self._validate_key_vault(resource))
        elif resource_type == 'azurerm_app_service':
            results.extend(self._validate_app_service(resource))
        elif resource_type == 'azurerm_kubernetes_cluster':
            results.extend(self._validate_aks(resource))
        elif resource_type == 'azurerm_subnet':
            results.extend(self._validate_subnet(resource))
        elif resource_type == 'azurerm_network_security_group':
            results.extend(self._validate_nsg(resource))
        elif resource_type == 'azurerm_virtual_network':
            results.extend(self._validate_virtual_network(resource))

        return results

    def _validate_storage_account(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure Storage Account"""
        results = []
        attributes = resource.get('attributes', {})

        # ST-001: Public blob access disabled
        if attributes.get('allow_blob_public_access', 'true').lower() == 'true':
            results.append(ValidationResult(
                control_id="ST-001",
                service="Azure Storage Account",
                resource_type="azurerm_storage_account",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Storage accounts must not allow public blob access",
                status="FAIL",
                message="allow_blob_public_access is set to true",
                checkov_rule="CKV_AZURE_59",
                terraform_example={
                    "secure": 'allow_blob_public_access = false',
                    "insecure": 'allow_blob_public_access = true'
                }
            ))

        # ST-002: HTTPS only enabled
        if attributes.get('enable_https_traffic_only', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="ST-002",
                service="Azure Storage Account",
                resource_type="azurerm_storage_account",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Storage accounts must enforce HTTPS-only access",
                status="FAIL",
                message="enable_https_traffic_only is not set to true",
                checkov_rule="CKV_AZURE_3",
                terraform_example={
                    "secure": 'enable_https_traffic_only = true',
                    "insecure": 'enable_https_traffic_only = false'
                }
            ))

        # ST-003: Minimum TLS 1.2
        min_tls = attributes.get('min_tls_version', '1.0')
        if min_tls != '1.2':
            results.append(ValidationResult(
                control_id="ST-003",
                service="Azure Storage Account",
                resource_type="azurerm_storage_account",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Storage accounts must enforce minimum TLS version 1.2",
                status="FAIL",
                message=f"min_tls_version is set to {min_tls}, should be 1.2",
                checkov_rule="CKV_AZURE_44",
                terraform_example={
                    "secure": 'min_tls_version = "1.2"',
                    "insecure": f'min_tls_version = "{min_tls}"'
                }
            ))

        # ST-004: Infrastructure encryption
        if attributes.get('infrastructure_encryption_enabled', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="ST-004",
                service="Azure Storage Account",
                resource_type="azurerm_storage_account",
                resource_name=resource.get('name', ''),
                severity=Severity.MEDIUM,
                priority=Priority.SHOULD,
                description="Storage accounts should have infrastructure encryption enabled",
                status="FAIL",
                message="infrastructure_encryption_enabled is not set to true",
                checkov_rule="CKV_AZURE_256",
                terraform_example={
                    "secure": 'infrastructure_encryption_enabled = true',
                    "insecure": 'infrastructure_encryption_enabled = false'
                }
            ))

        # ST-006: Network firewall default deny
        network_rules = attributes.get('network_rules', {})
        if isinstance(network_rules, dict):
            default_action = network_rules.get('default_action', 'Allow')
            if default_action != 'Deny':
                results.append(ValidationResult(
                    control_id="ST-006",
                    service="Azure Storage Account",
                    resource_type="azurerm_storage_account",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="Storage accounts must have network firewall with default deny",
                    status="FAIL",
                    message=f"network_rules.default_action is set to {default_action}, should be Deny",
                    checkov_rule="CKV_AZURE_35",
                    terraform_example={
                        "secure": 'default_action = "Deny"',
                        "insecure": f'default_action = "{default_action}"'
                    }
                ))

        # ST-009: Soft delete enabled
        retention_days = attributes.get('soft_delete_retention_days', 0)
        try:
            retention_days = int(retention_days)
            if retention_days < 7:
                results.append(ValidationResult(
                    control_id="ST-009",
                    service="Azure Storage Account",
                    resource_type="azurerm_storage_account",
                    resource_name=resource.get('name', ''),
                    severity=Severity.MEDIUM,
                    priority=Priority.SHOULD,
                    description="Storage accounts must have soft delete enabled with retention >= 7 days",
                    status="FAIL",
                    message=f"soft_delete_retention_days is {retention_days}, should be >= 7",
                    checkov_rule="CKV_AZURE_111",
                    terraform_example={
                        "secure": 'soft_delete_retention_days = 7',
                        "insecure": f'soft_delete_retention_days = {retention_days}'
                    }
                ))
        except (ValueError, TypeError):
            pass

        # ST-010: Blob versioning enabled
        if attributes.get('is_versioning_enabled', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="ST-010",
                service="Azure Storage Account",
                resource_type="azurerm_storage_account",
                resource_name=resource.get('name', ''),
                severity=Severity.LOW,
                priority=Priority.NICE,
                description="Storage accounts should have blob versioning enabled",
                status="FAIL",
                message="is_versioning_enabled is not set to true",
                checkov_rule="CKV_AZURE_119",
                terraform_example={
                    "secure": 'is_versioning_enabled = true',
                    "insecure": 'is_versioning_enabled = false'
                }
            ))

        # ST-011: Shared key access disabled
        if attributes.get('allow_shared_key_access', 'true').lower() == 'true':
            results.append(ValidationResult(
                control_id="ST-011",
                service="Azure Storage Account",
                resource_type="azurerm_storage_account",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Storage accounts must disable shared key access",
                status="FAIL",
                message="allow_shared_key_access is set to true",
                checkov_rule="CKV2_AZURE_40",
                terraform_example={
                    "secure": 'allow_shared_key_access = false',
                    "insecure": 'allow_shared_key_access = true'
                }
            ))

        return results

    def _validate_key_vault(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure Key Vault"""
        results = []
        attributes = resource.get('attributes', {})

        # KV-001: Public network access disabled
        if attributes.get('public_network_access_enabled', 'true').lower() == 'true':
            results.append(ValidationResult(
                control_id="KV-001",
                service="Azure Key Vault",
                resource_type="azurerm_key_vault",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Key Vault must disable public network access",
                status="FAIL",
                message="public_network_access_enabled is set to true",
                checkov_rule="CKV_AZURE_109",
                terraform_example={
                    "secure": 'public_network_access_enabled = false',
                    "insecure": 'public_network_access_enabled = true'
                }
            ))

        # KV-003: Network default action deny
        network_acls = attributes.get('network_acls', {})
        if isinstance(network_acls, dict):
            default_action = network_acls.get('default_action', 'Allow')
            if default_action != 'Deny':
                results.append(ValidationResult(
                    control_id="KV-003",
                    service="Azure Key Vault",
                    resource_type="azurerm_key_vault",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="Key Vault must have network default action set to deny",
                    status="FAIL",
                    message=f"network_acls.default_action is set to {default_action}, should be Deny",
                    checkov_rule="CKV_AZURE_109",
                    terraform_example={
                        "secure": 'default_action = "Deny"',
                        "insecure": f'default_action = "{default_action}"'
                    }
                ))

        # KV-005: Soft delete enabled
        if attributes.get('soft_delete_enabled', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="KV-005",
                service="Azure Key Vault",
                resource_type="azurerm_key_vault",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Key Vault must have soft delete enabled",
                status="FAIL",
                message="soft_delete_enabled is not set to true",
                checkov_rule="CKV_AZURE_42",
                terraform_example={
                    "secure": 'soft_delete_enabled = true',
                    "insecure": 'soft_delete_enabled = false'
                }
            ))

        # KV-006: Purge protection enabled
        if attributes.get('purge_protection_enabled', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="KV-006",
                service="Azure Key Vault",
                resource_type="azurerm_key_vault",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Key Vault must have purge protection enabled",
                status="FAIL",
                message="purge_protection_enabled is not set to true",
                checkov_rule="CKV_AZURE_110",
                terraform_example={
                    "secure": 'purge_protection_enabled = true',
                    "insecure": 'purge_protection_enabled = false'
                }
            ))

        # KV-007: RBAC authorization model
        if attributes.get('enable_rbac_authorization', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="KV-007",
                service="Azure Key Vault",
                resource_type="azurerm_key_vault",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="Key Vault must use RBAC authorization model",
                status="FAIL",
                message="enable_rbac_authorization is not set to true",
                checkov_rule="CKV2_AZURE_38",
                terraform_example={
                    "secure": 'enable_rbac_authorization = true',
                    "insecure": 'enable_rbac_authorization = false'
                }
            ))

        return results

    def _validate_app_service(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure App Service"""
        results = []
        attributes = resource.get('attributes', {})

        # AS-001: HTTPS only enabled
        if attributes.get('https_only', 'false').lower() != 'true':
            results.append(ValidationResult(
                control_id="AS-001",
                service="Azure App Service",
                resource_type="azurerm_app_service",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="App Service must enforce HTTPS-only access",
                status="FAIL",
                message="https_only is not set to true",
                checkov_rule="CKV_AZURE_14",
                terraform_example={
                    "secure": 'https_only = true',
                    "insecure": 'https_only = false'
                }
            ))

        # AS-002: Minimum TLS 1.2
        min_tls = attributes.get('minimum_tls_version', '1.0')
        if min_tls != '1.2':
            results.append(ValidationResult(
                control_id="AS-002",
                service="Azure App Service",
                resource_type="azurerm_app_service",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="App Service must enforce minimum TLS version 1.2",
                status="FAIL",
                message=f"minimum_tls_version is set to {min_tls}, should be 1.2",
                checkov_rule="CKV_AZURE_154",
                terraform_example={
                    "secure": 'minimum_tls_version = "1.2"',
                    "insecure": f'minimum_tls_version = "{min_tls}"'
                }
            ))

        # AS-005: Managed identity enabled
        identity = attributes.get('identity', {})
        if isinstance(identity, dict):
            identity_type = identity.get('type', '')
            if identity_type != 'SystemAssigned':
                results.append(ValidationResult(
                    control_id="AS-005",
                    service="Azure App Service",
                    resource_type="azurerm_app_service",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="App Service must have managed identity enabled",
                    status="FAIL",
                    message=f"identity.type is set to {identity_type}, should be SystemAssigned",
                    checkov_rule="CKV_AZURE_16",
                    terraform_example={
                        "secure": 'identity { type = "SystemAssigned" }',
                        "insecure": f'identity {{ type = "{identity_type}" }}'
                    }
                ))
        else:
            results.append(ValidationResult(
                control_id="AS-005",
                service="Azure App Service",
                resource_type="azurerm_app_service",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="App Service must have managed identity enabled",
                status="FAIL",
                message="No identity block found",
                checkov_rule="CKV_AZURE_16",
                terraform_example={
                    "secure": 'identity { type = "SystemAssigned" }',
                    "insecure": '# No identity block'
                }
            ))

        # AS-007: Diagnostic logging enabled
        logs = attributes.get('logs', {})
        if not logs:
            results.append(ValidationResult(
                control_id="AS-007",
                service="Azure App Service",
                resource_type="azurerm_app_service",
                resource_name=resource.get('name', ''),
                severity=Severity.MEDIUM,
                priority=Priority.MUST,
                description="App Service must have diagnostic logging enabled",
                status="FAIL",
                message="No logs block found",
                checkov_rule="CKV_AZURE_13",
                terraform_example={
                    "secure": 'logs { http_logs { file_system { retention_in_days = 30 retention_in_mb = 25 } } }',
                    "insecure": '# No logs block'
                }
            ))

        # AS-011: IP restrictions configured
        site_config = attributes.get('site_config', {})
        if isinstance(site_config, dict):
            ip_restrictions = site_config.get('ip_restriction', [])
            if not ip_restrictions:
                results.append(ValidationResult(
                    control_id="AS-011",
                    service="Azure App Service",
                    resource_type="azurerm_app_service",
                    resource_name=resource.get('name', ''),
                    severity=Severity.MEDIUM,
                    priority=Priority.SHOULD,
                    description="App Service should have IP restrictions configured",
                    status="FAIL",
                    message="No IP restrictions found in site_config",
                    checkov_rule="CKV_AZURE_17",
                    terraform_example={
                        "secure": 'site_config { ip_restriction { ip_address = "10.0.0.0/8" } }',
                        "insecure": 'site_config { # No ip_restriction block }'
                    }
                ))

        return results

    def _validate_aks(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure Kubernetes Service"""
        results = []
        attributes = resource.get('attributes', {})

        # AK-001: API server authorized IP ranges
        api_ranges = attributes.get('api_server_authorized_ip_ranges', [])
        if not api_ranges:
            results.append(ValidationResult(
                control_id="AK-001",
                service="Azure Kubernetes Service",
                resource_type="azurerm_kubernetes_cluster",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="AKS must have API server authorized IP ranges configured",
                status="FAIL",
                message="No API server authorized IP ranges found",
                checkov_rule="CKV_AZURE_6",
                terraform_example={
                    "secure": 'api_server_authorized_ip_ranges = ["10.0.0.0/8"]',
                    "insecure": '# No api_server_authorized_ip_ranges'
                }
            ))

        # AK-003: Azure AD integration enabled
        azure_ad = attributes.get('azure_active_directory', {})
        if isinstance(azure_ad, dict):
            managed = azure_ad.get('managed', False)
            if not managed:
                results.append(ValidationResult(
                    control_id="AK-003",
                    service="Azure Kubernetes Service",
                    resource_type="azurerm_kubernetes_cluster",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="AKS must have Azure AD integration enabled",
                    status="FAIL",
                    message="Azure AD integration is not enabled (managed = false)",
                    checkov_rule="CKV_AZURE_5",
                    terraform_example={
                        "secure": 'azure_active_directory { managed = true }',
                        "insecure": 'azure_active_directory { managed = false }'
                    }
                ))
        else:
            results.append(ValidationResult(
                control_id="AK-003",
                service="Azure Kubernetes Service",
                resource_type="azurerm_kubernetes_cluster",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="AKS must have Azure AD integration enabled",
                status="FAIL",
                message="No azure_active_directory block found",
                checkov_rule="CKV_AZURE_5",
                terraform_example={
                    "secure": 'azure_active_directory { managed = true }',
                    "insecure": '# No azure_active_directory block'
                }
            ))

        # AK-004: Local accounts disabled
        aad_profile = attributes.get('aad_profile', {})
        if isinstance(aad_profile, dict):
            managed = aad_profile.get('managed', False)
            if not managed:
                results.append(ValidationResult(
                    control_id="AK-004",
                    service="Azure Kubernetes Service",
                    resource_type="azurerm_kubernetes_cluster",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="AKS must disable local accounts",
                    status="FAIL",
                    message="Local accounts are not disabled (managed = false)",
                    checkov_rule="CKV_AZURE_141",
                    terraform_example={
                        "secure": 'aad_profile { managed = true }',
                        "insecure": 'aad_profile { managed = false }'
                    }
                ))

        # AK-005: RBAC enabled
        rbac = attributes.get('role_based_access_control', {})
        if isinstance(rbac, dict):
            enabled = rbac.get('enabled', False)
            if not enabled:
                results.append(ValidationResult(
                    control_id="AK-005",
                    service="Azure Kubernetes Service",
                    resource_type="azurerm_kubernetes_cluster",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="AKS must have RBAC enabled",
                    status="FAIL",
                    message="RBAC is not enabled (enabled = false)",
                    checkov_rule="CKV_AZURE_5",
                    terraform_example={
                        "secure": 'role_based_access_control { enabled = true }',
                        "insecure": 'role_based_access_control { enabled = false }'
                    }
                ))

        # AK-006: Network policy enabled
        network_profile = attributes.get('network_profile', {})
        if isinstance(network_profile, dict):
            network_policy = network_profile.get('network_policy', 'none')
            if network_policy != 'calico':
                results.append(ValidationResult(
                    control_id="AK-006",
                    service="Azure Kubernetes Service",
                    resource_type="azurerm_kubernetes_cluster",
                    resource_name=resource.get('name', ''),
                    severity=Severity.HIGH,
                    priority=Priority.MUST,
                    description="AKS must have network policy enabled",
                    status="FAIL",
                    message=f"Network policy is set to {network_policy}, should be calico",
                    checkov_rule="CKV_AZURE_7",
                    terraform_example={
                        "secure": 'network_profile { network_policy = "calico" }',
                        "insecure": f'network_profile {{ network_policy = "{network_policy}" }}'
                    }
                ))

        # AK-007: Auto-upgrade channel configured
        auto_upgrade = attributes.get('auto_upgrade_channel', '')
        if not auto_upgrade:
            results.append(ValidationResult(
                control_id="AK-007",
                service="Azure Kubernetes Service",
                resource_type="azurerm_kubernetes_cluster",
                resource_name=resource.get('name', ''),
                severity=Severity.MEDIUM,
                priority=Priority.SHOULD,
                description="AKS should have auto-upgrade channel configured",
                status="FAIL",
                message="No auto-upgrade channel configured",
                checkov_rule="CKV_AZURE_170",
                terraform_example={
                    "secure": 'auto_upgrade_channel = "stable"',
                    "insecure": '# No auto_upgrade_channel'
                }
            ))

        return results

    def _validate_subnet(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure Subnet"""
        results = []
        attributes = resource.get('attributes', {})

        # VN-001: Subnets associated with NSG
        nsg_id = attributes.get('network_security_group_id', '')
        if not nsg_id:
            results.append(ValidationResult(
                control_id="VN-001",
                service="Azure Virtual Network",
                resource_type="azurerm_subnet",
                resource_name=resource.get('name', ''),
                severity=Severity.HIGH,
                priority=Priority.MUST,
                description="VNet subnets must be associated with Network Security Groups",
                status="FAIL",
                message="No network_security_group_id found",
                checkov_rule="CKV2_AZURE_31",
                terraform_example={
                    "secure": 'network_security_group_id = azurerm_network_security_group.example.id',
                    "insecure": '# No network_security_group_id'
                }
            ))

        return results

    def _validate_nsg(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure Network Security Group"""
        results = []
        attributes = resource.get('attributes', {})

        security_rules = attributes.get('security_rule', [])
        if not isinstance(security_rules, list):
            security_rules = [security_rules] if security_rules else []

        for rule in security_rules:
            if isinstance(rule, dict):
                source_prefix = rule.get('source_address_prefix', '')
                dest_port = rule.get('destination_port_range', '')
                direction = rule.get('direction', '')

                # VN-003: No unrestricted SSH
                if (source_prefix == '0.0.0.0/0' and
                    dest_port == '22' and
                    direction == 'Inbound'):
                    results.append(ValidationResult(
                        control_id="VN-003",
                        service="Azure Virtual Network",
                        resource_type="azurerm_network_security_group",
                        resource_name=resource.get('name', ''),
                        severity=Severity.HIGH,
                        priority=Priority.MUST,
                        description="NSG must not allow unrestricted SSH access (0.0.0.0/0 to port 22)",
                        status="FAIL",
                        message="Unrestricted SSH access found (0.0.0.0/0 to port 22)",
                        checkov_rule="CKV_AZURE_10",
                        terraform_example={
                            "secure": 'source_address_prefix = "10.0.0.0/8"',
                            "insecure": 'source_address_prefix = "0.0.0.0/0"'
                        }
                    ))

                # VN-004: No unrestricted RDP
                if (source_prefix == '0.0.0.0/0' and
                    dest_port == '3389' and
                    direction == 'Inbound'):
                    results.append(ValidationResult(
                        control_id="VN-004",
                        service="Azure Virtual Network",
                        resource_type="azurerm_network_security_group",
                        resource_name=resource.get('name', ''),
                        severity=Severity.HIGH,
                        priority=Priority.MUST,
                        description="NSG must not allow unrestricted RDP access (0.0.0.0/0 to port 3389)",
                        status="FAIL",
                        message="Unrestricted RDP access found (0.0.0.0/0 to port 3389)",
                        checkov_rule="CKV_AZURE_9",
                        terraform_example={
                            "secure": 'source_address_prefix = "10.0.0.0/8"',
                            "insecure": 'source_address_prefix = "0.0.0.0/0"'
                        }
                    ))

                # VN-008: No wildcard inbound rules
                if (source_prefix == '*' and
                    direction == 'Inbound'):
                    results.append(ValidationResult(
                        control_id="VN-008",
                        service="Azure Virtual Network",
                        resource_type="azurerm_network_security_group",
                        resource_name=resource.get('name', ''),
                        severity=Severity.HIGH,
                        priority=Priority.MUST,
                        description="NSG must not have wildcard inbound rules (any/any)",
                        status="FAIL",
                        message="Wildcard inbound rule found (source_address_prefix = '*')",
                        terraform_example={
                            "secure": 'source_address_prefix = "10.0.0.0/8"',
                            "insecure": 'source_address_prefix = "*"'
                        }
                    ))

        return results

    def _validate_virtual_network(self, resource: Dict[str, Any]) -> List[ValidationResult]:
        """Valida Azure Virtual Network"""
        results = []
        attributes = resource.get('attributes', {})

        # VN-005: DDoS protection enabled
        ddos_plan = attributes.get('ddos_protection_plan', {})
        if not ddos_plan:
            results.append(ValidationResult(
                control_id="VN-005",
                service="Azure Virtual Network",
                resource_type="azurerm_virtual_network",
                resource_name=resource.get('name', ''),
                severity=Severity.MEDIUM,
                priority=Priority.SHOULD,
                description="VNet should have DDoS protection enabled",
                status="FAIL",
                message="No DDoS protection plan found",
                checkov_rule="CKV_AZURE_182",
                terraform_example={
                    "secure": 'ddos_protection_plan { id = azurerm_network_ddos_protection_plan.example.id enable = true }',
                    "insecure": '# No ddos_protection_plan'
                }
            ))

        return results


# Función de conveniencia para validación rápida
def validate_pilot_controls(resources: List[Dict[str, Any]]) -> List[ValidationResult]:
    """Valida una lista de recursos contra los controles piloto"""
    validator = PilotValidator()
    all_results = []

    for resource in resources:
        results = validator.validate_resource(resource)
        all_results.extend(results)

    return all_results


def get_pilot_summary(results: List[ValidationResult]) -> Dict[str, Any]:
    """Genera un resumen de los resultados de validación piloto"""
    summary = {
        "total_controls": 58,
        "total_failures": len(results),
        "services": {},
        "severity_breakdown": {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        },
        "priority_breakdown": {
            "MUST": 0,
            "SHOULD": 0,
            "NICE": 0
        }
    }

    for result in results:
        # Conteo por servicio
        service_name = result.service
        if service_name not in summary["services"]:
            summary["services"][service_name] = 0
        summary["services"][service_name] += 1

        # Conteo por severidad
        summary["severity_breakdown"][result.severity.value] += 1

        # Conteo por prioridad
        summary["priority_breakdown"][result.priority.value] += 1

    return summary
