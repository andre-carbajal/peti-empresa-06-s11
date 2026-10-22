# Informe de laboratorio S11 — borrador de integración

**Universidad Privada de Tacna · Facultad de Ingeniería · Escuela de Ingeniería de Sistemas**

**SI-886 Planeamiento Estratégico de TI · Semana 11 · Empresa 06**

**Taller:** Diagnóstico de gobierno digital y tablero de línea base

**Grupo, nombres completos y códigos:** pendientes de confirmación por el equipo.

**Docente:** Dr. Oscar Juan Jimenez Flores
**Fecha de revisión documental:** 22 de octubre de 2026

> Este borrador sigue las siete secciones de la plantilla oficial. No sustituye el PDF final: falta completar la carátula con nombres y códigos, actualizar el índice en Word y exportar. La guía habla de «sección 5. Resultados y evidencias»; la plantilla descargada enumera **3. Resultados** y **5. Cuestionario**. Se conserva la numeración de la plantilla y se registra la discrepancia para consulta docente.

## 1. Información sobre el evento práctico

### 1.1 Título

Diagnóstico de gobierno digital y tablero de línea base de Distribuidora Andina del Sur S.A.C., caso ficticio Empresa 06.

### 1.2 Objetivos

Catalogar al menos siete servicios, evaluar ocho ejes con evidencia, distinguir indicadores medidos de los pendientes, calcular la madurez provisional, comprobar el principio de una sola vez, preparar el tablero local y consolidar la sección 6.1 del PETI.

### 1.3 Tiempo de duración

Pendiente: registrar la duración efectiva del trabajo del equipo; la guía no entrega una medición de tiempo ejecutado.

### 1.4 Resultados de aprendizaje

El ejercicio permite comprobar cómo la falta de volúmenes, documentos por trámite y medidas de capacidad limita la línea base, aunque existan descripciones del caso. Los resultados parciales se reportan con su cobertura.

### 1.5 Recursos

Python 3.12, pandas y matplotlib para el análisis; PostgreSQL 16 y Metabase en Docker Compose para la carga y el tablero local; Git y GitHub para los artefactos. La disponibilidad de Docker y Metabase debe verificarse antes de declararlos usados en la ejecución final.

### 1.6 Seguridad

El caso es ficticio. El tablero se configura solo en `127.0.0.1`, no se versionan credenciales ni registros nominales y los volúmenes no disponibles permanecen vacíos.

## 2. Procedimiento o metodología

**Paso A. Catálogo:** Se consolidaron los siete servicios publicados en [GD01](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD01_catalogo_servicios.csv). Los niveles 3→4 son propuestas provisionales. La [salida de GD02](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/evidencias/S11/salidas/GD02_servicios.txt) informa promedio simple 3,00 y deja pendientes el ponderado, documentos reutilizables y brechas ponderadas.

**Paso B. Ejes:** [GD03](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD03_ejes.csv) incluye 25 indicadores en ocho ejes. [GD04](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/evidencias/S11/salidas/GD04_resumen.json) calcula 1,17/5 sobre 16 indicadores puntuados; diez carecen de línea base y tienen proyecto de instrumentación.

**Paso C. Tablero:** [Compose](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/compose.yaml) restringe PostgreSQL y Metabase a localhost. [GD05](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD05_carga_tablero.py) valida y carga los archivos disponibles. La [guía del tablero](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/docs/tablero-persona-3.md) especifica seis preguntas. En la revisión local, Docker Desktop estaba abierto pero el servicio del motor estaba detenido y no pudo iniciarse sin permisos del sistema; no se afirma haber creado preguntas o capturas en Metabase.

**Paso D. Redacción:** La [sección 6.1](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/6.1_situacion_actual.md) integra el catálogo, ocho ejes, indicadores pendientes, madurez y síntesis de brechas.

**Paso E. Validación:** La evidencia documental permite verificar la justificación de los ejes. Los recorridos de dos servicios y la prueba de documentos concretos siguen pendientes de entrevista o simulación documentada con el docente; el caso publicado no proporciona esos datos.

**Paso F. Registro:** Los artefactos se versionan en `main`. Las etiquetas `v0.11` y `taller-11` se crearán sobre el commit de entrega final, después de completar y revisar el informe y las evidencias.

## 3. Resultados

La matriz reproduce las 13 filas de la guía. «Parcial» indica que hay evidencia publicada pero falta una condición de aceptación; «Pendiente» indica que no existe la prueba exigida.

