# AI Agent Guide

This guide explains how an AI agent should navigate and update the repository.

## Read Order

1. `README.md`
2. `AGENTS.md`
3. `Secure-Development-Guide.md`
4. `controls/MCSB-control-matrix.md`
5. The relevant `controls/<service>/controls.md`

## Editing Rules

- Prefer existing service folders and naming patterns.
- Avoid creating new top-level documentation unless it is a repository entry point.
- Keep all new content in English.
- When control logic changes, update the matrix first and then the detailed control file.
- When examples change, keep `tests/terraform/` in sync with the documented control.

## Output Expectations

For a service-level change, an agent should usually touch:

- The matrix entry.
- The service `controls.md`.
- One or more Terraform examples.
- Documentation only if navigation, workflow, or contributor guidance changed.
