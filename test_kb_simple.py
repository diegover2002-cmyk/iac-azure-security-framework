#!/usr/bin/env python3
"""
Simple test script for the Knowledge Base.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from security_analyzer.knowledge_base.kb_loader import KnowledgeBaseLoader
    from security_analyzer.analyzer.validation_functions import get_validation_function

    print("🔍 Security Analyzer Knowledge Base Test")
    print("=" * 40)

    # Load the knowledge base
    kb_loader = KnowledgeBaseLoader()

    # Get statistics
    stats = kb_loader.get_statistics()
    print(f"📊 Total Controls: {stats['total_controls']}")
    print(f"   Services: {stats['services_count']}")
    print(f"   Resource Types: {stats['resource_types_count']}")
    print()

    # Show some controls
    controls = kb_loader.get_all_controls()
    print("📋 Available Controls:")
    for i, control in enumerate(controls[:5], 1):  # Show first 5
        print(f"   {i}. {control.control_id}: {control.description}")
        print(f"      Service: {control.service}")
        print(f"      Severity: {control.severity}")
        print()

    # Test ST-008
    print("🎯 Testing ST-008 (Diagnostic Logging)")
    st_008 = kb_loader.get_control("ST-008")
    if st_008:
        print(f"   Found: {st_008.description}")
        print(f"   Custom Check: {st_008.validation.custom_check}")

        # Test validation function
        validate_func = get_validation_function(st_008.validation.custom_check)
        if validate_func:
            print(f"   ✅ Validation function found")

            # Test with problematic resource
            test_resource = {
                'type': 'azurerm_storage_account',
                'name': 'test_storage',
                'attributes': {}
            }

            result = validate_func(test_resource)
            if result:
                print(f"   ❌ Test result: {result}")
            else:
                print(f"   ✅ Test passed")
        else:
            print(f"   ❌ Validation function not found")
    else:
        print(f"   ❌ ST-008 control not found")

    print()
    print("✅ Knowledge Base test completed successfully!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all modules are properly installed")
except Exception as e:
    print(f"❌ Error: {e}")
