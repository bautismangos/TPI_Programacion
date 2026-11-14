"""
Importa los paises de restcountries.com (API v5) a paises.csv.

La API key se lee de .env (RESTCOUNTRIES_API_KEY=...) o de la variable de
entorno RESTCOUNTRIES_API_KEY. Tambien se puede pasar con --api-key.

Uso:
    python importar_paises.py
    python importar_paises.py --todos
    python importar_paises.py --api-key TU_CLAVE --si
"""

import argparse
import json
import os
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import datos


URL_API = "https://api.restcountries.com/countries/v5"
CAMPOS_API = "names,population,area,region,classification.sovereign"

CONTINENTES = {
    "Americas": "América",
    "Europe": "Europa",
    "Asia": "Asia",
    "Africa": "África",
    "Oceania": "Oceanía",
    "Antarctic": "Antártida",
}


def sin_acentos(texto):
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(
        caracter for caracter in normalizado
        if not unicodedata.combining(caracter)
    ).lower()


def nombre_valido(nombre):
    # El menu solo puede editar letras, espacios, guiones, apostrofes,
    # puntos y "&". Si el nombre trae otros signos, no se usa.
    permitidos = " -' .&"
    return bool(nombre) and all(
        caracter.isalpha() or caracter in permitidos for caracter in nombre
    )


def leer_clave():
    clave = os.environ.get("RESTCOUNTRIES_API_KEY")
    if clave:
        return clave.strip()

    ruta = Path(__file__).with_name(".env")
    try:
        lineas = ruta.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return None

    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("export "):
            linea = linea[7:].strip()
        if linea.startswith("RESTCOUNTRIES_API_KEY="):
            return linea.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def pedir_json(url, clave):
    pedido = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {clave}",
            "Accept": "application/json",
            "User-Agent": "TPI-Paises/1.0",
        },
    )

    try:
        with urllib.request.urlopen(pedido, timeout=30) as respuesta:
            datos_json = json.load(respuesta)
    except urllib.error.HTTPError as error:
        detalle = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {detalle[:300]}") from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(f"No se pudo conectar con la API: {error}") from error

    if datos_json.get("errors"):
        mensajes = "; ".join(
            str(error.get("message", error)) for error in datos_json["errors"]
        )
        raise RuntimeError(f"La API devolvio un error: {mensajes}")

    return datos_json


def descargar_paises(clave):
    paises = []
    offset = 0

    while True:
        parametros = {
            "response_fields": CAMPOS_API,
            "limit": 100,
            "offset": offset,
        }
        url = f"{URL_API}?{urllib.parse.urlencode(parametros)}"
        print(f"Descargando paises (offset={offset})...")

        respuesta = pedir_json(url, clave)
        bloque = respuesta.get("data") or {}
        objetos = bloque.get("objects") or []
        meta = bloque.get("meta") or {}

        if not objetos:
            break

        paises.extend(objetos)
        offset += len(objetos)

        total = meta.get("total")
        if isinstance(total, int) and offset >= total:
            break
        if meta.get("more") is False:
            break

    return paises


def convertir_pais(objeto, todos):
    if not todos and (objeto.get("classification") or {}).get("sovereign") is False:
        return None

    nombres = objeto.get("names") or {}
    traduccion = (nombres.get("translations") or {}).get("spa") or {}

    nombre = " ".join((traduccion.get("common") or "").split())
    if not nombre_valido(nombre):
        # Algunas traducciones traen parentesis o comas (por ejemplo
        # "Congo (Rep. Dem.)"). En ese caso se usa el nombre comun.
        nombre = " ".join((nombres.get("common") or "").split())
    if not nombre_valido(nombre):
        return None

    poblacion = objeto.get("population")
    superficie = objeto.get("area")
    if isinstance(superficie, dict):
        superficie = superficie.get("kilometers")

    if not isinstance(poblacion, (int, float)) or poblacion <= 0:
        return None
    if not isinstance(superficie, (int, float)) or superficie <= 0:
        return None

    region = (objeto.get("region") or "").strip()
    continente = CONTINENTES.get(region, region or "Sin dato")

    return {
        "nombre": nombre,
        "poblacion": int(poblacion),
        "superficie": max(1, int(round(superficie))),
        "continente": continente,
    }


def cargar_argumentos():
    analizador = argparse.ArgumentParser(
        description="Importa paises desde restcountries.com a paises.csv."
    )
    analizador.add_argument(
        "--api-key",
        help="API key. Si se omite, se lee de .env o de RESTCOUNTRIES_API_KEY.",
    )
    analizador.add_argument(
        "--todos",
        action="store_true",
        help="Incluye territorios y dependencias (por defecto solo soberanos).",
    )
    analizador.add_argument(
        "--si",
        action="store_true",
        help="Reemplaza paises.csv sin pedir confirmacion.",
    )
    return analizador.parse_args()


def main():
    argumentos = cargar_argumentos()

    clave = (argumentos.api_key or leer_clave() or "").strip()
    if not clave:
        print("Falta la API key.")
        print("Guardala en .env como: RESTCOUNTRIES_API_KEY=TU_CLAVE")
        print("o pasala con --api-key TU_CLAVE.")
        return 1

    try:
        objetos = descargar_paises(clave)
    except (RuntimeError, ValueError, UnicodeError) as error:
        print(f"Error al consultar la API: {error}")
        return 1

    paises = []
    descartados = 0

    for objeto in objetos:
        pais = convertir_pais(objeto, argumentos.todos)
        if pais is None:
            descartados += 1
        else:
            paises.append(pais)

    paises.sort(key=lambda pais: sin_acentos(pais["nombre"]))

    print("\nResumen:")
    print(f"  Recibidos de la API: {len(objetos)}")
    print(f"  Guardados: {len(paises)}")
    print(f"  Descartados: {descartados}")

    if not paises:
        print("No hay datos para guardar.")
        return 1

    if not argumentos.si:
        try:
            respuesta = input(
                f"¿Reemplazar {datos.RUTA_CSV.name} con {len(paises)} paises? [s/N]: "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nImportacion cancelada.")
            return 1

        if respuesta not in ("s", "si", "sí", "y", "yes"):
            print("Importacion cancelada.")
            return 0

    if not datos.guardar_paises(paises):
        print("No se pudo guardar el CSV.")
        return 1

    print(f"\nListo: {datos.RUTA_CSV}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nImportacion cancelada.")
        raise SystemExit(1)
