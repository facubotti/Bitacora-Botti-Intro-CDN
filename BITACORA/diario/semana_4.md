## Semana 4 — 04/09

**Qué intentamos.** Armamos un script para bajar y analizar un dataset abierto: conteo vehicular en avenidas de Montevideo (foco en Bv Artigas), del catálogo de datos abiertos. Un script descarga el CSV y otro lo filtra y calcula el promedio de vehículos por hora.

**Qué falló.** Al mirar los datos vimos que "Bv Artigas" estaba escrito de dos formas (en miles de filas decía "Bv. Artgias" por error), así que hubo que corregirlo antes de filtrar. También pensábamos que la columna de volumen era por hora, pero en realidad era cada 5 minutos, y tuvimos que rehacer el cálculo sumando los bloques antes de promediar.

**Qué decidimos.** Dejar el CSV afuera del repo (pesa más de 100MB) y subir solo los scripts.
