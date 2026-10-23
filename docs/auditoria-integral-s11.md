# Auditoría de los pasos del equipo — Taller S11, Empresa 06

**Corte:** 23/10/2026. **Alcance:** archivos de `main` y ejecución local contrastada con ellos. «Documentado» significa que existe una fuente o salida verificable; no equivale a observación de la empresa ficticia. No se imputan datos ausentes.

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

`NO03_matriz_cumplimiento.csv` y `MG03_capacidad.csv` **no figuran entre los entregables asignados a Persona 2 en su plan S11**. Son insumos de etapas previas indicados en el Paso C del taller. Tampoco aparecen en `main` ni en las ramas remotas actuales. GD03 describe algunos controles y brechas, pero no enumera obligaciones normativas verificadas ni capacidad actual y objetivo de procesos; convertirlo en esas matrices produciría una evaluación sin sustento.

## Persona 3 — base, tablero e informe

Se contrastaron los seis pasos de [su plan](plan-persona-3.md) con las salidas y capturas.

| Paso del plan | Estado | Evidencia y límite |
|---|---|---|
| 1. Desplegar PostgreSQL y Metabase en localhost | Parcial | PostgreSQL 16 y Metabase v0.52.12 se ejecutaron en `127.0.0.1`, con [validación SQL](../evidencias/S11/salidas/GD05_postgres_validacion.txt). `compose.yaml` existe, pero el servicio Docker Desktop no puede iniciarse en este equipo por permisos; Compose no fue probado. |
| 2. Cargar cuatro CSV | Parcial | [GD05](../06_gobierno_digital/GD05_carga_tablero.py) cargó y comprobó GD01 y GD03: 7 y 25 filas. NO03 y MG03 no existen; no hay cuatro tablas fuente. |
| 3. Construir preguntas Metabase | Parcial respecto al contenido previsto | [GD06](../06_gobierno_digital/GD06_crea_metabase.py) y [salida](../evidencias/S11/salidas/GD06_salida.txt) verifican seis preguntas distintas con datos reales: 01, 02, 03, 06, 07 y 08. Las dos últimas miden cobertura de línea base y de puntajes. No sustituyen el anillo normativo 04 ni las barras de capacidad 05. |
| 4. Guardar capturas y salidas | Hecho para seis preguntas | [Capturas](../evidencias/S11/README.md) 01, 02, 03, 06, 07 y 08; el script coteja las filas con GD01, GD03 y GD04. |
| 5. Integrar informe de la plantilla | Parcial | Existe PDF de trabajo con 13 resultados y enlaces; faltan número de grupo y las comprobaciones dependientes de fuente. La plantilla lleva los nombres y códigos aportados por el equipo. |
| 6. Validar valores y publicar | Hecho para datos disponibles | Paridad de Metabase y fuentes: OK; 21 pruebas automáticas: OK. El cierre de etiquetas debe referirse al estado documental realmente entregado. |

## Comprobaciones del Paso E y cierre

| Comprobación | Resultado |
|---|---|
| Dos recorridos de servicios de principio a fin | Instrumentos S-06 y S-07 preparados; sin observación ni simulación con el docente. |
| Evidencia de cada eje evaluado | Estructura de 16 puntajes y ocho ejes cotejada; controles operativos aún sin observación. |
| «Una sola vez» con documentos concretos | Sin denominador ni documentos identificados; no calculable. |

**Conclusión de aceptación:** el expediente permite entregar un diagnóstico documental con seis visualizaciones respaldadas y limitaciones explícitas. El plan original del taller no está cumplido íntegramente: las filas 1–4 de la lista de comprobación, los contenidos normativo y de capacidad del tablero, dos validaciones del Paso E y el despliegue Compose dependen de fuentes o acceso que el repositorio actual no proporciona. Una etiqueta o un PDF no convierten estos resultados en mediciones verificadas.
