# Auditoría de los pasos del equipo — Taller S11, Empresa 06

**Corte:** 23/10/2026. **Alcance:** recursos de Semana 11 para Empresa 06, archivos de `main` y ejecución local contrastada con ellos. «Documentado» significa que existe una fuente o salida verificable; no equivale a observación de la empresa ficticia. No se imputan datos ausentes.

## Persona 1 — catálogo y análisis de servicios

| Paso | Estado | Evidencia y límite |
|---|---|---|
| Identificar servicios y fuentes del caso | Documentado | [GD01](../06_gobierno_digital/GD01_catalogo_servicios.csv) reúne los siete servicios reconocidos por la mesa; [criterios](criterios-provisionales-persona-1.md) distinguen datos expresos de hipótesis. |
| Asignar nivel actual y objetivo por servicio | Provisional | Los siete niveles 3→4 están propuestos, pero no existe recorrido observado o simulado que los confirme. [Validación Paso E](../evidencias/S11/salidas/S11_validacion_paso_e.md). |
| Registrar volumen anual de cada servicio | Pendiente de fuente | Los siete campos están vacíos. Los 1 929 registros globales e incompletos de mesa no se pueden repartir entre servicios ni usar como volumen anual verificado. [Entrevista preparada](preguntas-entrevista-persona-1.md). |
| Identificar documentos solicitados y ya poseídos | Pendiente de fuente | Los catorce campos están vacíos y no hay lista de documentos concretos. No se puede evaluar «una sola vez». |
| Calcular promedio simple, ponderado y cinco brechas | Parcial | [GD02](../evidencias/S11/salidas/GD02_servicios.txt) obtiene 3,00 simple provisional; el ponderado y las brechas por demanda quedan sin resultado al faltar volúmenes. |
| Graficar y verificar dos recorridos | Parcial | [Gráfico](../graficos/GD_servicios.png) generado; recorridos S-06 y S-07 instrumentados, aún sin ejecución con el docente. |

## Persona 2 — ocho ejes, madurez y sección 6.1

Se contrastaron los seis pasos de [su plan](plan-persona-2.md) con la [entrega](entrega-persona-2.md).

| Paso del plan | Estado | Evidencia y límite |
|---|---|---|
| 1. Leer fuentes y extraer hechos trazables | Documentado | [Criterios y evidencia](criterios-evidencia-persona-2.md) indican origen, fechas y límites; GD03 enlaza cada indicador. |
| 2. Crear matriz con columnas del taller | Hecho | [GD03](../06_gobierno_digital/GD03_ejes.csv) conserva las siete columnas solicitadas y añade ID, estado y proyecto. |
| 3. Cubrir los ocho ejes con dos indicadores como mínimo | Hecho con reservas | 25 indicadores, 15 líneas base declaradas y diez «No se mide» con proyecto. La fuente de varios valores es declarativa. |
| 4. Justificar cada nivel conocido | Hecho con reservas | 16 puntajes 1–2 con fuente, enlace y observación; nueve sin evidencia suficiente permanecen vacíos. |
| 5. Ejecutar GD04, radar y redactar PETI | Hecho con reservas | [Salida](../evidencias/S11/salidas/GD04_madurez.txt), [radar](../graficos/GD_madurez.png) y [sección 6.1](../06_gobierno_digital/6.1_situacion_actual.md): 1,17/5 provisional, cobertura 16/25. |
| 6. Revisar y publicar en main | Hecho | Archivos integrados en `main`; pruebas automáticas del cálculo presentes. Falta validación operativa de controles con responsables. |

`NO03_matriz_cumplimiento.csv` y `MG03_capacidad.csv` **no figuran entre los entregables asignados a Persona 2 en su plan S11**. Son insumos de etapas previas indicados en el Paso C del taller. El equipo creó [registros documentales S11](matrices-s11-empresa-06.md) con otros alcances: criterios operativos observados y capacidad de procesos de TI estimada. No equivalen a las matrices previas validadas.

### Alcance de los recursos de Semana 11

