# Security Analyzer Knowledge Base

This directory contains the machine-readable knowledge base for the Security Analyzer, which provides structured security controls and validation rules for Azure resources.

## Overview

The knowledge base is designed to be:
- **Machine-readable**: Structured in YAML/JSON format for programmatic access
- **Extensible**: Easy to add new controls and validation rules
- **Versioned**: Supports versioning and change tracking
- **Integrated**: Works seamlessly with Checkov and custom validation functions

## Structure

```
knowledge_base/
├── controls_schema.yaml    # Schema definition for control structure
├── controls.yaml          # Main knowledge base with all controls
├── kb_loader.py          # Python loader and parser
└── README.md            # This documentation
```

## Control Structure

Each control in the knowledge base follows this structure:

```yaml
control_id:
  control_id: "ST-008"                    # Unique identifier
  service: "Logging & Telemetry"          # Azure service category
  resource_types:                         # Terraform resource types affected
    - "azurerm_storage_account"
    - "azurerm_key_vault"
  priority: "LT-3"                        # Priority from MCSB matrix
  severity: "MEDIUM"                      # CRITICAL, HIGH, MEDIUM, LOW
  description: "Diagnostic logging enabled"
  requirement_type: "Must"                # Must, Should, Could
  implementation: "Partial"               # Full, Partial, None
  automation_type: "Custom"               # Custom, Checkov, Manual

  validation:
    checkov_rules: ["CKV_AZURE_20"]       # Associated Checkov rules
    custom_check: "validate_diagnostic_logging"  # Custom validation function
    required_attributes:                  # Required Terraform attributes
      - "diagnostic_settings.log_analytics_workspace_id"
    forbidden_attributes: []              # Forbidden Terraform attributes
    required_blocks: ["diagnostic_settings"]  # Required Terraform blocks
    forbidden_blocks: []                  # Forbidden Terraform blocks

  evidence:
    type: "terraform_config"              # Type of evidence required
    required_blocks: ["diagnostic_settings"]  # Evidence blocks
    required_categories: ["StorageRead", "StorageWrite", "StorageDelete"]
    evidence_format: "json"               # Format of evidence
```

## Available Controls

### Current Controls

| Control ID | Service | Description | Severity | Status |
|------------|---------|-------------|----------|---------|
| ST-008 | Logging & Telemetry | Diagnostic logging enabled | MEDIUM | Partial |
| KV-001 | Key Vault | Key Vault soft delete enabled | CRITICAL | Full |
| ST-001 | Storage | Storage account encryption enabled | HIGH | Full |
| VM-001 | Virtual Machine | Virtual Machine encryption enabled | HIGH | Partial |
| NSG-001 | Network Security | Network Security Group rules restricted | HIGH | Full |
| AKS-001 | AKS | AKS RBAC enabled | CRITICAL | Full |
| SQL-001 | SQL Database | SQL Server encryption enabled | HIGH | Full |
| APP-001 | App Service | App Service HTTPS only | MEDIUM | Partial |

### Control Categories

- **ST-xxx**: Storage controls
- **KV-xxx**: Key Vault controls
- **VM-xxx**: Virtual Machine controls
- **NSG-xxx**: Network Security controls
- **AKS-xxx**: AKS controls
- **SQL-xxx**: SQL Database controls
- **APP-xxx**: App Service controls
- **LT-xxx**: Logging & Telemetry controls

## Usage

### Loading the Knowledge Base

```python
from security_analyzer.knowledge_base.kb_loader import KnowledgeBaseLoader

# Load with default path
kb_loader = KnowledgeBaseLoader()

# Load from custom path
kb_loader = KnowledgeBaseLoader("path/to/custom/controls.yaml")

# Get all controls
controls = kb_loader.get_all_controls()

# Get controls by service
storage_controls = kb_loader.get_controls_by_service("Storage")

# Get controls by resource type
vm_controls = kb_loader.get_controls_by_resource_type("azurerm_virtual_machine")
```

### Getting Control Details

```python
# Get a specific control
control = kb_loader.get_control("ST-008")

if control:
    print(f"Control: {control.control_id}")
    print(f"Service: {control.service}")
    print(f"Description: {control.description}")
    print(f"Severity: {control.severity}")
    print(f"Custom Check: {control.validation.custom_check}")
```

### Validation Functions

Each control can have an associated validation function:

