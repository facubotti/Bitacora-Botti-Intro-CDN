# Tránsito y calidad del aire — junio 2024

Ejercicio de clase 10 (series de tiempo, correlación y regresión lineal). Datasets: [Conteo vehicular](https://catalogodatos.gub.uy/dataset/conteo-vehicular-en-las-principales-avenidas-de-montevideo), [PM2.5](https://catalogodatos.gub.uy/dataset/datos-por-estacion-pm-2-5) y [NO2](https://catalogodatos.gub.uy/dataset/dioxido-de-nitrogeno), Catálogo de Datos Abiertos de Uruguay.

Scripts: `funciones/descargar_transito_aire.py` (descarga los CSV, no se versionan) y `funciones/analisis_transito_aire.py` (arma el panel por hora y hace todo el análisis).

Nota sobre los datos: el NO2 y el PM2.5 que bajé cubren mayo-agosto 2024, pero el conteo vehicular se publica un archivo por mes y junio 2024 es el único mes en que las tres fuentes coinciden. El análisis usa junio.

Declaro que usé un asistente de IA (Claude) para escribir el código de este análisis, adaptando el script que subió la profe a los datos reales bajados del catálogo. Los números y gráficos los revisé yo contra lo que muestra la clase.

## Elección de estación

De las tres estaciones de aire, Tres Cruces es la que tiene más puntos de conteo vehicular cerca (55, contra 4 de Curva de Maroñas), aunque el NO2 ahí solo tiene datos hasta mitad de mes (291 horas contra 655 en Curva de Maroñas). Museo Romántico no mide NO2. Me quedé con Tres Cruces: prefiero tener el tránsito bien medido aunque sea con menos días.

## Resultados

| Paso | NO2 | PM2.5 |
|---|---|---|
| Correlación cruda | r = 0,59 | r = −0,02 |
| Sin el ciclo diario (desvíos) | r = 0,20 | r = −0,02 |
| Mejor rezago | 2 horas | 13 horas |
| ¿Supera al azar? | Sí, ninguna corrida al azar iguala la r real | No, queda en el 60% de las corridas al azar |
| R² solo con la hora del día | 0,47 | 0,19 |
| R² sumando el tránsito | 0,50 | 0,22 |
| b (µg/m³ por cada 1.000 veh/h) | 1,25 | 1,06 |

## Qué me llevo

El NO2 sí tiene relación con el tránsito: la correlación cruda (0,59) baja mucho al sacar el ciclo diario (0,20), pero no llega a cero, y responde con una demora corta (2 horas), como un gas que sale del caño de escape y se disipa rápido. Esa relación no es casualidad: ninguna de las corridas con el tránsito desplazado al azar da una correlación tan alta.

El PM2.5 es otra historia: la correlación cruda ya es prácticamente cero, y sacando el ciclo diario tampoco aparece nada. El mejor rezago (13 horas) no supera la prueba del azar. Con este mes de datos, no puedo decir que el tránsito medido cerca de Tres Cruces se vea en el PM2.5 — puede ser que la partícula fina tenga otras fuentes (leña, industria, el aire de toda la ciudad) que pesan más que el tránsito local.

Agregar el tránsito al modelo mejora poco el R² en los dos casos (de 0,47 a 0,50 en NO2, de 0,19 a 0,22 en PM2.5): la hora del día explica la mayor parte de lo que se puede explicar sin otras variables (viento, lluvia, temperatura).

## Limitaciones

- Un solo mes de tránsito (junio 2024), y dentro de ese mes el NO2 en Tres Cruces solo tiene la primera mitad.
- El "tránsito cercano" suma varios puntos de conteo: un mismo auto puede contarse más de una vez, así que es un indicador de actividad, no una cantidad real de vehículos.
- No hay datos de viento, lluvia ni temperatura, que la profe marca como las variables que más pueden estar faltando.
