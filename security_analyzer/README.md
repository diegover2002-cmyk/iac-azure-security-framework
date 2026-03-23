# Security Analyzer for Azure Infrastructure as Code

A comprehensive security analysis tool for Terraform code using the MCSB (Microsoft Cloud Security Benchmark) framework.

## Overview

The Security Analyzer provides automated security scanning for Azure Infrastructure as Code (IaC) using Terraform. It combines:

- **MCSB Controls**: Validation against Microsoft Cloud Security Benchmark controls
- **Checkov Integration**: Leverages existing Checkov security rules
- **Custom Validation**: Service-specific security checks
- **Detailed Reporting**: Comprehensive security reports in multiple formats

## Features

### 🛡️ Security Analysis
- **Terraform Parsing**: Extracts resources, variables, and configurations
- **MCSB Validation**: Validates against Microsoft Cloud Security Benchmark controls
- **Checkov Integration**: Uses existing Checkov rules for comprehensive coverage
- **Custom Rules**: Service-specific security validations

### 📊 Reporting
- **Multiple Formats**: JSON, HTML, and text report generation
- **Detailed Analysis**: Service-level compliance and risk assessment
- **Finding Prioritization**: Severity-based finding classification
- **Recommendations**: Actionable security recommendations

### 🔧 CLI Interface
- **Easy Usage**: Simple command-line interface
- **Flexible Options**: Configurable analysis parameters
- **Integration Ready**: Designed for CI/CD pipeline integration

## Installation

### Prerequisites
- Python 3.8+
- Terraform files to analyze

### Optional Dependencies
- **Checkov**: For enhanced security scanning
  ```bash
  pip install checkov
  ```

### Installation
The Security Analyzer is included in this repository. No additional installation required.

## Usage

### Basic Analysis
```bash
# Analyze Terraform code with MCSB controls
python -m security_analyzer analyze --path /path/to/terraform --controls mcsb

# Generate detailed report
python -m security_analyzer analyze --path /path/to/terraform --detailed --output report.json

# Analyze specific services only
python -m security_analyzer analyze --path /path/to/terraform --services azure-key-vault,azure-storage
```

### Quick Validation
```bash
# Quick security validation
python -m security_analyzer validate --path /path/to/terraform

# Validate with fail-fast behavior
python -m security_analyzer analyze --path /path/to/terraform --fail-on-findings
```

### Report Generation
```bash
# Generate HTML report
python -m security_analyzer analyze --path /path/to/terraform --format html --output report.html

# Generate text report
python -m security_analyzer analyze --path /path/to/terraform --format txt --output report.txt
```

## Command Reference

### analyze
Analyze Terraform code for security issues.

**Options:**
- `--path`: Path to Terraform code directory (required)
- `--controls`: Security controls to validate against (default: mcsb)
- `--services`: Comma-separated list of Azure services to analyze
- `--output`: Output file for the report
- `--format`: Output format (json, html, txt) - default: json
- `--detailed`: Generate detailed report with recommendations
- `--fail-on-findings`: Exit with non-zero code if findings are detected

**Example:**
```bash
python -m security_analyzer analyze --path ./terraform --controls mcsb --detailed --output security_report.json
```

### validate
Quick validation of Terraform code.

**Options:**
- `--path`: Path to Terraform code directory (required)
- `--controls`: Security controls to validate against

**Example:**
```bash
python -m security_analyzer validate --path ./terraform
```

### report
Generate security report from existing findings.

**Options:**
- `--findings`: Path to findings JSON file (required)
- `--output`: Output file for the report
- `--format`: Output format (json, html, txt)

**Example:**
```bash
python -m security_analyzer report --findings findings.json --format html --output report.html
```

## Supported Azure Services

The Security Analyzer supports validation for the following Azure services:

- **Key Vault**: Secrets and key management security
- **Storage**: Storage account encryption and access controls
- **Virtual Network**: Network security and segmentation
- **Virtual Machine**: VM security and disk encryption
- **App Service**: Web application security
- **Function App**: Serverless function security
- **Cosmos DB**: Database security
- **SQL Database**: Relational database security
- **Container Registry**: Container image security
- **AKS**: Kubernetes cluster security
- **Network Security Groups**: Firewall rule validation

## Security Controls

### MCSB Controls
The analyzer validates against key MCSB controls including:

- **KV-001**: Key Vault Soft Delete
- **ST-001**: Storage Account Encryption
- **VM-001**: Virtual Machine Disk Encryption
- **NSG-001**: Network Security Group Rules

### Checkov Integration
Leverages Checkov's extensive rule set for:
- Resource configuration validation
- Security best practice enforcement
- Compliance framework checks

## Report Formats

### JSON Format
Comprehensive machine-readable report with all findings and metadata.

```json
{
  "report_metadata": {
    "timestamp": "2024-01-01T12:00:00",
    "format": "json",
    "analyzer_version": "1.0.0"
  },
  "analysis_summary": {
    "resources_count": 15,
    "findings_count": 8,
    "compliance_score": 73.3,
    "summary": {
      "critical_findings": 2,
      "high_findings": 3,
      "medium_findings": 5,
      "services_analyzed": ["Key Vault", "Storage", "Virtual Network"]
    }
  },
  "findings": [...]
}
```

### HTML Format
Human-readable report with visualizations and detailed findings.

### Text Format
Simple text report for quick review and integration.

## Integration Examples

### GitHub Actions
```yaml
name: Security Analysis
on: [push, pull_request]

jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Security Analyzer
        run: |
          python -m security_analyzer analyze \
            --path ./terraform \
            --controls mcsb \
            --detailed \
            --output security_report.json
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: security_report.json
```

### Azure DevOps Pipeline
```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.8'

- script: |
    python -m security_analyzer analyze \
      --path $(Build.SourcesDirectory)/terraform \
      --controls mcsb \
      --fail-on-findings
  displayName: 'Run Security Analysis'
```

## Development

### Project Structure
```
security_analyzer/
├── __init__.py              # Package initialization
├── main.py                  # CLI entry point
├── cli.py                   # Command-line interface
├── analyzer/                # Core analysis modules
│   ├── __init__.py
│   ├── terraform_parser.py  # Terraform file parsing
│   ├── mcsb_validator.py    # MCSB control validation
│   ├── checkov_engine.py    # Checkov integration
│   └── report_generator.py  # Report generation
├── knowledge_base/          # Security knowledge
│   ├── __init__.py
│   └── mcsb_matrix.py       # MCSB control matrix
├── config/                  # Configuration
│   ├── __init__.py
│   └── rules/               # Custom rules
└── example_usage.py         # Usage examples
```

### Adding New Controls
To add new MCSB controls:

1. Add control definition to `mcsb_validator.py`
2. Implement validation function
3. Map to relevant resource types

### Custom Rules
Custom security rules can be added in the `config/rules/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create a GitHub issue
- Check the documentation in the main repository
- Review the example usage script

## Contributing to the Main Repository

This Security Analyzer is part of the larger Azure Security Framework repository. For contributions to the main framework:

- See `CONTRIBUTING.md` for contribution guidelines
- Review `Secure-Development-Guide.md` for development standards
- Check the main `README.md` for project overview