La [carpeta de Empresa 06 de Semana 11](https://github.com/OscarJimenezFlores/PETI/tree/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur) contiene `FICHA.md`, `mesa-de-servicio-y-sla.md` y `cuestionario-diagnostico.md`. La sección I de la ficha enumera siete CSV en `datos/`, pero esos archivos no están publicados en dicha carpeta. La [guía S11](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/3-TALLER.md) indica que los volúmenes anuales faltantes se piden en la entrevista simulada con el docente. Los 1 929 registros globales de mesa no proporcionan el volumen de cada servicio.

La guía usa NO03 y MG03 como insumos previos para el Paso C, pero no los entrega entre los recursos de Semana 11. La carpeta `04_normativa/` creada por el equipo permite consultar **brechas documentadas y estimaciones propuestas**, sin afirmar cumplimiento legal o capacidad validada. Esta auditoría se limita a Semana 11 y a los archivos ya versionados por el equipo.

## Persona 3 — base, tablero e informe

Se contrastaron los seis pasos de [su plan](plan-persona-3.md) con las salidas y capturas.

| Paso del plan | Estado | Evidencia y límite |
|---|---|---|
| 1. Desplegar PostgreSQL y Metabase en localhost | Parcial | PostgreSQL 16 y Metabase v0.52.12 se ejecutaron en `127.0.0.1`, con [validación SQL](../evidencias/S11/salidas/GD05_postgres_validacion.txt). `compose.yaml` existe, pero el servicio Docker Desktop no puede iniciarse en este equipo por permisos; Compose no fue probado. |
| 2. Cargar cuatro CSV | Hecho para registros documentales | [GD05](../06_gobierno_digital/GD05_carga_tablero.py) validó y cargó en PostgreSQL local los cuatro CSV: 7 servicios, 25 indicadores, 17 criterios y ocho procesos. [Salida SQL](../evidencias/S11/salidas/GD05_cuatro_fuentes_s11.txt). NO03 y MG03 aún necesitan validación con responsables. |
| 3. Construir preguntas Metabase | Hecho documental con reservas | [GD06](../06_gobierno_digital/GD06_crea_metabase.py) [ejecutó ocho preguntas](../evidencias/S11/salidas/GD06_ocho_preguntas_s11.txt). La 04 cuenta controles documentados y la 05 compara capacidad de TI estimada con objetivos propuestos. No representan dictamen legal ni capacidad validada. |
| 4. Guardar capturas y salidas | Hecho | [Capturas](../evidencias/S11/README.md) 01–08 y tablero completo; cotejo de filas con GD01, GD03, NO03, MG03 y GD04. |
| 5. Integrar informe de la plantilla | Parcial | Existe PDF de trabajo con 13 resultados y enlaces; faltan número de grupo y las comprobaciones dependientes de fuente. La plantilla lleva los nombres y códigos aportados por el equipo. |
| 6. Validar valores y publicar | Hecho documental con reservas | [Paridad de ocho preguntas](../evidencias/S11/salidas/GD06_ocho_preguntas_s11.txt): OK; validación de cuatro CSV y 22 pruebas automáticas: OK. Falta contrastar las estimaciones con responsables. |

## Comprobaciones del Paso E y cierre

| Comprobación | Resultado |
|---|---|
| Dos recorridos de servicios de principio a fin | Instrumentos S-06 y S-07 preparados; sin observación ni simulación con el docente. |
| Evidencia de cada eje evaluado | Estructura de 16 puntajes y ocho ejes cotejada; controles operativos aún sin observación. |
| «Una sola vez» con documentos concretos | Sin denominador ni documentos identificados; no calculable. |

**Conclusión de aceptación:** el expediente permite entregar un diagnóstico documental con ocho visualizaciones ejecutadas. El plan original del taller no está cumplido íntegramente: las filas 1–4 de la lista de comprobación, la validación operativa de las matrices, dos comprobaciones del Paso E y el despliegue Compose siguen pendientes. Una etiqueta o un PDF no convierten las estimaciones en mediciones verificadas.
