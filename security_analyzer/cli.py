"""
Command Line Interface for the Security Analyzer.

This module provides the main CLI class that orchestrates the analysis
of Terraform code against MCSB security controls.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .analyzer.terraform_parser import TerraformParser
from .analyzer.mcsb_validator import MCSBValidator
from .analyzer.checkov_engine import CheckovEngine
from .analyzer.report_generator import ReportGenerator


@dataclass
class AnalysisResult:
    """Result of a security analysis."""
    resources_count: int
    findings_count: int
    compliance_score: float
    findings: List[Dict[str, Any]]
    summary: Dict[str, Any]


class SecurityAnalyzerCLI:
    """Main CLI class for the Security Analyzer."""

    def __init__(self):
        """Initialize the Security Analyzer CLI."""
        self.parser = TerraformParser()
        self.validator = MCSBValidator()
        self.checkov_engine = CheckovEngine()
        self.report_generator = ReportGenerator()

    def analyze(
        self,
        path: str,
        controls: str = "mcsb",
        services: Optional[List[str]] = None,
        output: Optional[str] = None,
        format: str = "json",
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze Terraform code for security issues.

        Args:
            path: Path to Terraform code directory
            controls: Security controls to validate against
            services: List of Azure services to analyze (optional)
            output: Output file path (optional)
            format: Output format (json, html, txt)
            detailed: Generate detailed report

        Returns:
            Analysis result dictionary
        """
        print(f"🔍 Analyzing Terraform code in: {path}")

        # 1. Parse Terraform files
        print("📁 Parsing Terraform files...")
        terraform_path = Path(path)
        if not terraform_path.exists():
            raise ValueError(f"Path does not exist: {path}")

        parsed_resources = self.parser.parse_directory(terraform_path)
        print(f"✅ Found {len(parsed_resources)} resources to analyze")

        # 2. Run Checkov analysis
        print("🔍 Running Checkov analysis...")
        checkov_results = self.checkov_engine.validate_terraform(str(terraform_path))
        checkov_findings = checkov_results.get('results', [])

        # 3. Run MCSB validation
        print("🛡️ Running MCSB validation...")
        mcsb_findings = self.validator.validate_resources(
            parsed_resources,
            controls=controls,
            services=services
        )

        # 4. Combine findings
        all_findings = checkov_findings + mcsb_findings

        # 5. Calculate compliance score
        compliance_score = self._calculate_compliance_score(
            len(parsed_resources),
            len(all_findings)
        )

        # 6. Generate report
        result = {
            "resources_count": len(parsed_resources),
            "findings_count": len(all_findings),
            "compliance_score": compliance_score,
            "findings": all_findings,
            "summary": {
                "critical_findings": len([f for f in all_findings if getattr(f, 'severity', None) == "CRITICAL"]),
                "high_findings": len([f for f in all_findings if getattr(f, 'severity', None) == "HIGH"]),
                "medium_findings": len([f for f in all_findings if getattr(f, 'severity', None) == "MEDIUM"]),
                "low_findings": len([f for f in all_findings if getattr(f, 'severity', None) == "LOW"]),
                "services_analyzed": list(set(r.get("service", "unknown") for r in parsed_resources)),
                "controls_applied": [controls] if controls else []
            }
        }

        # 7. Generate output
        if output:
            print(f"📄 Generating {format} report...")
            self.report_generator.generate_report(
                result,
                output_file=output,
                format=format,
                detailed=detailed
            )
            print(f"✅ Report saved to: {output}")
        else:
            # Print to console
            if format == "json":
                print(json.dumps(result, indent=2))
            else:
                print(self.report_generator.format_report(result, format=format))

        return result

    def validate(
        self,
        path: str,
        controls: str = "mcsb"
    ) -> Dict[str, Any]:
        """
        Quick validation of Terraform code.

        Args:
            path: Path to Terraform code directory
            controls: Security controls to validate against

        Returns:
            Validation result
        """
        print(f"⚡ Quick validation of: {path}")

        terraform_path = Path(path)
        if not terraform_path.exists():
            raise ValueError(f"Path does not exist: {path}")

        # Parse and validate
        parsed_resources = self.parser.parse_directory(terraform_path)
        findings = self.validator.validate_resources(parsed_resources, controls=controls)

        result = {
            "resources_count": len(parsed_resources),
            "findings_count": len(findings),
            "compliance_score": self._calculate_compliance_score(len(parsed_resources), len(findings)),
            "quick_summary": {
                "status": "PASS" if len(findings) == 0 else "FAIL",
                "critical_issues": len([f for f in findings if getattr(f, 'severity', None) == "CRITICAL"]),
                "high_issues": len([f for f in findings if getattr(f, 'severity', None) == "HIGH"])
            }
        }

        print(f"📊 Resources: {result['resources_count']}")
        print(f"⚠️  Findings: {result['findings_count']}")
        print(f"📈 Compliance: {result['compliance_score']:.1f}%")

        return result

    def _calculate_compliance_score(self, total_resources: int, findings_count: int) -> float:
        """
        Calculate compliance score based on findings.

        Args:
            total_resources: Total number of resources analyzed
            findings_count: Number of findings detected

        Returns:
            Compliance score (0-100)
        """
        if total_resources == 0:
            return 0.0

        # Each finding reduces compliance score
        # Critical findings have more weight
        score = 100.0

        # This is a simplified calculation
        # In a real implementation, you'd want more sophisticated scoring
        if findings_count > 0:
            score = max(0, 100 - (findings_count * 5))

        return round(score, 1)


def main():
    """Main function for direct execution."""
    if len(sys.argv) < 2:
        print("Usage: python -m security_analyzer.cli <command> [options]")
        print("Commands: analyze, validate")
        sys.exit(1)

    cli = SecurityAnalyzerCLI()

    command = sys.argv[1]

    if command == "analyze":
        if len(sys.argv) < 3:
            print("Usage: python -m security_analyzer.cli analyze <path> [--controls mcsb] [--output file]")
            sys.exit(1)

        path = sys.argv[2]
        controls = "mcsb"  # default
        output = None

        # Parse additional arguments
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--controls" and i + 1 < len(sys.argv):
                controls = sys.argv[i + 1]
                i += 1
            elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
                output = sys.argv[i + 1]
                i += 1
            i += 1

        result = cli.analyze(path, controls=controls, output=output)
        print(f"\n🎯 Analysis complete!")
        print(f"   Resources: {result['resources_count']}")
        print(f"   Findings: {result['findings_count']}")
        print(f"   Compliance: {result['compliance_score']}%")

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Usage: python -m security_analyzer.cli validate <path> [--controls mcsb]")
            sys.exit(1)

        path = sys.argv[2]
        controls = "mcsb"  # default

        # Parse additional arguments
        if len(sys.argv) > 3 and sys.argv[3] == "--controls" and len(sys.argv) > 4:
            controls = sys.argv[4]

        result = cli.validate(path, controls=controls)
        print(f"\n✅ Validation complete!")
        print(f"   Status: {result['quick_summary']['status']}")
        print(f"   Compliance: {result['compliance_score']}%")

    else:
        print(f"Unknown command: {command}")
        print("Available commands: analyze, validate")
        sys.exit(1)


if __name__ == "__main__":
    main()
