# Criterios y evidencia — Persona 2

Este documento explica cómo leer y completar GD03. No contiene respuestas de una entrevista realizada. Revisión documental: **22/10/2026**.

## Reglas de uso de la evidencia

1. Se usan los hechos expresos de la ficha y los dos documentos de Empresa 06. Cada fila enlaza la sección y fija el commit consultado del material docente.
2. La fecha de entrega de Mesa (03/06/2026) y Cuestionario (01/05/2026) se distingue del periodo del dato. Las atenciones corresponden a 2025; el cuestionario se aplicó el 09/04/2026. La ficha no indica fecha de emisión ni fecha de corte de todas sus afirmaciones.
3. «Declarada» conserva una afirmación del caso; «Documental» registra presencia o ausencia expresa; «Calculada» identifica una razón reproducible; «No disponible» indica que falta una línea base utilizable.
4. Se usa «No se mide» en las líneas base no disponibles para seguir el formato del taller. En cada Observación se aclara si la fuente declara ausencia de medición o si simplemente no entrega evidencia. Lo no entregado no se toma como inexistente.
5. Se conserva el alcance del denominador: sistemas no equivalen a equipos, usuarios ERP no equivalen a personas en planilla y atenciones no equivalen a incidentes de seguridad.
6. No se usan los valores del ejemplo del taller. Un campo vacío de nivel significa evaluación pendiente.

## Operacionalización del modelo de madurez

La teoría define el modelo para la organización. Para valorar las prácticas de cada indicador se adopta la siguiente interpretación académica del equipo; no se presenta como una rúbrica oficial adicional:

| Nivel | Evidencia mínima de la práctica |
|---|---|
| 1 — Inicial | La fuente describe ausencia, reacción a demanda o una práctica aislada sin funcionamiento sistemático. |
| 2 — Emergente | Existe una práctica operativa parcial, por ejemplo clasificación incompleta de atenciones, MFA solo en correo o soporte de parte de los sistemas. |
| 3 — Definido | Harían falta responsables, procedimientos y ejecución estructurada acreditados. |
| 4 — Gestionado | Harían falta métricas periódicas, metas y revisión documentada del desempeño. |
| 5 — Optimizado | Harían falta mejora continua y adaptación proactiva sustentadas en datos. |

Solo se asignan niveles 1 o 2 porque son los que la evidencia consultada permite sostener. Cada fila explica el hecho que respalda su nivel. Cuando no se conoce la práctica, el puntaje queda vacío: no se presume nivel 1.

**Caso SEG-03.** El número de incidentes de seguridad es desconocido, pero la ficha declara que no se lleva registro. Esto permite evaluar la práctica de registro como inicial, sin afirmar cero incidentes.

**Caso INT-03.** Se evalúa la continuidad del flujo de ubicaciones descrito en hojas de cálculo paralelas. No se concluye que todas las aplicaciones carezcan de integración. Confirmar el flujo y sus interfaces en la entrevista antes de cerrar el puntaje.

El programa calcula la media de puntajes conocidos dentro de cada eje, y después la media de los ocho ejes. Si un eje no tiene ningún puntaje, no publica nivel global. Si hay ejes parcialmente puntuados, presenta el promedio como **provisional**, junto a su cobertura. El redondeo al entero más cercano conserva el posicionamiento orientativo del script docente; debe contrastarse con la descripción cualitativa del modelo.

## Qué solicitar para cerrar las diez líneas base pendientes

Los responsables siguientes son propuestas, no asignaciones aprobadas. Para cada proyecto, su primer entregable es una medición con fecha, universo y evidencia. El plazo debe acordarse con el docente o responsable.

| ID / proyecto | Pregunta o evidencia necesaria | Unidad o forma de obtener la primera línea base |
|---|---|---|
| SER-04 / P-SER-01 | Catálogo con volumen anual por servicio y recorridos que acrediten los niveles actuales. Coordinar con Persona 1. | Suma de volumen por nivel / volumen total; conservar también la media simple. |
| INT-01 / P-INT-01 | ¿Qué interfaces funcionan hoy? Solicitar inventario, mecanismo y una ejecución por interfaz, con fecha. | Número de integraciones activas verificadas en el alcance acordado. |
| INT-02 / P-INT-02 | Requisitos documentales de dos recorridos y evidencia de cuáles documentos ya posee la organización. Coordinar con Persona 1. | Documentos reutilizables / documentos solicitados. Si no se solicitan documentos, registrar «No aplica» con evidencia. |
| SEG-03 / P-SEG-01 | Registro específico de incidentes de seguridad, con periodo, clasificación y responsable; separar solicitudes de soporte. | Número de incidentes registrados en 12 meses; declarar cobertura y posible subregistro. |
| DAT-02 / P-DAT-01 | Inventario de entidades críticas y designaciones de sus dueños. | Número de entidades con dueño designado y total de entidades del alcance. |
| DAT-03 / P-DAT-02 | Actas o registro de decisiones y los datos utilizados para sustentarlas. | Decisiones con evidencia verificable / decisiones revisadas, con periodo. |
| IDE-02 / P-IDE-01 | Inventario conciliado de cuentas activas y mecanismo de correspondencia entre sistemas. | Usuarios con identidad única / usuarios del alcance; resultado agregado sin datos personales. |
| TAL-02 / P-TAL-01 | Asistencia a formación con fecha, tema y personas únicas del periodo, además del universo de personal. | Personas capacitadas en 12 meses / personal del alcance. |
| TAL-03 / P-TAL-02 | Instrumento válido para cultura y aplicación documentada; el cuestionario actual mide percepción y no trae resultados por pregunta. | Perfil y puntajes según el instrumento, participación y límites de interpretación. |
| INF-03 / P-INF-01 | Servicios críticos, ventanas comprometidas, reporte de caídas y monitoreo. | Tiempo disponible / tiempo comprometido durante un periodo definido. |

## Datos conocidos que requieren mayor trazabilidad

- GOB-01 y TAL-01: fijar la fecha de corte de «último año» y «hace tres años».
- DAT-01: pedir periodo y fórmula del 4,7 %; no se dispone de inventarios crudos para recalcularlo.
- INF-01: confirmar vigencia de los soportes y distinguir los cinco sistemas del inventario de equipos.
- SEG-02: solicitar actas de restauración; el caso afirma que nunca se hizo una prueba completa.
- Cuestionario: no calcular satisfacción o formación a partir de 41/157; esa razón solo mide participación voluntaria (26,11 %).
- Mesa: (1929 − 595) / 1929 = 69,16 % de registros con tipo; no mide cobertura de registro de todas las atenciones.

## Comprobaciones y límites de la entrega

- Ocho ejes con al menos dos indicadores cada uno.
- Veinticinco IDs únicos, evidencia y observación en todas las filas.
- Quince líneas base disponibles y diez proyectos para las restantes.
- Dieciséis puntajes justificados y nueve evaluaciones pendientes.
- Madurez provisional y cobertura visibles en salida, radar y PETI.
- Sin entrevista, recorridos ni validación de controles reales: esos pasos siguen pendientes.
- Las columnas ID, Estado de línea base y Proyecto de instrumentación complementan las siete columnas exigidas. GD05 puede cargarlas como columnas adicionales en ejes_gd.
