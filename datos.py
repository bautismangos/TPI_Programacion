import csv


def cargar_paises():
    #Lista vacia para cargar paises 
    paises = []

    try:
        #Se abre en modo lectura
        with open("paises.csv", "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                #Guarda los datos de los paises en un diccionario
                pais = {
                    "nombre": fila["nombre"],
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"]
                }

                paises.append(pais)
    #Previene errores
    except FileNotFoundError:
        print("No se encontro el archivo paises.csv")

    except (ValueError, KeyError):
        print("Error: el archivo CSV tiene datos incorrectos")
    #Devuelve la lista con todos los datos de los paises guardados
    return paises
