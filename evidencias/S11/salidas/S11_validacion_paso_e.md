# Paso E · tres comprobaciones del taller

Fecha de revisión documental: 22/10/2026. Alcance: únicamente los archivos versionados de Empresa 06. Esta revisión no equivale a una entrevista, una simulación con el docente ni una prueba de sistemas de la organización ficticia.

| Comprobación de la guía | Evidencia revisada | Resultado | Corrección o dato faltante |
|---|---|---|---|
| 1. Recorrer dos servicios de principio a fin y contrastar el nivel declarado | Filas `S-07` y `S-06` de [GD01](../../../06_gobierno_digital/GD01_catalogo_servicios.csv), [criterios provisionales](../../../docs/criterios-provisionales-persona-1.md) | **No comprobado.** Ambos tienen nivel 3→4 propuesto, pero no hay recorrido observado ni simulado con el docente. | Ejecutar y fechar dos recorridos, guardar etapas, canal, cambio de canal, duración, presencia requerida, documentos, aprobación y cierre sin datos personales. Ajustar niveles según lo observado. |
| 2. Verificar evidencia de cada eje evaluado | [GD03](../../../06_gobierno_digital/GD03_ejes.csv), [GD04](../../../evidencias/S11/salidas/GD04_resumen.json) | **Estructura documental comprobada.** Hay 25 indicadores en ocho ejes; los 16 puntuados tienen campo de fuente/fecha y enlace de evidencia; los diez sin línea base tienen proyecto. No se probaron controles operativos. | Comprobar con responsables la vigencia y alcance de cada control antes de llamar definitivos a los puntajes. Mantener los nueve puntajes desconocidos vacíos. |
| 3. Evaluar «una sola vez» con documentos concretos | Los siete campos `Documentos solicitados` y `De ellos, ya en poder de la organización` de [GD01](../../../06_gobierno_digital/GD01_catalogo_servicios.csv) | **No calculable.** Los catorce campos están vacíos; no hay documentos concretos ni denominador. | Registrar por trámite los documentos pedidos y cuáles ya posee la organización; verificar reutilización y ejecutar GD02. No reemplazar vacíos por cero. |

## Fichas de los dos recorridos seleccionados

| Servicio | Lo que sí consta | Lo que debe observarse en el recorrido | Estado |
|---|---|---|---|
| `S-07` Accesos y cuentas de usuario | Meta declarada de 24 horas, no firmada ni medida; MFA solo documentada para correo; canales de la mesa sin asignación al servicio; nivel 3→4 propuesto. | Quién solicita y aprueba, cómo se verifica identidad, qué sistema se aprovisiona, canal usado en cada etapa, cierre, tiempo real y documentos concretos. | Instrumento preparado; recorrido pendiente. |
| `S-06` Respaldo y recuperación de archivos | Respaldos a disco local, sin prueba de restauración completa; horario no definido; nivel 3→4 propuesto. | Solicitud, autorización, identificación de archivo, restauración de prueba, entrega segura, confirmación, canal y duración, sin copiar archivos personales. | Instrumento preparado; recorrido pendiente. |

Estas fallas permanecen registradas en **Problemas y mejoras** del informe. El tablero parcial y su paridad con GD01/GD03/GD04 están documentados por separado en [GD06_metabase_validacion.txt](GD06_metabase_validacion.txt).
