import importlib.util
from pathlib import Path
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "06_gobierno_digital" / "GD02_analisis_servicios.py"
SPEC = importlib.util.spec_from_file_location("gd02", SCRIPT_PATH)
gd02 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gd02)


def catalogo_valido():
    return pd.DataFrame(
        [
            {
                "id": f"S-{index:02d}",
                "Servicio": f"Servicio {index}",
                "Volumen anual": 100,
                "Nivel actual (0–5)": 1,
                "Documentos solicitados": 2,
                "De ellos, ya en poder de la organización": 1,
                "Nivel objetivo": 3,
            }
            for index in range(1, 8)
        ]
    )


class ValidacionCatalogoTests(unittest.TestCase):
    def test_borrador_sin_metricas_no_pasa(self):
        borrador = pd.read_csv(ROOT / "06_gobierno_digital" / "GD01_catalogo_servicios.csv")
        errors = gd02.validar_catalogo(borrador)
        self.assertTrue(any("Volumen anual" in error for error in errors))
        self.assertTrue(any("Nivel actual" in error for error in errors))

    def test_catalogo_completo_pasa(self):
        self.assertEqual(gd02.validar_catalogo(catalogo_valido()), [])

    def test_no_acepta_documentos_disponibles_mayores_a_solicitados(self):
        datos = catalogo_valido()
        datos.loc[0, "De ellos, ya en poder de la organización"] = 3
        self.assertTrue(
            any("no pueden exceder" in error for error in gd02.validar_catalogo(datos))
        )

    def test_no_acepta_niveles_fuera_de_rango(self):
        datos = catalogo_valido()
        datos.loc[0, "Nivel objetivo"] = 6
        self.assertTrue(any("entre 0 y 5" in error for error in gd02.validar_catalogo(datos)))


if __name__ == "__main__":
    unittest.main()
