# Plan de implementación — Persona 2: diagnóstico de ejes y madurez

**Entrega del 22/10/2026:** terminados la matriz, GD04, el radar y la sección 6.1 consolidada con Persona 1. Ver [entrega e insumos para Kiara](entrega-persona-2.md). El diagnóstico conserva sus limitaciones documentadas.

**Responsable:** Sofxx7  
**Rama de trabajo:** main; cambios directos del equipo.
**Fuentes:** [Ficha de Empresa 06](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/FICHA.md), [mesa de servicio](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/mesa-de-servicio-y-sla.md) y [cuestionario](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/cuestionario-diagnostico.md).

## Objetivo y entregables

Producir 06_gobierno_digital/GD03_ejes.csv con los ocho ejes y al menos dos indicadores por eje; adaptar GD04_madurez.py; generar graficos/GD_madurez.png; y redactar las secciones 6.1.1 y 6.1.4–6.1.6 de 06_gobierno_digital/6.1_situacion_actual.md.

## Pasos

1. Leer solo los documentos citados y extraer hechos con fuente. No trasladar nombres, registros nominales ni credenciales al repo público.
2. Crear la tabla con las columnas del taller: Eje, Indicador, Línea base, Fuente y fecha del dato, Evidencia, Nivel del eje (1–5) y Observación.
3. Completar un mínimo de dos indicadores por eje, usando la guía siguiente como punto de partida. Lo que no se conoce debe preguntarse en la entrevista simulada; si no se mide, escribir literalmente «No se mide» y proponer un proyecto para instrumentarlo.
4. Justificar cada nivel de 1 a 5 con el modelo de madurez y el hecho fuente. No convertir «No se mide» en un valor de línea base; diferenciarlo del nivel de madurez asignado.
5. Adaptar el cálculo del script fuente, ejecutar únicamente con el CSV completo y escribir los resultados y limitaciones en el PETI. El programa promedia los indicadores por eje y después promedia los ejes; documentar que no pondera indicadores por volumen.
6. Revisar las filas contra fuentes y subir los cambios directamente a main.

## Evidencia disponible por eje

| Eje | Hechos iniciales que pueden respaldar indicadores | Validaciones pendientes |
|---|---|---|
| Gobernanza | El comité existe en papel pero no se reunió el último año; no existe PETI. | Actas, responsables y vigencia del presupuesto. |
| Servicios | La mesa reconoce siete servicios, sin dueños ni SLA firmados; el registro de atenciones es incompleto. | Métricas por servicio y catálogo final (depende de Persona 1). |
| Interoperabilidad | Se describen ERP, fuerza de ventas móvil, OSE, portal y hojas paralelas de almacén. | Número de integraciones activas y documentos reutilizables; no inferir integraciones. |
| Seguridad digital | Política de 2022 sin difusión/revisión; no se registran incidentes; respaldos locales sin restauración probada; MFA solo en correo. | Fuentes/fechas de controles y alcance de los sistemas. |
| Datos | Inventario físico y contable difieren en promedio; se usan hojas paralelas y el inventario de activos está desactualizado. | Método/fecha del dato, dueños de datos y decisiones con datos verificables. |
| Identidad digital | MFA solo en correo; la ficha informa usuarios ERP y personal en planilla. | Identidad única, revisión de cuentas y cobertura por sistema; no inferir cuentas huérfanas. |
| Talento | Se reporta una charla de seguridad en inducción hace tres años. | Cobertura de capacitación en 12 meses. El cuestionario no tiene respuestas y fue voluntario/no validado: no es una línea base representativa. |
| Infraestructura | El ERP corre en servidor propio con soporte; el portal no tiene soporte vigente; la continuidad y las restauraciones no están probadas. | Disponibilidad, equipos dentro de soporte y pruebas de recuperación. |

## Criterios de aceptación

- Al menos 16 indicadores, repartidos en los ocho ejes.
- Cada línea base tiene valor, fuente y fecha, o declara «No se mide»; cada nivel tiene evidencia y justificación.
- Se identifican y cuentan indicadores sin línea base, con proyecto de instrumentación para cada uno.
- GD04_madurez.py corre desde la carpeta prevista, informa promedio por eje y nivel global, y produce el radar.
- La entrega explica valores no disponibles y no presenta como medido lo que solo es declarado.
