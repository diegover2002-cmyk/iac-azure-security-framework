#!/usr/bin/env python3
"""
Main entry point for the Security Analyzer CLI.

This module provides the command-line interface for analyzing Terraform code
against MCSB security controls.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .cli import SecurityAnalyzerCLI
from .analyzer.terraform_parser import TerraformParser
from .analyzer.mcsb_validator import MCSBValidator
from .analyzer.checkov_engine import CheckovEngine
from .analyzer.report_generator import ReportGenerator


def main():
    """Main entry point for the Security Analyzer CLI."""
    parser = argparse.ArgumentParser(
        description="Security Analyzer for Azure Infrastructure as Code",
        prog="security_analyzer"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze Terraform code for security issues"
    )
    analyze_parser.add_argument(
        "--path",
        required=True,
        help="Path to Terraform code directory"
    )
    analyze_parser.add_argument(
        "--controls",
        default="mcsb",
        help="Security controls to validate against (default: mcsb)"
    )
    analyze_parser.add_argument(
        "--services",
        help="Comma-separated list of Azure services to analyze"
    )
    analyze_parser.add_argument(
        "--output",
        help="Output file for the report"
    )
    analyze_parser.add_argument(
        "--format",
        choices=["json", "html", "txt"],
        default="json",
        help="Output format (default: json)"
    )
    analyze_parser.add_argument(
        "--detailed",
        action="store_true",
        help="Generate detailed report with recommendations"
    )
    analyze_parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit with non-zero code if findings are detected"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Quick validation of Terraform code"
    )
    validate_parser.add_argument(
        "--path",
        required=True,
        help="Path to Terraform code directory"
    )
    validate_parser.add_argument(
        "--controls",
        default="mcsb",
        help="Security controls to validate against"
    )

    # Report command
    report_parser = subparsers.add_parser(
        "report",
        help="Generate security report from existing findings"
    )
    report_parser.add_argument(
        "--findings",
        required=True,
        help="Path to findings JSON file"
    )
    report_parser.add_argument(
        "--output",
        help="Output file for the report"
    )
    report_parser.add_argument(
        "--format",
        choices=["json", "html", "txt"],
        default="json",
        help="Output format"
    )

    # Version command
    parser.add_argument(
        "--version",
        action="version",
        version=f"Security Analyzer {__version__}"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "analyze":
            analyzer = SecurityAnalyzerCLI()
            result = analyzer.analyze(
                path=args.path,
                controls=args.controls,
                services=args.services.split(",") if args.services else None,
                output=args.output,
                format=args.format,
                detailed=args.detailed
            )

            if args.fail_on_findings and result.get("findings_count", 0) > 0:
                sys.exit(1)

        elif args.command == "validate":
            analyzer = SecurityAnalyzerCLI()
            result = analyzer.validate(
                path=args.path,
                controls=args.controls
            )

        elif args.command == "report":
            generator = ReportGenerator()
            report = generator.generate_from_findings(
                findings_file=args.findings,
                output=args.output,
                format=args.format
            )

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
