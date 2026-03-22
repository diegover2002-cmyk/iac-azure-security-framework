# Reporte de Estado del Proyecto: IAC Azure Security Framework (MCSB)

**Fecha de Análisis:** 2026-03-22
**Auditor:** Ingeniero Senior de Seguridad Cloud y DevSecOps

## 1. Resumen Ejecutivo

Este reporte evalúa el estado actual del repositorio `iac-azure-security-framework` con el objetivo de alinearlo al estándar **Microsoft Cloud Security Benchmark (MCSB) v1.0**.

El proyecto tiene una base excelente, con una estructura de directorios clara, ejemplos de código seguro/inseguro y la intención de automatizar la conformidad de la seguridad como código. Sin embargo, se han identificado **gaps significativos** en tres áreas principales:

1.  **Documentación Incompleta y Desincronizada:** Los documentos maestros de seguimiento de controles no reflejan el estado real del repositorio.
2.  **Cobertura Parcial de Servicios de Azure:** Múltiples servicios han sido iniciados pero no están documentados, y muchos otros de la línea base oficial de MCSB ni siquiera han sido considerados.
3.  **Automatización CI/CD Inexistente:** El gate de seguridad para Pull Requests, un pilar fundamental del proyecto, no está implementado.

El repositorio **no está actualmente en un estado "audit-ready"**. Las siguientes secciones detallan los hallazgos y proponen un plan de acción para alcanzar este objetivo.

---

## 2. Análisis de Cobertura de Servicios

Se realizó una comparación cruzada entre cuatro fuentes: la matriz de controles del proyecto, el catálogo de servicios, las carpetas existentes y la lista oficial de servicios MCSB v1.0 de Microsoft.

| Servicio de Azure | Matriz Principal (`-matrix.md`) | Catálogo Detallado (`-catalog.md`) | Carpeta Existente (`/controls`) | Gap Identificado |
| :--- | :---: | :---: | :---: | :--- |
| **Servicios Completos y Documentados** | | | | |
| Azure Storage Account | ✅ | ✅ | ✅ | Ninguno |
| Azure Key Vault | ✅ | ✅ | ✅ | Ninguno |
| Azure Virtual Network (VNet) | ✅ | ✅ | ✅ | Ninguno |
| Azure App Service | ✅ | ✅ | ✅ | Ninguno |
| Azure Kubernetes Service (AKS) | ✅ | ✅ | ✅ | Ninguno |
| | | | | |
| **Servicios con Documentación Parcial (TBD)** | | | | |
| Azure SQL Database | 🚧 (TBD) | ✅ | ✅ | **Crítico:** Controles no definidos en matriz. |
| Azure Cosmos DB | 🚧 (TBD) | ✅ | ✅ | **Crítico:** Controles no definidos en matriz. |
| Azure API Management | 🚧 (TBD) | ✅ | ✅ | **Crítico:** Controles no definidos en matriz. |
| Azure Functions | 🚧 (TBD) | ✅ | ✅ | **Crítico:** Controles no definidos en matriz. |
| Azure Backup | 🚧 (TBD) | ✅ | ✅ | **Crítico:** Controles no definidos en matriz. |
| | | | | |
| **Servicios Existentes pero No Documentados** | | | | |
| Azure App Configuration | ❌ | ❌ | ✅ | **Alto:** Trabajo iniciado, pero sin trazabilidad. |
| Azure Application Gateway | ❌ | ❌ | ✅ | **Alto:** Trabajo iniciado, pero sin trazabilidad. |
| Azure Bastion | ❌ | ❌ | ✅ | **Alto:** Trabajo iniciado, pero sin trazabilidad. |
| Azure Container Registry | ❌ | ❌ | ✅ | **Alto:** Trabajo iniciado, pero sin trazabilidad. |
| Azure Firewall | ❌ | ❌ | ✅ | **Alto:** Trabajo iniciado, pero sin trazabilidad. |
| ... *(y otros 12 servicios)*| ❌ | ❌ | ✅ | **Alto:** Requieren integración formal. |
| | | | | |
| **Dominios Transversales** | | | | |
| Endpoint Security | 🚧 (TBD) | 🚧 | ❌ | **Crítico:** Dominio no desarrollado. |
| DevOps Security | 🚧 (TBD) | 🚧 | ❌ | **Crítico:** Dominio no desarrollado. |
| AI Security | 🚧 (TBD) | 🚧 | ❌ | **Crítico:** Dominio no desarrollado. |

