# Tablero de línea base — Persona 3

## Estado

El trabajo de las tres personas está integrado en `main`. GD01 contiene siete servicios con niveles propuestos, pero sin volúmenes anuales validados. GD03 contiene el diagnóstico documental. Se añadieron [NO03 y MG03 documentales](matrices-s11-empresa-06.md) basados en S11; describen controles y estiman capacidad de TI, sin acreditar cumplimiento legal ni capacidad validada. El promedio ponderado queda pendiente. El tablero ejecutado contiene ocho preguntas, incluidas 04 y 05 con [capturas y cotejo](../evidencias/S11/salidas/GD06_ocho_preguntas_s11.txt). La [auditoría](auditoria-integral-s11.md) explica cada paso.

## Arranque local

1. Copiar `.env.example` a `.env` y cambiar la clave. Configurar `DATABASE_URL` en la terminal, por ejemplo en PowerShell: `$env:DATABASE_URL = 'postgresql://peti:CLAVE@127.0.0.1:5433/peti_s11'`.
2. Ejecutar `docker compose up -d`. PostgreSQL escucha en `127.0.0.1:5433` y Metabase en `http://127.0.0.1:3001`.
3. Ejecutar `python -m pip install -r requirements-persona-3.txt` y `python 06_gobierno_digital/GD05_carga_tablero.py`.
4. En Metabase, agregar PostgreSQL con nombre `PETI Empresa 06 S11`, host `postgres`, puerto `5432`, base `peti_s11`, usuario `peti` y la clave local.
5. Configurar `METABASE_EMAIL` y `METABASE_PASSWORD` en la terminal con la cuenta administradora local; ejecutar `python 06_gobierno_digital/GD06_crea_metabase.py`. El script comprueba sus consultas y crea diez tarjetas para ocho preguntas distintas, sin duplicados.
6. Detener con `docker compose down`.

La tabla `tablero_columnas` mapea los encabezados originales a las columnas cargadas. Los campos base son texto para preservar vacíos; las vistas convierten únicamente los niveles y volúmenes necesarios.

Antes de iniciar la base puede ejecutarse `python 06_gobierno_digital/GD05_carga_tablero.py --check`. Este modo valida los CSV presentes sin conexión y coteja los ocho promedios de GD03 con el resumen de Persona 2. Su salida versionada está en [GD05_validacion_fuentes.txt](../evidencias/S11/salidas/GD05_validacion_fuentes.txt).

## Ocho preguntas

Las preguntas 1–8 se crearon y ejecutaron en la colección `S11 · Línea base`. [GD06_crea_metabase.py](../06_gobierno_digital/GD06_crea_metabase.py) recrea de forma idempotente las preguntas y el tablero en un Metabase inicializado; requiere `METABASE_EMAIL`, `METABASE_PASSWORD` y una fuente PostgreSQL llamada `PETI Empresa 06 S11` (o configurar `METABASE_DATABASE_NAME`). El script no guarda credenciales y coteja cada fila con GD01/GD03/GD04/NO03/MG03. El [registro de validación](../evidencias/S11/salidas/GD06_ocho_preguntas_s11.txt) incluye resultados y límites.

| N.º | Visualización | Consulta | Estado |
|---|---|---|---|
| 1 | Barras horizontales: actual y objetivo por servicio | `SELECT servicio, nivel_actual, nivel_objetivo FROM tablero_servicios ORDER BY id` | [Captura real](../evidencias/S11/tablero-01.png); niveles provisionales |
| 2 | Comparación ponderado/simple y dos tarjetas auxiliares | `SELECT promedio_ponderado, promedio_simple, volumenes_pendientes FROM tablero_niveles` | [Captura real](../evidencias/S11/tablero-02.png); ponderado NULL |
| 3 | Barras: madurez por eje | `SELECT eje, madurez, indicadores FROM tablero_ejes ORDER BY eje` | [Captura real](../evidencias/S11/tablero-03.png); diagnóstico documental |
| 4 | Anillo: estado de controles descritos en S11 | `SELECT * FROM tablero_controles_s11` | [Captura real](../evidencias/S11/tablero-04.png); 15 brechas y dos coberturas parciales; sin dictamen jurídico |
| 5 | Barras agrupadas: capacidad documental actual y objetivo propuesto | `SELECT * FROM tablero_capacidad_s11` | [Captura real](../evidencias/S11/tablero-05.png); ocho estimaciones no validadas |
| 6 | Tabla: indicadores sin línea base | `SELECT * FROM tablero_indicadores_sin_linea_base ORDER BY id` | [Captura real](../evidencias/S11/tablero-06.png); diez filas |
| 7 | Barras agrupadas: líneas base disponibles y sin medir por eje | `SELECT * FROM tablero_cobertura_linea_base ORDER BY eje` | [Captura real](../evidencias/S11/tablero-07.png); 25 indicadores contrastados |
| 8 | Barras agrupadas: puntajes disponibles y pendientes por eje | `SELECT * FROM tablero_cobertura_puntajes ORDER BY eje` | [Captura real](../evidencias/S11/tablero-08.png); 16 puntuados y nueve pendientes |

El promedio ponderado es SQL `NULL` cuando falta cualquier volumen o el total es cero. El promedio simple es descriptivo y no sustituye al indicador ponderado.

**Comprobación de entorno:** El 22/10/2026 se inició PostgreSQL 16 portátil ligado a 127.0.0.1:5433 y se ejecutó GD05 sobre GD01 y GD03; [la validación inicial](../evidencias/S11/salidas/GD05_postgres_validacion.txt) registra conteos y el ponderado nulo. El 23/10/2026 se [cargaron y comprobaron los cuatro CSV](../evidencias/S11/salidas/GD05_cuatro_fuentes_s11.txt). Metabase v0.52.12 con Java 21 respondió en localhost y se [comprobaron ocho preguntas](../evidencias/S11/salidas/GD06_ocho_preguntas_s11.txt), con capturas 04 y 05. `com.docker.service` siguió detenido y el intento de iniciarlo devolvió un error de permisos. Esta ejecución no constituye un despliegue de Compose.

## Evidencia e informe

Las capturas [01](../evidencias/S11/tablero-01.png), [02](../evidencias/S11/tablero-02.png), [03](../evidencias/S11/tablero-03.png), [04](../evidencias/S11/tablero-04.png), [05](../evidencias/S11/tablero-05.png), [06](../evidencias/S11/tablero-06.png), [07](../evidencias/S11/tablero-07.png) y [08](../evidencias/S11/tablero-08.png) corresponden a ocho preguntas accesibles en la sesión local. El [tablero completo](../evidencias/S11/tablero-ocho-preguntas.png) incluye diez tarjetas, dos auxiliares. Las preguntas 07 y 08 miden cobertura de GD03. No mostrar contraseñas ni nombres de usuarios.

La plantilla DOCX oficial está en el [repositorio del curso](https://github.com/OscarJimenezFlores/PETI/blob/main/PLANTILLAS/SI886-PLANTILLA-TALLER.docx). El [borrador del informe](informe-taller-s11-borrador.md) contiene las 13 filas de resultados con estado y enlace. Se generó un PDF local con los nombres y códigos ya presentes en la copia de plantilla aportada por el usuario; no está versionado en este repositorio público. Para cerrar el entregable faltan confirmar el número de grupo, los volúmenes y documentos validados, los dos recorridos y la validación operativa de NO03/MG03. La guía llama «sección 5» a los resultados, pero la plantilla real los numera como sección 3; se conserva la plantilla y se consulta la discrepancia con el docente. El caso es ficticio; no afirmar que se probó una organización real.
