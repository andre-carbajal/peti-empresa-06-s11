"""Comprobaciones de la carga antes de acceder a PostgreSQL."""

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gd05", ROOT / "06_gobierno_digital/GD05_carga_tablero.py")
GD05 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GD05)


class CargaTableroTests(unittest.TestCase):
    def test_csv_vigentes_coinciden_con_resumen_de_persona_2(self):
        prepared = {}
        for table in ("servicios", "ejes_gd"):
            headers, rows = GD05.read_csv(GD05.SOURCES[table])
            GD05.validate(table, headers, rows)
            prepared[table] = headers, rows
        GD05.audit(prepared)

    def test_rechaza_volumen_no_numerico_antes_de_cargar(self):
        headers, rows = GD05.read_csv(GD05.SOURCES["servicios"])
        rows[0]["Volumen anual"] = "desconocido"
        with self.assertRaisesRegex(ValueError, "no es numérico"):
            GD05.validate("servicios", headers, rows)

    def test_rechaza_columnas_reordenadas_que_alterarian_las_vistas(self):
        headers, rows = GD05.read_csv(GD05.SOURCES["servicios"])
        headers[3], headers[4] = headers[4], headers[3]
        with self.assertRaisesRegex(ValueError, "columna 4"):
            GD05.validate("servicios", headers, rows)

    def test_rechaza_infinito_como_volumen(self):
        headers, rows = GD05.read_csv(GD05.SOURCES["servicios"])
        rows[0]["Volumen anual"] = "Infinity"
        with self.assertRaisesRegex(ValueError, "fuera de rango"):
            GD05.validate("servicios", headers, rows)

    def test_rechaza_indicador_no_medido_sin_proyecto(self):
        headers, rows = GD05.read_csv(GD05.SOURCES["ejes_gd"])
        row = next(row for row in rows if row["Línea base"] == "No se mide")
        row["Proyecto de instrumentación"] = ""
        with self.assertRaisesRegex(ValueError, "falta proyecto"):
            GD05.validate("ejes_gd", headers, rows)


if __name__ == "__main__":
    unittest.main()