| # | Resultado esperado | Estado | Evidencia o faltante |
|---|---|---|---|
| 1 | Catálogo ≥7 con volumen y nivel | Parcial | [GD01](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD01_catalogo_servicios.csv): siete servicios; faltan volúmenes y recorridos validados. |
| 2 | Ponderado y contraste simple | Pendiente | [Salida GD02](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/evidencias/S11/salidas/GD02_servicios.txt): simple 3,00 provisional; ponderado sin datos. |
| 3 | Principio de una sola vez | Pendiente | [GD01](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD01_catalogo_servicios.csv): documentos concretos vacíos. |
| 4 | Cinco brechas ponderadas | Pendiente | [Salida GD02](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/evidencias/S11/salidas/GD02_servicios.txt): faltan volúmenes y niveles comprobados. |
| 5 | Gráfico del catálogo | Parcial | [GD_servicios.png](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/graficos/GD_servicios.png): niveles provisionales. |
| 6 | Ocho ejes y ≥2 indicadores | Logrado documentalmente | [GD03](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD03_ejes.csv): 25 indicadores. |
| 7 | Línea base o «No se mide» | Logrado documentalmente | [GD03](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/GD03_ejes.csv): 15 disponibles, diez pendientes. |
| 8 | Pendientes y proyectos | Logrado documentalmente | [Diez proyectos](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/evidencias/S11/salidas/GD04_sin_linea_base.csv). |
| 9 | Madurez calculada | Parcial | [Resumen GD04](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/evidencias/S11/salidas/GD04_resumen.json): 1,17/5, 16 de 25 puntuados. |
| 10 | Radar por eje | Logrado documentalmente | [GD_madurez.png](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/graficos/GD_madurez.png). |
| 11 | Seis visualizaciones en Metabase | Pendiente | [Configuración y consultas](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/docs/tablero-persona-3.md); faltan NO03, MG03 y motor Docker operativo. |
| 12 | Sección 6.1 con síntesis | Logrado documentalmente | [Sección 6.1](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/06_gobierno_digital/6.1_situacion_actual.md), con limitaciones explícitas. |
| 13 | Etiqueta `v0.11` | Pendiente | Crear sobre el commit final de entrega, junto a `taller-11`. |

**Problemas y mejoras.** Solicitar al docente los volúmenes y recorridos; recuperar las matrices NO03 y MG03 de las semanas anteriores; obtener permisos para iniciar Docker; comparar las seis preguntas con los CSV antes de capturar; añadir nombres, códigos y número de grupo al PDF.

## 4. Conclusiones

1. Los siete servicios están identificados, pero los volúmenes vacíos impiden priorizar por demanda; el promedio simple de 3,00 no responde la pregunta ponderada del taller.
2. La evaluación de ocho ejes permite una madurez documental provisional de 1,17/5. La cobertura de 16/25 puntajes y diez líneas base pendientes limita cualquier afirmación de madurez definitiva.
3. Una carga técnicamente correcta no convierte fuentes ausentes en evidencia. Las visualizaciones de cumplimiento y capacidad solo pueden cerrarse al recibir sus matrices y verificar sus campos.

## 5. Cuestionario

**Pregunta de transferencia de la guía:** ¿Qué riesgo correría una organización real si esto se hiciera mal? Podría priorizar inversiones con promedios sesgados al tratar volúmenes ausentes como cero y presentar controles normativos sin evidencia. También podría exponer datos sensibles si publica registros de atención o abre la base fuera de localhost.

## 6. Referencias bibliográficas

- Jimenez Flores, O. J. (s. f.). *Diagnóstico de gobierno digital y tablero de línea base. Taller de Semana 11*. Universidad Privada de Tacna. https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/3-TALLER.md
- Jimenez Flores, O. J. (s. f.). *Ficha de Distribuidora Andina del Sur S.A.C.* Caso académico. https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/FICHA.md
- Jimenez Flores, O. J. (2026, 3 de junio). *Mesa de servicio, catálogo y niveles de servicio*. https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/mesa-de-servicio-y-sla.md
- Metabase. (s. f.). *Metabase documentation*. https://www.metabase.com/docs/latest/
- PostgreSQL Global Development Group. (s. f.). *PostgreSQL 16 documentation*. https://www.postgresql.org/docs/16/

## 7. Anexos

- **Anexo A:** [catálogo y gráfico de servicios](https://github.com/andre-carbajal/peti-empresa-06-s11/tree/main/06_gobierno_digital).
- **Anexo B:** [matriz, radar y salidas de madurez](https://github.com/andre-carbajal/peti-empresa-06-s11/tree/main/evidencias/S11/salidas).
- **Anexo C:** [configuración y consultas del tablero](https://github.com/andre-carbajal/peti-empresa-06-s11/blob/main/docs/tablero-persona-3.md). Las capturas de Metabase se anexarán solo tras ejecutar las preguntas.
