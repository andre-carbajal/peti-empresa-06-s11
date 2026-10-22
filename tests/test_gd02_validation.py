from contextlib import redirect_stdout
import io
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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
    def test_catalogo_parcial_acepta_vacios_sin_tratarlos_como_cero(self):
        borrador = pd.read_csv(ROOT / "06_gobierno_digital" / "GD01_catalogo_servicios.csv")
        errors = gd02.validar_catalogo(borrador)
        self.assertEqual(errors, [])
        self.assertTrue(borrador["Volumen anual"].isna().all())
        self.assertTrue(borrador["Documentos solicitados"].isna().all())
        self.assertTrue((borrador["Nivel actual (0–5)"] == 3).all())

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

    def test_no_confunde_texto_invalido_con_valor_faltante(self):
        datos = catalogo_valido()
        datos["Volumen anual"] = datos["Volumen anual"].astype(object)
        datos.loc[0, "Volumen anual"] = "desconocido"
        self.assertTrue(any("no numéricos" in error for error in gd02.validar_catalogo(datos)))

    def _ejecutar_analisis(self, datos, carpeta):
        catalogo = Path(carpeta) / "catalogo.csv"
        graficos = Path(carpeta) / "graficos"
        datos.to_csv(catalogo, index=False)
        salida = io.StringIO()
        with patch.object(gd02, "CATALOG", catalogo), patch.object(gd02, "GRAPH_DIR", graficos):
            with redirect_stdout(salida):
                gd02.analizar()
        archivo_grafico = graficos / "GD_servicios.png"
        return salida.getvalue(), archivo_grafico.read_bytes() if archivo_grafico.exists() else None

    def test_analiza_campos_disponibles_y_deja_otros_pendientes(self):
        datos = pd.read_csv(ROOT / "06_gobierno_digital" / "GD01_catalogo_servicios.csv")
        with tempfile.TemporaryDirectory() as carpeta:
            salida, grafico = self._ejecutar_analisis(datos, carpeta)

        self.assertIn("Nivel medio simple actual    : 3.00 de 5", salida)
        self.assertIn("Nivel medio simple objetivo  : 4.00 de 5", salida)
        self.assertIn("Nivel medio ponderado        : PENDIENTE", salida)
        self.assertIn("PENDIENTE: identificar documentos solicitados", salida)
        self.assertIn("PENDIENTE: se requieren niveles y volúmenes", salida)
        self.assertNotIn("Documentos solicitados: 0", salida)
        self.assertTrue(grafico.startswith(b"\x89PNG"))

    def test_calcula_lo_disponible_sin_inventar_objetivos_ni_grafico(self):
        datos = pd.read_csv(ROOT / "06_gobierno_digital" / "GD01_catalogo_servicios.csv")
        datos.loc[0, "Nivel objetivo"] = float("nan")
        datos["Volumen anual"] = range(1, 8)
        with tempfile.TemporaryDirectory() as carpeta:
            salida, grafico = self._ejecutar_analisis(datos, carpeta)

        self.assertIn("Nivel medio simple actual    : 3.00 de 5", salida)
        self.assertIn("Nivel medio PONDERADO actual : 3.00 de 5", salida)
        self.assertIn("Nivel medio simple objetivo  : PENDIENTE", salida)
        self.assertIn("Gráfico                       : PENDIENTE", salida)
        self.assertIn("PENDIENTE: se requieren niveles y volúmenes", salida)
        self.assertIsNone(grafico)

    def test_catalogo_completo_conserva_calculos(self):
        datos = catalogo_valido()
        datos["Volumen anual"] = [1, 2, 3, 4, 5, 6, 7]
        datos["Nivel actual (0–5)"] = [0, 1, 2, 3, 4, 5, 0]
        datos["Nivel objetivo"] = 5
        with tempfile.TemporaryDirectory() as carpeta:
            salida, grafico = self._ejecutar_analisis(datos, carpeta)

        self.assertIn("Nivel medio PONDERADO actual : 2.50 de 5", salida)
        self.assertIn("Documentos solicitados: 14 | ya en poder de la organización: 7 (50%)", salida)
        brechas = salida.split("=== BRECHA POR SERVICIO, PONDERADA POR VOLUMEN ===", 1)[1]
        filas = [line.strip() for line in brechas.splitlines() if line.strip().startswith("S-")]
        self.assertEqual(len(filas), 5)
        self.assertTrue(any(line.startswith("S-07") for line in filas))
        self.assertTrue(grafico.startswith(b"\x89PNG"))


if __name__ == "__main__":
    unittest.main()
