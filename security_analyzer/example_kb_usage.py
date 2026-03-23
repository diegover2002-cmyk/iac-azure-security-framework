"""
Example usage of the Knowledge Base for the Security Analyzer.

This module demonstrates how to use the machine-readable knowledge base
to validate Terraform resources against MCSB controls.
"""

from security_analyzer.knowledge_base.kb_loader import KnowledgeBaseLoader
from security_analyzer.analyzer.validation_functions import get_validation_function


def demonstrate_kb_usage():
    """Demonstrate how to use the knowledge base."""
    print("🔍 Security Analyzer Knowledge Base Demo")
    print("=" * 50)

    # Load the knowledge base
    kb_loader = KnowledgeBaseLoader()

    # Get statistics
    stats = kb_loader.get_statistics()
    print(f"📊 Knowledge Base Statistics:")
    print(f"   Total Controls: {stats['total_controls']}")
    print(f"   Services: {stats['services_count']}")
    print(f"   Resource Types: {stats['resource_types_count']}")
    print(f"   Severity Distribution: {stats['severity_distribution']}")
    print()

    # Show available services
    print("📋 Available Services:")
    for service in stats['services']:
        controls = kb_loader.get_controls_by_service(service)
        print(f"   • {service}: {len(controls)} controls")
    print()

    # Show controls for a specific service
    print("🔍 Example: Storage Controls")
    storage_controls = kb_loader.get_controls_by_service("Storage")
    for control in storage_controls:
        print(f"   • {control.control_id}: {control.description}")
        print(f"     Severity: {control.severity}")
        print(f"     Resource Types: {', '.join(control.resource_types)}")
        print(f"     Custom Check: {control.validation.custom_check}")
        print()

    # Show ST-008 control details
    print("🎯 Example: ST-008 (Diagnostic Logging)")
    st_008 = kb_loader.get_control("ST-008")
    if st_008:
        print(f"   Control ID: {st_008.control_id}")
        print(f"   Service: {st_008.service}")
        print(f"   Description: {st_008.description}")
        print(f"   Severity: {st_008.severity}")
        print(f"   Resource Types: {', '.join(st_008.resource_types)}")
        print(f"   Custom Check: {st_008.validation.custom_check}")
        print(f"   Required Attributes: {', '.join(st_008.validation.required_attributes)}")
        print(f"   Required Blocks: {', '.join(st_008.validation.required_blocks)}")
        print()

    # Show Checkov mapping
    print("🔗 Checkov Rules Mapping:")
    checkov_mapping = kb_loader.get_checkov_mapping()
    for checkov_rule, control_ids in checkov_mapping.items():
        print(f"   {checkov_rule} → {', '.join(control_ids)}")
    print()

    # Show custom checks
    print("⚙️  Custom Validation Functions:")
    custom_checks = kb_loader.get_custom_checks()
    for function_name, control_id in custom_checks.items():
        print(f"   {function_name} → {control_id}")
    print()

    # Test a validation function
    print("🧪 Testing Validation Function")
    validate_func = get_validation_function("validate_diagnostic_logging")
    if validate_func:
        # Mock resource for testing
        mock_resource = {
            'type': 'azurerm_storage_account',
            'name': 'test_storage',
            'attributes': {
                'diagnostic_settings': []
            }
        }

        result = validate_func(mock_resource)
        if result:
            print(f"   ❌ Finding: {result}")
        else:
            print(f"   ✅ No issues found")
    else:
        print(f"   ⚠️  Validation function not found")

    print()
    print("✅ Knowledge Base demo completed!")


def demonstrate_control_validation():
    """Demonstrate how to validate a specific control."""
    print("\n🔍 Control Validation Demo")
    print("=" * 30)

    kb_loader = KnowledgeBaseLoader()

    # Get ST-008 control
    st_008 = kb_loader.get_control("ST-008")
    if not st_008:
        print("❌ ST-008 control not found")
        return

    print(f"Validating control: {st_008.control_id} - {st_008.description}")
    print(f"Service: {st_008.service}")
    print(f"Severity: {st_008.severity}")
    print()

    # Test different resource scenarios
    test_cases = [
        {
            'name': 'Storage Account without diagnostic logging',
            'resource': {
                'type': 'azurerm_storage_account',
                'name': 'test_storage',
                'attributes': {}
            },
            'expected': 'Should fail - missing diagnostic_settings'
        },
        {
            'name': 'Storage Account with empty diagnostic settings',
            'resource': {
                'type': 'azurerm_storage_account',
                'name': 'test_storage',
                'attributes': {
                    'diagnostic_settings': [{}]
                }
            },
            'expected': 'Should fail - missing log_analytics_workspace_id'
        },
        {
            'name': 'Storage Account with proper diagnostic logging',
            'resource': {
                'type': 'azurerm_storage_account',
                'name': 'test_storage',
                'attributes': {
                    'diagnostic_settings': [{
                        'log_analytics_workspace_id': '/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.OperationalInsights/workspaces/law'
                    }]
                }
            },
            'expected': 'Should pass - proper configuration'
        }
    ]

    # Get validation function
    validate_func = get_validation_function(st_008.validation.custom_check)
    if not validate_func:
        print("❌ Validation function not found")
        return

    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Expected: {test_case['expected']}")

        result = validate_func(test_case['resource'])
        if result:
            print(f"Result: ❌ {result}")
        else:
            print(f"Result: ✅ No issues found")
        print()


if __name__ == "__main__":
    demonstrate_kb_usage()
    demonstrate_control_validation()
