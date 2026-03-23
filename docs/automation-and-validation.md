# Automation and Validation

The repository uses scripts and policy tooling to turn control guidance into actionable CI/CD checks.

## Validation Sources of Truth

- `controls/MCSB-control-matrix.md`: source of truth for which controls this repository expects per deployable Azure service.
- `https://github.com/bridgecrewio/checkov`: source of truth for Checkov rule IDs, supported resource coverage, and whether a mapping is real versus assumed.

Keep these roles separate:

- The repository defines the control baseline.
- Checkov defines the subset of that baseline that can be enforced through existing Checkov rules.
- Any remaining coverage must be labeled as `Custom`, `Needs verification`, or manual review rather than being mapped to invented rule IDs.

## Current Components

- `scripts/gate_check.py`: Reads the matrix and identifies `Must` controls.
- `scripts/aggregate_results.py`: Intended to aggregate scan outputs.
- `scripts/generate_pr_report.py`: Intended to summarize validation results for pull requests.
- `.github/workflows/pr-security-scan.yml`: Pull request validation workflow.

## Intended Validation Flow

1. Run Terraform static validation and formatting checks.
2. Run Checkov against changed Terraform examples or modules, using `bridgecrewio/checkov` as the authoritative rule catalog.
3. Map failed checks to the matrix and fail the pipeline for `Must` controls.
4. Publish a report that explains which controls passed, failed, or require manual review.
