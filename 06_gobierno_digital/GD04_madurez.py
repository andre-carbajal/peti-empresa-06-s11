"""Diagnóstico documental de Empresa 06, adaptado de GD04 del curso.

El vacío en la columna de nivel significa no evaluado; nunca se reemplaza por 1.
El promedio global otorga el mismo peso a cada eje con cobertura completa de ejes.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LEVEL = "Nivel del eje (1–5)"
BASELINE = "Línea base"
BASELINE_STATE = "Estado de línea base"
PROJECT = "Proyecto de instrumentación"
NO_MEASUREMENT = "no se mide"
AXES = (
    "1. Gobernanza", "2. Servicios", "3. Interoperabilidad",
    "4. Seguridad digital", "5. Datos", "6. Identidad digital",
    "7. Talento", "8. Infraestructura",
)
REQUIRED = (
    "ID", "Eje", "Indicador", BASELINE, "Fuente y fecha del dato",
    "Evidencia", LEVEL, "Observación", BASELINE_STATE,
    PROJECT,
)
NAMES = {
    1: "Inicial — reactivo", 2: "Emergente — en formación",
    3: "Definido — estructurado", 4: "Gestionado — medido",
    5: "Optimizado — centrado en el usuario",
}


def leer_ejes(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        missing = set(REQUIRED) - set(headers)
        if missing:
            raise ValueError("Faltan columnas: " + ", ".join(sorted(missing)))
        if len(headers) != len(set(headers)):
            raise ValueError("Hay columnas duplicadas.")
        rows = []
        for number, original in enumerate(reader, start=2):
            if None in original or any(value is None for value in original.values()):
                raise ValueError(f"Fila {number}: cantidad de columnas incorrecta.")
            rows.append({key: value.strip() for key, value in original.items()})
    validar_ejes(rows)
    return rows


def validar_linea_base(row):
    identifier = row["ID"]
    no_baseline = row[BASELINE].casefold() == NO_MEASUREMENT
    if no_baseline != (row[BASELINE_STATE] == "No disponible"):
        raise ValueError(f"{identifier}: estado y disponibilidad de línea base no coinciden.")
    if no_baseline and not row[PROJECT].startswith("P-"):
        raise ValueError(f"{identifier}: falta proyecto de instrumentación.")
    if row[BASELINE_STATE] not in {"Declarada", "Documental", "Calculada", "No disponible"}:
        raise ValueError(f"{identifier}: estado de línea base desconocido.")


def validar_fila(row):
    identifier = row["ID"]
    if row["Eje"] not in AXES:
        raise ValueError(f"{identifier}: eje desconocido.")
    for field in REQUIRED:
        if field != LEVEL and not row[field]:
            raise ValueError(f"{identifier}: falta «{field}».")
    score = row[LEVEL]
    if score and score not in {"1", "2", "3", "4", "5"}:
        raise ValueError(f"{identifier}: nivel inválido; use enteros 1–5 o vacío.")
    validar_linea_base(row)
    url = urlparse(row["Evidencia"])
    if url.scheme != "https" or url.netloc != "github.com":
        raise ValueError(f"{identifier}: se requiere una URL HTTPS de evidencia en GitHub.")


def validar_ejes(rows):
    if not rows:
        raise ValueError("El diagnóstico está vacío.")
    counts = Counter()
    identifiers = set()
    for row in rows:
        identifier = row["ID"]
        if not identifier or identifier in identifiers:
            raise ValueError("Cada indicador debe tener un ID único y no vacío.")
        identifiers.add(identifier)
        validar_fila(row)
        counts[row["Eje"]] += 1
    for axis in AXES:
        if counts[axis] < 2:
            raise ValueError(f"{axis}: se requieren al menos dos indicadores.")


def resumir(rows):
    axes = []
    for axis in AXES:
        selected = [row for row in rows if row["Eje"] == axis]
        scores = [int(row[LEVEL]) for row in selected if row[LEVEL]]
        axes.append({
            "eje": axis,
            "indicadores": len(selected),
            "puntuados": len(scores),
            "sin_linea_base": sum(row[BASELINE].casefold() == NO_MEASUREMENT for row in selected),
            "nivel": mean(scores) if scores else None,
        })
    # No se redondean los promedios por eje antes de promediar los ocho ejes.
    global_score = mean(axis["nivel"] for axis in axes) if all(
        axis["nivel"] is not None for axis in axes
    ) else None
    no_baseline = [row for row in rows if row[BASELINE].casefold() == NO_MEASUREMENT]
    unscored = [row["ID"] for row in rows if not row[LEVEL]]
    return {
        "fecha_revision_documental": "2026-10-22",
        "alcance": "Diagnóstico documental provisional; no es entrevista ni validación operativa.",
        "indicadores": len(rows),
        "con_linea_base": len(rows) - len(no_baseline),
        "sin_linea_base": len(no_baseline),
        "puntuados": len(rows) - len(unscored),
        "sin_puntaje": unscored,
        "ejes": axes,
        "nivel_global": global_score,
        "posicionamiento": NAMES[round(global_score)] if global_score is not None else "No evaluable: faltan ejes",
        "metodo": "Media de puntajes conocidos dentro de cada eje; media de ocho ejes, sin ponderación por volumen.",
        "limitacion": "Los niveles vacíos se excluyen; el resultado parcial no acredita la madurez de todos los indicadores.",
        "proyectos": [
            {"id": row["ID"], "eje": row["Eje"], "indicador": row["Indicador"],
             "proyecto": row[PROJECT]}
            for row in no_baseline
        ],
    }


def construir_salida(summary):
    lines = [
        "EMPRESA 06 — DIAGNÓSTICO DOCUMENTAL DE GOBIERNO DIGITAL",
        "Responsable del entregable: Persona 2 (Sofxx7)",
        "Fecha de revisión documental: " + summary["fecha_revision_documental"],
        "La revisión no es la fecha de medición de los hechos.",
        "Fuente de entrada: 06_gobierno_digital/GD03_ejes.csv",
        "", "=== NIVEL POR EJE ===",
    ]
    for axis in summary["ejes"]:
        score = f'{axis["nivel"]:.2f}' if axis["nivel"] is not None else "No evaluable"
        lines.append(
            f'{axis["eje"]}: {score}/5 | {axis["puntuados"]}/{axis["indicadores"]} '
            f'puntuados | {axis["sin_linea_base"]} sin línea base'
        )
    lines.extend([
        "",
        f'Indicadores: {summary["indicadores"]}; con línea base: {summary["con_linea_base"]}; '
        f'sin línea base: {summary["sin_linea_base"]}.',
        f'Puntajes documentados: {summary["puntuados"]}/{summary["indicadores"]}.',
        "Indicadores sin puntaje: " + ", ".join(summary["sin_puntaje"]),
    ])
    if summary["nivel_global"] is None:
        lines.append("NIVEL GLOBAL: no evaluable; falta al menos un eje con puntaje.")
    else:
        lines.extend([
            f'NIVEL GLOBAL PROVISIONAL: {summary["nivel_global"]:.2f} de 5',
            "Posicionamiento orientativo: " + summary["posicionamiento"],
        ])
    lines.extend([
        "", summary["metodo"], summary["limitacion"],
        "No se reemplaza un dato desconocido por cero ni un puntaje desconocido por 1.",
        "SEG-03 no tiene cantidad de incidentes, pero sí puntaje de la práctica: se declara que no se registran.",
        "Los niveles 1–5 de madurez no son los niveles 0–5 de digitalización de servicios.",
        "", "=== INDICADORES SIN LÍNEA BASE Y PROYECTOS ===",
    ])
    for project in summary["proyectos"]:
        lines.extend([project["id"] + " — " + project["indicador"], project["proyecto"], ""])
    lines.extend([
        "=== CÁLCULOS DOCUMENTALES REPRODUCIBLES ===",
        "SER-01: dueños designados = 0/7 x 100 = 0 %.",
        "SER-02: acuerdos escritos = 0/7 x 100 = 0 % (distintos del contrato del proveedor ERP).",
        f"SER-03: clasificación completa = (1929 - 595)/1929 x 100 = {(1929 - 595) / 1929 * 100:.6f} %.",
        "INF-01: sistemas con soporte Sí = 3/5 x 100 = 60 %; 1 Parcial y 1 No.",
        "El 4,7 % de diferencia de inventario es declarado por la ficha; no se recalculó.",
        "", "=== VALIDACIÓN Y LIMITACIONES ===",
        "GD04 valida estructura, ocho ejes, mínimos, niveles, evidencia y proyectos.",
        "La evidencia procede de documentos del caso ficticio; no se realizó entrevista.",
        "No se ejecutaron recorridos de servicios ni se probaron controles en sistemas reales.",
        "Volúmenes y documentos por servicio no disponibles para esta entrega; no se sustituyen por cero.",
        "La fecha de emisión de FICHA.md y varias fechas de corte no están indicadas.",
        "El cuestionario es voluntario, no validado y no incluye respuestas por pregunta.",
    ])
    return "\n".join(lines) + "\n"


def alineacion_etiqueta(index):
    if index in (1, 2, 3):
        return "left"
    if index in (5, 6, 7):
        return "right"
    return "center"


def guardar_radar(summary, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    axes = summary["ejes"]
    angles = [index * 2 * math.pi / len(axes) for index in range(len(axes))]
    values = [axis["nivel"] if axis["nivel"] is not None else float("nan") for axis in axes]
    names = ["Gobernanza", "Servicios", "Interoperabilidad", "Seguridad\ndigital",
             "Datos", "Identidad\ndigital", "Talento", "Infraestructura"]
    labels = [name + f'\n({axis["puntuados"]}/{axis["indicadores"]} puntuados)'
              for name, axis in zip(names, axes)]
    fig, ax = plt.subplots(figsize=(10, 9.6), subplot_kw={"polar": True})
    fig.subplots_adjust(top=0.80, bottom=0.25, left=0.20, right=0.80)
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.plot(angles + angles[:1], values + values[:1], color="#16285C", linewidth=2.5, marker="o")
    ax.fill(angles + angles[:1], values + values[:1], color="#0EA5E9", alpha=0.22)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10)
    for index, label in enumerate(ax.get_xticklabels()):
        label.set_horizontalalignment(alineacion_etiqueta(index))
    ax.tick_params(axis="x", pad=18)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)
    ax.set_rlabel_position(15)
    ax.grid(color="#CED7E1")
    global_text = f'{summary["nivel_global"]:.2f}/5' if summary["nivel_global"] is not None else "No evaluable"
    fig.suptitle("Distribuidora Andina del Sur\nMadurez documental provisional: " + global_text,
                 fontsize=17, fontweight="bold", color="#16285C", y=0.97)
    fig.text(0.5, 0.065,
             f'{summary["puntuados"]}/{summary["indicadores"]} indicadores puntuados · '
             f'{summary["sin_linea_base"]} sin línea base\n'
             "Los puntajes desconocidos se excluyen; cada eje conserva el mismo peso.\n"
             "Fuentes: Ficha, Mesa y Cuestionario de Empresa 06 · Revisión: 22/10/2026",
             ha="center", va="center", fontsize=10, color="#374151")
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)


def ejecutar():
    # Las entradas y salidas pertenecen al proyecto; no se aceptan rutas de la CLI.
    rows = leer_ejes(Path(__file__).with_name("GD03_ejes.csv"))
    summary = resumir(rows)
    evidence = ROOT / "evidencias" / "S11" / "salidas"
    graphs = ROOT / "graficos"
    evidence.mkdir(parents=True, exist_ok=True)
    graphs.mkdir(parents=True, exist_ok=True)
    output = construir_salida(summary)
    (evidence / "GD04_madurez.txt").write_text(output, encoding="utf-8")
    (evidence / "GD04_resumen.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (evidence / "GD04_resumen_ejes.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["eje", "indicadores", "puntuados", "sin_linea_base", "nivel"])
        writer.writeheader()
        writer.writerows(summary["ejes"])
    with (evidence / "GD04_sin_linea_base.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=REQUIRED)
        writer.writeheader()
        writer.writerows({key: row[key] for key in REQUIRED} for row in rows
                         if row[BASELINE].casefold() == NO_MEASUREMENT)
    guardar_radar(summary, graphs / "GD_madurez.png")
    print(output)
    print("Radar: graficos/GD_madurez.png")
    print("Salidas: evidencias/S11/salidas/GD04_*")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        ejecutar()
    except (ValueError, OSError) as error:
        parser.exit(1, f"GD04 no generó resultados válidos: {error}\n")
