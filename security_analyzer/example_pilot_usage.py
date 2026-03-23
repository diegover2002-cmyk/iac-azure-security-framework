"""
Ejemplo de uso del Security Analyzer - Piloto 58 Controles
Demostración de cómo validar proyectos Terraform contra los controles MCSB
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Importar los módulos del Security Analyzer
from security_analyzer.analyzer.terraform_parser import TerraformParser
from security_analyzer.analyzer.pilot_validation_functions import (
    validate_pilot_controls,
    get_pilot_summary,
    ValidationResult
)
from security_analyzer.analyzer.report_generator import ReportGenerator


def load_sample_terraform_resources() -> List[Dict[str, Any]]:
    """Carga recursos Terraform de ejemplo para demostración"""
    return [
        # Storage Account - Algunos controles fallan
        {
            "type": "azurerm_storage_account",
            "name": "insecurestorage",
            "attributes": {
                "name": "insecurestorage123",
                "allow_blob_public_access": "true",  # ❌ ST-001: Debe ser false
                "enable_https_traffic_only": "false",  # ❌ ST-002: Debe ser true
                "min_tls_version": "1.0",             # ❌ ST-003: Debe ser 1.2
                "infrastructure_encryption_enabled": "false",  # ❌ ST-004: Debe ser true
                "network_rules": {
                    "default_action": "Allow"         # ❌ ST-006: Debe ser Deny
                },
                "soft_delete_retention_days": 1,      # ❌ ST-009: Debe ser >= 7
                "is_versioning_enabled": "false",     # ❌ ST-010: Debe ser true
                "allow_shared_key_access": "true"     # ❌ ST-011: Debe ser false
            }
        },
        # Key Vault - Algunos controles pasan, otros fallan
        {
            "type": "azurerm_key_vault",
            "name": "securevault",
            "attributes": {
                "name": "securevault123",
                "public_network_access_enabled": "false",  # ✅ KV-001: Correcto
                "network_acls": {
                    "default_action": "Deny"               # ✅ KV-003: Correcto
                },
                "soft_delete_enabled": "true",             # ✅ KV-005: Correcto
                "purge_protection_enabled": "true",        # ✅ KV-006: Correcto
                "enable_rbac_authorization": "false"       # ❌ KV-007: Debe ser true
            }
        },
        # App Service - Algunos controles fallan
        {
            "type": "azurerm_app_service",
            "name": "insecureapp",
            "attributes": {
                "name": "insecureapp123",
                "https_only": "false",                    # ❌ AS-001: Debe ser true
                "minimum_tls_version": "1.0",             # ❌ AS-002: Debe ser 1.2
                "identity": {
                    "type": "None"                        # ❌ AS-005: Debe ser SystemAssigned
                },
                "logs": {},                               # ❌ AS-007: Debe tener configuración
                "site_config": {
                    "ip_restriction": []                  # ❌ AS-011: Debe tener restricciones
                }
            }
        },
        # AKS - Algunos controles fallan
        {
            "type": "azurerm_kubernetes_cluster",
            "name": "insecureaks",
            "attributes": {
                "name": "insecureaks123",
                "api_server_authorized_ip_ranges": [],    # ❌ AK-001: Debe tener rangos
                "azure_active_directory": {
                    "managed": "false"                    # ❌ AK-003: Debe ser true
                },
                "aad_profile": {
                    "managed": "false"                    # ❌ AK-004: Debe ser true
                },
                "role_based_access_control": {
                    "enabled": "false"                    # ❌ AK-005: Debe ser true
                },
                "network_profile": {
                    "network_policy": "none"              # ❌ AK-006: Debe ser calico
                },
                "auto_upgrade_channel": ""                # ❌ AK-007: Debe tener canal
            }
        },
        # Virtual Network - Algunos controles fallan
        {
            "type": "azurerm_subnet",
            "name": "insecuresubnet",
            "attributes": {
                "name": "insecuresubnet123",
                "network_security_group_id": ""          # ❌ VN-001: Debe tener NSG
            }
        },
        # NSG - Algunos controles fallan
        {
            "type": "azurerm_network_security_group",
            "name": "insecurensg",
            "attributes": {
                "name": "insecurensg123",
                "security_rule": [
                    {
                        "name": "Allow-SSH",
                        "source_address_prefix": "0.0.0.0/0",  # ❌ VN-003: No debe ser 0.0.0.0/0
                        "destination_port_range": "22",
                        "direction": "Inbound"
                    },
                    {
                        "name": "Allow-RDP",
                        "source_address_prefix": "0.0.0.0/0",  # ❌ VN-004: No debe ser 0.0.0.0/0
                        "destination_port_range": "3389",
                        "direction": "Inbound"
                    },
                    {
                        "name": "Allow-All",
                        "source_address_prefix": "*",          # ❌ VN-008: No debe ser *
                        "destination_port_range": "*",
                        "direction": "Inbound"
                    }
                ]
            }
        },
        # Virtual Network - Algunos controles fallan
        {
            "type": "azurerm_virtual_network",
            "name": "insecurevnet",
            "attributes": {
                "name": "insecurevnet123",
                "ddos_protection_plan": {}                   # ❌ VN-005: Debe tener DDoS protection
            }
        }
    ]


def run_pilot_validation():
    """Ejecuta la validación piloto de los 58 controles"""
    print("🚀 Security Analyzer - Piloto 58 Controles")
    print("=" * 60)

    # Cargar recursos de ejemplo
    print("📁 Cargando recursos Terraform de ejemplo...")
    resources = load_sample_terraform_resources()
    print(f"✅ Cargados {len(resources)} recursos para validación")

    # Validar contra controles piloto
    print("\n🔍 Validando recursos contra controles MCSB...")
    validation_results = validate_pilot_controls(resources)

    # Generar resumen
    summary = get_pilot_summary(validation_results)

    # Mostrar resultados
    print("\n📊 RESULTADOS DE VALIDACIÓN")
    print("=" * 60)

    print(f"📋 Total de controles analizados: {summary['total_controls']}")
    print(f"❌ Controles con fallas: {summary['total_failures']}")
    print(f"✅ Controles aprobados: {summary['total_controls'] - summary['total_failures']}")

    print(f"\n📈 DESGLOSE POR SERVICIO:")
    for service, count in summary['services'].items():
        print(f"   • {service}: {count} fallas")

    print(f"\n🚨 DESGLOSE POR SEVERIDAD:")
    for severity, count in summary['severity_breakdown'].items():
        emoji = "🔴" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
        print(f"   {emoji} {severity}: {count}")

    print(f"\n🎯 DESGLOSE POR PRIORIDAD:")
    for priority, count in summary['priority_breakdown'].items():
        symbol = "❗" if priority == "MUST" else "⚠️" if priority == "SHOULD" else "ℹ️"
        print(f"   {symbol} {priority}: {count}")

    # Mostrar detalles de fallas críticas
    print(f"\n🚨 FALLAS CRÍTICAS (HIGH)")
    print("-" * 40)
    critical_failures = [r for r in validation_results if r.severity.value == "HIGH"]

    for i, result in enumerate(critical_failures[:10], 1):  # Mostrar solo las 10 primeras
        print(f"{i:2d}. {result.control_id} - {result.service}")
        print(f"    Recurso: {result.resource_type}.{result.resource_name}")
        print(f"    Mensaje: {result.message}")
        if result.checkov_rule:
            print(f"    Checkov: {result.checkov_rule}")
        print()

    if len(critical_failures) > 10:
        print(f"    ... y {len(critical_failures) - 10} más fallas críticas")

    # Generar reporte
    print(f"\n📄 GENERANDO REPORTE")
    print("-" * 40)

    report_data = {
        "summary": summary,
        "failures": [
            {
                "control_id": r.control_id,
                "service": r.service,
                "resource": f"{r.resource_type}.{r.resource_name}",
                "severity": r.severity.value,
                "priority": r.priority.value,
                "message": r.message,
                "checkov_rule": r.checkov_rule,
                "terraform_example": r.terraform_example
            }
            for r in validation_results
        ]
    }

    # Guardar reporte JSON
    report_file = "pilot_validation_report.json"
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)

    print(f"✅ Reporte guardado en: {report_file}")

    # Simular bloqueo de PR (para CI/CD)
    print(f"\n🔒 SIMULACIÓN DE BLOQUEO DE PR")
    print("-" * 40)

    critical_count = summary['severity_breakdown']['HIGH']
    must_failures = summary['priority_breakdown']['MUST']

    if critical_count > 0 or must_failures > 0:
        print(f"❌ PR BLOQUEADO: {critical_count} fallas críticas, {must_failures} controles MUST fallidos")
        print("   Se deben corregir antes de mergear.")
        return False
    else:
        print("✅ PR APROBADO: No hay fallas críticas ni controles MUST fallidos")
        return True


def simulate_cicd_integration():
    """Simula la integración con CI/CD"""
    print("\n🔄 SIMULACIÓN DE INTEGRACIÓN CI/CD")
    print("=" * 60)

    # Simular validación en pipeline
    print("📦 Pipeline: Validando cambios en Terraform...")

    # Cargar recursos (en un pipeline real, esto vendría de los archivos .tf)
    resources = load_sample_terraform_resources()

    # Validar controles críticos (MUST + HIGH)
    validation_results = validate_pilot_controls(resources)
    critical_failures = [
        r for r in validation_results
        if r.severity.value == "HIGH" and r.priority.value == "MUST"
    ]

    if critical_failures:
        print(f"❌ Pipeline fallido: {len(critical_failures)} controles críticos fallidos")
        print("   Deteniendo despliegue...")

        # Generar reporte para el desarrollador
        print("\n📝 Reporte para desarrollador:")
        for failure in critical_failures[:5]:  # Mostrar primeras 5
            print(f"   • {failure.control_id}: {failure.message}")

        return False
    else:
        print("✅ Pipeline exitoso: No hay controles críticos fallidos")
        print("   Continuando con despliegue...")
        return True


def main():
    """Función principal"""
    print("🎯 Security Analyzer - Demostración Piloto")
    print("Validación de 58 controles MCSB para servicios Azure")
    print()

    try:
        # Ejecutar validación piloto
        pr_approved = run_pilot_validation()

        # Simular CI/CD
        pipeline_success = simulate_cicd_integration()

        print(f"\n🏁 RESUMEN FINAL")
        print("=" * 60)
        print(f"✅ Validación piloto completada")
        print(f"📋 Controles analizados: 58")
        print(f"🔍 Controles con fallas: {len(validate_pilot_controls(load_sample_terraform_resources()))}")
        print(f"🔒 PR {'APROBADO' if pr_approved else 'BLOQUEADO'}")
        print(f"🚀 Pipeline {'EXITOSO' if pipeline_success else 'FALLIDO'}")

        return 0 if (pr_approved and pipeline_success) else 1

    except Exception as e:
        print(f"❌ Error durante la validación: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
