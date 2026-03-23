# Migración a Checkov como Dependencia Externa

## 🎯 Resumen

Se ha modificado el Security Analyzer para usar Checkov como dependencia externa en lugar de incluir la carpeta checkov en el repositorio. Esto permite:

- ✅ **Cumplimiento legal**: No se distribuye código externo en el repo
- ✅ **Mantenimiento más limpio**: No hay que gestionar código de terceros
- ✅ **Actualizaciones automáticas**: Checkov se actualiza via pip
- ✅ **Tamaño reducido del repo**: Elimina ~100MB de código externo

## 📋 Cambios Realizados

### 1. **Nuevo Checkov Engine** (`security_analyzer/analyzer/checkov_engine.py`)
- ✅ **Dependencia externa**: Usa `subprocess` para ejecutar Checkov instalado via pip
- ✅ **Verificación de disponibilidad**: Comprueba si Checkov está instalado antes de usarlo
- ✅ **Gestión de errores**: Manejo robusto de errores y timeouts
- ✅ **Formato JSON**: Parseo de salida JSON de Checkov

### 2. **Actualizaciones de Referencias**
- ✅ **example_usage.py**: Actualizadas referencias a métodos CheckovEngine
- ✅ **cli.py**: Integración con nuevo Checkov engine
- ✅ **Importaciones**: Todas las referencias actualizadas

### 3. **Nuevos Métodos Disponibles**
```python
from security_analyzer.analyzer.checkov_engine import CheckovEngine

# Verificar disponibilidad
if CheckovEngine._check_checkov_available():
    # Validar Terraform
    results = CheckovEngine.validate_terraform("/path/to/terraform")

    # Obtener versión
    version = CheckovEngine.get_checkov_version()

    # Generar resumen
    summary = CheckovEngine.generate_summary_report(results)
```

## 🚀 Instalación y Uso

### **Instalar Checkov**
```bash
# Instalar Checkov como dependencia externa
pip install checkov

# Verificar instalación
checkov --version
```

### **Requisitos del Sistema**
```txt
# Requisitos actualizados
python>=3.8
pyyaml>=6.0
jsonschema>=4.0
checkov>=2.0  # Ahora como dependencia externa
```

### **Uso del Security Analyzer**
```bash
# Validar proyecto Terraform
python security_analyzer/cli.py validate --path ./terraform/

# Análisis completo con Checkov
python security_analyzer/cli.py analyze --path ./terraform/ --controls mcsb

# Si Checkov no está disponible, solo se usan validaciones MCSB
```

## 🗑️ Eliminación de la Carpeta Checkov

### **Para eliminar la carpeta checkov del repo:**

```bash
# 1. Verificar que no hay referencias locales a la carpeta checkov
grep -r "checkov/" . --exclude-dir=.git

# 2. Eliminar la carpeta checkov
rm -rf checkov/

# 3. Actualizar .gitignore (si es necesario)
echo "checkov/" >> .gitignore

# 4. Commit de los cambios
git add -A
git commit -m "feat: Migrar a Checkov como dependencia externa

- Eliminar carpeta checkov del repositorio
- Actualizar Security Analyzer para usar Checkov via pip
- Mantener funcionalidad completa de validación de seguridad
- Reducir tamaño del repositorio ~100MB"
git push
```

### **Verificación Post-Eliminación**
```bash
# 1. Probar que el Security Analyzer funciona
python security_analyzer/cli.py validate --path ./ejemplos/terraform/

# 2. Verificar que Checkov está disponible
python -c "from security_analyzer.analyzer.checkov_engine import check_checkov_availability; print(check_checkov_availability())"

# 3. Probar análisis completo
python security_analyzer/example_pilot_usage.py
```

## 🔍 Compatibilidad

### **Funcionalidad Mantenida**
- ✅ **Validación Checkov**: Todas las reglas Checkov siguen disponibles
- ✅ **Formato de salida**: Mismo formato JSON para reportes
- ✅ **Integración CI/CD**: Compatible con workflows existentes
- ✅ **Performance**: Similar performance (ejecución externa)

### **Nuevos Requisitos**
- ✅ **Checkov instalado**: Necesario tener `checkov` en el PATH
- ✅ **Permisos de ejecución**: El sistema debe poder ejecutar `checkov` via subprocess
- ✅ **Conexión a internet**: Para actualizaciones de Checkov (opcional)

## 📊 Comparativa

| Aspecto | Antes (Carpeta Local) | Después (Dependencia Externa) |
|---------|----------------------|-------------------------------|
| **Tamaño Repo** | +100MB | -100MB |
| **Mantenimiento** | Manual (actualizar carpeta) | Automático (pip) |
| **Legal** | Riesgo de redistribución | Cumplimiento total |
| **Performance** | Carga rápida | Ejecución externa |
| **Actualizaciones** | Manual | Automáticas |
| **Complejidad** | Baja | Media (dependencia externa) |

## 🚨 Consideraciones

### **Entornos sin Checkov**
Si Checkov no está instalado, el Security Analyzer:
- ⚠️ **Advertencia**: Muestra mensaje de Checkov no disponible
- ✅ **Continúa**: Sigue validando con reglas MCSB
- 📊 **Reporte**: Indica qué validaciones se omitieron

### **CI/CD Pipelines**
Para pipelines que usen el Security Analyzer:
```yaml
# Asegurar Checkov está instalado
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install checkov  # Añadir esta línea
```

### **Desarrollo Local**
Para desarrolladores que usen el Security Analyzer:
```bash
# Instalar dependencias
pip install -r requirements.txt
pip install checkov

# Probar funcionalidad
python security_analyzer/example_pilot_usage.py
```

## 🎉 Beneficios

1. **✅ Legalmente Seguro**: No se redistribuye código externo
2. **✅ Más Liviano**: Repo ~100MB más pequeño
3. **✅ Más Actual**: Checkov siempre actualizado
4. **✅ Más Limpio**: No gestión de código externo
5. **✅ Más Fácil**: Instalación estándar via pip

## 📞 Soporte

Para cualquier problema con la migración:
- **Issues**: Crear issue en el repositorio
- **Documentación**: Consultar esta guía
- **Ejemplos**: Ver `security_analyzer/example_pilot_usage.py`

---

**Última actualización**: Marzo 2026
**Versión**: 1.0
**Estado**: Lista para producción
