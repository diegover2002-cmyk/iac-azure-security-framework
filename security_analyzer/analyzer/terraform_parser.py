"""
Terraform Parser for the Security Analyzer.

This module parses Terraform files and extracts resource information
for security analysis.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import json


class TerraformParser:
    """Parser for Terraform files."""

    def __init__(self):
        """Initialize the Terraform parser."""
        self.resources = []
        self.variables = []
        self.outputs = []
        self.data_sources = []

    def parse_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """
        Parse all Terraform files in a directory.

        Args:
            directory: Path to directory containing Terraform files

        Returns:
            List of parsed resources
        """
        self.resources = []
        self.variables = []
        self.outputs = []
        self.data_sources = []

        # Find all .tf files
        tf_files = list(directory.glob("**/*.tf"))

        for tf_file in tf_files:
            self.parse_file(tf_file)

        return self.resources

    def parse_file(self, file_path: Path) -> None:
        """
        Parse a single Terraform file.

        Args:
            file_path: Path to Terraform file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse resources
            self._parse_resources(content, file_path)

            # Parse variables
            self._parse_variables(content, file_path)

            # Parse outputs
            self._parse_outputs(content, file_path)

            # Parse data sources
            self._parse_data_sources(content, file_path)

        except Exception as e:
            print(f"⚠️  Warning: Could not parse {file_path}: {e}")

    def _parse_resources(self, content: str, file_path: Path) -> None:
        """
        Parse resource blocks from Terraform content.

        Args:
            content: Terraform file content
            file_path: Path to the file being parsed
        """
        # Regex to match resource blocks
        resource_pattern = r'resource\s+["\']?([^"\'\s]+)["\']?\s+["\']?([^"\'\s]+)["\']?\s*{([^}]+)}'

        matches = re.finditer(resource_pattern, content, re.DOTALL)

        for match in matches:
            resource_type = match.group(1)
            resource_name = match.group(2)
            resource_body = match.group(3)

            # Extract attributes
            attributes = self._parse_attributes(resource_body)

            # Determine Azure service from resource type
            service = self._get_azure_service(resource_type)

            resource = {
                "type": resource_type,
                "name": resource_name,
                "service": service,
                "file": str(file_path),
                "line": self._get_line_number(content, match.start()),
                "attributes": attributes,
                "block": resource_body.strip()
            }

            self.resources.append(resource)

    def _parse_variables(self, content: str, file_path: Path) -> None:
        """
        Parse variable blocks from Terraform content.

        Args:
            content: Terraform file content
            file_path: Path to the file being parsed
        """
        # Simple variable parsing
        variable_pattern = r'variable\s+["\']?([^"\'\s]+)["\']?\s*{([^}]+)}'

        matches = re.finditer(variable_pattern, content, re.DOTALL)

        for match in matches:
            var_name = match.group(1)
            var_body = match.group(2)

            attributes = self._parse_attributes(var_body)

            variable = {
                "name": var_name,
                "file": str(file_path),
                "line": self._get_line_number(content, match.start()),
                "attributes": attributes
            }

            self.variables.append(variable)

    def _parse_outputs(self, content: str, file_path: Path) -> None:
        """
        Parse output blocks from Terraform content.

        Args:
            content: Terraform file content
            file_path: Path to the file being parsed
        """
        # Simple output parsing
        output_pattern = r'output\s+["\']?([^"\'\s]+)["\']?\s*{([^}]+)}'

        matches = re.finditer(output_pattern, content, re.DOTALL)

        for match in matches:
            output_name = match.group(1)
            output_body = match.group(2)

            attributes = self._parse_attributes(output_body)

            output = {
                "name": output_name,
                "file": str(file_path),
                "line": self._get_line_number(content, match.start()),
                "attributes": attributes
            }

            self.outputs.append(output)

    def _parse_data_sources(self, content: str, file_path: Path) -> None:
        """
        Parse data source blocks from Terraform content.

        Args:
            content: Terraform file content
            file_path: Path to the file being parsed
        """
        # Simple data source parsing
        data_pattern = r'data\s+["\']?([^"\'\s]+)["\']?\s+["\']?([^"\'\s]+)["\']?\s*{([^}]+)}'

        matches = re.finditer(data_pattern, content, re.DOTALL)

        for match in matches:
            data_type = match.group(1)
            data_name = match.group(2)
            data_body = match.group(3)

            attributes = self._parse_attributes(data_body)

            data_source = {
                "type": data_type,
                "name": data_name,
                "file": str(file_path),
                "line": self._get_line_number(content, match.start()),
                "attributes": attributes
            }

            self.data_sources.append(data_source)

    def _parse_attributes(self, block_content: str) -> Dict[str, Any]:
        """
        Parse attributes from a Terraform block.

        Args:
            block_content: Content of a Terraform block

        Returns:
            Dictionary of attributes
        """
        attributes = {}

        # Simple attribute parsing
        # This is a simplified parser - in production you'd want to use hcl2
        lines = block_content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().rstrip(',')

                # Clean up the value
                value = value.strip('"\'')

                attributes[key] = value

        return attributes

    def _get_azure_service(self, resource_type: str) -> str:
        """
        Determine Azure service from resource type.

        Args:
            resource_type: Terraform resource type

        Returns:
            Azure service name
        """
        # Map resource types to Azure services
        service_mapping = {
            'azurerm_key_vault': 'Key Vault',
            'azurerm_storage_account': 'Storage',
            'azurerm_virtual_network': 'Virtual Network',
            'azurerm_subnet': 'Virtual Network',
            'azurerm_network_security_group': 'Network Security',
            'azurerm_public_ip': 'Public IP',
            'azurerm_network_interface': 'Network Interface',
            'azurerm_virtual_machine': 'Virtual Machine',
            'azurerm_app_service': 'App Service',
            'azurerm_function_app': 'Function App',
            'azurerm_cosmosdb_account': 'Cosmos DB',
            'azurerm_sql_server': 'SQL Database',
            'azurerm_sql_database': 'SQL Database',
            'azurerm_container_registry': 'Container Registry',
            'azurerm_kubernetes_cluster': 'AKS',
            'azurerm_monitor_diagnostic_setting': 'Monitor',
            'azurerm_role_assignment': 'Identity & Access',
            'azurerm_role_definition': 'Identity & Access',
            'azurerm_policy_assignment': 'Policy',
            'azurerm_policy_definition': 'Policy',
        }

        return service_mapping.get(resource_type, 'General')

    def _get_line_number(self, content: str, position: int) -> int:
        """
        Get line number from character position.

        Args:
            content: File content
            position: Character position

        Returns:
            Line number (1-based)
        """
        return content[:position].count('\n') + 1

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of parsed resources.

        Returns:
            Summary dictionary
        """
        services = {}
        for resource in self.resources:
            service = resource.get('service', 'Unknown')
            if service not in services:
                services[service] = 0
            services[service] += 1

        return {
            "total_resources": len(self.resources),
            "total_variables": len(self.variables),
            "total_outputs": len(self.outputs),
            "total_data_sources": len(self.data_sources),
            "services": services,
            "resource_types": list(set(r['type'] for r in self.resources))
        }
