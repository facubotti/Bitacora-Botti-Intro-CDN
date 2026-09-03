# %%
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

# Dataset: Conteo vehicular en las principales avenidas de Montevideo (Agosto 2026)
# https://catalogodatos.gub.uy/dataset/conteo-vehicular-en-las-principales-avenidas-de-montevideo
# El archivo pesa mas de 100MB, por eso no se sube al repo (ver .gitignore).
# Correr este script una vez para tener el CSV en la compu.

URL = "https://ckan-data.montevideo.gub.uy/dataset/a2b2243b-358f-4f03-b7bc-0a32c25ed10c/resource/1fd7010a-30a7-4060-a4e3-bfbeb2fb348e/download/conteo_agosto_2026.zip"

# 1. Definir la ruta donde va a quedar el CSV
BASE_DIR = Path.cwd()
carpeta_destino = BASE_DIR / "BITACORA" / "Dataset de Datos Abiertos"
carpeta_destino.mkdir(exist_ok=True)
zip_path = carpeta_destino / "conteo_agosto_2026.zip"

# 2. Descargar el zip
print("Descargando dataset...")
urlretrieve(URL, zip_path)

# 3. Descomprimir y borrar el zip
print("Descomprimiendo...")
with zipfile.ZipFile(zip_path) as z:
    z.extractall(carpeta_destino)
zip_path.unlink()

print(f"Listo. CSV en: {carpeta_destino}")
