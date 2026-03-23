"""
MCSB Validator for the Security Analyzer.

This module validates Terraform resources against MCSB (Microsoft Cloud Security Benchmark)
security controls.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class Finding:
    """Security finding from validation."""
    resource_type: str
    resource_name: str
    control_id: str
    severity: str
    description: str
    recommendation: str
    file: str
    line: int
    service: str


class MCSBValidator:
    """Validator for MCSB security controls."""

    def __init__(self):
        """Initialize the MCSB validator."""
        self.findings = []
        self.controls = self._load_mcsb_controls()

    def _load_mcsb_controls(self) -> Dict[str, Dict[str, Any]]:
        """
        Load MCSB controls from the knowledge base.

        Returns:
            Dictionary of MCSB controls
        """
        try:
            from ..knowledge_base.kb_loader import KnowledgeBaseLoader
            kb_loader = KnowledgeBaseLoader()

            controls = {}
            for control in kb_loader.get_all_controls():
                # Import validation functions
                from .validation_functions import get_validation_function

                # Get the validation function
                validation_function = get_validation_function(control.validation.custom_check) if control.validation.custom_check else None

                controls[control.control_id] = {
                    "id": control.control_id,
                    "name": control.description,
                    "description": control.description,
                    "severity": control.severity,
                    "service": control.service,
                    "check_function": validation_function,
                    "required_attributes": control.validation.required_attributes,
                    "forbidden_attributes": control.validation.forbidden_attributes,
                    "required_blocks": control.validation.required_blocks,
                    "forbidden_blocks": control.validation.forbidden_blocks
                }

            return controls

        except ImportError:
            # Fallback to hardcoded controls if knowledge base not available
            return {
                "KV-001": {
                    "id": "KV-001",
                    "name": "Key Vault Soft Delete",
                    "description": "Key Vault should have soft delete enabled",
                    "severity": "HIGH",
                    "service": "Key Vault",
                    "check_function": self._check_key_vault_soft_delete
                },
                "ST-001": {
                    "id": "ST-001",
                    "name": "Storage Account Encryption",
                    "description": "Storage accounts should have encryption enabled",
                    "severity": "MEDIUM",
                    "service": "Storage",
                    "check_function": self._check_storage_encryption
                },
                "VM-001": {
                    "id": "VM-001",
                    "name": "VM Disk Encryption",
                    "description": "Virtual machine disks should be encrypted",
                    "severity": "HIGH",
                    "service": "Virtual Machine",
                    "check_function": self._check_vm_disk_encryption
                },
                "NSG-001": {
                    "id": "NSG-001",
                    "name": "Network Security Group Rules",
                    "description": "NSG rules should not allow unrestricted access",
                    "severity": "HIGH",
                    "service": "Network Security",
                    "check_function": self._check_nsg_rules
                }
            }

    def validate_resources(
        self,
        resources: List[Dict[str, Any]],
        controls: str = "mcsb",
        services: Optional[List[str]] = None
    ) -> List[Finding]:
        """
        Validate resources against MCSB controls.

        Args:
            resources: List of parsed Terraform resources
            controls: Controls to validate against
            services: Specific services to validate (optional)

        Returns:
            List of security findings
        """
        self.findings = []

        for resource in resources:
            resource_type = resource.get('type', '')
            service = resource.get('service', '')

            # Skip if services filter is specified and this service is not included
            if services and service not in services:
                continue

            # Find relevant controls for this resource type/service
            relevant_controls = self._get_relevant_controls(resource_type, service)

            for control_id in relevant_controls:
                control = self.controls[control_id]

                # Run the check function
                if control.get('check_function'):
                    try:
                        result = control['check_function'](resource)
                        if result:
                            finding = Finding(
                                resource_type=resource_type,
                                resource_name=resource.get('name', ''),
                                control_id=control_id,
                                severity=control['severity'],
                                description=control['description'],
                                recommendation=result,
                                file=resource.get('file', ''),
                                line=resource.get('line', 0),
                                service=service
                            )
                            self.findings.append(finding)
                    except Exception as e:
                        print(f"⚠️  Error validating {resource_type}.{resource.get('name', '')}: {e}")

        return self.findings

    def _get_relevant_controls(self, resource_type: str, service: str) -> List[str]:
        """
        Get relevant controls for a resource type and service.

        Args:
            resource_type: Terraform resource type
            service: Azure service name

        Returns:
            List of relevant control IDs
        """
        relevant_controls = []

        for control_id, control in self.controls.items():
            # Match by service
            if control.get('service') == service:
                relevant_controls.append(control_id)

            # Match by resource type patterns
            if resource_type.startswith('azurerm_key_vault') and control_id.startswith('KV-'):
                relevant_controls.append(control_id)
            elif resource_type.startswith('azurerm_storage') and control_id.startswith('ST-'):
                relevant_controls.append(control_id)
            elif resource_type.startswith('azurerm_virtual_machine') and control_id.startswith('VM-'):
                relevant_controls.append(control_id)
            elif resource_type.startswith('azurerm_network_security_group') and control_id.startswith('NSG-'):
                relevant_controls.append(control_id)

        return list(set(relevant_controls))  # Remove duplicates

    def _check_key_vault_soft_delete(self, resource: Dict[str, Any]) -> Optional[str]:
        """
        Check if Key Vault has soft delete enabled.

        Args:
            resource: Terraform resource dictionary

        Returns:
            Recommendation if check fails, None if passes
        """
        attributes = resource.get('attributes', {})

        # Check if soft_delete_enabled is set to true
        soft_delete = attributes.get('soft_delete_enabled', 'false').lower()

        if soft_delete != 'true':
            return "Enable soft delete by setting soft_delete_enabled = true to protect against accidental deletion"

        return None

    def _check_storage_encryption(self, resource: Dict[str, Any]) -> Optional[str]:
        """
        Check if Storage Account has encryption enabled.

        Args:
            resource: Terraform resource dictionary

        Returns:
            Recommendation if check fails, None if passes
        """
        attributes = resource.get('attributes', {})

        # Check encryption settings
        encryption_type = attributes.get('encryption_type', 'Service')

        if encryption_type.lower() != 'service':
            return "Enable encryption by setting encryption_type = 'Service' for data protection"

        return None

    def _check_vm_disk_encryption(self, resource: Dict[str, Any]) -> Optional[str]:
        """
        Check if Virtual Machine disks are encrypted.

        Args:
            resource: Terraform resource dictionary

        Returns:
            Recommendation if check fails, None if passes
        """
        attributes = resource.get('attributes', {})

        # Check if os_disk encryption is enabled
        os_disk = attributes.get('os_disk', {})
        if isinstance(os_disk, dict):
            encryption_settings = os_disk.get('encryption_settings', {})
            if not encryption_settings:
                return "Enable disk encryption by configuring os_disk.encryption_settings for data protection"

        return None

    def _check_nsg_rules(self, resource: Dict[str, Any]) -> Optional[str]:
        """
        Check if NSG rules allow unrestricted access.

        Args:
            resource: Terraform resource dictionary

        Returns:
            Recommendation if check fails, None if passes
        """
        attributes = resource.get('attributes', {})

        # Check security rules
        security_rules = attributes.get('security_rule', [])

        for rule in security_rules:
            if isinstance(rule, dict):
                # Check for unrestricted access (0.0.0.0/0 or * for source)
                source_address_prefix = rule.get('source_address_prefix', '').lower()
                destination_port_range = rule.get('destination_port_range', '')

                if (source_address_prefix in ['0.0.0.0/0', '*'] and
                    destination_port_range in ['*', '22', '3389']):  # Common risky ports
                    return f"Restrict NSG rule '{rule.get('name', 'unnamed')}' to specific IP ranges instead of allowing access from anywhere"

        return None

    def get_findings_summary(self) -> Dict[str, Any]:
        """
        Get summary of findings.

        Returns:
            Summary dictionary
        """
        if not self.findings:
            return {
                "total_findings": 0,
                "by_severity": {},
                "by_service": {},
                "by_control": {}
            }

        severity_counts = {}
        service_counts = {}
        control_counts = {}

        for finding in self.findings:
            # Count by severity
            severity = finding.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # Count by service
            service = finding.service
            service_counts[service] = service_counts.get(service, 0) + 1

            # Count by control
            control_id = finding.control_id
            control_counts[control_id] = control_counts.get(control_id, 0) + 1

        return {
            "total_findings": len(self.findings),
            "by_severity": severity_counts,
            "by_service": service_counts,
            "by_control": control_counts
        }
