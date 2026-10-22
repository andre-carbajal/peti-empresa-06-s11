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
    """Return data-quality errors before calculating from the team CSV."""
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
        values = pd.to_numeric(servicios[column], errors="coerce")
        if values.isna().any():
            errors.append(f"Completar valores numéricos faltantes en «{column}».")
            continue
        numeric[column] = values

    for column in LEVEL_COLUMNS:
        if column in numeric and not numeric[column].isin(range(6)).all():
            errors.append(f"«{column}» debe estar entre 0 y 5, en niveles enteros.")
    for column in ("Volumen anual", *DOCUMENT_COLUMNS):
        if column in numeric:
            if (numeric[column] < 0).any():
                errors.append(f"«{column}» no puede ser negativo.")
            if not numeric[column].mod(1).eq(0).all():
                errors.append(f"«{column}» debe contener conteos enteros.")
    if "Volumen anual" in numeric and numeric["Volumen anual"].sum() <= 0:
        errors.append("El volumen anual total debe ser mayor que cero para ponderar.")
    if all(column in numeric for column in DOCUMENT_COLUMNS):
        if (numeric[DOCUMENT_COLUMNS[1]] > numeric[DOCUMENT_COLUMNS[0]]).any():
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
    servicios["nivel"] = servicios["Nivel actual (0–5)"]

    print(f"Servicios catalogados        : {len(servicios)}")
    print(f"Volumen anual total          : {servicios['Volumen anual'].sum():,} unidades reportadas")
    print(f"Nivel medio de digitalización: {servicios.nivel.mean():.2f} de 5")
    print(f"Servicios en nivel ≥ 4       : {(servicios.nivel >= 4).sum()} ({(servicios.nivel >= 4).mean():.0%})")
    print(f"Servicios en nivel 0 o 1     : {(servicios.nivel <= 1).sum()}")

    ponderado = (servicios.nivel * servicios["Volumen anual"]).sum() / servicios["Volumen anual"].sum()
    print(f"\nNivel medio PONDERADO por volumen: {ponderado:.2f}")

    solicitados = servicios["Documentos solicitados"].sum()
    ya_disponibles = servicios["De ellos, ya en poder de la organización"].sum()
    print("\n=== PRINCIPIO DE UNA SOLA VEZ ===")
    if solicitados == 0:
        print("No aplica: no se registraron documentos solicitados.")
    else:
        print(
            f"Documentos solicitados: {solicitados} | ya en poder de la organización: "
            f"{ya_disponibles} ({ya_disponibles / solicitados:.0%})"
        )

    servicios["brecha"] = servicios["Nivel objetivo"] - servicios.nivel
    servicios["impacto"] = servicios.brecha * servicios["Volumen anual"]
    print("\n=== BRECHA POR SERVICIO, PONDERADA POR VOLUMEN ===")
    print(
        servicios.nlargest(5, "impacto")[
            ["id", "Servicio", "nivel", "Nivel objetivo", "Volumen anual", "impacto"]
        ].to_string(index=False)
    )

    import matplotlib.pyplot as plt

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(servicios.Servicio, servicios.nivel, color="#16285C", label="Nivel actual")
    ax.barh(
        servicios.Servicio,
        servicios["brecha"],
        left=servicios.nivel,
        color="#0EA5E9",
        alpha=0.55,
        label="Brecha al objetivo",
    )
    ax.set_xlabel("Nivel de digitalización (0–5)")
    ax.set_xlim(0, 5)
    ax.set_title("Catálogo de servicios: nivel actual y objetivo")
    ax.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "GD_servicios.png", dpi=140)


if __name__ == "__main__":
    analizar()
