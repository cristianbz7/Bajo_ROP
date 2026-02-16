import os
import json
import pandas as pd
import psycopg2


SQL_BELOW_ROP = """
WITH stock_actual AS (
  SELECT DISTINCT ON (hs.sku, hs.store)
    hs.sku,
    hs.store,
    hs.stock AS stock_actual,
    hs.datetime AS stock_datetime
  FROM public.hechos_stock hs
  ORDER BY hs.sku, hs.store, hs.datetime DESC
),
stock_mapeado AS (
  SELECT
    sku,
    store,
    stock_actual,
    stock_datetime,
    CASE
      WHEN store = 'penuelas'     THEN 'PEÑUELAS'
      WHEN store = 'ulriksen'     THEN 'ULRIKSEN'
      WHEN store = 'los clarines' THEN 'LOS CLARINES'
      WHEN store = 'centro'       THEN 'Local'
      ELSE store
    END AS sucursal_norm
  FROM stock_actual
),
rop_actual AS (
  SELECT DISTINCT ON (m.sku, m.sucursal)
    m.sku,
    m.sucursal,
    m."ROP"::numeric AS rop,
    m.created_at AS metricas_datetime
  FROM public.metricas m
  ORDER BY m.sku, m.sucursal, m.created_at DESC
),
ip AS (
  SELECT
    s.sku,
    s.store,
    s.sucursal_norm AS sucursal,
    s.stock_actual,
    COALESCE(t.qty_in_transit, 0) AS qty_in_transit,
    (s.stock_actual + COALESCE(t.qty_in_transit, 0)) AS ip,
    s.stock_datetime
  FROM stock_mapeado s
  LEFT JOIN public.in_transit_by_sku t
    ON t.sku = s.sku AND t.store = s.store
)
SELECT
  ip.sku,
  ip.store,
  ip.sucursal,
  ip.stock_actual,
  ip.qty_in_transit,
  ip.ip,
  r.rop,
  (r.rop - ip.ip) AS gap,
  ip.stock_datetime,
  r.metricas_datetime
FROM ip
JOIN rop_actual r
  ON r.sku = ip.sku AND r.sucursal = ip.sucursal
WHERE ip.ip < r.rop
ORDER BY gap DESC, ip.sku;
"""


def main():
    # Recomendado: setear variables de entorno (más seguro que hardcodear)
    host = os.environ.get("PGHOST")
    dbname = os.environ.get("PGDATABASE", "postgres")
    user = os.environ.get("PGUSER")
    password = os.environ.get("PGPASSWORD")
    port = int(os.environ.get("PGPORT", "5432"))

    if not all([host, user, password]):
        raise RuntimeError("Faltan variables: PGHOST, PGUSER, PGPASSWORD (y opcional PGDATABASE, PGPORT).")

    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port,
        sslmode="require"  # Supabase normalmente lo exige
    )

    try:
        df = pd.read_sql(SQL_BELOW_ROP, conn)

        # Convertir a JSON "amigable n8n"
        items = df.to_dict(orient="records")
        print(json.dumps({"items": items}, default=str))  # default=str para timestamps
    finally:
        conn.close()


if __name__ == "__main__":
    main()
