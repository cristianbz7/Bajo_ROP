# Conexion a Supabase

Este proyecto usa PostgreSQL en Supabase con `psycopg2` y variables de entorno cargadas desde `.env`.

## Requisitos

- Python 3.12+
- Entorno virtual activado (ejemplo: `.venv`)

## Instalacion

1. Crear y activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

## Configuracion de credenciales

1. Copia el archivo de ejemplo:

```powershell
copy .env.example .env
```

2. Edita `.env` con tus credenciales reales de Supabase:

- `SUPABASE_URL` - URL de tu proyecto (ej: `https://xxxxx.supabase.co`)
- `SUPABASE_DB_PASSWORD` - Contraseña de la base de datos (Database Password)

**Variables opcionales** (ya tienen valores por defecto):
- `SUPABASE_DB_USER` - Usuario (por defecto `postgres`)
- `SUPABASE_DB_NAME` - Nombre de la BD (por defecto `postgres`)
- `SUPABASE_DB_PORT` - Puerto (por defecto `5432`)

**⚠️ IMPORTANTE:** 
- Nunca subas el archivo `.env` a Git. Ya está incluido en `.gitignore`.
- La contraseña es la **Database Password** de Supabase, NO el API Key.

## Ejecutar el script

```powershell
python bajo_ROP.py
```

## Notas de Supabase

- `sslmode="require"` ya esta configurado en el script.
- Si el acceso falla, revisa el allowlist de IP en Supabase o usa el Pooler.
- Para el Pooler, reemplaza `PGHOST` por el host del pooler y mantén el mismo usuario y password.
