# Manual CI/CD Process (PoC Phase)

## 1. Introduction

This document describes the manual Continuous Integration and Continuous Deployment (CI/CD) process to follow during the current proof-of-concept phase.

The goal is to ensure that all code submitted to the repository meets a consistent quality, formatting, and security baseline before the automated pipeline is fully implemented.

This process is mandatory for both developers and AI assistants contributing to the project.

## 2. Prerequisites

Before proposing changes, make sure the following tools are installed locally:

- [Terraform](https://www.terraform.io/downloads.html)
- [Checkov](https://www.checkov.io/1.Welcome/Installation.html)
- [Python 3](https://www.python.org/downloads/)

## 3. Workflow

### 3.1. Branch Creation

All new development, fixes, or changes must be done on a new branch created from `main`.

```bash
# Make sure local main is up to date
git checkout main
git pull origin main

# Create a descriptive branch for your change
git checkout -b <descriptive-branch-name>
```

### 3.2. Manual Validation Steps (CI)

Before considering your work ready for integration, run the following commands from the repository root.

#### a. Format the Code

This step ensures Terraform code uses a consistent format.

```bash
terraform fmt --recursive
```

#### b. Validate Terraform Syntax

This command checks that Terraform configuration is syntactically valid.

```bash
terraform validate
```

If this command returns errors, fix them before continuing.

#### c. Scan the Code with Checkov

This is the most important security step. Checkov scans Infrastructure as Code for known security misconfigurations.

```bash
checkov -d .
```

The command uses the configuration defined in `.checkov.yaml`. Review the output and resolve all reported `CRITICAL` and `HIGH` findings.

## 4. Pull Request Process

After completing and verifying the previous steps:

1. Add and commit your changes on the branch.
    ```bash
    git add .
    git commit -m "feat: clear description of the changes"
    ```
2. Push your branch to the remote repository.
    ```bash
    git push origin <descriptive-branch-name>
    ```
3. Create a pull request from your branch to `main`.
4. In the pull request description, explicitly confirm that you completed the manual validation steps from this document.
