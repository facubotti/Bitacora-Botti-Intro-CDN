# %%
from pathlib import Path
from urllib.request import urlretrieve


URLS = {
    "autoscope_06_2024_volumen.csv":
        "https://ckan-data.montevideo.gub.uy/dataset/a2b2243b-358f-4f03-b7bc-0a32c25ed10c"
        "/resource/90b6b287-bd28-447b-9cd9-fd19d36e4433/download/autoscope_06_2024_volumen.csv",
    "pm_2_5_05_2024_08_2024.csv":
        "https://ckan-data.montevideo.gub.uy/dataset/b9904d06-d466-4a2a-b582-ec01c6700a3c"
        "/resource/26cfdc3e-355f-4315-9d1e-2fc33949a9b9/download/pm_2_5_05_2024_08_2024.csv",
    "no2_05_2024_08_2024.csv":
        "https://ckan-data.montevideo.gub.uy/dataset/bd346fc1-3251-48de-b36a-e57596b250c7"
        "/resource/cd458e42-a2ee-4874-b566-87a53b944ed8/download/no2_05_2024_08_2024.csv",
}


BASE_DIR = Path(__file__).resolve().parent.parent.parent
carpeta_destino = BASE_DIR / "BITACORA" / "Dataset de Datos Abiertos"
carpeta_destino.mkdir(exist_ok=True)

for nombre, url in URLS.items():
    destino = carpeta_destino / nombre
    if destino.exists():
        print(f"Ya existe: {nombre}")
        continue
    print(f"Descargando {nombre}...")
    urlretrieve(url, destino)

print(f"Listo. CSV en: {carpeta_destino}")
