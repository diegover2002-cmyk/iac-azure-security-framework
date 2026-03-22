# Control Matrix Guide

The control matrix in `controls/MCSB-control-matrix.md` is the canonical inventory of repository controls.

## How to Use It

1. Identify the Azure service you are working on.
2. Review the control rows for priority, applicability, and validation method.
3. Follow the linked `controls/<service>/controls.md` file for implementation details.
4. Treat `Must` controls as blocking requirements for pull requests and CI/CD gates.

## Priority Meanings

- `Must`: Mandatory baseline control. Missing compliance should fail validation.
- `Should`: Recommended control. Missing compliance should create a warning or require justification.
- `Nice`: Optional hardening. Track it, but do not block delivery by default.

## Validation Meanings

- `Yes`: The control can be checked directly in IaC.
- `Partial`: IaC can validate part of the control, but runtime or integration checks are still needed.
- `No`: The control is documentation-only or must be validated outside Terraform.
