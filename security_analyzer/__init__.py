"""
Security Analyzer for Azure Infrastructure as Code (IaC)

This module provides a comprehensive security analysis tool for Terraform code
using the MCSB (Microsoft Cloud Security Benchmark) framework.

Main features:
- Terraform code parsing and analysis
- MCSB control validation
- Checkov integration
- Detailed security reporting
- CLI interface for local analysis

Usage:
    python -m security_analyzer analyze --path /path/to/terraform --controls mcsb
"""

__version__ = "1.0.0"
__author__ = "Security Analyzer Team"
__email__ = "security@example.com"

from .main import main
from .cli import SecurityAnalyzerCLI

__all__ = [
    "main",
    "SecurityAnalyzerCLI"
]
