"""
Validation Functions for the Security Analyzer.

This module contains specific validation functions for different MCSB controls.
Each function validates a specific security requirement.
"""

from typing import Dict, Any, Optional, List


def validate_diagnostic_logging(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate ST-008: Diagnostic logging enabled.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    # Only validate for supported resource types
    supported_types = [
        'azurerm_storage_account',
        'azurerm_key_vault',
        'azurerm_sql_server',
        'azurerm_postgresql_server',
        'azurerm_mysql_server'
    ]

    if resource_type not in supported_types:
        return None

    attributes = resource.get('attributes', {})

    # Check if diagnostic_settings block exists
    diagnostic_settings = attributes.get('diagnostic_settings', [])

    if not diagnostic_settings:
        return f"Add diagnostic_settings block to enable diagnostic logging for {resource_type}"

    # Check if log_analytics_workspace_id is configured
    for setting in diagnostic_settings:
        if isinstance(setting, dict):
            workspace_id = setting.get('log_analytics_workspace_id')
            if not workspace_id:
                return f"Configure log_analytics_workspace_id in diagnostic_settings for {resource_type}"

    return None


def validate_key_vault_soft_delete(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate KV-001: Key Vault soft delete enabled.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type != 'azurerm_key_vault':
        return None

    attributes = resource.get('attributes', {})

    # Check soft_delete_enabled
    soft_delete = attributes.get('soft_delete_enabled', 'false').lower()
    if soft_delete != 'true':
        return "Enable soft delete by setting soft_delete_enabled = true to protect against accidental deletion"

    # Check purge_protection_enabled
    purge_protection = attributes.get('purge_protection_enabled', 'false').lower()
    if purge_protection != 'true':
        return "Enable purge protection by setting purge_protection_enabled = true for additional security"

    return None


def validate_storage_encryption(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate ST-001: Storage account encryption enabled.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type != 'azurerm_storage_account':
        return None

    attributes = resource.get('attributes', {})

    # Check enable_https_traffic_only
    https_only = attributes.get('enable_https_traffic_only', 'false').lower()
    if https_only != 'true':
        return "Enable HTTPS-only traffic by setting enable_https_traffic_only = true"

    # Check allow_blob_public_access (should be false)
    public_access = attributes.get('allow_blob_public_access', 'true').lower()
    if public_access == 'true':
        return "Disable public blob access by setting allow_blob_public_access = false"

    return None


def validate_vm_encryption(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate VM-001: Virtual Machine encryption enabled.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type not in ['azurerm_virtual_machine', 'azurerm_linux_virtual_machine', 'azurerm_windows_virtual_machine']:
        return None

    attributes = resource.get('attributes', {})

    # Check os_disk configuration
    os_disk = attributes.get('os_disk', {})
    if not os_disk:
        return "Configure os_disk settings for encryption"

    if isinstance(os_disk, dict):
        # Check caching
        caching = os_disk.get('caching', '').lower()
        if caching not in ['readonly', 'readwrite']:
            return "Set os_disk.caching to 'ReadOnly' or 'ReadWrite' for performance and security"

        # Check storage account type
        storage_type = os_disk.get('managed_disk_storage_account_type', '').lower()
        if storage_type not in ['premium_lrs', 'standard_ssd_lrs', 'premium_ssd_lrs']:
            return "Use premium or standard SSD storage types for better performance and security"

    return None


def validate_nsg_rules(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate NSG-001: Network Security Group rules restricted.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type != 'azurerm_network_security_group':
        return None

    attributes = resource.get('attributes', {})

    # Check security rules
    security_rules = attributes.get('security_rule', [])

    risky_ports = ['22', '3389', '23', '1433', '3306', '5432']  # SSH, RDP, Telnet, SQL ports

    for rule in security_rules:
        if isinstance(rule, dict):
            # Check for unrestricted source access
            source_prefix = rule.get('source_address_prefix', '').lower()
            source_prefixes = rule.get('source_address_prefixes', [])

            unrestricted_sources = ['0.0.0.0/0', '*', '::/0']

            has_unrestricted_source = (
                source_prefix in unrestricted_sources or
                any(prefix.lower() in unrestricted_sources for prefix in source_prefixes)
            )

            if has_unrestricted_source:
                # Check destination port
                port_range = rule.get('destination_port_range', '').lower()
                port_ranges = rule.get('destination_port_ranges', [])

                # Check if targeting risky ports
                targets_risky_ports = (
                    port_range in risky_ports or
                    any(str(port) in risky_ports for port in port_ranges) or
                    port_range == '*' or
                    any(str(range_val) == '*' for range_val in port_ranges)
                )

                if targets_risky_ports:
                    rule_name = rule.get('name', 'unnamed')
                    return f"Restrict NSG rule '{rule_name}' to specific IP ranges instead of allowing access from anywhere to port(s) {port_range or port_ranges}"

    return None


def validate_aks_rbac(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate AKS-001: AKS RBAC enabled.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type != 'azurerm_kubernetes_cluster':
        return None

    attributes = resource.get('attributes', {})

    # Check RBAC configuration
    rbac = attributes.get('role_based_access_control', {})
    if isinstance(rbac, dict):
        rbac_enabled = rbac.get('enabled', 'false').lower()
        if rbac_enabled != 'true':
            return "Enable RBAC by setting role_based_access_control.enabled = true"

    return None


def validate_sql_encryption(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate SQL-001: SQL Server encryption enabled.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type not in ['azurerm_sql_server', 'azurerm_mssql_server']:
        return None

    attributes = resource.get('attributes', {})

    # Check identity configuration
    identity = attributes.get('identity', {})
    if isinstance(identity, dict):
        identity_type = identity.get('type', '').lower()
        if identity_type != 'systemassigned':
            return "Enable system-assigned identity by setting identity.type = 'SystemAssigned' for encryption"

    return None


def validate_app_service_https(resource: Dict[str, Any]) -> Optional[str]:
    """
    Validate APP-001: App Service HTTPS only.

    Args:
        resource: Terraform resource dictionary

    Returns:
        Recommendation if validation fails, None if passes
    """
    resource_type = resource.get('type', '')

    if resource_type not in ['azurerm_app_service', 'azurerm_function_app']:
        return None

    attributes = resource.get('attributes', {})

    # Check https_only setting
    https_only = attributes.get('https_only', 'false').lower()
    if https_only != 'true':
        return "Enable HTTPS-only access by setting https_only = true"

    return None


# Mapping of validation functions to their names
VALIDATION_FUNCTIONS = {
    'validate_diagnostic_logging': validate_diagnostic_logging,
    'validate_key_vault_soft_delete': validate_key_vault_soft_delete,
    'validate_storage_encryption': validate_storage_encryption,
    'validate_vm_encryption': validate_vm_encryption,
    'validate_nsg_rules': validate_nsg_rules,
    'validate_aks_rbac': validate_aks_rbac,
    'validate_sql_encryption': validate_sql_encryption,
    'validate_app_service_https': validate_app_service_https,
}


def get_validation_function(function_name: str):
    """
    Get a validation function by name.

    Args:
        function_name: Name of the validation function

    Returns:
        Validation function or None if not found
    """
    return VALIDATION_FUNCTIONS.get(function_name)
