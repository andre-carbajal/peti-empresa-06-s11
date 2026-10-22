from pathlib import Path

import pandas as pd


CATALOG = Path(__file__).with_name("GD01_catalogo_servicios.csv")
GRAPH_DIR = Path(__file__).resolve().parents[1] / "graficos"
SERVICE = "Servicio"
VOLUME = "Volumen anual"
CURRENT_LEVEL = "Nivel actual (0–5)"
TARGET_LEVEL = "Nivel objetivo"
REQUESTED_DOCUMENTS = "Documentos solicitados"
AVAILABLE_DOCUMENTS = "De ellos, ya en poder de la organización"
NUMERIC_COLUMNS = (VOLUME, CURRENT_LEVEL, REQUESTED_DOCUMENTS, AVAILABLE_DOCUMENTS, TARGET_LEVEL)
LEVEL_COLUMNS = (CURRENT_LEVEL, TARGET_LEVEL)
DOCUMENT_COLUMNS = (REQUESTED_DOCUMENTS, AVAILABLE_DOCUMENTS)


def validar_identificadores(servicios):
    errors = []
    if len(servicios) < 7:
        errors.append("El catálogo debe contener al menos siete servicios.")
    if servicios["id"].isna().any() or servicios["id"].duplicated().any():
        errors.append("Cada servicio debe tener un id único y no vacío.")
    if servicios[SERVICE].isna().any() or servicios[SERVICE].astype(str).str.strip().eq("").any():
        errors.append("Hay servicios sin nombre.")
    return errors


def convertir_numericos(servicios):
    numeric = {}
    errors = []
    for column in NUMERIC_COLUMNS:
        raw = servicios[column]
        values = pd.to_numeric(raw, errors="coerce")
        supplied = raw.notna() & raw.astype(str).str.strip().ne("")
        if (supplied & values.isna()).any():
            errors.append(f"«{column}» contiene valores no numéricos.")
        numeric[column] = values
    return numeric, errors


def validar_rangos(numeric):
    errors = []
    for column in LEVEL_COLUMNS:
        if not numeric[column].dropna().isin(range(6)).all():
            errors.append(f"«{column}» debe estar entre 0 y 5, en niveles enteros.")
    for column in (VOLUME, *DOCUMENT_COLUMNS):
        values = numeric[column].dropna()
        if (values < 0).any():
            errors.append(f"«{column}» no puede ser negativo.")
        if not values.mod(1).eq(0).all():
            errors.append(f"«{column}» debe contener conteos enteros.")
    return errors


def validar_totales(numeric):
    errors = []
    volume = numeric[VOLUME]
    if volume.notna().all() and volume.sum() <= 0:
        errors.append("El volumen anual total debe ser mayor que cero para ponderar.")
    known = numeric[REQUESTED_DOCUMENTS].notna() & numeric[AVAILABLE_DOCUMENTS].notna()
    if (numeric[AVAILABLE_DOCUMENTS][known] > numeric[REQUESTED_DOCUMENTS][known]).any():
        errors.append("Los documentos ya en poder no pueden exceder los solicitados.")
    return errors


def validar_catalogo(servicios):
    """Valida lo disponible sin convertir datos ausentes en cero."""
    missing = sorted({"id", SERVICE, *NUMERIC_COLUMNS}.difference(servicios.columns))
    if missing:
        return [f"Faltan columnas requeridas: {', '.join(missing)}"]
    numeric, errors = convertir_numericos(servicios)
    errors.extend(validar_identificadores(servicios))
    errors.extend(validar_rangos(numeric))
    errors.extend(validar_totales(numeric))
    return errors


def imprimir_niveles(servicios, actual_completo, objetivo_completo):
    if actual_completo:
        print(f"Nivel medio simple actual    : {servicios.nivel.mean():.2f} de 5")
        print(f"Servicios en nivel actual ≥ 4: {(servicios.nivel >= 4).sum()} ({(servicios.nivel >= 4).mean():.0%})")
        print(f"Servicios en nivel actual 0–1: {(servicios.nivel <= 1).sum()}")
    else:
        print("Nivel medio simple actual    : PENDIENTE (faltan niveles actuales)")
    if objetivo_completo:
        print(f"Nivel medio simple objetivo  : {servicios[TARGET_LEVEL].mean():.2f} de 5")
    else:
        print("Nivel medio simple objetivo  : PENDIENTE (faltan niveles objetivo)")


