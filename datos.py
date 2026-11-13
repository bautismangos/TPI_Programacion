import csv

#Carga inicial de paises
def cargar_paises():
    #Lista vacia para cargar paises 
    paises = []

    try:
        #Se abre en modo lectura
        with open("paises.csv", "r", encoding="utf-8-sig") as archivo:
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

# Guardamos la lista de países en el archivo CSV
def guardar_paises(paises):
    try:
        with open("paises.csv", "w", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]

            # Escribimos los nombres de las columnas
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()

            # Guardamos cada país en una fila
            escritor.writerows(paises)

        return True

    except OSError:
        print("Error al guardar los datos.")
        return False

# Agregamos un país nuevo a la lista
def agregar_pais(paises, nombre, poblacion, superficie, continente):

    # Verificamos que no haya campos vacíos
    if not nombre.strip() or not continente.strip():
        print("Error: no puede haber campos vacíos.")
        return False

    try:
        poblacion = int(poblacion)
        superficie = int(superficie)
    except ValueError:
        print("Error: población y superficie deben ser números.")
        return False

    # Verificamos que los valores sean positivos
    if poblacion <= 0 or superficie <= 0:
        print("Error: los valores deben ser mayores a cero.")
        return False

    # Evitamos agregar países con nombres repetidos
    for pais in paises:
        if pais["nombre"].lower() == nombre.strip().lower():
            print("Ese país ya existe.")
            return False

    # Creamos el diccionario con los datos del país
    pais = {
        "nombre": nombre.strip(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente.strip()
    }

    paises.append(pais)

    # Guardamos los cambios en el CSV
    if guardar_paises(paises):
        print("País agregado correctamente.")
        return True

    return False


# Actualizamos la población y superficie de un país
def actualizar_pais(paises, nombre, poblacion, superficie):

    # Recorremos la lista buscando el país que se desea modificar
    for pais in paises:

        # Comparamos los nombres sin distinguir mayúsculas y minúsculas
        if pais["nombre"].lower() == nombre.strip().lower():

            try:
                # Convertimos los nuevos valores a números enteros
                poblacion = int(poblacion)
                superficie = int(superficie)

                # Comprobamos que los valores sean positivos
                if poblacion <= 0 or superficie <= 0:
                    print("Los valores deben ser mayores a cero.")
                    return False

                # Guardamos temporalmente los valores anteriores
                poblacion_anterior = pais["poblacion"]
                superficie_anterior = pais["superficie"]

                # Modificamos los datos del país encontrado
                pais["poblacion"] = poblacion
                pais["superficie"] = superficie

                # Guardamos los cambios en el archivo CSV
                if guardar_paises(paises):
                    print("País actualizado correctamente.")
                    return True

                # Si falla el guardado, recuperamos los datos anteriores
                pais["poblacion"] = poblacion_anterior
                pais["superficie"] = superficie_anterior
                return False

            except ValueError:
                # Informamos si se ingresaron valores incorrectos
                print("Error: debe ingresar números válidos.")
                return False

    # Se ejecuta si termina la búsqueda y no encuentra el país
    print("No se encontró el país.")
    return False

