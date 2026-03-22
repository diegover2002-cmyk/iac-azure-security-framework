# Contributing to IAC Azure Security Framework

Thank you for your interest in contributing!

## Getting Started

1. Read [Secure-Development-Guide.md](Secure-Development-Guide.md) for security standards and naming conventions.
2. Read [AGENTS.md](AGENTS.md) if you are using an AI-assisted workflow.
3. Review [docs/README.md](docs/README.md) for the documentation map.
4. Check the MCSB control matrix for current gaps.

## How to Submit a Change

1. Fork the repository.
2. Create a branch for your feature or control (e.g., `control/azure-sql`).
3. Ensure you have added:
   - The entry in the matrix.
   - The detailed `controls.md`.
   - Terraform tests/examples.
4. Run `checkov -d tests/` to verify compliance.
5. Submit a Pull Request.

## Documentation Rules

- Keep documentation in English, including file names.
- Use `docs/` for repository documentation and `wiki/` for GitHub Wiki pages.
- Do not add duplicate copies of the same guide in multiple locations unless one copy is explicitly the wiki version.
