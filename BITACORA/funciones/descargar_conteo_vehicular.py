"""
Descarga el dataset "Conteo vehicular en las principales avenidas de Montevideo"
del Catalogo de Datos Abiertos de Uruguay (Agosto 2026).

Fuente: https://catalogodatos.gub.uy/dataset/conteo-vehicular-en-las-principales-avenidas-de-montevideo

El archivo pesa mas de 100MB, por eso no se versiona en el repo (ver .gitignore).
Correr este script para tener el CSV localmente.
"""

import zipfile
from pathlib import Path
from urllib.request import urlretrieve

URL = "https://ckan-data.montevideo.gub.uy/dataset/a2b2243b-358f-4f03-b7bc-0a32c25ed10c/resource/1fd7010a-30a7-4060-a4e3-bfbeb2fb348e/download/conteo_agosto_2026.zip"

CARPETA_DESTINO = Path(__file__).resolve().parent.parent / "Dataset de Datos Abiertos"


def descargar():
    CARPETA_DESTINO.mkdir(exist_ok=True)
    zip_path = CARPETA_DESTINO / "conteo_agosto_2026.zip"

    print("Descargando dataset...")
    urlretrieve(URL, zip_path)

    print("Descomprimiendo...")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(CARPETA_DESTINO)

    zip_path.unlink()
    print(f"Listo. Datos en: {CARPETA_DESTINO}")


if __name__ == "__main__":
    descargar()
