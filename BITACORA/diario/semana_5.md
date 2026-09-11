Semana 5 11/09/25

**Qué intentamos.** Aplicamos los conceptos de clase 7 (perfilado, transformación de fechas, agregación temporal) a nuestro dataset de conteo vehicular en Bv Artigas: id de fila (detector+carril+fecha+hora), agregación de 5 min a horaria y diaria, y análisis de faltantes implícitos.

**Qué falló.** Encontramos 148 filas duplicadas exactas que hubo que sacar antes de agregar. También vimos picos raros en el máximo diario (20/08 y 25/08, hasta 2300 veh/hora) que no aparecen en el p95 — parece error de sensor, no tráfico real.

**Qué decidimos.** Usar el p95 en vez del máximo como indicador de tráfico pico, porque es más robusto a esos errores. Los gráficos van en `salidas/`, afuera del repo (se regeneran con el script).