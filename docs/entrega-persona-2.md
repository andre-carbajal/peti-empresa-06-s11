# Entrega de Persona 2 — Sofxx7

**Estado:** entrega documental de Persona 2 terminada con los insumos disponibles y aporte de Persona 1 integrado. Los datos no disponibles se declaran y tienen un proyecto de instrumentación. PR de integración: [#1](https://github.com/andre-carbajal/peti-empresa-06-s11/pull/1).

## Archivos para revisar

| Archivo | Contenido |
|---|---|
| [GD03_ejes.csv](../06_gobierno_digital/GD03_ejes.csv) | 25 indicadores en los ocho ejes; 15 líneas base disponibles y 10 pendientes, con evidencia, estado y proyecto. |
| [GD04_madurez.py](../06_gobierno_digital/GD04_madurez.py) | Valida la matriz, calcula promedios sin imputar puntajes y genera las evidencias. |
| [6.1_situacion_actual.md](../06_gobierno_digital/6.1_situacion_actual.md) | Sección 6.1 consolidada: incluye la parte de Persona 2 y los aportes de catálogo, una sola vez y síntesis de Persona 1. |
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
| 12. Sección 6.1 | 6.1_situacion_actual.md | Consolidada con Persona 1; mantiene visibles los datos y validaciones pendientes. |

El informe debe enlazar el [PR #1](https://github.com/andre-carbajal/peti-empresa-06-s11/pull/1) y los artefactos de la rama feat/s11-persona-2-ejes. Las etiquetas v0.11 y taller-11 corresponden al cierre conjunto del taller.

## Entrega a Kiara

Kiara puede preparar PostgreSQL y Metabase y utilizar desde ahora GD03, el radar y los resúmenes. La rama feat/s11-persona-2-ejes incorpora el commit a00c6ff de André y la sección 6.1 consolidada.

- [Matriz de ejes en GitHub](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/feat/s11-persona-2-ejes/06_gobierno_digital/GD03_ejes.csv)
- [Promedios numéricos por eje](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/feat/s11-persona-2-ejes/evidencias/S11/salidas/GD04_resumen_ejes.csv)
- [Indicadores sin línea base y proyectos](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/feat/s11-persona-2-ejes/evidencias/S11/salidas/GD04_sin_linea_base.csv)
- [Sección 6.1 consolidada](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/feat/s11-persona-2-ejes/06_gobierno_digital/6.1_situacion_actual.md)

Los gráficos de niveles del catálogo se pueden presentar como hipótesis provisional. La tarjeta de promedio ponderado y el cálculo de documentos reutilizables deben señalar datos pendientes hasta disponer de sus insumos. Las matrices normativas y de capacidad también siguen siendo dependencias del tablero.

## Pendientes de validación del equipo

1. Confirmar con el docente los volúmenes, documentos y recorridos de servicios.
2. Validar los puntajes documentales y las fechas de corte; conservar las limitaciones que no puedan resolverse.
3. Cuando lleguen los datos, actualizar SER-04 e INT-02 y regenerar GD04 si cambia su evaluación.
4. Persona 3 prepara el tablero y el informe PDF; el equipo revisa la integración a develop y crea las etiquetas al cierre.

Estos pendientes se entregan identificados y con su proyecto; no se inventan mediciones para completar casillas.
