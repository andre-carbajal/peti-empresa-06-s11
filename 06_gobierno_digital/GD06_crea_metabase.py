"""Crea preguntas Metabase sustentadas por los cuatro CSV disponibles.

Requiere un Metabase inicializado y una fuente PostgreSQL ya conectada.
Credenciales solo por METABASE_EMAIL y METABASE_PASSWORD; no se guardan.
NO03 registra controles descritos en S11, sin dictamen jurídico; MG03 contiene
estimaciones documentales, no una medición validada de capacidad.
"""

import csv
import json
import os
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


BASE = os.environ.get("METABASE_URL", "http://127.0.0.1:3001").rstrip("/")
EMAIL = os.environ.get("METABASE_EMAIL")
PASSWORD = os.environ.get("METABASE_PASSWORD")
DATABASE_NAME = os.environ.get("METABASE_DATABASE_NAME", "PETI Empresa 06 S11")
COLLECTION_NAME = "S11 · Línea base"
DASHBOARD_NAME = "S11 · Línea base · datos disponibles"
ROOT = Path(__file__).resolve().parents[1]


def csv_rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def as_decimal(value):
    return None if value is None else Decimal(str(value))


def rounded(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_source_parity(rows_by_name):
    """Coteja filas efectivas de Metabase con los CSV versionados."""
    services = csv_rows("06_gobierno_digital/GD01_catalogo_servicios.csv")
    by_service = {row[0]: row for row in rows_by_name[QUESTIONS[0][0]]}
    if len(by_service) != len(services):
        raise ValueError("Metabase no muestra todos los servicios de GD01.")
    for service in services:
        actual = by_service.get(service["Servicio"])
        if actual is None or as_decimal(actual[1]) != Decimal(service["Nivel actual (0–5)"]) \
                or as_decimal(actual[2]) != Decimal(service["Nivel objetivo"]):
            raise ValueError(f"Diferencia entre GD01 y Metabase: {service['Servicio']}")

    level_rows = rows_by_name[QUESTIONS[1][0]]
    if len(level_rows) != 1:
        raise ValueError("La tarjeta de promedios debe devolver una sola fila.")
    weighted, simple, missing = level_rows[0]
    levels = [Decimal(row["Nivel actual (0–5)"]) for row in services]
    volumes = [row["Volumen anual"].strip() for row in services]
    expected_simple = rounded(sum(levels) / len(levels))
    expected_missing = sum(not volume for volume in volumes)
    expected_weighted = None
    if not expected_missing:
        weights = [Decimal(volume) for volume in volumes]
        if sum(weights) > 0:
            expected_weighted = rounded(sum(a * b for a, b in zip(levels, weights)) / sum(weights))
    if as_decimal(simple) != expected_simple or int(missing) != expected_missing \
            or as_decimal(weighted) != expected_weighted:
        raise ValueError("Los promedios de Metabase no coinciden con GD01.")

    ejes = csv_rows("evidencias/S11/salidas/GD04_resumen_ejes.csv")
    by_axis = {row[0]: row for row in rows_by_name[QUESTIONS[4][0]]}
    if len(by_axis) != len(ejes):
        raise ValueError("Metabase no muestra los ocho ejes de GD04.")
    for axis in ejes:
        actual = by_axis.get(axis["eje"])
        if actual is None or as_decimal(actual[1]) != rounded(Decimal(axis["nivel"])) \
                or int(actual[2]) != int(axis["indicadores"]):
            raise ValueError(f"Diferencia entre GD04 y Metabase: {axis['eje']}")

    indicators = csv_rows("06_gobierno_digital/GD03_ejes.csv")
    expected_unmeasured = {row["ID"]: row for row in indicators if row["Línea base"] == "No se mide"}
    actual_unmeasured = {row[0]: row for row in rows_by_name[QUESTIONS[5][0]]}
    if expected_unmeasured.keys() != actual_unmeasured.keys():
        raise ValueError("Los indicadores sin línea base no coinciden con GD03.")
    for identifier, source in expected_unmeasured.items():
        actual = actual_unmeasured[identifier]
        if actual[1:] != [source["Eje"], source["Indicador"], source["Línea base"],
                          source["Proyecto de instrumentación"]]:
            raise ValueError(f"Diferencia entre GD03 y Metabase: {identifier}")
    for key, selected, predicate in (
        (QUESTIONS[6][0], "con_linea_base", lambda row: row["Línea base"] != "No se mide"),
        (QUESTIONS[7][0], "puntuados", lambda row: bool(row["Nivel del eje (1–5)"].strip())),
    ):
        expected = {}
        for source in indicators:
            counts = expected.setdefault(source["Eje"], [0, 0])
            counts[0 if predicate(source) else 1] += 1
        actual = {row[0]: [int(row[1]), int(row[2])] for row in rows_by_name[key]}
        if actual != expected:
            raise ValueError(f"Cobertura distinta entre GD03 y Metabase: {selected}")
    controls = csv_rows("04_normativa/NO03_matriz_cumplimiento.csv")
    expected_controls = {}
    for source in controls:
        state = source["Estado de verificación"]
        expected_controls[state] = expected_controls.get(state, 0) + 1
    actual_controls = {row[0]: int(row[1]) for row in rows_by_name[QUESTIONS[8][0]]}
    if actual_controls != expected_controls:
        raise ValueError("El recuento de controles S11 no coincide con NO03.")
    capacity = csv_rows("04_normativa/MG03_capacidad.csv")
    expected_capacity = {
        row["ID"]: [row["Proceso"], int(row["Capacidad actual (1-5)"]),
                    int(row["Capacidad objetivo (1-5)"])] for row in capacity
    }
    actual_capacity = {}
    for process, series, level in rows_by_name[QUESTIONS[9][0]]:
        actual_capacity.setdefault(process, {})[series] = int(level)
    expected_chart = {
        values[0]: {"Actual documental": values[1], "Objetivo propuesto": values[2]}
        for values in expected_capacity.values()
    }
    if actual_capacity != expected_chart:
        raise ValueError("La capacidad documental no coincide con MG03.")
    print("Paridad completa Metabase ↔ GD01/GD03/GD04/NO03/MG03: OK")


def api(method, path, payload=None, session=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if session:
        headers["X-Metabase-Session"] = session
    request = Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Metabase {method} {path}: HTTP {error.code}") from error


QUESTIONS = [
    (
        "01 · Nivel actual y objetivo por servicio", "row",
        "SELECT servicio, nivel_actual, nivel_objetivo FROM tablero_servicios ORDER BY id",
        {"graph.dimensions": ["servicio"], "graph.metrics": ["nivel_actual", "nivel_objetivo"]},
        "Niveles propuestos en GD01; recorridos de servicio pendientes de validación.",
    ),
    (
        "02 · Nivel ponderado y promedio simple", "table",
        "SELECT promedio_ponderado, promedio_simple, volumenes_pendientes FROM tablero_niveles",
        {}, "El ponderado queda NULL mientras falte cualquier volumen anual.",
    ),
    (
        "02a · Promedio simple provisional", "scalar",
        "SELECT promedio_simple FROM tablero_niveles",
        {}, "Promedio descriptivo; no reemplaza el ponderado por volumen.",
    ),
    (
        "02b · Volúmenes pendientes", "scalar",
        "SELECT volumenes_pendientes FROM tablero_niveles",
        {}, "Número de servicios sin volumen anual validado.",
    ),
    (
        "03 · Madurez provisional por eje", "bar",
        "SELECT eje, madurez, indicadores FROM tablero_ejes ORDER BY eje",
        {"graph.dimensions": ["eje"], "graph.metrics": ["madurez"]},
        "Diagnóstico documental; la cobertura de puntajes se explica en GD04.",
    ),
    (
        "06 · Indicadores sin línea base", "table",
        "SELECT * FROM tablero_indicadores_sin_linea_base ORDER BY id",
        {}, "Indicadores de GD03 sin medida y con proyecto de instrumentación.",
    ),
    (
        "07 · Cobertura de líneas base por eje", "bar",
        "SELECT eje, con_linea_base, sin_linea_base FROM tablero_cobertura_linea_base ORDER BY eje",
        {"graph.dimensions": ["eje"], "graph.metrics": ["con_linea_base", "sin_linea_base"]},
        "Cobertura documental de los 25 indicadores de GD03; no representa cumplimiento normativo.",
    ),
    (
        "08 · Cobertura de puntajes por eje", "bar",
        "SELECT eje, puntuados, sin_puntaje FROM tablero_cobertura_puntajes ORDER BY eje",
        {"graph.dimensions": ["eje"], "graph.metrics": ["puntuados", "sin_puntaje"]},
        "Cobertura de los puntajes de madurez de GD03; no representa capacidad de procesos.",
    ),
    (
        "04 · Estado de controles descritos en S11", "pie",
        "SELECT estado_de_verificacion, criterios FROM tablero_controles_s11 ORDER BY estado_de_verificacion",
        {"graph.dimensions": ["estado_de_verificacion"], "graph.metrics": ["criterios"]},
        "Recuento de brechas y coberturas parciales de NO03; no es dictamen de cumplimiento legal.",
    ),
    (
        "05 · Capacidad documental actual y objetivo propuesto", "bar",
        "SELECT proceso, 'Actual documental' AS serie, capacidad_actual_documental AS nivel FROM tablero_capacidad_s11 "
        "UNION ALL SELECT proceso, 'Objetivo propuesto' AS serie, capacidad_objetivo_propuesta AS nivel FROM tablero_capacidad_s11 "
        "ORDER BY proceso, serie",
        {"graph.dimensions": ["proceso", "serie"], "graph.metrics": ["nivel"]},
        "Estimación del equipo con fuentes S11; requiere validación con responsables.",
    ),
]


def main():
    if not EMAIL or not PASSWORD:
        raise SystemExit("Configure METABASE_EMAIL y METABASE_PASSWORD en la terminal.")
    parsed = urlsplit(BASE)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise SystemExit("METABASE_URL debe apuntar al Metabase local en localhost.")
    session = api("POST", "/api/session", {
        "username": EMAIL, "password": PASSWORD,
    })["id"]
    databases = api("GET", "/api/database", session=session)["data"]
    database = next((item for item in databases if item["name"] == DATABASE_NAME), None)
    if database is None:
        raise SystemExit(f"Agregue la fuente PostgreSQL '{DATABASE_NAME}' en Metabase.")
    database_id = database["id"]
    collections = api("GET", "/api/collection/", session=session)
    collection = next((item for item in collections if item["name"] == COLLECTION_NAME), None)
    if collection is None:
        collection = api("POST", "/api/collection/", {
            "name": COLLECTION_NAME,
            "description": "Empresa 06, línea base sustentada por los CSV del repositorio.",
        }, session=session)
    collection_id = collection["id"]
    existing_cards = api("GET", "/api/card/", session=session)
    card_ids = []
    rows_by_name = {}
    for name, display, query, settings, description in QUESTIONS:
        payload = {
            "name": name, "description": description, "display": display,
            "visualization_settings": settings, "collection_id": collection_id,
            "dataset_query": {
                "database": database_id, "type": "native", "native": {"query": query},
            },
        }
        existing = next((item for item in existing_cards
                         if item["name"] == name and item["collection_id"] == collection_id), None)
        if existing:
            card_id = existing["id"]
            api("PUT", f"/api/card/{card_id}", payload, session=session)
        else:
            card_id = api("POST", "/api/card/", payload, session=session)["id"]
        result = api("POST", f"/api/card/{card_id}/query", {}, session=session)
        rows = result.get("data", {}).get("rows")
        if result.get("status") != "completed" or rows is None:
            raise RuntimeError(f"Pregunta {card_id}: la consulta no terminó correctamente.")
        print(f"{name}: id {card_id}; {len(rows)} fila(s)")
        card_ids.append(card_id)
        rows_by_name[name] = rows
    validate_source_parity(rows_by_name)

    dashboards = api("GET", "/api/dashboard/", session=session)
    dashboard = next((item for item in dashboards
                      if item["name"] == DASHBOARD_NAME and item["collection_id"] == collection_id), None)
    if dashboard is None:
        dashboard = api("POST", "/api/dashboard/", {
            "name": DASHBOARD_NAME,
            "description": "Ocho preguntas distintas; controles y capacidad son evaluaciones documentales provisionales.",
            "collection_id": collection_id,
        }, session=session)
    dashboard_id = dashboard["id"]
    current = api("GET", f"/api/dashboard/{dashboard_id}", session=session)
    existing_dashcards = {item["card_id"]: item["id"] for item in current.get("dashcards", [])}
    layout = [
        (card_ids[0], 0, 0, 24, 9),
        (card_ids[1], 9, 0, 24, 4),
        (card_ids[2], 13, 0, 12, 5),
        (card_ids[3], 13, 12, 12, 5),
        (card_ids[4], 18, 0, 24, 9),
        (card_ids[5], 27, 0, 24, 10),
        (card_ids[6], 37, 0, 24, 9),
        (card_ids[7], 46, 0, 24, 9),
        (card_ids[8], 55, 0, 24, 9),
        (card_ids[9], 64, 0, 24, 9),
    ]
    dashcards = [
        {"id": existing_dashcards.get(card_id, -index - 1), "card_id": card_id,
         "row": row, "col": col, "size_x": width, "size_y": height,
         "parameter_mappings": []}
        for index, (card_id, row, col, width, height) in enumerate(layout)
    ]
    api("PUT", f"/api/dashboard/{dashboard_id}", {"dashcards": dashcards}, session=session)
    verified = api("GET", f"/api/dashboard/{dashboard_id}", session=session)
    if len(verified.get("dashcards", [])) != len(layout):
        raise RuntimeError("El tablero no contiene todas las tarjetas previstas.")
    print(f"Tablero: {BASE}/dashboard/{dashboard_id}; {len(layout)} tarjetas, 8 preguntas distintas sustentadas")


if __name__ == "__main__":
    main()
