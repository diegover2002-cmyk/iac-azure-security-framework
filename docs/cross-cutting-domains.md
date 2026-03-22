# Cross-Cutting Domains

This repository distinguishes between deployable Azure service baselines and cross-cutting security domains.

## Deployable Service Catalog

Use `controls/MCSB-control-matrix.md` for services that map cleanly to a deployable Azure resource or service family, such as Storage, Key Vault, SQL, APIM, or Functions.

## Cross-Cutting Domains

The following topics should not appear in the deployable service matrix:

- DevOps Security
- Endpoint Security
- AI Security
- Microsoft Defender for Cloud

These domains apply across multiple services, pipelines, platforms, or operational processes. They should be maintained as separate guidance or domain catalogs.

## Current Repository Placement

- `controls/devops-security/controls.md` can remain as cross-cutting guidance, but it should not be treated as part of the deployable resource matrix.
- `controls/microsoft-defender-for-cloud/controls.md` should be treated as posture guidance, not as a single deployable resource baseline.

## Why This Separation Matters

- It keeps the service matrix deterministic for Terraform-oriented work.
- It avoids mixing deployable resources with organizational process controls.
- It makes AI-agent navigation simpler because one file answers one question: "Which Azure services can I model here?"
