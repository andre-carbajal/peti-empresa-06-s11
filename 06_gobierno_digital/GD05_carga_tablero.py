"""Carga reproducible de los CSV públicos del taller a PostgreSQL local.

Uso: DATABASE_URL=postgresql://... python 06_gobierno_digital/GD05_carga_tablero.py
Los archivos ausentes se registran como pendientes; nunca se imputan ceros.
"""

import csv
import argparse
import json
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

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
VIEW_POSITIONS = {
    "servicios": {
        "id": 0, "Servicio": 1, "Volumen anual": 3,
        "Nivel actual (0–5)": 4, "Nivel objetivo": 11,
    },
    "ejes_gd": {
        "ID": 0, "Eje": 1, "Indicador": 2, "Línea base": 3,
        "Nivel del eje (1–5)": 6, "Proyecto de instrumentación": 9,
    },
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
    for header, position in VIEW_POSITIONS.get(table, {}).items():
        if len(headers) <= position or headers[position] != header:
            raise ValueError(f"{table}: columna {position + 1} debe ser «{header}» para las vistas SQL")
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
                if not number.is_finite() or number != number.to_integral_value() or number < 0 or (field != "Volumen anual" and number > 5):
                    raise ValueError(f"{row['id']}: {field} fuera de rango")
    if table == "ejes_gd":
        for row in rows:
            value = (row["Nivel del eje (1–5)"] or "").strip()
            if value and value not in {"1", "2", "3", "4", "5"}:
                raise ValueError(f"{row['ID']}: nivel de eje inválido")
            if row["Línea base"] == "No se mide" and not (row["Proyecto de instrumentación"] or "").strip():
                raise ValueError(f"{row['ID']}: falta proyecto de instrumentación")


def load_table(conn, table, headers, rows):
    from psycopg import sql

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


def audit(prepared):
    """Comprueba cobertura y paridad con la salida versionada de GD04 sin PostgreSQL."""
    services = prepared["servicios"][1]
    ejes = prepared["ejes_gd"][1]
    levels = [Decimal(row["Nivel actual (0–5)"]) for row in services if row["Nivel actual (0–5)"]]
    volumes_missing = sum(not (row["Volumen anual"] or "").strip() for row in services)
    unmeasured = sum(row["Línea base"] == "No se mide" for row in ejes)
    by_axis = {}
    for row in ejes:
        if row["Nivel del eje (1–5)"]:
            by_axis.setdefault(row["Eje"], []).append(Decimal(row["Nivel del eje (1–5)"]))
    summary_path = ROOT / "evidencias/S11/salidas/GD04_resumen.json"
    if summary_path.exists():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if len(ejes) != summary["indicadores"] or unmeasured != summary["sin_linea_base"]:
            raise ValueError("GD03 no coincide con GD04_resumen.json en cobertura")
        for axis in summary["ejes"]:
            values = by_axis.get(axis["eje"], [])
            if len(values) != axis["puntuados"]:
                raise ValueError(f"Cobertura distinta en {axis['eje']}")
            if values and abs(float(sum(values) / len(values)) - axis["nivel"]) > 1e-9:
                raise ValueError(f"Promedio distinto en {axis['eje']}")
    print(f"Servicios: {len(services)}; volúmenes pendientes: {volumes_missing}")
    print(f"Promedio simple provisional: {sum(levels) / len(levels):.2f}" if levels else "Promedio simple: pendiente")
    print(f"Indicadores: {len(ejes)}; sin línea base: {unmeasured}; puntuados: {sum(map(len, by_axis.values()))}")
    print("Paridad con GD04_resumen.json: OK" if summary_path.exists() else "Paridad con GD04: sin archivo de referencia")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validar CSV y paridad GD04 sin conectar a PostgreSQL")
    args = parser.parse_args()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url and not args.check:
        raise SystemExit("Falta DATABASE_URL. Configure la variable de entorno sin versionar credenciales.")
    prepared = {}
    for table, path in SOURCES.items():
        if path.exists():
            headers, rows = read_csv(path)
            validate(table, headers, rows)
            prepared[table] = (headers, rows)
        else:
            print(f"{table}: PENDIENTE — falta {path.relative_to(ROOT)}")
    if "servicios" in prepared and "ejes_gd" in prepared:
        audit(prepared)
    if args.check:
        return
    import psycopg
    from psycopg import sql

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS tablero_columnas (
                tabla text NOT NULL, columna text NOT NULL, encabezado text NOT NULL,
                PRIMARY KEY (tabla, columna))""")
        for table, (headers, rows) in prepared.items():
            print(f"{table}: {load_table(conn, table, headers, rows)} filas de {SOURCES[table].relative_to(ROOT)}")
        for table in SOURCES.keys() - prepared.keys():
            with conn.cursor() as cur:
                cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table)))
                cur.execute("DELETE FROM tablero_columnas WHERE tabla = %s", (table,))
        if "servicios" in prepared and "ejes_gd" in prepared:
            make_views(conn)
        conn.commit()


if __name__ == "__main__":
    main()
