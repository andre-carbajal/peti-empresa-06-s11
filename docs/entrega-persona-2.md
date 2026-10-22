# Entrega de Persona 2 — Sofxx7

**Estado:** avance documental implementado y ejecutado. La validación con el docente y la incorporación de datos faltantes siguen pendientes.

## Archivos para revisar

| Archivo | Contenido |
|---|---|
| [GD03_ejes.csv](../06_gobierno_digital/GD03_ejes.csv) | 25 indicadores en los ocho ejes; 15 líneas base disponibles y 10 pendientes, con evidencia, estado y proyecto. |
| [GD04_madurez.py](../06_gobierno_digital/GD04_madurez.py) | Valida la matriz, calcula promedios sin imputar puntajes y genera las evidencias. |
| [6.1_situacion_actual.md](../06_gobierno_digital/6.1_situacion_actual.md) | Redacción de 6.1.1 y 6.1.4–6.1.6. Las secciones 6.1.2, 6.1.3 y 6.1.7 están identificadas para integración del equipo. |
| [Criterios y evidencia](criterios-evidencia-persona-2.md) | Justificación del método, límites de las fuentes y preguntas para cerrar cada dato pendiente. |
| [Radar](../graficos/GD_madurez.png) | Madurez provisional con cobertura por eje. |
| [Salida GD04](../evidencias/S11/salidas/GD04_madurez.txt) | Cálculos, cobertura, limitaciones y diez proyectos de instrumentación. |
| [Pruebas de GD04](../evidencias/S11/salidas/GD04_validacion.txt) | Resultado de las comprobaciones automáticas del programa. |

## Resultado e interpretación

**1,17 de 5 — Inicial, con carácter provisional.** Se puntuaron 16 de los 25 indicadores. Los nueve restantes conservan el nivel vacío. Los diez indicadores sin línea base tienen proyecto de instrumentación; SEG-03 puede valorar la ausencia de práctica de registro, aunque se desconozca cuántos incidentes ocurrieron.

Este resultado permite presentar un diagnóstico documental. La entrevista y las validaciones pendientes deben completarse antes de presentarlo como diagnóstico final verificado. La existencia de un radar no acredita que se hayan comprobado los servicios en operación.

## Cómo reproducir en Windows

Desde la raíz del repositorio, crear un entorno local si no existe:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-persona-2.txt
.\.venv\Scripts\python.exe 06_gobierno_digital/GD04_madurez.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_gd04_madurez.py -v
```

El programa también funciona desde 06_gobierno_digital porque resuelve rutas a partir de su propio archivo. Las dependencias locales quedan excluidas de Git. El programa solo requiere matplotlib; sus cálculos y lectura CSV usan la biblioteca estándar.

## Insumos para Persona 3

- Cargar GD03 completo como ejes_gd. La columna Línea base contiene texto porque combina razones, estados y «No se mide».
- Para el gráfico por eje, usar [GD04_resumen_ejes.csv](../evidencias/S11/salidas/GD04_resumen_ejes.csv), que contiene el promedio numérico junto a cobertura y cantidad de indicadores.
- Los niveles vacíos deben conservarse como valores nulos. No aplicar COALESCE a cero o a uno para obtener un promedio.
- [GD04_sin_linea_base.csv](../evidencias/S11/salidas/GD04_sin_linea_base.csv) sirve como tabla de los diez indicadores y sus proyectos.
- [GD04_resumen.json](../evidencias/S11/salidas/GD04_resumen.json) contiene el resultado global sin redondeo intermedio.
- Importar una matriz en PostgreSQL o generar un radar local no equivale a haber construido el tablero Metabase. Ese trabajo corresponde a Persona 3.

## Evidencia para las filas del taller

| Resultado del taller | Artefacto de esta entrega | Reserva |
|---|---|---|
| 6. Ocho ejes con dos o más indicadores | GD03_ejes.csv | 25 indicadores; nueve puntajes pendientes. |
| 7. Línea base o «No se mide» | GD03_ejes.csv | 15 disponibles, con distinta calidad de evidencia. |
| 8. Indicadores sin línea base y proyectos | GD04_sin_linea_base.csv y GD04_madurez.txt | 10 proyectos propuestos; responsables por acordar. |
| 9. Nivel de madurez | GD04_madurez.txt y GD04_resumen.json | Resultado documental provisional. |
| 10. Radar | graficos/GD_madurez.png | Informa cobertura parcial por eje. |
| 12. Sección 6.1 | 6.1_situacion_actual.md | Contiene la parte de Persona 2; falta integración del equipo. |

Al publicar la rama, el informe debe usar la URL del PR y de cada artefacto. Las etiquetas v0.11 y taller-11 corresponden al cierre conjunto del taller.

## Qué falta para cerrar tu parte

1. Obtener o confirmar las diez líneas base con las evidencias indicadas; registrar las limitaciones que persistan.
2. Validar con el docente los puntajes documentales y sus fechas de corte, especialmente los ejes con cobertura de 1/3.
3. Incorporar los resultados de Persona 1 que afectan SER-04 e INT-02, ejecutar GD04 de nuevo y actualizar el texto si cambia la media.
4. Integrar mediante PR hacia develop junto a la revisión del equipo.
