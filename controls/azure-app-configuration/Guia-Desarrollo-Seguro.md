# Secure Development Best Practices and Standards Guide

This document defines the mandatory standards for contributing to the `iac-azure-security-framework`. It is designed to guide both developers and AI agents in creating consistent security controls.

## 1. Framework Philosophy

* **MCSB First**: Every control must originate from a *Microsoft Cloud Security Benchmark* requirement.
* **Code over Text**: Documentation is not theoretical; it must include executable Terraform examples.
* **Explicit vs. Implicit**: In secure examples, define attributes explicitly, even if they match Azure defaults (to avoid regressions if defaults change).

## 2. `controls.md` Structure

Each control file (e.g., `controls/azure-sql/controls.md`) must strictly follow this structure. Use Azure Storage as the golden reference.

### Control Header

Each individual control must start with its ID and name, followed by a standardized metadata table:

| Field | Description | Rule |
|---|---|---|
| **MCSB** | Benchmark ID (e.g. NS-1) | Must exist in the official MCSB. |
| **Severity** | High, Medium, Low | Based on the impact of a breach. |
| **Priority** | Must, Should, Nice | **Must**: Blocks PRs. **Should**: Alert/Warning. |
| **Justification** | The "Why" | Clearly explains the technical risk (e.g., "Allows data exfiltration"). |
| **Checkov** | Rule ID | Use the official ID (e.g., `CKV_AZURE_59`) or "Custom". |

### Code Blocks: Insecure vs. Secure

It is **mandatory** to show the contrast. This trains agents and developers to detect incorrect patterns.

#### HCL Code Rules

1. Use `resource "type" "bad"` for the insecure example.
2. Use `resource "type" "good"` for the secure example.
3. Include comments explaining which specific property is missing or wrong.

**Ejemplo:**

```hcl
# Insecure — Enables unnecessary public access
resource "azurerm_storage_account" "bad" {
  # Missing public_network_access_enabled = false
  allow_nested_items_to_be_public = true
}

# Secure — Blocks public access and enforces HTTPS
resource "azurerm_storage_account" "good" {
  public_network_access_enabled   = false
  allow_nested_items_to_be_public = false
  enable_https_traffic_only       = true
}
```

## 3. Criterios de Prioridad (Priority)

* **Must (Obligatorio)**:
  * Exposición pública directa (Internet-facing).
  * Falta de encriptación en tránsito (HTTP).
  * Autenticación débil o inexistente (Anonymous access).
  * *Acción*: El pipeline de CI/CD debe fallar si esto no se cumple.

* **Should (Recomendado)**:
  * Encriptación avanzada (CMK, Infrastructure Encryption).
  * Logging/Audit logs (importante, pero no detiene el servicio).
  * Protecciones de borrado (Soft Delete).
  * *Acción*: El pipeline genera warnings; requiere aprobación manual o justificación.

## 4. Checklist para Agentes

Antes de confirmar un cambio o generar un nuevo archivo de control:

1. [ ] ¿El `Control ID` (ej. `SQ-001`) es único y secuencial?
2. [ ] ¿Existe un mapeo válido al MCSB (Domain-Number)?
3. [ ] ¿El bloque HCL es sintácticamente válido? (No inventes argumentos de Terraform).
4. [ ] ¿Has verificado si existe una regla de Checkov para este control?
5. [ ] ¿La justificación explica el riesgo de seguridad real?

## 5. Ubicación de Archivos

* Controles: `controls/<servicio-azure>/controls.md`
* Tests: `tests/terraform/<servicio-azure>/`
