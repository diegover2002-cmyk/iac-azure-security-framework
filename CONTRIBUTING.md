# Contributing to IAC Azure Security Framework

Thank you for your interest in contributing!

## Getting Started

1. Read the Secure Development Guide to understand the security standards and naming conventions.
2. Check the MCSB Control Matrix for current gaps.

## How to Submit a Change

1. Fork the repository.
2. Create a branch for your feature or control (e.g., `control/azure-sql`).
3. Ensure you have added:
    * The entry in the Matrix.
    * The detailed `controls.md`.
    * Terraform tests/examples.
4. Run `checkov -d tests/` to verify compliance.
5. Submit a Pull Request.
