# Conteo vehicular en Bv Artigas — Agosto 2026

Dataset: [Conteo vehicular en las principales avenidas de Montevideo](https://catalogodatos.gub.uy/dataset/conteo-vehicular-en-las-principales-avenidas-de-montevideo), Catálogo de Datos Abiertos de Uruguay.

Scripts: `funciones/descargar_conteo_vehicular.py` (descarga el CSV, no se versiona porque pesa >100MB) y `funciones/analizar_conteo_vehicular.py` (filtra por avenida, fecha y volumen, y calcula el promedio por hora).

Dos cosas que noté al mirar los datos:

- "Bv Artigas" está escrito de dos formas en el dataset: `Bv Artigas` y, en 8.928 filas, `Bv. Artgias` (error de tipeo). Lo corregí antes de filtrar.
- La columna `volumen_hora` en realidad es el conteo cada 5 minutos, no por hora. Para el promedio por hora sumé los bloques de cada hora antes de promediar.

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

Promedio general: 235.0 vehículos/hora. Mínimo de madrugada (3-4hs), pico entre las 16 y 18hs.

*Usé IA para escribir el código de descarga y análisis; corrí los scripts y revisé los resultados.*
