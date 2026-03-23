"""
Knowledge Base Loader for the Security Analyzer.

This module loads and parses the machine-readable knowledge base
containing MCSB controls and validation rules.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ControlValidation:
    """Validation configuration for a control."""
    checkov_rules: List[str]
    custom_check: str
    required_attributes: List[str]
    forbidden_attributes: List[str]
    required_blocks: List[str]
    forbidden_blocks: List[str]


@dataclass
class ControlEvidence:
    """Evidence configuration for a control."""
    type: str
    required_blocks: List[str]
    required_categories: List[str]
    evidence_format: str


@dataclass
class MCSBControl:
    """MCSB Control definition."""
    control_id: str
    service: str
    resource_types: List[str]
    priority: str
    severity: str
    description: str
    requirement_type: str
    implementation: str
    automation_type: str
    validation: ControlValidation
    evidence: ControlEvidence


class KnowledgeBaseLoader:
    """Loader for the machine-readable knowledge base."""

    def __init__(self, kb_path: Optional[str] = None):
        """
        Initialize the knowledge base loader.

        Args:
            kb_path: Path to the knowledge base file (optional)
        """
        self.kb_path = kb_path or self._get_default_kb_path()
        self.controls: Dict[str, MCSBControl] = {}
        self._load_controls()

    def _get_default_kb_path(self) -> str:
        """Get the default path to the knowledge base file."""
        return str(Path(__file__).parent / "controls.yaml")

    def _load_controls(self) -> None:
        """Load controls from the knowledge base file."""
        try:
            with open(self.kb_path, 'r') as f:
                kb_data = yaml.safe_load(f)

            # Skip version and schema entries
            for control_id, control_data in kb_data.items():
                if control_id in ['version', 'schema']:
                    continue

                self.controls[control_id] = self._parse_control(control_id, control_data)

        except FileNotFoundError:
            print(f"Warning: Knowledge base file not found at {self.kb_path}")
        except yaml.YAMLError as e:
            print(f"Error parsing knowledge base YAML: {e}")
        except Exception as e:
            print(f"Error loading knowledge base: {e}")

    def _parse_control(self, control_id: str, control_data: Dict[str, Any]) -> MCSBControl:
        """Parse a control definition from YAML data."""
        validation_data = control_data.get('validation', {})
        evidence_data = control_data.get('evidence', {})

        return MCSBControl(
            control_id=control_id,
            service=control_data.get('service', ''),
            resource_types=control_data.get('resource_types', []),
            priority=control_data.get('priority', ''),
            severity=control_data.get('severity', ''),
            description=control_data.get('description', ''),
            requirement_type=control_data.get('requirement_type', ''),
            implementation=control_data.get('implementation', ''),
            automation_type=control_data.get('automation_type', ''),
            validation=ControlValidation(
                checkov_rules=validation_data.get('checkov_rules', []),
                custom_check=validation_data.get('custom_check', ''),
                required_attributes=validation_data.get('required_attributes', []),
                forbidden_attributes=validation_data.get('forbidden_attributes', []),
                required_blocks=validation_data.get('required_blocks', []),
                forbidden_blocks=validation_data.get('forbidden_blocks', [])
            ),
            evidence=ControlEvidence(
                type=evidence_data.get('type', ''),
                required_blocks=evidence_data.get('required_blocks', []),
                required_categories=evidence_data.get('required_categories', []),
                evidence_format=evidence_data.get('evidence_format', '')
            )
        )

    def get_control(self, control_id: str) -> Optional[MCSBControl]:
        """
        Get a control by its ID.

        Args:
            control_id: Control ID (e.g., "ST-008", "KV-001")

        Returns:
            Control definition or None if not found
        """
        return self.controls.get(control_id)

    def get_controls_by_service(self, service: str) -> List[MCSBControl]:
        """
        Get all controls for a specific service.

        Args:
            service: Service name (e.g., "Storage", "Key Vault")

        Returns:
            List of controls for the service
        """
        return [
            control for control in self.controls.values()
            if control.service.lower() == service.lower()
        ]

    def get_controls_by_resource_type(self, resource_type: str) -> List[MCSBControl]:
        """
        Get all controls that apply to a specific resource type.

        Args:
            resource_type: Terraform resource type (e.g., "azurerm_storage_account")

        Returns:
            List of applicable controls
        """
        return [
            control for control in self.controls.values()
            if resource_type in control.resource_types
        ]

    def get_all_controls(self) -> List[MCSBControl]:
        """Get all controls in the knowledge base."""
        return list(self.controls.values())

    def get_control_ids(self) -> List[str]:
        """Get all control IDs."""
        return list(self.controls.keys())

    def get_services(self) -> List[str]:
        """Get all unique services in the knowledge base."""
        return list(set(control.service for control in self.controls.values()))

    def get_resource_types(self) -> List[str]:
        """Get all unique resource types in the knowledge base."""
        resource_types = set()
        for control in self.controls.values():
            resource_types.update(control.resource_types)
        return list(resource_types)

    def validate_control_structure(self, control_id: str) -> bool:
        """
        Validate that a control has the required structure.

        Args:
            control_id: Control ID to validate

        Returns:
            True if valid, False otherwise
        """
        control = self.get_control(control_id)
        if not control:
            return False

        required_fields = [
            'control_id', 'service', 'resource_types', 'severity',
            'description', 'requirement_type', 'validation'
        ]

        for field in required_fields:
            if not getattr(control, field):
                return False

        return True

    def get_checkov_mapping(self) -> Dict[str, List[str]]:
        """
        Get mapping of Checkov rules to controls.

        Returns:
            Dictionary mapping Checkov rule IDs to control IDs
        """
        mapping = {}
        for control in self.controls.values():
            for checkov_rule in control.validation.checkov_rules:
                if checkov_rule not in mapping:
                    mapping[checkov_rule] = []
                mapping[checkov_rule].append(control.control_id)
        return mapping

    def get_custom_checks(self) -> Dict[str, str]:
        """
        Get mapping of custom check functions to controls.

        Returns:
            Dictionary mapping custom check function names to control IDs
        """
        checks = {}
        for control in self.controls.values():
            if control.validation.custom_check:
                checks[control.validation.custom_check] = control.control_id
        return checks

    def export_to_json(self, output_path: str) -> None:
        """
        Export the knowledge base to JSON format.

        Args:
            output_path: Path to output JSON file
        """
        export_data = {
            "version": "1.0",
            "controls": {}
        }

        for control_id, control in self.controls.items():
            export_data["controls"][control_id] = {
                "control_id": control.control_id,
                "service": control.service,
                "resource_types": control.resource_types,
                "priority": control.priority,
                "severity": control.severity,
                "description": control.description,
                "requirement_type": control.requirement_type,
                "implementation": control.implementation,
                "automation_type": control.automation_type,
                "validation": {
                    "checkov_rules": control.validation.checkov_rules,
                    "custom_check": control.validation.custom_check,
                    "required_attributes": control.validation.required_attributes,
                    "forbidden_attributes": control.validation.forbidden_attributes,
                    "required_blocks": control.validation.required_blocks,
                    "forbidden_blocks": control.validation.forbidden_blocks
                },
                "evidence": {
                    "type": control.evidence.type,
                    "required_blocks": control.evidence.required_blocks,
                    "required_categories": control.evidence.required_categories,
                    "evidence_format": control.evidence.evidence_format
                }
            }

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base.

        Returns:
            Dictionary with statistics
        """
        total_controls = len(self.controls)
        services = self.get_services()
        resource_types = self.get_resource_types()

        severity_counts = {}
        for control in self.controls.values():
            severity = control.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "total_controls": total_controls,
            "services_count": len(services),
            "resource_types_count": len(resource_types),
            "services": services,
            "resource_types": resource_types,
            "severity_distribution": severity_counts,
            "checkov_rules_count": len(self.get_checkov_mapping()),
            "custom_checks_count": len(self.get_custom_checks())
        }
