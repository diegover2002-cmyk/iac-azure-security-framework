# Control Matrix Guide

The control matrix in `controls/MCSB-control-matrix.md` is the canonical inventory of deployable Azure service controls.

## How to Use It

1. Identify the Azure service you are working on.
2. Review the control rows for priority, applicability, and validation method.
3. Follow the linked `controls/<service>/controls.md` file for implementation details.
4. Treat `Must` controls as blocking requirements for pull requests and CI/CD gates.

## Scope Boundary

- The matrix is for deployable Azure services and resource baselines.
- Cross-cutting domains and subscription-scoped posture services such as DevOps Security, Endpoint Security, AI Security, and Microsoft Defender for Cloud are not part of the matrix.
- Keep those domains in separate guidance documents or domain catalogs.

## Relationship to Other Documents

- `controls/MCSB-control-matrix.md` is the deployable-service index and quick reference.
- `controls/<service>/controls.md` contains the service baseline and implementation guidance.
- `controls/MCSB-service-control-catalog.md` is the normalized service-to-control catalog for analysis, export, and CI/CD design. It is broader in tabular form but does not replace the matrix.
- `docs/service-catalog-maturity-roadmap.md` tracks which services are golden references versus still needing deeper treatment.
- `https://github.com/bridgecrewio/checkov` is the external source of truth for actual Checkov rule coverage and rule identifiers.

## Priority Meanings

- `Must`: Mandatory baseline control. Missing compliance should fail validation.
- `Should`: Recommended control. Missing compliance should create a warning or require justification.
- `Nice`: Optional hardening. Track it, but do not block delivery by default.

## Validation Meanings

- `Yes`: The control can be checked directly in IaC.
- `Partial`: IaC can validate part of the control, but runtime or integration checks are still needed.
- `No`: The control is documentation-only or must be validated outside Terraform.

When a row references Checkov, confirm the rule ID and resource support against the official `bridgecrewio/checkov` repository before treating the mapping as authoritative.
