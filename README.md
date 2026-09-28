## Self Dashboard Backend

Esqueleto de una API Flask organizada por capas. La lógica de dominio, persistencia, autenticación y consumo de eToro quedan deliberadamente pendientes.

### Preparar el entorno

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements-dev.txt
```

### Ejecutar en desarrollo

```powershell
$env:PYTHONPATH = "src"
flask --app self_dashboard_backend.app:create_app run --debug
```

La comprobación de disponibilidad está en `GET /health`. Las rutas de eToro están registradas como contrato inicial y devuelven `501 Not Implemented` hasta que se implementen sus servicios.

### Ejecutar pruebas

```powershell
python -m pytest
```

### Estructura

```text
src/self_dashboard_backend/
	api/       # Blueprints y contratos HTTP
	business/  # Casos de uso y reglas de dominio
	dao/       # Acceso a datos
	schemas/   # Validación y serialización
	services/  # Integraciones externas
	app.py     # Application factory
	config.py  # Configuración por entorno
	routes.py  # Rutas transversales
tests/       # Pruebas automatizadas
```
