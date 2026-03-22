# iac-azure-security-framework

## Visión General

Repositorio para **controles de seguridad Azure** con **MCSB** usando IaC.

## Rápido Inicio

1. Ver matriz: `controls/MCSB-control-matrix.md`
2. Test Checkov: `checkov -d tests/`
3. Gate PR: `python scripts/gate_check.py`

## Servicios Cubiertos

- Storage, Key Vault, VNet, App Service, AKS +30

## Contribuir

- Agregar controls/azure-NUEVO/controls.md
- Expandir tests/

[![CI/CD Gate](https://img.shields.io/badge/Gate-MCSB%20Must-blue)]
