# Tablero de línea base — Persona 3

## Estado

El trabajo de las tres personas está integrado en `main`. GD01 contiene siete servicios con niveles propuestos, pero sin volúmenes anuales validados. GD03 contiene el diagnóstico documental. Faltan `04_normativa/NO03_matriz_cumplimiento.csv` y `04_normativa/MG03_capacidad.csv`. El promedio ponderado y las visualizaciones 4 y 5 quedan pendientes; no se imputan valores.

## Arranque local

1. Copiar `.env.example` a `.env` y cambiar la clave. Configurar `DATABASE_URL` en la terminal, por ejemplo en PowerShell: `$env:DATABASE_URL = 'postgresql://peti:CLAVE@127.0.0.1:5433/peti_s11'`.
2. Ejecutar `docker compose up -d`. PostgreSQL escucha en `127.0.0.1:5433` y Metabase en `http://127.0.0.1:3001`.
3. Ejecutar `python -m pip install -r requirements-persona-3.txt` y `python 06_gobierno_digital/GD05_carga_tablero.py`.
4. En Metabase, agregar PostgreSQL con host `postgres`, puerto `5432`, base `peti_s11`, usuario `peti` y la clave local.
5. Detener con `docker compose down`.

La tabla `tablero_columnas` mapea los encabezados originales a las columnas cargadas. Los campos base son texto para preservar vacíos; las vistas convierten únicamente los niveles y volúmenes necesarios.

Antes de iniciar la base puede ejecutarse `python 06_gobierno_digital/GD05_carga_tablero.py --check`. Este modo valida los CSV presentes sin conexión y coteja los ocho promedios de GD03 con el resumen de Persona 2. Su salida versionada está en [GD05_validacion_fuentes.txt](../evidencias/S11/salidas/GD05_validacion_fuentes.txt).

## Seis preguntas

Hay cuatro consultas SQL preparadas para los datos presentes y dos visualizaciones descritas que dependen de las matrices ausentes. Al disponer de las cuatro fuentes, crear las seis preguntas en una colección `S11 · Línea base` y guardar capturas completas en `evidencias/S11/` solo cuando estén accesibles.

| N.º | Visualización | Consulta | Estado |
|---|---|---|---|
| 1 | Barras horizontales: actual y objetivo por servicio | `SELECT servicio, nivel_actual, nivel_objetivo FROM tablero_servicios ORDER BY id` | Niveles provisionales |
| 2 | Tarjeta: ponderado y promedio simple | `SELECT promedio_ponderado, promedio_simple, volumenes_pendientes FROM tablero_niveles` | Ponderado nulo hasta completar volúmenes |
| 3 | Barras: madurez por eje | `SELECT eje, madurez, indicadores FROM tablero_ejes ORDER BY eje` | Diagnóstico documental |
| 4 | Anillo: estado de cumplimiento | Agrupar estado en `cumplimiento` y contar filas | Falta NO03 |
| 5 | Barras agrupadas: capacidad actual y objetivo | Seleccionar capacidades de `capacidad` | Falta MG03 |
| 6 | Tabla: indicadores sin línea base | `SELECT * FROM tablero_indicadores_sin_linea_base ORDER BY id` | Disponible |

El promedio ponderado es SQL `NULL` cuando falta cualquier volumen o el total es cero. El promedio simple es descriptivo y no sustituye al indicador ponderado.

**Comprobación de entorno del 22/10/2026:** Docker Desktop estaba abierto, pero `com.docker.service` estaba detenido. `docker ps` no respondió y el intento de iniciar el servicio devolvió un error de permisos. Se inició PostgreSQL 16 portátil ligado a 127.0.0.1:5433 y se ejecutó GD05 sobre las dos fuentes disponibles; [la validación SQL](../evidencias/S11/salidas/GD05_postgres_validacion.txt) registra conteos y el ponderado nulo. Esto no constituye un despliegue de Compose. Metabase no se ejecutó y no hay preguntas ni capturas verificadas.

## Evidencia e informe

Nombrar las capturas `tablero-01.png` a `tablero-06.png`; enlazarlas desde el informe solo tras comprobar las preguntas. Registrar la fecha de carga y el commit fuente. No mostrar contraseñas ni nombres de usuarios.

La plantilla DOCX oficial está en el [repositorio del curso](https://github.com/OscarJimenezFlores/PETI/blob/main/PLANTILLAS/SI886-PLANTILLA-TALLER.docx). El [borrador del informe](informe-taller-s11-borrador.md) contiene las 13 filas de resultados con estado y enlace. Se generó un PDF local con los nombres y códigos ya presentes en la copia de plantilla aportada por el usuario; no está versionado en este repositorio público. Para cerrar el entregable faltan confirmar el número de grupo, los dos CSV, los volúmenes validados, los recorridos y las capturas verificadas. La guía llama «sección 5» a los resultados, pero la plantilla real los numera como sección 3; se conserva la plantilla y se consulta la discrepancia con el docente. El caso es ficticio; no afirmar que se probó una organización real.
