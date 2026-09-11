

# Clase 7 - Carga y transformacion, aplicado a mi dataset de conteo vehicular
# (Bv Artigas, agosto 2026)

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar datos (correr este script desde la raiz del repo)
BASE_DIR = Path.cwd()
ruta_csv = BASE_DIR / "BITACORA" / "Dataset de Datos Abiertos" / "Conteo_Agosto_2026.csv"
if not ruta_csv.exists():
    raise FileNotFoundError(f"No se encontro el archivo en: {ruta_csv}. Correr primero descargar_conteo_vehicular.py")

SALIDAS = BASE_DIR / "BITACORA" / "salidas"
SALIDAS.mkdir(exist_ok=True)

df = pd.read_csv(ruta_csv)
df["dsc_avenida"] = df["dsc_avenida"].replace({"Bv. Artgias": "Bv Artigas"})
datos = df[df["dsc_avenida"] == "Bv Artigas"].copy()
print(f"Filas en Bv Artigas: {len(datos)}")

# 2. Data profiling: identificador, nulos y duplicados

## 2.1 Info basica
print(datos.info())
print(datos.head())

## 2.2 Identificador
# Cada fila es un bloque de 5 minutos de un detector, en un carril, fecha y hora dados. El identificador es la combinacion de esas 4 columnas.
print(datos[["cod_detector", "id_carril", "fecha", "hora"]].head())

## 2.3 Valores faltantes
print(datos.isna().sum())
# dsc_int_anterior y dsc_int_siguiente tienen nulos, pero es porque esos detectores estan en la punta de la avenida (no tienen interseccion antes o despues).

## 2.4 Duplicados
n_dup = datos.duplicated(subset=["cod_detector", "id_carril", "fecha", "hora"]).sum()
print(f"Filas duplicadas (mismo detector, carril, fecha y hora): {n_dup}")

duplicadas = datos[datos.duplicated(subset=["cod_detector", "id_carril", "fecha", "hora"], keep=False)]
print(duplicadas.sort_values(["cod_detector", "id_carril", "fecha", "hora"]).head(10))

## 2.5 Eliminar duplicados
# Me quedo con la primera fila de cada duplicado.
datos_sindup = datos.drop_duplicates(subset=["cod_detector", "id_carril", "fecha", "hora"])

# 3. Tipos de datos y transformacion

## 3.1 Fecha y hora venian separadas como texto, las junto en una sola columna de fecha-y-hora para poder hacer cuentas con ella.
datos_sindup["fecha_hora"] = pd.to_datetime(datos_sindup["fecha"] + " " + datos_sindup["hora"])
print(datos_sindup["fecha_hora"].dtype)

## 3.2 Variables nuevas a partir de esa columna
datos_new = datos_sindup.copy()
datos_new["dia"] = datos_new["fecha_hora"].dt.date
datos_new["hora_del_dia"] = datos_new["fecha_hora"].dt.hour

# 4. Agregacion temporal: 5 minutos -> horaria -> diaria
# volumen_hora es el conteo de cada bloque de 5 minutos, no de la hora
# entera, asi que primero sumo los bloques de cada hora y recien ahi
# promedio.


def p95(x):
    return x.quantile(0.95)


## 4.1 Horaria: sumo los bloques de 5 min de cada hora, por detector y carril
vehiculos_hora = (
    datos_new.groupby(["cod_detector", "id_carril", "dia", "hora_del_dia"])["volumen_hora"]
    .sum()
    .reset_index(name="vehiculos")
)

## 4.2 Diaria: sumo las 24 horas de cada dia, por detector y carril
resumen_diario = vehiculos_hora.groupby(["cod_detector", "id_carril", "dia"])["vehiculos"].agg(
    media="mean", maximo="max", p95=p95, n_horas="size"  # n_horas deberia dar 24
).reset_index()
print(resumen_diario.head())

## 4.3 Promedio de vehiculos por hora del dia, toda la avenida junta
promedio_horario = vehiculos_hora.groupby("hora_del_dia")["vehiculos"].mean().round(1)
print("\nPromedio de vehiculos por hora en Bv Artigas:")
print(promedio_horario)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(promedio_horario.index, promedio_horario.values, color="blue", linewidth=1.5)
ax.scatter(promedio_horario.index, promedio_horario.values, color="red", s=25, zorder=3)
ax.set(title="Vehiculos por hora del dia, Bv Artigas, agosto 2026",
       xlabel="Hora del dia", ylabel="Vehiculos (promedio)")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(SALIDAS / "vehiculos_por_hora_bv_artigas.png", dpi=150)
plt.close()

## 4.4 Comparo media, p95 y maximo por dia para toda la avenida
# (media = nivel tipico, maximo = puede ser un error del sensor, p95 = pico
# alto pero mas confiable que el maximo)
resumen_avenida_dia = vehiculos_hora.groupby("dia")["vehiculos"].agg(
    media="mean", maximo="max", p95=p95
).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
for col in ("media", "p95", "maximo"):
    ax.plot(resumen_avenida_dia["dia"], resumen_avenida_dia[col], label=col)
ax.set(title="Agregacion diaria: media, p95 y maximo, Bv Artigas, agosto 2026",
       ylabel="Vehiculos por hora")
ax.legend()
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(SALIDAS / "agregacion_diaria_bv_artigas.png", dpi=150)
plt.close()


# 5. Datos faltantes implicitos (filas que directamente no estan)
# No hay NaN en volumen_hora (ya lo vimos en el punto 2.3), asi que lo unico
# que puede faltar es que un bloque de 5 min no aparezca en el archivo.
# Cada detector/carril deberia tener un bloque cada 5 min durante agosto:
# 31 dias * 288 bloques por dia = 8928 filas esperadas.
ESPERADOS_MES = 31 * 288

cobertura = datos_sindup.groupby(["cod_detector", "id_carril"]).agg(
    presentes=("fecha_hora", "nunique")
).reset_index()
cobertura["esperados"] = ESPERADOS_MES
cobertura["cobertura_pct"] = (100 * cobertura["presentes"] / cobertura["esperados"]).round(1)
cobertura = cobertura.sort_values("cobertura_pct")

print(cobertura.head(10))
print(f"\nCobertura promedio de la avenida: {cobertura['cobertura_pct'].mean():.1f}%")

peor = cobertura.iloc[0]
print(f"Peor cobertura: detector {peor['cod_detector']} carril {peor['id_carril']} ({peor['cobertura_pct']}%)")
