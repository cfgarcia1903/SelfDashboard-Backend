# SelfDashboard Backend

Backend Flask de SelfDashboard, organizado por capas para integrar la lógica
de negocio, persistencia y clientes externos.

## Estado actual

La API publica actualmente:

- `GET /health`: comprobación de disponibilidad.
- `GET /api/etoro/etoro/summary`: resumen de cuenta de eToro.
- `GET /api/etoro/etoro/deposits`: devuelve todos los depósitos.
- `PUT /api/etoro/etoro/deposits/edit`: crea o actualiza depósitos.
- `POST /api/etoro/etoro/deposits/delete`: elimina depósitos por identificador.

El contrato OpenAPI está en [openapi.yaml](openapi.yaml). Las rutas de otros
dominios financieros todavía no están implementadas; las rutas no registradas
responden `404 Not Found`.

Las tres operaciones de depósitos devuelven una respuesta JSON con la tabla
completa:

```json
{
  "deposits": [
    {
      "id": 3,
      "amount": 200.0,
      "currency": "USD",
      "deposited_at": "2026-09-30",
      "created_at": "2026-09-30 10:15:00"
    }
  ]
}
```

`PUT /api/etoro/etoro/deposits/edit` recibe una lista de diccionarios dentro
de `deposits`. Cada elemento necesita `amount` y `deposited_at`; `id` puede
omitirse para insertar un depósito nuevo o incluirse para actualizar uno
existente. `created_at` también puede omitirse y no se modifica durante la
actualización.

```json
{
  "deposits": [
    {
      "amount": 200.0,
      "currency": "USD",
      "deposited_at": "2026-09-30"
    },
    {
      "id": 3,
      "amount": 250.0,
      "currency": "USD",
      "deposited_at": "2026-09-29"
    }
  ]
}
```

`POST /api/etoro/etoro/deposits/delete` recibe los identificadores a eliminar:

```json
{
  "deposit_ids": [3, 8]
}
```

La validación de autorización de eToro es provisional. Los endpoints de eToro
reciben las cabeceras `user_ID`, `user_PIN` y `X-APIKEY`. El resumen de cuenta
necesita `ETORO_PUBLIC_KEY` y `ETORO_PRIVATE_KEY`; la persistencia local necesita
además `ETORO_DB_PATH`, normalmente `data/etoro.db`.

## Preparar el entorno

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Ejecutar en desarrollo

Desde la raíz del repositorio:

```powershell
$env:PYTHONPATH = "src"
$env:ETORO_DB_PATH = "data/etoro.db"
flask --app backend.app:create_app run --debug --port 5001
```

También se puede iniciar directamente:

```powershell
$env:PYTHONPATH = "src"
$env:ETORO_DB_PATH = "data/etoro.db"
python src/backend/app.py --port 5001
```

La documentación interactiva puede generarse o visualizarse con cualquier
herramienta compatible con OpenAPI 3.0 a partir de [openapi.yaml](openapi.yaml).

## Ejecutar pruebas

```powershell
$env:ETORO_DB_PATH = "data/etoro.db"
python -m pytest
```

## Estructura

```text
src/backend/
    business/      # Casos de uso y reglas de dominio
    client/        # Clientes de servicios externos
    controllers/   # Blueprints y controladores HTTP
    dao/           # Acceso a datos
    schemas/       # Modelos de solicitud y datos
    services/      # Servicios de aplicación
    app.py         # Application factory
    config.py      # Configuración por entorno
    routes.py      # Rutas transversales
tests/             # Pruebas automatizadas
```
