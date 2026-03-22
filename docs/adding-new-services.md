# Adding New Services

Use this workflow when onboarding a new Azure service into the framework.

## Required Steps

1. Add the service to `controls/MCSB-control-matrix.md`.
2. Create `controls/<service>/controls.md` using an existing mature service as a template.
3. Map each control to MCSB, priority, and validation method.
4. Add secure and insecure Terraform examples in `tests/terraform/<service>/`.
5. Update documentation only if repository navigation or process guidance changes.

## Quality Bar

- Control IDs must be unique and sequential within the service prefix.
- Secure examples must use explicit settings.
- Validation references must point to Checkov rules or clearly mark custom/manual validation.