```python
from security_analyzer.analyzer.validation_functions import get_validation_function

# Get validation function for a control
validate_func = get_validation_function("validate_diagnostic_logging")

# Test the function
resource = {
    'type': 'azurerm_storage_account',
    'attributes': {
        'diagnostic_settings': []
    }
}

result = validate_func(resource)
if result:
    print(f"Security issue: {result}")
```

## Adding New Controls

To add a new control to the knowledge base:

1. **Edit `controls.yaml`** and add your control following the structure above
2. **Create a validation function** in `validation_functions.py` if needed
3. **Update the control mapping** in the validation functions module
4. **Test the control** using the example usage scripts

### Example: Adding a New Storage Control

```yaml
# Add to controls.yaml
ST-009:
  control_id: "ST-009"
  service: "Storage"
  resource_types:
    - "azurerm_storage_account"
  priority: "ST-2"
  severity: "HIGH"
  description: "Storage account network access restricted"
  requirement_type: "Must"
  implementation: "Full"
  automation_type: "Custom"

  validation:
    checkov_rules: ["CKV_AZURE_21"]
    custom_check: "validate_storage_network_access"
    required_attributes:
      - "network_rules.default_action"
    forbidden_attributes: []
    required_blocks: []
    forbidden_blocks: []

  evidence:
    type: "terraform_config"
    required_blocks: []
    required_categories: []
    evidence_format: "json"
```

```python
# Add to validation_functions.py
def validate_storage_network_access(resource: Dict[str, Any]) -> Optional[str]:
    """Validate ST-009: Storage account network access restricted."""
    resource_type = resource.get('type', '')

    if resource_type != 'azurerm_storage_account':
        return None

    attributes = resource.get('attributes', {})

    # Check network rules
    network_rules = attributes.get('network_rules', {})
    if isinstance(network_rules, dict):
        default_action = network_rules.get('default_action', '').lower()
        if default_action != 'deny':
            return "Restrict network access by setting network_rules.default_action = 'Deny'"

    return None

# Add to VALIDATION_FUNCTIONS mapping
VALIDATION_FUNCTIONS['validate_storage_network_access'] = validate_storage_network_access
```

## Integration with Security Analyzer

The knowledge base integrates with the Security Analyzer through:

1. **MCSB Validator**: Loads controls and applies validation functions
2. **Checkov Engine**: Maps Checkov rules to MCSB controls
3. **Report Generator**: Uses control metadata for detailed reports
4. **CLI**: Provides control-specific analysis and filtering

## Best Practices

### Control Design

- Use clear, descriptive control IDs
- Follow the service prefix convention (ST-, KV-, VM-, etc.)
- Set appropriate severity levels based on impact
- Provide actionable recommendations in descriptions
- Include specific Terraform attribute references

### Validation Functions

- Handle edge cases gracefully
- Provide clear, actionable error messages
- Support multiple resource type variations
- Use consistent error message format
- Include resource type and name in messages

### Maintenance

- Version control changes to the knowledge base
- Test new controls thoroughly before deployment
- Document control rationale and references
- Review and update controls regularly
- Maintain backward compatibility when possible

## Troubleshooting

### Common Issues

1. **Control not found**: Check control ID spelling and ensure it's in `controls.yaml`
2. **Validation function missing**: Verify the function exists in `validation_functions.py`
3. **Import errors**: Ensure all dependencies are installed and paths are correct
4. **YAML parsing errors**: Validate YAML syntax using online tools or linters

### Debugging

```python
# Enable debug output
import logging
logging.basicConfig(level=logging.DEBUG)

# Check knowledge base loading
kb_loader = KnowledgeBaseLoader()
print(f"Loaded {len(kb_loader.get_all_controls())} controls")

# Validate a specific control
control = kb_loader.get_control("ST-008")
print(f"Control found: {control is not None}")

# Test validation function
from security_analyzer.analyzer.validation_functions import get_validation_function
func = get_validation_function("validate_diagnostic_logging")
print(f"Function found: {func is not None}")
```

## Future Enhancements

- **Dynamic control loading**: Load controls from multiple sources
- **Control dependencies**: Define relationships between controls
- **Risk scoring**: Calculate composite risk scores
- **Compliance mapping**: Map to multiple compliance frameworks
- **Custom rule engine**: Allow users to define custom validation rules
- **Control testing**: Automated testing framework for controls

## Contributing

When contributing new controls:

1. Follow the established naming conventions
2. Include comprehensive test cases
3. Document the security rationale
4. Provide example configurations
5. Update this README with new control information

For questions or issues, please refer to the main Security Analyzer documentation.
