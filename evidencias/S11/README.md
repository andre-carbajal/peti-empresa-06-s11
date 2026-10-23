# Evidencias Semana 11

Guardar aquí capturas y salidas requeridas por el taller, sin nombres ni datos personales. Cada archivo debe citarse en el informe y corresponder a un artefacto verificable del repositorio.

## Persona 2 — diagnóstico documental

- [Salida de madurez](salidas/GD04_madurez.txt): cálculo, cobertura, proyectos y límites.
- [Resumen estructurado](salidas/GD04_resumen.json): valores sin redondeo intermedio.
- [Promedios por eje](salidas/GD04_resumen_ejes.csv): datos numéricos para el tablero.
- [Indicadores sin línea base](salidas/GD04_sin_linea_base.csv): diez filas con proyectos.
- [Validación automática](salidas/GD04_validacion.txt): siete comprobaciones del programa.
- [Entorno de ejecución](salidas/GD04_entorno.txt): versiones utilizadas.
- [Radar](../../graficos/GD_madurez.png): diagnóstico provisional con cobertura por eje.

Estas salidas documentan una ejecución local y una evaluación de las fuentes del caso. No son capturas de Metabase ni pruebas de controles o recorridos en una organización real. El detalle está en [la entrega de Persona 2](../../docs/entrega-persona-2.md).

## Persona 3 — preparación del tablero

- [Validación de fuentes GD05](salidas/GD05_validacion_fuentes.txt): siete servicios, siete volúmenes pendientes, 25 indicadores, diez sin línea base y paridad con el resumen de Persona 2.
- [Validación PostgreSQL GD05](salidas/GD05_postgres_validacion.txt): carga real de dos tablas, conteos de vistas y promedio ponderado NULL. La ejecución fue local y sin Docker.
- [Validación Metabase](salidas/GD06_metabase_validacion.txt): seis preguntas distintas ejecutadas, ocho tarjetas y límites de la prueba.
- [Salida directa de GD06](salidas/GD06_salida.txt): identificadores de preguntas, filas por consulta y paridad completa con los CSV.
- [Carga de cuatro fuentes](salidas/GD05_cuatro_fuentes_s11.txt): conteos de GD01, GD03, NO03 y MG03 en PostgreSQL local.
- [Validación de ocho preguntas](salidas/GD06_ocho_preguntas_s11.txt): identificadores, filas y paridad con las cuatro fuentes y GD04.
- [Paso E del taller](salidas/S11_validacion_paso_e.md): tres comprobaciones, con dos recorridos seleccionados y pendientes, evidencia documental de los ejes y prueba «una sola vez» no calculable.
- Capturas reales de Metabase: [servicios](tablero-01.png), [ponderado y simple](tablero-02.png), [madurez por eje](tablero-03.png), [controles documentales](tablero-04.png), [capacidad documental](tablero-05.png), [indicadores sin línea base](tablero-06.png), [cobertura de líneas base](tablero-07.png), [cobertura de puntajes](tablero-08.png) y [tablero completo](tablero-ocho-preguntas.png). Las preguntas 04 y 05 muestran evaluaciones provisionales de S11.
- [Guía del tablero y estado del entorno](../../docs/tablero-persona-3.md): procedimiento de reproducción y comprobación de Docker.

Las preguntas 07 y 08 se construyeron con GD03 y se cotejaron contra sus 25 filas. La 04 cuenta controles descritos en S11, sin dictamen legal; la 05 muestra capacidad de TI estimada y objetivo propuesto, sin validación de responsables.
