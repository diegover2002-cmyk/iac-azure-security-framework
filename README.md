# iac-azure-security-framework

## Overview

Repository for **Azure security controls** with **MCSB** using IaC.

## Quick Start

1. View matrix: `controls/MCSB-control-matrix.md`
2. Checkov Test: `checkov -d tests/`
3. PR Gate: `python scripts/gate_check.py`

## Covered Services

- Storage, Key Vault, VNet, App Service, AKS +30

## Contributing

- **IMPORTANT:** Read the Secure Development Guide before starting.
- Add `controls/azure-NEW/controls.md` following the standard.
- Expand tests/

[![CI/CD Gate](https://img.shields.io/badge/Gate-MCSB%20Must-blue)]
