"""
Analisis del dataset de conteo vehicular en avenidas de Montevideo (Agosto 2026).

Filtra los datos por avenida, fecha y volumen, y calcula el promedio
de vehiculos por hora en Bv Artigas.

Fuente: https://catalogodatos.gub.uy/dataset/conteo-vehicular-en-las-principales-avenidas-de-montevideo
El CSV se descarga con funciones/descargar_conteo_vehicular.py (no se versiona, pesa >700MB).
"""

import pandas as pd
from pathlib import Path

RUTA_CSV = Path(__file__).resolve().parent.parent / "Dataset de Datos Abiertos" / "Conteo_Agosto_2026.csv"

COLUMNAS = ["cod_detector", "id_carril", "fecha", "hora", "dsc_avenida", "volumen_hora"]

# En el dataset "Bv Artigas" tambien aparece mal escrito como "Bv. Artgias"
CORRECCIONES_AVENIDA = {"Bv. Artgias": "Bv Artigas"}


def cargar_datos():
    """Lee el CSV en partes porque es muy pesado para cargarlo entero de una
    (mas de 8 millones de filas). Corrige el nombre de avenida mal escrito."""
    partes = []
    for parte in pd.read_csv(RUTA_CSV, usecols=COLUMNAS, chunksize=500_000):
        parte["dsc_avenida"] = parte["dsc_avenida"].replace(CORRECCIONES_AVENIDA)
        partes.append(parte)
    return pd.concat(partes, ignore_index=True)


def filtrar_por_avenida(df, avenida):
    return df[df["dsc_avenida"] == avenida]


def filtrar_por_fecha(df, fecha_desde, fecha_hasta):
    return df[(df["fecha"] >= fecha_desde) & (df["fecha"] <= fecha_hasta)]


def filtrar_por_volumen(df, minimo):
    return df[df["volumen_hora"] >= minimo]


def promedio_vehiculos_por_hora(df):
    """El dataset viene en bloques de 5 minutos (la columna se llama
    volumen_hora pero es el conteo de esos 5 min, no de la hora entera).
    Primero se suman los bloques de cada hora, y despues se promedia
    entre todos los detectores y dias."""
    df = df.copy()
    df["hora_del_dia"] = df["hora"].str.slice(0, 2).astype(int)
    vehiculos_por_hora = (
        df.groupby(["fecha", "hora_del_dia", "cod_detector", "id_carril"])["volumen_hora"]
        .sum()
        .reset_index(name="vehiculos")
    )
    return vehiculos_por_hora.groupby("hora_del_dia")["vehiculos"].mean().round(1)


if __name__ == "__main__":
    datos = cargar_datos()

    # ejemplos de los tres filtros pedidos
    datos_bv_artigas = filtrar_por_avenida(datos, "Bv Artigas")
    datos_primera_semana = filtrar_por_fecha(datos_bv_artigas, "2026-08-01", "2026-08-07")
    datos_con_trafico = filtrar_por_volumen(datos_bv_artigas, 5)

    print(f"Filas totales: {len(datos)}")
    print(f"Filas en Bv Artigas: {len(datos_bv_artigas)}")
    print(f"Filas en Bv Artigas, primera semana de agosto: {len(datos_primera_semana)}")
    print(f"Filas en Bv Artigas con volumen >= 5: {len(datos_con_trafico)}")

    print("\nPromedio de vehiculos por hora en Bv Artigas:")
    promedio = promedio_vehiculos_por_hora(datos_bv_artigas)
    print(promedio)
    print(f"\nPromedio general (todas las horas): {promedio.mean():.1f} vehiculos/hora")
