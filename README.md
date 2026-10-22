# SI-886 · Taller Semana 11 · Empresa 06

Repositorio de trabajo para el diagnóstico de gobierno digital y el tablero de línea base de Distribuidora Andina del Sur S.A.C. El caso del curso es ficticio. Este repositorio es público por decisión del equipo: no agregar datos de una organización real, nombres de usuarios, registros de atenciones ni credenciales.

**Confidencialidad:** la guía del taller clasifica el catálogo y sus volúmenes como confidenciales. Por decisión del equipo, el repositorio se mantiene público y solo incorpora hechos publicados del caso ficticio, cálculos agregados y puntajes que se identifican expresamente como propuestas provisionales. No cargar respuestas de entrevista, datos personales, nombres ni archivos crudos. Los volúmenes por servicio permanecen vacíos; antes de publicar respuestas nuevas del docente, confirmar si pueden versionarse o cambiar el repositorio a privado.

## Estado

- **Persona 1 — catálogo:** siete servicios con canales generales y niveles provisionales 3→4; volúmenes y documentos concretos siguen pendientes. Ver [criterios de Persona 1](docs/criterios-provisionales-persona-1.md).
- **Persona 2 — ejes y madurez:** entrega documental terminada con 25 indicadores, diez proyectos para líneas base pendientes, radar y sección 6.1 integrada con el aporte de Persona 1. Resultado provisional: 1,17/5 con 16 indicadores puntuados. Ver [entrega y evidencias](docs/entrega-persona-2.md).
- **Persona 3 — tablero:** plan de trabajo en [docs/plan-persona-3.md](docs/plan-persona-3.md).
- El análisis publica los resultados que sí pueden calcularse y señala como pendientes los que requieren volúmenes o documentos. Los campos faltantes están vacíos; nunca se deben interpretar como cero.
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
- 06_gobierno_digital/GD03_ejes.csv y GD04_madurez.py: diagnóstico documental y cálculo de madurez; ejecución y dependencias en docs/entrega-persona-2.md.
- 06_gobierno_digital/6.1_situacion_actual.md: sección 6.1 consolidada con los aportes de Personas 1 y 2.
- docs/plan-persona-2.md, docs/plan-persona-3.md: planes asignados para que el equipo los desarrolle.
- graficos/: gráficos generados por los programas del taller.
- evidencias/S11/: capturas y salidas versionadas.

## Ejecutar Persona 1

Con Python 3.12, desde la raíz del repositorio:

```sh
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python 06_gobierno_digital/GD02_analisis_servicios.py
python -m unittest discover -s tests -v
```

El script genera `graficos/GD_servicios.png`. Los promedios simples y el gráfico usan los niveles provisionales cargados; la ponderación y los demás cálculos permanecen pendientes hasta completar sus datos de entrada.

## Fuentes del curso

- [Guía del taller](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/3-TALLER.md)
- [Ficha Empresa 06](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/FICHA.md)
- [Mesa de servicio y SLA](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/mesa-de-servicio-y-sla.md)
- [Cuestionario diagnóstico](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/RECURSOS-TALLER/EMPRESA-06-distribuidora-andina-sur/cuestionario-diagnostico.md)

No se copian los documentos fuente ni los registros nominales. Las salidas del tablero deben estar agregadas y Metabase/PostgreSQL deben permanecer ligados a 127.0.0.1.
