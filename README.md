# Conexion a Supabase

Este proyecto usa PostgreSQL en Supabase con `psycopg2` y variables de entorno.

## Requisitos

- Python 3.12
- Entorno virtual activado (ejemplo: `.venv`)
- Paquete: `psycopg2-binary`

Instalacion:

```powershell
python -m pip install psycopg2-binary
```

## Variables de entorno requeridas

Configura estas variables antes de ejecutar el script:

- `PGHOST` (host de Supabase)
- `PGUSER` (usuario)
- `PGPASSWORD` (password)
- `PGDATABASE` (opcional, por defecto `postgres`)
- `PGPORT` (opcional, por defecto `5432`)

Ejemplo en PowerShell (solo para la sesion actual):

```powershell
$env:PGHOST="<tu-host>"
$env:PGUSER="<tu-usuario>"
$env:PGPASSWORD="<tu-password>"
$env:PGDATABASE="postgres"
$env:PGPORT="5432"
```

## Ejecutar el script

```powershell
python bajo_ROP.py
```

## Notas de Supabase

- `sslmode="require"` ya esta configurado en el script.
- Si el acceso falla, revisa el allowlist de IP en Supabase o usa el Pooler.
- Para el Pooler, reemplaza `PGHOST` por el host del pooler y mantén el mismo usuario y password.
