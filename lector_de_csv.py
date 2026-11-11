
import csv
import os
from consultas import menu_consultas


# Leer los datos del archivo CSV
def cargar_paises():

    paises = []

    try:
        ruta = os.path.join(os.path.dirname(__file__), "paises.csv")
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:

            lector = csv.DictReader(archivo)

            columnas = ["nombre", "continente", "poblacion", "superficie"]

            # Comprobar que existan las columnas necesarias
            if lector.fieldnames is None or not all(columna in lector.fieldnames for columna in columnas):
                print("Error: el CSV no tiene las columnas necesarias.")
                return paises

            for fila in lector:

                try:
                    # Comprobar que no haya campos vacios
                    if any(fila[columna] is None or fila[columna].strip() == "" for columna in columnas):
                        print("Se omitio una fila porque contiene campos vacios.")
                        continue

                    # Convertir los datos numericos
                    fila["poblacion"] = int(fila["poblacion"])
                    fila["superficie"] = float(fila["superficie"])

                    if fila["poblacion"] < 0 or fila["superficie"] < 0:
                        print("Se omitio un pais con valores negativos.")
                        continue

                    paises.append(fila)

                except ValueError:
                    print("Se omitio una fila por tener datos numericos incorrectos.")

        print("Paises cargados correctamente:", len(paises))

    except FileNotFoundError:
        print("Error: no se encontro el archivo paises.csv.")

    except OSError:
        print("Error al intentar leer el archivo CSV.")

    return paises


# Programa principal de prueba
paises = cargar_paises()

if len(paises) > 0:
    menu_consultas(paises)
else:
    print("No hay paises disponibles para realizar consultas.")
