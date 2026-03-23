# IAC Azure Security Framework

[![CI/CD Gate](https://img.shields.io/badge/Gate-MCSB%20Must-blue)](scripts/gate_check.py)
[![Security: MCSB](https://img.shields.io/badge/Security-MCSB-green)](https://learn.microsoft.com/en-us/security/benchmark/azure/overview)
[![IaC: Terraform](https://img.shields.io/badge/IaC-Terraform-purple)](https://www.terraform.io/)

## Overview

The **IAC Azure Security Framework** is a comprehensive repository designed to operationalize the **Microsoft Cloud Security Benchmark (MCSB)** using **Infrastructure as Code (Terraform)**.

It bridges the gap between theoretical security compliance documents and actual deployed infrastructure by providing:

1. **Traceability**: Direct mapping between MCSB controls and Terraform resources.
2. **Validation**: Automated scripts and Checkov policies to verify compliance.
3. **Education**: Explicit "Secure vs. Insecure" code examples for developers.

## Key Features

- **Centralized Control Matrix**: A single source of truth (`controls/MCSB-control-matrix.md`) mapping Azure services to security requirements.
- **Service Catalogs**: Detailed implementation guides for key services like Storage, Key Vault, AKS, SQL, and more.
- **Automated Gates**: Python scripts (`scripts/gate_check.py`) to enforce "Must" priority controls in CI/CD pipelines.
- **Policy as Code**: Integration with Checkov for static analysis of Terraform plans.

## Repository Structure

```text
.
├── controls/                 # Security controls documentation & matrix
│   ├── MCSB-control-matrix.md    # Master list of all controls
│   ├── azure-storage/            # Storage-specific controls & examples
│   ├── azure-key-vault/          # Key Vault controls
│   └── ...
├── docs/                     # Canonical contributor and process documentation
├── wiki/                     # GitHub Wiki source pages
├── scripts/                  # Automation for CI/CD gates (Python)
├── tests/                    # Terraform code for validation testing
└── README.md                 # This file
```

## Quick Start

### Prerequisites

- Terraform (v1.0+)
- Python 3.8+
- Checkov (`pip install checkov`)

### Usage

1. **Explore Standards**: Check the MCSB Control Matrix.
2. **Validate Infrastructure**: `checkov -d tests/terraform`
3. **Run CI/CD Gate**: `python scripts/gate_check.py`

## Documentation

- [Documentation Index](docs/README.md)
- [Service Catalog Maturity Roadmap](docs/service-catalog-maturity-roadmap.md)
- [AI Agent Guide](docs/ai-agent-guide.md)
- [Control Matrix Guide](docs/control-matrix-guide.md)
- [Modules Repo Integration Plan](docs/modules-repo-integration.md)
- [Adding New Services](docs/adding-new-services.md)
- [Automation and Validation](docs/automation-and-validation.md)
- [Secure Development Guide](Secure-Development-Guide.md)

## Current Catalog Status

The deployable service catalog in `controls/MCSB-control-matrix.md` currently covers 31 Azure service families.

- Golden references: Storage, Key Vault, Virtual Network, App Service, AKS
- Strong baselines: SQL, Cosmos DB, API Management, Functions, Backup, Firewall, Front Door, Container Registry, Service Bus, Event Hubs, Monitor, Application Gateway, App Configuration, Redis
- Expanded baselines: Bastion, Container Apps, Container Instances, Data Factory, Data Share, DNS, Event Grid, Load Balancer, Logic Apps, Private Link, Public IP, WAF

Use the maturity roadmap in `docs/service-catalog-maturity-roadmap.md` to prioritize which services should be deepened next.

## Contributing

We welcome contributions! Please read the Secure Development Guide and CONTRIBUTING.md before submitting a Pull Request to ensure alignment with our naming conventions and security standards.