def imprimir_ponderado(servicios, disponible):
    if not disponible:
        print("Nivel medio ponderado        : PENDIENTE (faltan volúmenes anuales por servicio)")
        return
    total = servicios[VOLUME].sum()
    ponderado = (servicios.nivel * servicios[VOLUME]).sum() / total
    print(f"Volumen anual total          : {total:,} unidades reportadas")
    print(f"Nivel medio PONDERADO actual : {ponderado:.2f} de 5")


def imprimir_documentos(servicios):
    print("\n=== PRINCIPIO DE UNA SOLA VEZ ===")
    if not servicios[list(DOCUMENT_COLUMNS)].notna().all().all():
        print("PENDIENTE: identificar documentos solicitados y cuáles ya posee la organización.")
        return
    solicitados = servicios[REQUESTED_DOCUMENTS].sum()
    disponibles = servicios[AVAILABLE_DOCUMENTS].sum()
    if solicitados == 0:
        print("No aplica: se confirmó que no se solicitan documentos.")
        return
    print(
        f"Documentos solicitados: {solicitados} | ya en poder de la organización: "
        f"{disponibles} ({disponibles / solicitados:.0%})"
    )


def imprimir_brechas(servicios, disponible):
    print("\n=== BRECHA POR SERVICIO, PONDERADA POR VOLUMEN ===")
    if not disponible:
        print("PENDIENTE: se requieren niveles y volúmenes anuales completos por servicio.")
        return
    servicios["brecha"] = servicios[TARGET_LEVEL] - servicios.nivel
    servicios["impacto"] = servicios.brecha * servicios[VOLUME]
    print(
        servicios.nlargest(5, "impacto")[
            ["id", SERVICE, "nivel", TARGET_LEVEL, VOLUME, "impacto"]
        ].to_string(index=False)
    )


def guardar_grafico(servicios, niveles_completos):
    if not niveles_completos:
        print("\nGráfico                       : PENDIENTE (faltan niveles actuales u objetivos)")
        return
    import matplotlib.pyplot as plt

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(servicios[SERVICE], servicios.nivel, color="#16285C", label="Nivel actual provisional")
    ax.barh(
        servicios[SERVICE], servicios[TARGET_LEVEL] - servicios.nivel,
        left=servicios.nivel, color="#0EA5E9", alpha=0.55,
        label="Brecha propuesta al objetivo",
    )
    ax.set_xlabel("Nivel de digitalización (0–5)")
    ax.set_xlim(0, 5)
    ax.set_title("Catálogo de servicios: niveles provisionales actual y objetivo")
    ax.legend()
    fig.tight_layout()
    fig.savefig(GRAPH_DIR / "GD_servicios.png", dpi=140)
    plt.close(fig)
    print(f"\nGráfico provisional          : {GRAPH_DIR / 'GD_servicios.png'}")


def analizar():
    servicios = pd.read_csv(CATALOG)
    errors = validar_catalogo(servicios)
    if errors:
        raise SystemExit("GD01 incompleto o inválido; no se calcularon resultados:\n- " + "\n- ".join(errors))
    for column in NUMERIC_COLUMNS:
        servicios[column] = pd.to_numeric(servicios[column])
    servicios["nivel"] = servicios[CURRENT_LEVEL]
    actual_completo = servicios[CURRENT_LEVEL].notna().all()
    objetivo_completo = servicios[TARGET_LEVEL].notna().all()
    volumen_completo = servicios[VOLUME].notna().all()
    ponderado_disponible = volumen_completo and actual_completo and servicios[VOLUME].sum() > 0
    print(f"Servicios catalogados        : {len(servicios)}")
    print("AVISO: los niveles actuales y objetivos son provisionales; validar con recorridos.")
    imprimir_niveles(servicios, actual_completo, objetivo_completo)
    imprimir_ponderado(servicios, ponderado_disponible)
    imprimir_documentos(servicios)
    imprimir_brechas(servicios, ponderado_disponible and objetivo_completo)
    guardar_grafico(servicios, actual_completo and objetivo_completo)


if __name__ == "__main__":
    analizar()
