import csv
import os
import shutil
from pathlib import Path


# Ruta absoluta al CSV: no depende del directorio desde donde se ejecuta el programa
RUTA_CSV = Path(__file__).resolve().parent / "paises.csv"

# Columnas que debe tener el archivo
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


# Carga inicial de paises
def cargar_paises():
    # Lista vacia para cargar paises
    paises = []

    try:
        # Se abre en modo lectura
        with open(RUTA_CSV, "r", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)

            # Verificamos que el archivo tenga todas las columnas necesarias
            campos_archivo = lector.fieldnames or []
            faltantes = [campo for campo in CAMPOS if campo not in campos_archivo]

            if faltantes:
                print(f"Error: al archivo CSV le faltan las columnas: {', '.join(faltantes)}")
                return None

            for numero_fila, fila in enumerate(lector, start=2):
                # Guarda los datos de los paises en un diccionario
                nombre = (fila.get("nombre") or "").strip()
                continente = (fila.get("continente") or "").strip()

                try:
                    poblacion = int(fila["poblacion"])
                    superficie = int(fila["superficie"])
                except (TypeError, ValueError):
                    print(f"Error: la fila {numero_fila} del CSV tiene numeros invalidos.")
                    return None

                if not nombre:
                    print(f"Error: la fila {numero_fila} del CSV no tiene nombre.")
                    return None

                pais = {
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente
                }

                paises.append(pais)

    # El archivo no existe: se empieza con la lista vacia y se crea al guardar
    except FileNotFoundError:
        print(f"No se encontro {RUTA_CSV.name}. Se creara al agregar el primer pais.")
        return []

    # Cualquier otro problema de lectura se informa y se corta la carga
    except (OSError, csv.Error, UnicodeError) as error:
        print(f"Error al leer el archivo CSV: {error}")
        return None

    # Devuelve la lista con todos los datos de los paises guardados
    return paises


# Guardamos la lista de paises en el archivo CSV
def guardar_paises(paises):

    # Escribimos primero en un archivo temporal y despues lo reemplazamos.
    # Asi, si el programa falla a mitad del guardado, el CSV original queda intacto.
    archivo_temporal = Path(str(RUTA_CSV) + ".tmp")

    try:
        with open(archivo_temporal, "w", newline="", encoding="utf-8") as archivo:

            # Escribimos los nombres de las columnas
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()

            # Guardamos cada pais en una fila
            escritor.writerows(paises)

        # Copia de seguridad del archivo anterior antes de reemplazarlo
        if RUTA_CSV.exists():
            shutil.copy2(RUTA_CSV, str(RUTA_CSV) + ".bak")

        # os.replace es atomico: reemplaza el archivo viejo por el nuevo
        os.replace(archivo_temporal, RUTA_CSV)

        return True

    except OSError as error:
        print(f"Error al guardar los datos: {error}")

        # Borramos el archivo temporal incompleto, si quedo
        if archivo_temporal.exists():
            try:
                archivo_temporal.unlink()
            except OSError:
                pass

        return False


# Busca un pais por nombre sin distinguir mayusculas ni minusculas.
# Devuelve el diccionario del pais o None si no existe.
def buscar_pais(paises, nombre):

    if nombre is None:
        return None

    nombre = nombre.strip().lower()

    for pais in paises:
        if pais["nombre"].strip().lower() == nombre:
            return pais

    return None


# Agregamos un pais nuevo a la lista
def agregar_pais(paises, nombre, poblacion, superficie, continente):

    # Verificamos que no haya campos vacios
    if nombre is None or continente is None:
        print("Error: no puede haber campos vacios.")
        return False

    if not nombre.strip() or not continente.strip():
        print("Error: no puede haber campos vacios.")
        return False

    try:
        poblacion = int(poblacion)
        superficie = int(superficie)
    except (TypeError, ValueError):
        print("Error: poblacion y superficie deben ser numeros.")
        return False

    # Verificamos que los valores sean positivos
    if poblacion <= 0 or superficie <= 0:
        print("Error: los valores deben ser mayores a cero.")
        return False

    # Evitamos agregar paises con nombres repetidos
    if buscar_pais(paises, nombre) is not None:
        print("Ese pais ya existe.")
        return False

    # Creamos el diccionario con los datos del pais
    pais = {
        "nombre": nombre.strip(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente.strip()
    }

    paises.append(pais)

    # Guardamos los cambios en el CSV
    if guardar_paises(paises):
        print("Pais agregado correctamente.")
        return True

    # Si no se pudo guardar, deshacemos el cambio en memoria
    paises.remove(pais)
    print("No se pudo guardar el pais en el archivo.")
    return False


# Actualizamos la poblacion y superficie de un pais.
# Si se recibe "continente", tambien se actualiza ese campo.
def actualizar_pais(paises, nombre, poblacion, superficie, continente=None):

    # Buscamos el pais que se desea modificar
    pais = buscar_pais(paises, nombre)

    if pais is None:
        print("No se encontro el pais.")
        return False

    try:
        # Convertimos los nuevos valores a numeros enteros
        poblacion = int(poblacion)
        superficie = int(superficie)
    except (TypeError, ValueError):
        # Informamos si se ingresaron valores incorrectos
        print("Error: debe ingresar numeros validos.")
        return False

    # Comprobamos que los valores sean positivos
    if poblacion <= 0 or superficie <= 0:
        print("Los valores deben ser mayores a cero.")
        return False

    # Si se recibe un continente, validamos que no este vacio
    if continente is not None:
        continente = continente.strip()
        if not continente:
            print("Error: el continente no puede estar vacio.")
            return False

    # Guardamos temporalmente los valores anteriores
    poblacion_anterior = pais["poblacion"]
    superficie_anterior = pais["superficie"]
    continente_anterior = pais["continente"]

    # Modificamos los datos del pais encontrado
    pais["poblacion"] = poblacion
    pais["superficie"] = superficie

    if continente is not None:
        pais["continente"] = continente

    # Guardamos los cambios en el archivo CSV
    if guardar_paises(paises):
        print("Pais actualizado correctamente.")
        return True

    # Si falla el guardado, recuperamos los datos anteriores
    pais["poblacion"] = poblacion_anterior
    pais["superficie"] = superficie_anterior
    pais["continente"] = continente_anterior
    print("No se pudo guardar la actualizacion.")
    return False


# Eliminamos un pais de la lista y del archivo CSV
def eliminar_pais(paises, nombre):

    pais = buscar_pais(paises, nombre)

    if pais is None:
        print("No se encontro el pais.")
        return False

    # Guardamos la posicion para poder restaurar el pais si falla el guardado
    indice = paises.index(pais)
    paises.pop(indice)

    if guardar_paises(paises):
        print("Pais eliminado correctamente.")
        return True

    # Si falla el guardado, volvemos a insertar el pais en su lugar
    paises.insert(indice, pais)
    print("No se pudo guardar la eliminacion.")
    return False