Leyenda: ✅ (Completo), 🚧 (Parcial/TBD), ❌ (No Existe)

---

## 3. Gaps de Seguridad y Próximos Pasos

### Gap 1: Sincronización y Completitud de la Documentación (Prioridad: Alta)

Los documentos `MCSB-control-matrix.md` y `MCSB-service-control-catalog.md` deben ser la **fuente única de verdad**. Actualmente están desactualizados.

*   **Recomendación:**
    1.  **Unificar la Documentación:** Consolidar la matriz y el catálogo en un único documento maestro, o asegurar que se sincronicen automáticamente.
    2.  **Completar Controles "TBD":** Priorizar la definición de controles MCSB para **Azure SQL, Cosmos DB, APIM, Functions y Backup**. Esto implica investigar la línea base oficial de cada uno y mapear los controles a políticas de Checkov (`CKV_...`) o scripts personalizados.
    3.  **Integrar Servicios "Ocultos":** Añadir formalmente a la matriz los servicios que ya tienen una carpeta en `controls/` (ej. App Gateway, Bastion, ACR, Firewall).

### Gap 2: Automatización de CI/CD (Prioridad: Crítica)

El gate de seguridad es la pieza clave para que este framework sea efectivo. Sin él, el repositorio es solo una guía de referencia, no un sistema de cumplimiento activo.

*   **Recomendación:**
    1.  **Implementar el Workflow de GitHub Actions:** Crear el contenido del archivo `.github/workflows/pr-security-scan.yml`.
    2.  **Definir la Lógica del Workflow:**
        *   **Disparador:** El workflow debe ejecutarse en cada `pull_request` que modifique archivos `.tf`.
        *   **Pasos:**
            *   Hacer checkout del código.
            *   Instalar `checkov` y `python`.
            *   Ejecutar `checkov` sobre los directorios de terraform modificados.
            *   Ejecutar el script `scripts/gate_check.py`, que debe ser diseñado para leer la matriz de controles y fallar el PR si un control con `Priority = Must` no se cumple.
    3.  **Proteger la Rama Principal:** Configurar una regla de protección en la rama `main` que exija que el check "pr-security-scan" pase antes de poder hacer merge.

### Gap 3: Cobertura de Dominios Transversales y Nuevos Servicios (Prioridad: Media)

El proyecto ya identifica la necesidad de cubrir dominios como **AI Security** y **DevOps Security**. Además, la línea base de MCSB es más amplia.

*   **Recomendación:**
    1.  **Crear Documentos de Dominio:** Para cada dominio transversal (AI, DevOps, Endpoint Security), crear un documento `controls-<dominio>.md`. Este no se enfocará en un solo servicio de Azure, sino en prácticas que afectan todo el ciclo de vida (ej. seguridad de agentes de CI/CD, protección de modelos de ML, configuración de EDR).
    2.  **Plan de Adopción de Nuevos Servicios:** Realizar un análisis comparativo entre los servicios ya cubiertos y la lista oficial de MCSB v1.0. Priorizar la incorporación de servicios críticos para la organización que aún no están en el framework (ej. **Azure Databricks, Azure OpenAI, Microsoft Sentinel**).

---

## 4. Propuesta de Siguiente Acción Inmediata

Para demostrar el proceso de cierre de gaps, propongo generar el documento de control para uno de los servicios marcados como "TBD" que es fundamental en muchas arquitecturas: **Azure SQL Database**.

Generaré el archivo `controls/azure-sql/controls.md` basándome en la plantilla implícita de los servicios ya existentes y la línea base de seguridad oficial de Microsoft Learn.

**¿Procedo con la creación de este documento como primer paso para remediar los gaps identificados?**
