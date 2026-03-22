# General CI/CD Best Practices

This document serves as a "skill" or knowledge base for Continuous Integration and Continuous Deployment (CI/CD) patterns, independent of specific tools (Azure DevOps, GitHub Actions, Jenkins) or cloud providers.

## 1. Core Principles

* **Fail Fast**: Run the fastest and cheapest checks (linting, static analysis) first. If they fail, stop the pipeline immediately to save resources and feedback time.
* **Build Once, Deploy Many**: Generate a single immutable artifact (binary, container image, package) during the build stage. Promote this exact artifact through environments (Dev -> Staging -> Prod). Never rebuild the artifact for different environments.
* **Infrastructure as Code (IaC)**: Define the pipeline itself in code (YAML, Groovy) stored in the repository. Avoid manual configuration in the CI tool's UI.
* **Ephemerality**: Use short-lived agents/runners (containers) to ensure a clean state for every build and prevent configuration drift on build servers.

## 2. Security Patterns

* **Zero Trust Secrets**:
  * Never commit secrets to Git.
  * Do not inject secrets as environment variables in logs.
  * Use OIDC (OpenID Connect) federation for cloud authentication instead of long-lived static keys (Service Principals).
* **Least Privilege**:
  * The deployment agent for "Dev" should not have permissions on "Prod".
  * Scope tokens strictly to the repositories and resources needed.
* **Shift Left**:
  * Run SAST (Static Application Security Testing) and Secret Scanning on every Pull Request.
  * Block merges if high-severity vulnerabilities are found.

## 3. Pipeline Structure Strategy

A robust pipeline typically follows this flow:

### A. Pull Request (Validation)

* **Trigger**: On PR creation/update.
* **Goal**: Verify code quality before merging.
* **Steps**:
    1. **Lint**: Code style and syntax (e.g., pylint, tflint).
    2. **Test**: Unit tests with mocking.
    3. **Scan**: Security checks (Checkov, SonarQube).
    4. **Plan**: For IaC, run a "plan" or "dry-run" to visualize changes.

### B. Continuous Integration (Merge to Main)

* **Trigger**: Push to `main`.
* **Goal**: Create a deployable artifact.
* **Steps**:
    1. **Version**: Semantic versioning (v1.0.1).
    2. **Build**: Compile/Package.
    3. **Publish**: Push artifact to Registry (ACR, Artifactory).

### C. Continuous Deployment (Release)

* **Trigger**: Artifact publication or Manual Approval.
* **Goal**: Safe delivery to environments.
* **Steps**:
    1. **Dev**: Auto-deploy.
    2. **Staging**: Auto-deploy + Integration Tests.
    3. **Prod**: Manual Gate/Approval + Deploy + Smoke Tests.

## 4. Performance & Reliability

* **Caching**: Cache dependencies (node_modules, pip, maven) based on lockfiles. Invalidate cache when dependencies change.
* **Concurrency**: Run independent jobs (e.g., frontend build vs backend build) in parallel.
* **Idempotency**: Deployment scripts must be able to run multiple times without side effects (e.g., "create if missing, update if exists").

## 5. Branching Strategy

* **Trunk-Based Development**: Preferred for high-velocity CI/CD. Merge small, frequent updates to `main`.
* **Branch Protection**: Enforce PR reviews, status checks, and signed commits on the main branch.
