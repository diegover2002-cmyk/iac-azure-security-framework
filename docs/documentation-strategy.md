# Documentation Strategy

This repository should use a three-layer documentation model.

## Layer 1: Root Entry Points

Keep only high-signal entry points in the repository root:

- `README.md`
- `CONTRIBUTING.md`
- `Secure-Development-Guide.md`
- `AGENTS.md`

## Layer 2: Canonical Repository Docs

Use `docs/` for durable repository guidance:

- Structure and navigation
- Authoring workflow
- Validation process
- Guidance for AI agents
- Catalog maturity and roadmap decisions
- Future integration plans with related repositories

## Layer 3: Public Wiki

Use `wiki/` for GitHub Wiki pages that mirror the high-level guidance from `docs/` without duplicating every internal detail.

## Why This Works for AI Agents

- Clear source-of-truth ordering reduces conflicting context.
- English-only file names improve deterministic file discovery.
- Service-specific documentation stays close to the implementation in `controls/`.
- Root-level entry points remain small enough for fast agent onboarding.
