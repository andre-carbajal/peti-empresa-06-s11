# Tablero de línea base — Persona 3

## Estado

La rama parte de `develop`, que integra el trabajo de Personas 1 y 2. GD01 contiene siete servicios con niveles propuestos, pero sin volúmenes anuales validados. GD03 contiene el diagnóstico documental. Faltan `04_normativa/NO03_matriz_cumplimiento.csv` y `04_normativa/MG03_capacidad.csv`. El promedio ponderado y las visualizaciones 4 y 5 quedan pendientes; no se imputan valores.

## Arranque local

1. Copiar `.env.example` a `.env` y cambiar la clave. Configurar `DATABASE_URL` en la terminal, por ejemplo en PowerShell: `$env:DATABASE_URL = 'postgresql://peti:CLAVE@127.0.0.1:5433/peti_s11'`.
2. Ejecutar `docker compose up -d`. PostgreSQL escucha en `127.0.0.1:5433` y Metabase en `http://127.0.0.1:3001`.
3. Ejecutar `python -m pip install -r requirements-persona-3.txt` y `python 06_gobierno_digital/GD05_carga_tablero.py`.
4. En Metabase, agregar PostgreSQL con host `postgres`, puerto `5432`, base `peti_s11`, usuario `peti` y la clave local.
5. Detener con `docker compose down`.

La tabla `tablero_columnas` mapea los encabezados originales a las columnas cargadas. Los campos base son texto para preservar vacíos; las vistas convierten únicamente los niveles y volúmenes necesarios.

## Seis preguntas

Crear estas preguntas en una colección `S11 · Línea base` y guardar capturas completas en `evidencias/S11/` solo cuando estén accesibles.

| N.º | Visualización | Consulta | Estado |
|---|---|---|---|
| 1 | Barras horizontales: actual y objetivo por servicio | `SELECT servicio, nivel_actual, nivel_objetivo FROM tablero_servicios ORDER BY id` | Niveles provisionales |
| 2 | Tarjeta: ponderado y promedio simple | `SELECT promedio_ponderado, promedio_simple, volumenes_pendientes FROM tablero_niveles` | Ponderado nulo hasta completar volúmenes |
| 3 | Barras: madurez por eje | `SELECT eje, madurez, indicadores FROM tablero_ejes ORDER BY eje` | Diagnóstico documental |
| 4 | Anillo: estado de cumplimiento | Agrupar estado en `cumplimiento` y contar filas | Falta NO03 |
| 5 | Barras agrupadas: capacidad actual y objetivo | Seleccionar capacidades de `capacidad` | Falta MG03 |
| 6 | Tabla: indicadores sin línea base | `SELECT * FROM tablero_indicadores_sin_linea_base ORDER BY id` | Disponible |

El promedio ponderado es SQL `NULL` cuando falta cualquier volumen o el total es cero. El promedio simple es descriptivo y no sustituye al indicador ponderado.

## Evidencia e informe

Nombrar las capturas `tablero-01.png` a `tablero-06.png`; enlazarlas desde el informe solo tras comprobar las preguntas. Registrar la fecha de carga y el commit fuente. No mostrar contraseñas ni nombres de usuarios.

La plantilla DOCX del curso y la matriz de 13 resultados no están en el repositorio. Para cerrar el PDF faltan la plantilla, los dos CSV, los volúmenes validados y los tres recorridos. Conservar la numeración de la plantilla y consultar al docente la discrepancia con la guía. El caso es ficticio; no afirmar que se probó una organización real.
