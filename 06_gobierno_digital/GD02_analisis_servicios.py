from pathlib import Path

import pandas as pd


CATALOG = Path(__file__).with_name("GD01_catalogo_servicios.csv")
GRAPH_DIR = Path(__file__).resolve().parents[1] / "graficos"

NUMERIC_COLUMNS = (
    "Volumen anual",
    "Nivel actual (0–5)",
    "Documentos solicitados",
    "De ellos, ya en poder de la organización",
    "Nivel objetivo",
)
LEVEL_COLUMNS = ("Nivel actual (0–5)", "Nivel objetivo")
DOCUMENT_COLUMNS = (
    "Documentos solicitados",
    "De ellos, ya en poder de la organización",
)


def validar_catalogo(servicios):
    """Return data-quality errors without treating missing measurements as zero."""
    errors = []
    required = {"id", "Servicio", *NUMERIC_COLUMNS}
    missing_columns = sorted(required.difference(servicios.columns))
    if missing_columns:
        return [f"Faltan columnas requeridas: {', '.join(missing_columns)}"]

    if len(servicios) < 7:
        errors.append("El catálogo debe contener al menos siete servicios.")
    if servicios["id"].isna().any() or servicios["id"].duplicated().any():
        errors.append("Cada servicio debe tener un id único y no vacío.")
    if servicios["Servicio"].isna().any() or servicios["Servicio"].astype(str).str.strip().eq("").any():
        errors.append("Hay servicios sin nombre.")

    numeric = {}
    for column in NUMERIC_COLUMNS:
        raw = servicios[column]
        values = pd.to_numeric(raw, errors="coerce")
        supplied = raw.notna() & raw.astype(str).str.strip().ne("")
        if (supplied & values.isna()).any():
            errors.append(f"«{column}» contiene valores no numéricos.")
        numeric[column] = values

    for column in LEVEL_COLUMNS:
        values = numeric[column].dropna()
        if not values.isin(range(6)).all():
            errors.append(f"«{column}» debe estar entre 0 y 5, en niveles enteros.")
    for column in ("Volumen anual", *DOCUMENT_COLUMNS):
        values = numeric[column].dropna()
        if (values < 0).any():
            errors.append(f"«{column}» no puede ser negativo.")
        if not values.mod(1).eq(0).all():
            errors.append(f"«{column}» debe contener conteos enteros.")
    if numeric["Volumen anual"].notna().all() and numeric["Volumen anual"].sum() <= 0:
        errors.append("El volumen anual total debe ser mayor que cero para ponderar.")
    both_documents_known = numeric[DOCUMENT_COLUMNS[0]].notna() & numeric[DOCUMENT_COLUMNS[1]].notna()
    if (
        numeric[DOCUMENT_COLUMNS[1]][both_documents_known]
        > numeric[DOCUMENT_COLUMNS[0]][both_documents_known]
    ).any():
        errors.append("Los documentos ya en poder no pueden exceder los solicitados.")

    return errors


def analizar():
    servicios = pd.read_csv(CATALOG)
    errors = validar_catalogo(servicios)
    if errors:
        raise SystemExit(
            "GD01 incompleto o inválido; no se calcularon resultados:\n- "
            + "\n- ".join(errors)
        )

    for column in NUMERIC_COLUMNS:
        servicios[column] = pd.to_numeric(servicios[column])

    print(f"Servicios catalogados        : {len(servicios)}")
    print("AVISO: los niveles actuales y objetivos son provisionales; validar con recorridos.")

    nivel_actual_completo = servicios[LEVEL_COLUMNS[0]].notna().all()
    nivel_objetivo_completo = servicios[LEVEL_COLUMNS[1]].notna().all()
    niveles_completos = nivel_actual_completo and nivel_objetivo_completo
    volumen_completo = servicios["Volumen anual"].notna().all()
    documentos_completos = servicios[list(DOCUMENT_COLUMNS)].notna().all().all()

    if nivel_actual_completo:
        servicios["nivel"] = servicios["Nivel actual (0–5)"]
        print(f"Nivel medio simple actual    : {servicios.nivel.mean():.2f} de 5")
        print(f"Servicios en nivel actual ≥ 4: {(servicios.nivel >= 4).sum()} ({(servicios.nivel >= 4).mean():.0%})")
        print(f"Servicios en nivel actual 0–1: {(servicios.nivel <= 1).sum()}")
    else:
        print("Nivel medio simple actual    : PENDIENTE (faltan niveles actuales)")
    if nivel_objetivo_completo:
        print(f"Nivel medio simple objetivo  : {servicios['Nivel objetivo'].mean():.2f} de 5")
    else:
        print("Nivel medio simple objetivo  : PENDIENTE (faltan niveles objetivo)")

    if volumen_completo and servicios["Volumen anual"].sum() > 0 and nivel_actual_completo:
        print(f"Volumen anual total          : {servicios['Volumen anual'].sum():,} unidades reportadas")
        ponderado = (servicios.nivel * servicios["Volumen anual"]).sum() / servicios["Volumen anual"].sum()
        print(f"Nivel medio PONDERADO actual : {ponderado:.2f} de 5")
    else:
        print("Nivel medio ponderado        : PENDIENTE (faltan volúmenes anuales por servicio)")

    print("\n=== PRINCIPIO DE UNA SOLA VEZ ===")
    if not documentos_completos:
        print("PENDIENTE: identificar documentos solicitados y cuáles ya posee la organización.")
    else:
        solicitados = servicios["Documentos solicitados"].sum()
        ya_disponibles = servicios["De ellos, ya en poder de la organización"].sum()
        if solicitados == 0:
            print("No aplica: se confirmó que no se solicitan documentos.")
        else:
            print(
                f"Documentos solicitados: {solicitados} | ya en poder de la organización: "
                f"{ya_disponibles} ({ya_disponibles / solicitados:.0%})"
            )

    print("\n=== BRECHA POR SERVICIO, PONDERADA POR VOLUMEN ===")
    if volumen_completo and niveles_completos and servicios["Volumen anual"].sum() > 0:
        servicios["brecha"] = servicios["Nivel objetivo"] - servicios.nivel
        servicios["impacto"] = servicios.brecha * servicios["Volumen anual"]
        print(
            servicios.nlargest(5, "impacto")[
                ["id", "Servicio", "nivel", "Nivel objetivo", "Volumen anual", "impacto"]
            ].to_string(index=False)
        )
    else:
        print("PENDIENTE: se requieren niveles y volúmenes anuales completos por servicio.")

    if niveles_completos:
        import matplotlib.pyplot as plt

        GRAPH_DIR.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(servicios.Servicio, servicios.nivel, color="#16285C", label="Nivel actual provisional")
        ax.barh(
            servicios.Servicio,
            servicios["Nivel objetivo"] - servicios.nivel,
            left=servicios.nivel,
            color="#0EA5E9",
            alpha=0.55,
            label="Brecha propuesta al objetivo",
        )
        ax.set_xlabel("Nivel de digitalización (0–5)")
        ax.set_xlim(0, 5)
        ax.set_title("Catálogo de servicios: niveles provisionales actual y objetivo")
        ax.legend()
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "GD_servicios.png", dpi=140)
        plt.close(fig)
        print(f"\nGráfico provisional          : {GRAPH_DIR / 'GD_servicios.png'}")
    else:
        print("\nGráfico                       : PENDIENTE (faltan niveles actuales u objetivos)")


if __name__ == "__main__":
    analizar()
