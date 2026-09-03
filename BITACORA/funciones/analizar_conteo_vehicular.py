# %%
from pathlib import Path
import pandas as pd

# 1. Definir la ruta del archivo
# (correr este script desde la raiz del repo)
BASE_DIR = Path.cwd()
ruta_csv = BASE_DIR / "BITACORA" / "Dataset de Datos Abiertos" / "Conteo_Agosto_2026.csv"

# 2. Verificar que el archivo existe antes de cargarlo
if not ruta_csv.exists():
    raise FileNotFoundError(f"No se encontró el archivo en: {ruta_csv}. Correr primero descargar_conteo_vehicular.py")

# 3. Cargar el archivo CSV
df = pd.read_csv(ruta_csv)

print(f"--- Archivo cargado desde: {ruta_csv.name} ---")
print(df.shape)
print(df.head())

# 4. Corregir un error de tipeo: "Bv Artigas" aparece tambien como "Bv. Artgias"
df["dsc_avenida"] = df["dsc_avenida"].replace({"Bv. Artgias": "Bv Artigas"})

# 5. Filtrar por avenida
filtro_avenida = df[df["dsc_avenida"] == "Bv Artigas"]
print(f"Filas en Bv Artigas: {len(filtro_avenida)}")

# 6. Filtrar por fecha (primera semana de agosto, a modo de ejemplo)
filtro_fecha = filtro_avenida[(filtro_avenida["fecha"] >= "2026-08-01") & (filtro_avenida["fecha"] <= "2026-08-07")]
print(f"Filas en la primera semana de agosto: {len(filtro_fecha)}")

# 7. Filtrar por volumen (solo bloques de 5 min con 5 vehiculos o mas)
filtro_volumen = filtro_avenida[filtro_avenida["volumen_hora"] >= 5]
print(f"Filas con volumen >= 5: {len(filtro_volumen)}")

# 8. Promedio de vehiculos por hora en Bv Artigas
# La columna volumen_hora es en realidad el conteo cada 5 minutos, no por hora,
# entonces primero sumo los bloques de cada hora y despues promedio entre
# detectores, carriles y dias.
filtro_avenida = filtro_avenida.copy()
filtro_avenida["hora_del_dia"] = filtro_avenida["hora"].str[:2].astype(int)

vehiculos_por_hora = (
    filtro_avenida.groupby(["fecha", "hora_del_dia", "cod_detector", "id_carril"])["volumen_hora"]
    .sum()
    .reset_index(name="vehiculos")
)

promedio_horario = vehiculos_por_hora.groupby("hora_del_dia")["vehiculos"].mean().round(1)

print("\nPromedio de vehiculos por hora en Bv Artigas:")
print(promedio_horario)
print(f"\nPromedio general (todas las horas): {promedio_horario.mean():.1f} vehiculos/hora")
