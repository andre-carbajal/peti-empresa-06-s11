# Plan de implementación — Persona 3: base local, tablero e integración

**Responsable:** Kiara1616  
**Rama de trabajo:** main; cambios directos del equipo.
**Fuente principal:** [Guía del taller, pasos C–F](https://github.com/OscarJimenezFlores/PETI/blob/main/SEMANA-11/3-TALLER.md).

## Avance verificado al 22/10/2026

- Integrados en `main` los aportes de Personas 1 y 2 y la preparación de Persona 3.
- Compose validado para puertos locales 5433 y 3001; GD05 valida los CSV antes de cargar y ofrece `--check` sin PostgreSQL.
- La validación de fuentes confirma siete servicios, 25 indicadores, diez sin línea base y paridad de los ocho promedios con GD04. Los 21 tests del repositorio pasan. GD05 rechaza columnas reordenadas o valores no finitos y elimina tablas de fuentes ausentes para no conservar datos obsoletos.
- Seis preguntas definidas en [tablero-persona-3.md](tablero-persona-3.md) y matriz de 13 resultados redactada en [informe-taller-s11-borrador.md](informe-taller-s11-borrador.md).
- Pendientes de ejecución: Docker no ofrece motor accesible en esta sesión; faltan NO03, MG03 y siete volúmenes anuales. Sin ello no hay cuatro tablas cargadas, seis visualizaciones ni capturas válidas.
- Pendiente de entrega: el usuario pidió dejar en espera nombres, códigos y grupo de la carátula; el PDF final y las etiquetas se prepararán al cierre conjunto.

## Objetivo y entregables

Desplegar PostgreSQL y Metabase solo en localhost; cargar los cuatro CSV definidos por el taller; construir al menos seis visualizaciones; archivar capturas/salidas en evidencias/S11/; y ensamblar el informe PDF con evidencias y enlaces.

## Dependencias antes de construir el tablero

- Esperar los CSV completos de Persona 1 (GD01_catalogo_servicios.csv) y Persona 2 (GD03_ejes.csv). No cargar el borrador con campos vacíos como si fueran ceros.
- Solicitar al equipo los insumos previos 04_normativa/NO03_matriz_cumplimiento.csv y 04_normativa/MG03_capacidad.csv. No están en el workspace con el que se inició este repositorio. Si no se reciben, documentar el bloqueo; no inventar obligaciones, niveles ni capacidad.
- No incluir los documentos originales del caso ni datos personales. Usar tablas agregadas para el tablero.

## Pasos de trabajo

1. Crear PostgreSQL local con el puerto host ligado a 127.0.0.1:5433; ligar Metabase a 127.0.0.1:3001 (no publicar el puerto en todas las interfaces). Mantener los contenedores locales y documentar cómo detenerlos.
2. Crear 06_gobierno_digital/GD05_carga_tablero.py para cargar servicios, ejes_gd, cumplimiento y capacidad. No guardar credenciales en el repo; leer la URL de conexión de una variable de entorno y excluir .env mediante .gitignore.
3. Conectar Metabase a la base local y crear estas preguntas:
   - barras horizontales: nivel actual vs. objetivo por servicio;
   - tarjeta: nivel ponderado por volumen (mostrar también el promedio simple para comparar);
   - barras/radar: madurez por eje;
   - anillo: estado del cumplimiento normativo;
   - barras agrupadas: capacidad actual vs. objetivo;
   - tabla: indicadores sin línea base.
4. Guardar capturas completas y salidas reproducibles en evidencias/S11/; cada captura debe corresponder a una visualización accesible y estar enlazada desde el informe.
5. Integrar el informe con la plantilla del curso. Añadir la matriz de resultados con 13 filas, estado y URL; preservar la numeración de la plantilla y dejar registrada la discrepancia con la guía para confirmación docente.
6. Comprobar con Persona 1 y 2 que los valores de Metabase coinciden con los CSV y salidas de scripts; subir los cambios directamente a main.

## Pruebas y aceptación

- Los dos servicios son accesibles en localhost; PostgreSQL contiene las cuatro tablas esperadas y Metabase las consulta.
- Se ven seis visualizaciones con datos del caso, sin columnas personales ni valores inventados.
- Capturas y salidas están en evidencias/S11/ y sus URL están incluidas en el informe.
- Los tres recorridos de validación del taller quedan ejecutados o documentados como simulación/limitación.
- El PDF tiene carátula, integrantes y códigos, índice actualizado, instrucciones eliminadas, conclusiones sustentadas, referencias APA y anexos citados; no se presenta el DOCX como entrega final.
- Al cerrar la entrega en main, registrar las etiquetas v0.11 y taller-11 sobre el commit entregado.
