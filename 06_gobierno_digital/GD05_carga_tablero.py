"""Carga reproducible de los CSV públicos del taller a PostgreSQL local.

Uso: DATABASE_URL=postgresql://... python 06_gobierno_digital/GD05_carga_tablero.py
Los archivos ausentes se registran como pendientes; nunca se imputan ceros.
"""

import csv
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

import psycopg
from psycopg import sql


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "servicios": ROOT / "06_gobierno_digital/GD01_catalogo_servicios.csv",
    "ejes_gd": ROOT / "06_gobierno_digital/GD03_ejes.csv",
    "cumplimiento": ROOT / "04_normativa/NO03_matriz_cumplimiento.csv",
    "capacidad": ROOT / "04_normativa/MG03_capacidad.csv",
}
REQUIRED = {
    "servicios": ["id", "Servicio", "Volumen anual", "Nivel actual (0–5)", "Nivel objetivo"],
    "ejes_gd": ["ID", "Eje", "Indicador", "Línea base", "Nivel del eje (1–5)", "Proyecto de instrumentación"],
}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError(f"Encabezados vacíos o duplicados: {path}")
        rows = list(reader)
        if any(None in row for row in rows):
            raise ValueError(f"Filas con más campos que encabezados: {path}")
    return reader.fieldnames, rows


def validate(table, headers, rows):
    missing = set(REQUIRED.get(table, ())) - set(headers)
    if missing:
        raise ValueError(f"{table}: faltan columnas {', '.join(sorted(missing))}")
    if not rows:
        raise ValueError(f"{table}: el archivo está vacío")
    if table == "servicios":
        for row in rows:
            for field in ("Volumen anual", "Nivel actual (0–5)", "Nivel objetivo"):
                value = (row[field] or "").strip()
                if not value:
                    continue
                try:
                    number = Decimal(value)
                except InvalidOperation as exc:
                    raise ValueError(f"{row['id']}: {field} no es numérico") from exc
                if number != int(number) or number < 0 or (field != "Volumen anual" and number > 5):
                    raise ValueError(f"{row['id']}: {field} fuera de rango")
    if table == "ejes_gd":
        for row in rows:
            value = (row["Nivel del eje (1–5)"] or "").strip()
            if value and value not in {"1", "2", "3", "4", "5"}:
                raise ValueError(f"{row['ID']}: nivel de eje inválido")
            if row["Línea base"] == "No se mide" and not (row["Proyecto de instrumentación"] or "").strip():
                raise ValueError(f"{row['ID']}: falta proyecto de instrumentación")


def load_table(conn, table, headers, rows):
    columns = [f"col_{i:02d}" for i in range(len(headers))]
    with conn.cursor() as cur:
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table)))
        definitions = sql.SQL(", ").join(
            sql.SQL("{} text").format(sql.Identifier(col)) for col in columns
        )
        cur.execute(sql.SQL("CREATE TABLE {} (row_number integer generated always as identity, {})").format(
            sql.Identifier(table), definitions
        ))
        cur.executemany(
            sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(", ").join(sql.Placeholder() for _ in columns),
            ),
            [tuple((row[h] or None) for h in headers) for row in rows],
        )
        cur.execute("DELETE FROM tablero_columnas WHERE tabla = %s", (table,))
        cur.executemany(
            "INSERT INTO tablero_columnas(tabla, columna, encabezado) VALUES (%s, %s, %s)",
            [(table, col, header) for col, header in zip(columns, headers)],
        )
    return len(rows)


def make_views(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE OR REPLACE VIEW tablero_servicios AS
            SELECT col_00 AS id, col_01 AS servicio,
              NULLIF(col_03, '')::numeric AS volumen_anual,
              NULLIF(col_04, '')::numeric AS nivel_actual,
              NULLIF(col_11, '')::numeric AS nivel_objetivo
            FROM servicios""")
        cur.execute("""CREATE OR REPLACE VIEW tablero_niveles AS
            SELECT round(avg(nivel_actual), 2) AS promedio_simple,
              CASE WHEN count(*) FILTER (WHERE volumen_anual IS NULL OR nivel_actual IS NULL) = 0
                        AND sum(volumen_anual) > 0
                   THEN round(sum(volumen_anual * nivel_actual) / sum(volumen_anual), 2)
                   ELSE NULL END AS promedio_ponderado,
              count(*) AS servicios,
              count(*) FILTER (WHERE volumen_anual IS NULL) AS volumenes_pendientes
            FROM tablero_servicios""")
        cur.execute("""CREATE OR REPLACE VIEW tablero_ejes AS
            SELECT col_01 AS eje,
              round(avg(NULLIF(col_06, '')::numeric), 2) AS madurez,
              count(*) AS indicadores,
              count(*) FILTER (WHERE col_03 = 'No se mide' OR col_06 IS NULL) AS sin_linea_base
            FROM ejes_gd GROUP BY col_01""")
        cur.execute("""CREATE OR REPLACE VIEW tablero_indicadores_sin_linea_base AS
            SELECT col_00 AS id, col_01 AS eje, col_02 AS indicador,
              col_03 AS linea_base, col_09 AS proyecto_de_instrumentacion
            FROM ejes_gd WHERE col_03 = 'No se mide'""")


def main():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("Falta DATABASE_URL. Configure la variable de entorno sin versionar credenciales.")
    prepared = {}
    for table, path in SOURCES.items():
        if path.exists():
            headers, rows = read_csv(path)
            validate(table, headers, rows)
            prepared[table] = (headers, rows)
        else:
            print(f"{table}: PENDIENTE — falta {path.relative_to(ROOT)}")
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS tablero_columnas (
                tabla text NOT NULL, columna text NOT NULL, encabezado text NOT NULL,
                PRIMARY KEY (tabla, columna))""")
        for table, (headers, rows) in prepared.items():
            print(f"{table}: {load_table(conn, table, headers, rows)} filas de {SOURCES[table].relative_to(ROOT)}")
        if "servicios" in prepared and "ejes_gd" in prepared:
            make_views(conn)
        conn.commit()


if __name__ == "__main__":
    main()
