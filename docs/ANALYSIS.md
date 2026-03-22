# Comprehensive Repository Analysis: iac-azure-security-framework

Date: $(date)
Analysis performed with tools: list_files, search_files (regex security/terraform), read_file (20+ files).

## 1. Project Purpose

IaC Framework for **Azure security and compliance** using **Terraform + Checkov**, aligned with **MCSB**.

## 2. Structure

```
. (33 archivos)
├── controls/ (detallados MCSB)
│   ├── MCSB-control-matrix.md (35 servicios, 300+ controles)
│   ├── MCSB-service-control-catalog.md (catálogo priorizado)
│   └── azure-*/controls.md (e.g. Storage: 12 reglas con HCL)
├── tests/terraform/storage/ (insecure/secure: placeholders)
├── scripts/*.py (placeholders para CI/CD gates)
└── .checkov.yaml (vacío)
```

## 3. Contenido Detallado

### Matriz MCSB

- Servicios: Storage, KV, VNet, AppSvc, AKS + 30 más.
- Campos: Control ID, MCSB, Priority (Must/Should), Checkov (CKV_AZURE_*).

**Top Must/High Storage**:

| ID | Control | Checkov |
|----|---------|---------|
| ST-001 | Public blob disable | CKV_AZURE_59 |
| ST-006 | Firewall deny | CKV_AZURE_35 |
| ST-011 | No shared key | CKV2_AZURE_40 |

### Ejemplo Storage Controls.md

- 12 reglas con HCL secure/insecure.
- Compliant template al final.

## 4. Gaps

- Tests/scripts vacíos.
- Duplicación docs/wiki.

## 5. Uso CI/CD

```
checkov --check CKV_AZURE_59,CKV_AZURE_35 --fail-threshold cli
```

**Recomendación**: Completar scripts para gates automáticos.
