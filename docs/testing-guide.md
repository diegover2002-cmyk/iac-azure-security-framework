# Testing Guide

Use `tests/terraform/` to keep runnable secure and insecure examples close to the documented controls.

## Layout

- `tests/terraform/<service>/secure/`: Compliant examples.
- `tests/terraform/<service>/insecure/`: Intentionally non-compliant examples.

## Purpose

- Validate that policy tooling detects insecure patterns.
- Give contributors and AI agents concrete Terraform examples to copy from.
- Reduce ambiguity in control interpretation.
