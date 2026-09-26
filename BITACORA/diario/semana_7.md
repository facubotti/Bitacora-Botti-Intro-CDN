## Semana 7 — 25/09

**Qué intentamos.** Hicimos el ejercicio de clase 10 (tránsito y calidad del aire) con datos reales del catálogo abierto: conteo vehicular, NO2 y PM2.5. Adaptamos el script de la profe para correrlo con los CSV bajados en vez de los de ejemplo.

**Qué falló.** El dataset de conteo vehicular no bajaba desde el portal (pesa 332MB). Encontramos la URL directa del archivo llamando a la API del catálogo, y ahí sí funcionó. También nos dimos cuenta de que el tránsito solo tiene un archivo por mes, y junio 2024 es el único mes en que coincide con el NO2 y el PM2.5 que habíamos bajado (mayo-agosto), así que el análisis quedó acotado a junio.

**Qué decidimos.** Reproducir el análisis completo sobre junio 2024 en Tres Cruces. Confirmamos lo que muestra la clase: el NO2 se relaciona con el tránsito (r=0,20 sin el ciclo diario, supera la prueba del azar) y el PM2.5 no.
