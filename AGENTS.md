# AI Agent Operating Guide

This repository is designed to be consumable by both human contributors and AI agents. Follow this guide before proposing or editing security controls.

## Source of Truth

1. `controls/MCSB-control-matrix.md`: Canonical inventory and priority for deployable Azure services.
2. `controls/<service>/controls.md`: Service-specific implementation guidance and secure/insecure examples.
3. `Secure-Development-Guide.md`: Authoring standards for new controls.
4. `docs/`: Contributor and repository documentation.

If two documents disagree, prefer the control matrix first and then the service-specific `controls.md`.

## Working Rules

- Keep the repository English-only, including file names.
- Do not add documentation in the repository root unless it is top-level contributor guidance.
- When adding a new Azure service, update the matrix, add `controls/<service>/controls.md`, and add runnable test examples under `tests/terraform/<service>/`.
- Do not add cross-cutting domains or subscription-scoped posture services such as DevOps Security, AI Security, or Microsoft Defender for Cloud to the deployable service matrix.
- Reuse existing control IDs and naming patterns. Do not invent new schemas.
- Prefer explicit Terraform attributes in secure examples, even when Azure defaults are already secure.
- Record whether a control is enforced by Checkov, custom validation, or manual review.

## Documentation Map

- `README.md`: Project overview and quick start.
- `docs/README.md`: Documentation index.
- `docs/ai-agent-guide.md`: Navigation and contribution workflow for agents.
- `docs/control-matrix-guide.md`: How to use the matrix and interpret priorities.
- `docs/service-catalog-maturity-roadmap.md`: Which services are mature, usable, or still need deeper work.
- `docs/modules-repo-integration.md`: Planned relationship with the separate deployable modules repository.
- `docs/adding-new-services.md`: Required steps to onboard a new Azure service.
- `wiki/`: GitHub Wiki source pages.

## Expected Output Shape

When an agent creates or updates a service control set, it should produce:

1. A matrix entry in `controls/MCSB-control-matrix.md`.
2. A detailed `controls/<service>/controls.md`.
3. Supporting Terraform examples in `tests/terraform/<service>/secure` and `tests/terraform/<service>/insecure`.
4. Documentation updates only when repository navigation or process changes.
