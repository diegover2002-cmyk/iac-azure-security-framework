# Modules Repo Integration Plan

This repository and the separate deployable Terraform modules repository should remain distinct, but intentionally connected.

## Separation of Concerns

- This repository defines security baselines, control mappings, and validation intent.
- The modules repository implements deployable Terraform modules and opinionated service patterns.

## Planned Integration Model

1. Each service baseline in `controls/<service>/controls.md` should eventually reference the corresponding module or module family.
2. The modules repository should consume this repository as the security source of truth, not re-invent control definitions.
3. Validation logic can later map module outputs or module conventions back to control IDs defined here.

## What Not to Do Yet

- Do not duplicate Terraform module code into this repository.
- Do not make this repo depend on module implementation details too early.
- Do not treat a module as the control definition; the module should implement the control, not replace it.

## Future Linking Pattern

When the modules repository is ready to integrate, add:

- A service-level link from `controls/<service>/controls.md` to the corresponding module path.
- A short "reference implementation" section that points to the module repo.
- Optional validation mapping notes that explain how the module enforces key `Must` controls.
