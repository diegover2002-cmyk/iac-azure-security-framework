#!/usr/bin/env python3
"""
Example usage of the Security Analyzer.

This script demonstrates how to use the Security Analyzer to analyze
Terraform code for security issues.
"""

import sys
from pathlib import Path

# Add the security_analyzer to the path
sys.path.insert(0, str(Path(__file__).parent))

from security_analyzer.cli import SecurityAnalyzerCLI
from security_analyzer.analyzer.terraform_parser import TerraformParser
from security_analyzer.analyzer.mcsb_validator import MCSBValidator
from security_analyzer.analyzer.checkov_engine import CheckovEngine
from security_analyzer.analyzer.report_generator import ReportGenerator


def example_basic_analysis():
    """Example of basic security analysis."""
    print("🔍 Basic Security Analysis Example")
    print("=" * 50)

    # Create CLI instance
    cli = SecurityAnalyzerCLI()

    # Example: Analyze a Terraform directory
    # For this example, we'll use the current directory
    terraform_path = Path(__file__).parent.parent  # Go up to the root

    try:
        result = cli.analyze(
            path=str(terraform_path),
            controls="mcsb",
            output="example_report.json",
            format="json",
            detailed=True
        )

        print(f"\n✅ Analysis complete!")
        print(f"   Resources: {result['resources_count']}")
        print(f"   Findings: {result['findings_count']}")
        print(f"   Compliance: {result['compliance_score']}%")
        print(f"   Report saved to: example_report.json")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")


def example_quick_validation():
    """Example of quick validation."""
    print("\n⚡ Quick Validation Example")
    print("=" * 50)

    cli = SecurityAnalyzerCLI()

    terraform_path = Path(__file__).parent.parent

    try:
        result = cli.validate(
            path=str(terraform_path),
            controls="mcsb"
        )

        print(f"\n✅ Validation complete!")
        print(f"   Status: {result['quick_summary']['status']}")
        print(f"   Compliance: {result['compliance_score']}%")
        print(f"   Critical issues: {result['quick_summary']['critical_issues']}")
        print(f"   High issues: {result['quick_summary']['high_issues']}")

    except Exception as e:
        print(f"❌ Error during validation: {e}")


def example_module_usage():
    """Example of using individual modules."""
    print("\n🔧 Module Usage Example")
    print("=" * 50)

    # 1. Parse Terraform files
    print("📁 Parsing Terraform files...")
    parser = TerraformParser()
    terraform_path = Path(__file__).parent.parent

    try:
        resources = parser.parse_directory(terraform_path)
        summary = parser.get_summary()

        print(f"✅ Found {summary['total_resources']} resources")
        print(f"   Services: {', '.join(summary['services'].keys())}")
        print(f"   Resource types: {', '.join(summary['resource_types'][:5])}...")

        # 2. Validate against MCSB controls
        print("\n🛡️ Validating against MCSB controls...")
        validator = MCSBValidator()
        findings = validator.validate_resources(resources, controls="mcsb")

        print(f"✅ Found {len(findings)} security findings")

        # 3. Generate report
        print("\n📄 Generating report...")
        report_gen = ReportGenerator()

        analysis_result = {
            "resources_count": len(resources),
            "findings_count": len(findings),
            "compliance_score": max(0, 100 - (len(findings) * 5)),
            "summary": {
                "critical_findings": len([f for f in findings if f.severity == "CRITICAL"]),
                "high_findings": len([f for f in findings if f.severity == "HIGH"]),
                "medium_findings": len([f for f in findings if f.severity == "MEDIUM"]),
                "low_findings": len([f for f in findings if f.severity == "LOW"]),
                "services_analyzed": list(summary['services'].keys()),
                "controls_applied": ["mcsb"]
            },
            "findings": [
                {
                    "resource_type": f.resource_type,
                    "resource_name": f.resource_name,
                    "control_id": f.control_id,
                    "severity": f.severity,
                    "description": f.description,
                    "recommendation": f.recommendation,
                    "file": f.file,
                    "line": f.line,
                    "service": f.service
                }
                for f in findings
            ]
        }

        report_gen.generate_report(
            analysis_result,
            output_file="module_example_report.json",
            format="json",
            detailed=True
        )

        print("✅ Report generated: module_example_report.json")

    except Exception as e:
        print(f"❌ Error: {e}")


def example_checkov_integration():
    """Example of Checkov integration."""
    print("\n🔍 Checkov Integration Example")
    print("=" * 50)

    engine = CheckovEngine()

    if engine._check_checkov_available():
        print("✅ Checkov is available")
        print(f"   Version: {engine.get_checkov_version()}")

        terraform_path = Path(__file__).parent.parent

        try:
            findings = engine.validate_terraform(str(terraform_path))
            print(f"✅ Checkov analysis complete")
            print(f"   Found {len(findings.get('results', []))} findings from Checkov")

        except Exception as e:
            print(f"❌ Checkov analysis error: {e}")
    else:
        print("⚠️  Checkov is not available in this environment")
        print("   Install Checkov with: pip install checkov")


if __name__ == "__main__":
    print("Security Analyzer - Example Usage")
    print("=" * 60)

    # Run examples
    example_basic_analysis()
    example_quick_validation()
    example_module_usage()
    example_checkov_integration()

    print("\n" + "=" * 60)
    print("🎉 All examples completed!")
    print("\nTo use the Security Analyzer:")
    print("  python -m security_analyzer analyze --path /path/to/terraform --controls mcsb")
    print("  python -m security_analyzer validate --path /path/to/terraform")
