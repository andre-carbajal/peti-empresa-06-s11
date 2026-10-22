# SI-886 · Taller Semana 11 · Empresa 06

Repositorio de trabajo para el diagnóstico de gobierno digital y el tablero de línea base de Distribuidora Andina del Sur S.A.C. El caso del curso es ficticio. Este repositorio es público por decisión del equipo: no agregar datos de una organización real, nombres de usuarios, registros de atenciones ni credenciales.

## Estado

- **Persona 1 — catálogo:** borrador de siete servicios preparado; volúmenes, niveles, documentos y canales por servicio esperan la entrevista simulada con el docente.
- **Personas 2 y 3:** planes de trabajo en [docs/plan-persona-2.md](docs/plan-persona-2.md) y [docs/plan-persona-3.md](docs/plan-persona-3.md).
- No ejecutar el análisis del catálogo hasta completar y validar sus campos numéricos. Los campos pendientes están vacíos, nunca se deben interpretar como cero.
- Las matrices 04_normativa/NO03_matriz_cumplimiento.csv y 04_normativa/MG03_capacidad.csv no estaban en el workspace al preparar este repo; son un requisito pendiente del tablero.

## Equipo y flujo

| Persona | GitHub | Área |
|---|---|---|
| 1 | andre-carbajal | Catálogo, preguntas de entrevista y cálculos por servicio |
| 2 | Sofxx7 | Ocho ejes, evidencia, línea base y madurez |
| 3 | Kiara1616 | PostgreSQL, Metabase, tablero e integración del informe |

Integrar el trabajo mediante ramas feat/s11-persona-1-catalogo, feat/s11-persona-2-ejes y feat/s11-persona-3-tablero, con Pull Request hacia develop. No incorporar resultados sin fuente y evidencia.

## Estructura

- 06_gobierno_digital/GD01_catalogo_servicios.csv: borrador inicial del catálogo.
- docs/preguntas-entrevista-persona-1.md: datos que deben solicitarse antes de calcular.
- docs/plan-persona-2.md, docs/plan-persona-3.md: planes asignados para que el equipo los desarrolle.
- graficos/: gráficos generados por los programas del taller.
- evidencias/S11/: capturas y salidas versionadas.

## Fuentes del curso

- [Guía del taller](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/3-TALLER.md)
- [Ficha Empresa 06](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/FICHA.md)
- [Mesa de servicio y SLA](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/mesa-de-servicio-y-sla.md)
- [Cuestionario diagnóstico](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/cuestionario-diagnostico.md)

No se copian los documentos fuente ni los registros nominales. Las salidas del tablero deben estar agregadas y Metabase/PostgreSQL deben permanecer ligados a 127.0.0.1.
