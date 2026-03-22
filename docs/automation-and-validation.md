# Automation and Validation

The repository uses scripts and policy tooling to turn control guidance into actionable CI/CD checks.

## Current Components

- `scripts/gate_check.py`: Reads the matrix and identifies `Must` controls.
- `scripts/aggregate_results.py`: Intended to aggregate scan outputs.
- `scripts/generate_pr_report.py`: Intended to summarize validation results for pull requests.
- `.github/workflows/pr-security-scan.yml`: Pull request validation workflow.

## Intended Validation Flow

1. Run Terraform static validation and formatting checks.
2. Run Checkov against changed Terraform examples or modules.
3. Map failed checks to the matrix and fail the pipeline for `Must` controls.
4. Publish a report that explains which controls passed, failed, or require manual review.
