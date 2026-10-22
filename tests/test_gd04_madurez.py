"""Comprobaciones de los casos que pueden distorsionar el diagnóstico."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gd04", ROOT / "06_gobierno_digital" / "GD04_madurez.py")
gd04 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gd04)


class MadurezTests(unittest.TestCase):
    def test_cli_rechaza_rutas_externas_sin_crear_archivos(self):
        for option in ("--csv", "--salida"):
            with self.subTest(opcion=option), tempfile.TemporaryDirectory() as external:
                result = subprocess.run(
                    [sys.executable, str(ROOT / "06_gobierno_digital" / "GD04_madurez.py"), option, external],
                    capture_output=True, timeout=15, check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertEqual(list(Path(external).iterdir()), [])

    def setUp(self):
        self.rows = gd04.leer_ejes(ROOT / "06_gobierno_digital" / "GD03_ejes.csv")

    def test_ejes_tienen_el_mismo_peso_aunque_tengan_distinta_cantidad_de_filas(self):
        rows = []
        for index, axis in enumerate(gd04.AXES):
            for _ in range(2 if index else 10):
                rows.append({"ID": str(len(rows)), "Eje": axis, gd04.LEVEL: "5" if index == 0 else "1",
                             "Línea base": "Dato conocido", "Indicador": "Práctica", "Proyecto de instrumentación": ""})
        result = gd04.resumir(rows)
        self.assertAlmostEqual(result["nivel_global"], 1.5)

    def test_puntaje_desconocido_no_se_convierte_en_inicial(self):
        baseline = gd04.resumir(self.rows)
        rows = deepcopy(self.rows)
        for row in rows:
            if row["Eje"] == "3. Interoperabilidad":
                row[gd04.LEVEL] = ""
        result = gd04.resumir(rows)
        self.assertIsNotNone(baseline["nivel_global"])
        self.assertIsNone(result["nivel_global"])
        self.assertIsNone(result["ejes"][2]["nivel"])

    def test_cantidad_de_incidentes_desconocida_no_se_convierte_en_cero(self):
        row = next(row for row in self.rows if row["ID"] == "SEG-03")
        self.assertEqual(row["Línea base"], "No se mide")
        self.assertEqual(row[gd04.LEVEL], "1")
        result = gd04.resumir(self.rows)
        self.assertIn("SEG-03", [project["id"] for project in result["proyectos"]])

    def test_rechaza_un_eje_con_un_solo_indicador(self):
        rows = [row for row in self.rows if row["Eje"] != "1. Gobernanza" or row["ID"] == "GOB-01"]
        with self.assertRaisesRegex(ValueError, "al menos dos"):
            gd04.validar_ejes(rows)

    def test_rechaza_nivel_cero_y_fraccionario(self):
        for invalid in ("0", "2.5"):
            with self.subTest(nivel=invalid):
                rows = deepcopy(self.rows)
                rows[0][gd04.LEVEL] = invalid
                with self.assertRaisesRegex(ValueError, "nivel inválido"):
                    gd04.validar_ejes(rows)

    def test_rechaza_indicador_sin_linea_base_y_sin_proyecto(self):
        rows = deepcopy(self.rows)
        row = next(row for row in rows if row["Línea base"] == "No se mide")
        row["Proyecto de instrumentación"] = "No aplica"
        with self.assertRaisesRegex(ValueError, "falta proyecto"):
            gd04.validar_ejes(rows)

    def test_rechaza_id_duplicado_y_eje_desconocido(self):
        for field, value, message in (
            ("ID", self.rows[0]["ID"], "ID único"),
            ("Eje", "9. Otro eje", "eje desconocido"),
        ):
            with self.subTest(campo=field):
                rows = deepcopy(self.rows)
                rows[1][field] = value
                with self.assertRaisesRegex(ValueError, message):
                    gd04.validar_ejes(rows)


if __name__ == "__main__":
    unittest.main()
