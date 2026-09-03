# Análisis — Conteo vehicular en Bv Artigas (Agosto 2026)

Dataset: [Conteo vehicular en las principales avenidas de Montevideo](https://catalogodatos.gub.uy/dataset/conteo-vehicular-en-las-principales-avenidas-de-montevideo), Catálogo de Datos Abiertos de Uruguay.

**Cómo lo procesé.** El script `funciones/analizar_conteo_vehicular.py` descarga (con `funciones/descargar_conteo_vehicular.py`), filtra por avenida, fecha y volumen, y calcula el promedio de vehículos por hora. El CSV tiene 8.883.366 filas y viene en bloques de 5 minutos por detector y carril, no de una hora entera, así que primero sumé los bloques de cada hora y después promedié entre detectores y días.

**Un detalle del dataset:** "Bv Artigas" aparece escrito de dos formas (`Bv Artigas` y, en 8.928 filas, `Bv. Artgias` con error de tipeo). Lo corregí antes de filtrar para no perder esas filas.

## Promedio de vehículos por hora en Bv Artigas

| Hora | Promedio | Hora | Promedio |
|------|----------|------|----------|
| 00   | 115.3    | 12   | 352.2    |
| 01   | 59.6     | 13   | 354.8    |
| 02   | 39.3     | 14   | 351.2    |
| 03   | 32.7     | 15   | 357.0    |
| 04   | 37.5     | 16   | 373.4    |
| 05   | 101.4    | 17   | 383.9    |
| 06   | 162.7    | 18   | 347.8    |
| 07   | 242.7    | 19   | 296.7    |
| 08   | 291.4    | 20   | 268.5    |
| 09   | 290.9    | 21   | 229.5    |
| 10   | 297.5    | 22   | 180.4    |
| 11   | 328.3    | 23   | 145.1    |

**Promedio general (todas las horas):** 235.0 vehículos/hora.

Se ve el patrón esperado: mínimo de madrugada (3-4hs) y pico entre las 16 y 18hs.

*Nota: usé un asistente de IA para escribir el script de análisis; corrí el código y verifiqué los resultados.*
