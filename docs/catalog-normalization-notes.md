# Catalog Normalization Notes

This document records normalization decisions for the deployable service catalog.

## Current Decisions

- The deployable matrix only includes Azure services or service families that map cleanly to a deployable baseline.
- Cross-cutting domains and posture services remain outside the matrix.
- Service `controls.md` files may contain richer narrative guidance than the matrix; the matrix is intentionally concise.
- The normalized service control catalog is allowed to evolve separately when it is used for export, analysis, or CI/CD design.

## Review Focus Areas

- Keep service naming consistent between matrix, service folders, and README.
- Keep severity and priority labels aligned with the service baseline.
- Prefer English Microsoft Learn references in documentation unless there is a specific reason not to.
