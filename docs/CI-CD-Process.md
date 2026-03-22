# Proceso de CI/CD Manual (Fase PoC)

## 1. Introducción

Este documento describe el proceso de "Integración Continua" y "Despliegue Continuo" (CI/CD) que debe seguirse de forma manual durante la fase actual de Prueba de Concepto (PoC).

El objetivo es asegurar que todo el código subido al repositorio mantenga un estándar de calidad, formato y seguridad, incluso antes de implementar un pipeline de automatización completo.

**Este proceso es de obligado cumplimiento tanto para desarrolladores como para los asistentes de IA que colaboren en el proyecto.**

## 2. Prerrequisitos

Antes de proponer cambios, asegúrate de tener instaladas las siguientes herramientas en tu entorno local:

- [Terraform](https://www.terraform.io/downloads.html)
- [Checkov](https://www.checkov.io/1.Welcome/Installation.html)
- [Python 3](https://www.python.org/downloads/)

## 3. Flujo de Trabajo

### 3.1. Creación de Rama

Todo nuevo desarrollo, corrección o cambio debe realizarse en una rama nueva, creada a partir de la rama `main`.

```bash
# Asegúrate de tener la última versión de main
git checkout main
git pull origin main

# Crea una nueva rama para tus cambios
git checkout -b <nombre-descriptivo-de-la-rama>
```

### 3.2. Pasos de Validación Manual (CI)

Antes de considerar que tu trabajo está listo para ser integrado, debes ejecutar los siguientes comandos desde la raíz del repositorio para validar tu código.

#### a. Formatear el Código

Este paso asegura que todo el código de Terraform sigue una sintaxis y formato consistentes.

```bash
terraform fmt --recursive
```

#### b. Validar la Sintaxis de Terraform

Este comando comprueba que la sintaxis del código de Terraform es válida y coherente.

```bash
terraform validate
```

Si este comando devuelve errores, debes solucionarlos antes de continuar.

#### c. Escanear el Código con Checkov

Este es el paso de seguridad más importante. Checkov analizará tu código de Infraestructura como Código (IaC) en busca de malas configuraciones de seguridad conocidas.

```bash
checkov -d .
```

El comando utilizará la configuración definida en el archivo `.checkov.yaml` del repositorio. Revisa la salida del comando y soluciona todos los problemas críticos (`CRITICAL`) y altos (`HIGH`) que se reporten.

## 4. Proceso de Pull Request (PR)

Una vez que has completado y verificado todos los pasos anteriores:

1.  Añade y confirma tus cambios en tu rama.
    ```bash
    git add .
    git commit -m "feat: Descripción clara de los cambios"
    ```
2.  Sube tu rama al repositorio remoto.
    ```bash
    git push origin <nombre-descriptivo-de-la-rama>
    ```
3.  Crea una **Pull Request** en el repositorio de GitHub desde tu rama hacia la rama `main`.
4.  En la descripción de la Pull Request, **confirma explícitamente** que has seguido todos los pasos de validación manual descritos en este documento.
