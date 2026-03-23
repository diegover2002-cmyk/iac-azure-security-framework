"""
Checkov Integration Engine - Dependencia Externa
Integración con Checkov como dependencia externa (pip install checkov)
"""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CheckovResult:
    """Resultado de una validación Checkov"""
    file_path: str
    check_id: str
    check_name: str
    severity: str
    resource: str
    file_line_range: List[int]
    code_block: List[List[int]]
    guideline: Optional[str] = None


class CheckovEngine:
    """Motor de integración con Checkov como dependencia externa"""

    def __init__(self, checkov_path: Optional[str] = None):
        """
        Inicializa el motor Checkov

        Args:
            checkov_path: Ruta al ejecutable checkov (opcional)
        """
        self.checkov_path = checkov_path
        self._check_checkov_available()

    def _check_checkov_available(self) -> bool:
        """Verifica si Checkov está disponible como dependencia externa"""
        try:
            # Intentar ejecutar checkov --version para verificar disponibilidad
            result = subprocess.run(
                ['checkov', '--version'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info(f"Checkov disponible: {result.stdout.strip()}")
                return True
            else:
                logger.warning("Checkov no está disponible como dependencia externa")
                return False

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"Checkov no disponible: {e}")
            return False

    def validate_terraform(self, terraform_path: str) -> Dict[str, Any]:
        """
        Valida archivos Terraform usando Checkov

        Args:
            terraform_path: Ruta al directorio o archivo Terraform

        Returns:
            Dict con resultados de validación Checkov
        """
        if not self._check_checkov_available():
            logger.warning("Checkov no está disponible, omitiendo validación")
            return {"results": [], "summary": {}}

        try:
            # Crear archivo temporal para salida JSON
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_path = temp_file.name

            # Comando Checkov para validación Terraform
            cmd = [
                'checkov',
                '-f', terraform_path,
                '-o', 'json',
                '--output-file', temp_path,
                '--soft-fail'  # No fallar en errores, solo reportar
            ]

            logger.info(f"Ejecutando Checkov: {' '.join(cmd)}")

            # Ejecutar Checkov
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )

            # Leer resultados
            checkov_results = self._parse_checkov_output(temp_path)

            # Limpiar archivo temporal
            try:
                os.unlink(temp_path)
            except OSError:
                pass

            if result.returncode == 0:
                logger.info(f"Checkov completado exitosamente: {len(checkov_results.get('results', []))} resultados")
            else:
                logger.warning(f"Checkov completado con advertencias: {result.stderr}")

            return checkov_results

        except subprocess.TimeoutExpired:
            logger.error("Checkov timeout después de 5 minutos")
            return {"results": [], "summary": {}}
        except Exception as e:
            logger.error(f"Error ejecutando Checkov: {e}")
            return {"results": [], "summary": {}}

    def validate_single_file(self, file_path: str) -> Dict[str, Any]:
        """
        Valida un archivo Terraform específico

        Args:
            file_path: Ruta al archivo Terraform

        Returns:
            Dict con resultados de validación
        """
        return self.validate_terraform(file_path)

    def validate_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Valida todos los archivos Terraform en un directorio

        Args:
            directory_path: Ruta al directorio

        Returns:
            Dict con resultados de validación
        """
        return self.validate_terraform(directory_path)

    def get_checkov_version(self) -> Optional[str]:
        """Obtiene la versión de Checkov instalada"""
        try:
            result = subprocess.run(
                ['checkov', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None

        except Exception:
            return None

    def _parse_checkov_output(self, output_file: str) -> Dict[str, Any]:
        """
        Parsea la salida JSON de Checkov

        Args:
            output_file: Archivo JSON de salida de Checkov

        Returns:
            Dict con resultados parseados
        """
        try:
            with open(output_file, 'r') as f:
                data = json.load(f)

            # Estructura típica de salida Checkov
            results = []
            summary = {}

            if isinstance(data, list):
                # Formato de lista de resultados
                results = data
            elif isinstance(data, dict):
                # Formato con resultados y resumen
                results = data.get('results', [])
                summary = data.get('summary', {})

            return {
                "results": results,
                "summary": summary
            }

        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON de Checkov: {e}")
            return {"results": [], "summary": {}}
        except FileNotFoundError:
            logger.error(f"Archivo de salida Checkov no encontrado: {output_file}")
            return {"results": [], "summary": {}}
        except Exception as e:
            logger.error(f"Error procesando salida Checkov: {e}")
            return {"results": [], "summary": {}}

    def filter_results_by_severity(self, results: Dict[str, Any], severity: str) -> List[Dict[str, Any]]:
        """
        Filtra resultados por severidad

        Args:
            results: Resultados de Checkov
            severity: Severidad a filtrar (HIGH, MEDIUM, LOW)

        Returns:
            Lista de resultados filtrados
        """
        filtered_results = []

        for result in results.get('results', []):
            if isinstance(result, dict):
                result_severity = result.get('severity', '').upper()
                if result_severity == severity.upper():
                    filtered_results.append(result)

        return filtered_results

    def get_failed_checks(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtiene solo los checks que fallaron"""
        failed_results = []

        for result in results.get('results', []):
            if isinstance(result, dict):
                check_result = result.get('check_result', {})
                if check_result.get('result') == 'FAILED':
                    failed_results.append(result)

        return failed_results

    def get_passed_checks(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtiene solo los checks que pasaron"""
        passed_results = []

        for result in results.get('results', []):
            if isinstance(result, dict):
                check_result = result.get('check_result', {})
                if check_result.get('result') == 'PASSED':
                    passed_results.append(result)

        return passed_results

    def get_skipped_checks(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtiene solo los checks que fueron omitidos"""
        skipped_results = []

        for result in results.get('results', []):
            if isinstance(result, dict):
                check_result = result.get('check_result', {})
                if check_result.get('result') == 'SKIPPED':
                    skipped_results.append(result)

        return skipped_results

    def generate_summary_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera un reporte resumen de resultados Checkov

        Args:
            results: Resultados de Checkov

        Returns:
            Dict con resumen de resultados
        """
        all_results = results.get('results', [])

        # Contar por estado
        passed = 0
        failed = 0
        skipped = 0

        # Contar por severidad
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}

        # Contar por check ID
        check_counts = {}

        for result in all_results:
            if isinstance(result, dict):
                check_result = result.get('check_result', {})
                result_status = check_result.get('result', 'UNKNOWN')

                if result_status == 'PASSED':
                    passed += 1
                elif result_status == 'FAILED':
                    failed += 1
                elif result_status == 'SKIPPED':
                    skipped += 1

                # Contar por severidad
                severity = result.get('severity', 'UNKNOWN').upper()
                if severity in severity_counts:
                    severity_counts[severity] += 1

                # Contar por check ID
                check_id = result.get('check_id', 'UNKNOWN')
                check_counts[check_id] = check_counts.get(check_id, 0) + 1

        return {
            "total_checks": len(all_results),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "severity_breakdown": severity_counts,
            "check_breakdown": check_counts,
            "summary": results.get('summary', {})
        }


# Función de conveniencia para uso rápido
def quick_checkov_validation(terraform_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para validación rápida con Checkov

    Args:
        terraform_path: Ruta al archivo o directorio Terraform

    Returns:
        Dict con resultados de validación
    """
    engine = CheckovEngine()
    return engine.validate_terraform(terraform_path)


def check_checkov_availability() -> bool:
    """Verifica si Checkov está disponible como dependencia externa"""
    engine = CheckovEngine()
    return engine._check_checkov_available()


# Ejemplo de uso
if __name__ == "__main__":
    # Verificar disponibilidad
    if check_checkov_availability():
        print("✅ Checkov está disponible como dependencia externa")

        # Validar un proyecto
        results = quick_checkov_validation("./terraform/")
        print(f"Resultados: {len(results.get('results', []))} checks")

        # Generar resumen
        summary = CheckovEngine().generate_summary_report(results)
        print(f"Resumen: {summary}")
    else:
        print("❌ Checkov no está disponible. Instala con: pip install checkov")
