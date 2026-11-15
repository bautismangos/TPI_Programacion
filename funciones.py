import csv
import math
import statistics
import datos

# Pide un texto obligatorio y repite hasta que sea valido.
# Devuelve None si el usuario deja el campo vacio (cancela la operacion).
def pedir_texto_obligatorio(mensaje):

    while True:

        entrada = funciones.leer_entrada(mensaje)

        if entrada.strip() == "":
            print("Operacion cancelada.")
            return None

        texto = funciones.pedir_texto(entrada)

        if texto is not None:
            return texto


# Pide un numero entero positivo y repite hasta que sea valido.
# Devuelve None si el usuario deja el campo vacio (cancela la operacion).
def pedir_entero_positivo(mensaje):

    while True:

        entrada = funciones.leer_entrada(mensaje).strip()

        if entrada == "":
            print("Operacion cancelada.")
            return None

        # Solo digitos: evita que se acepten valores como "1.5", "1e3", "nan" o "inf"
        if not (entrada.isascii() and entrada.isdigit()):
            print("Error: debe ingresar un numero entero mayor a cero.")
            continue

        numero = int(entrada)

        if numero <= 0:
            print("Error: debe ingresar un numero entero mayor a cero.")
            continue

        return numero


# ==========================================
# FUNCIONES DEL MENU PRINCIPAL
# ==========================================

# Agregar un pais nuevo
def agregar_nuevo_pais(paises):

    print("\n========== AGREGAR PAIS ==========")

    nombre = pedir_texto_obligatorio("Ingrese el nombre del pais: ")

    if nombre is None:
        return

    # Verificamos sobre la lista en memoria (unica fuente de verdad)
    if datos.buscar_pais(paises, nombre) is not None:
        print("Ese pais ya existe.")
        return

    continente = pedir_texto_obligatorio("Ingrese el continente: ")

    if continente is None:
        return

    poblacion = pedir_entero_positivo("Ingrese la poblacion: ")

    if poblacion is None:
        return

    superficie = pedir_entero_positivo("Ingrese la superficie: ")

    if superficie is None:
        return

    # Llamamos a la funcion del modulo datos.py y controlamos el resultado
    if not datos.agregar_pais(paises, nombre, poblacion, superficie, continente):
        print("No se pudo agregar el pais.")


# Actualizar los datos de un pais
def modificar_pais(paises):

    print("\n========== ACTUALIZAR PAIS ==========")

    nombre = pedir_texto_obligatorio("Ingrese el nombre del pais que desea modificar: ")

    if nombre is None:
        return

    # Verificamos que el pais exista antes de pedir los nuevos datos
    if datos.buscar_pais(paises, nombre) is None:
        print("No se encontro el pais.")
        return

    poblacion = pedir_entero_positivo("Ingrese la nueva poblacion: ")

    if poblacion is None:
        return

    superficie = pedir_entero_positivo("Ingrese la nueva superficie: ")

    if superficie is None:
        return

    # Llamamos a la funcion del modulo datos.py y controlamos el resultado
    if not datos.actualizar_pais(paises, nombre, poblacion, superficie):
        print("No se pudo actualizar el pais.")


# ==========================================
# MENU DE ESTADISTICAS
# ==========================================

def menu_estadisticas(ruta_csv):

    while True:

        print("\n========== ESTADISTICAS ==========")
        print("1. Pais con mayor y menor poblacion")
        print("2. Promedio de poblacion")
        print("3. Promedio de superficie")
        print("4. Cantidad de paises por continente")
        print("5. Volver al menu principal")

        opcion = funciones.leer_entrada("Seleccione una opcion: ").strip()

        match opcion:

            case "1":
                funciones.masymenos_poblacion(ruta_csv)

            case "2":
                funciones.promedio_poblacion(ruta_csv)

            case "3":
                funciones.promedio_superficie(ruta_csv)

            case "4":
                funciones.cantidad_continente(ruta_csv)

            case "5":
                print("Volviendo al menu principal...")
                return

            case _:
                print("Error: seleccione una opcion valida.")

def leer_entrada(mensaje):
    # Pide un dato por teclado y corta el programa de forma ordenada si se interrumpe.
    # Evita que un Ctrl+C o un fin de entrada (EOF) terminen con un traceback.
    try:
        return input(mensaje)
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada interrumpida. Saliendo del programa...")
        raise SystemExit(0)


def pedir_texto(texto):
    texto = texto.strip()
    if texto == "":
        print("Campo obligatorio")
        return None
    # replace saca los espacios, guiones, apostrofes, puntos y "&" para que la
    # validacion acepte nombres reales como 'Republica Dominicana',
    # 'Timor-Leste', "Cote d'Ivoire" o 'U.S. Virgin Islands'
    elif not (
        texto
        .replace(" ", "")
        .replace("-", "")
        .replace("'", "")
        .replace(".", "")
        .replace("&", "")
        .isalpha()
    ):
        print("Ingrese solo texto")
        return None
    else:
        return texto
#pedir texto sirve para verificar si lo puesto es un texto, con la funcion replace permite poner nombres como 'Republica Dominicana'


def pedir_numero(entrada):
    entrada = str(entrada).strip()
    if entrada == "":
        print("Campo obligatorio")
        return None
    try:
        # replace permite escribir el numero con coma o con punto (3,5 o 3.5)
        numero = float(entrada.replace(",", "."))
    except ValueError:
        print("Ingrese solo numeros")
        return None
    # float() tambien acepta "nan" e "inf": los rechazamos
    if not math.isfinite(numero):
        print("Ingrese un numero valido")
        return None
    if numero < 0:
        print("Ingrese solo numeros positivos")
        return None
    return numero
#pedir numero verifica si lo puesto es un numero flotante, gracias a replace que permite las comas y puntos


# Lee el CSV y devuelve una lista de filas, o None si no se puede leer
def leer_filas(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector = csv.DictReader(r)
            campos = lector.fieldnames or []
            columnas = ("nombre", "poblacion", "superficie", "continente")

            if any(columna not in campos for columna in columnas):
                print("Error: el archivo CSV no tiene las columnas esperadas")
                return None

            return list(lector)
    except FileNotFoundError:
        print("El archivo no existe")
        return None
    except (OSError, csv.Error, UnicodeError):
        print("Error al leer el archivo")
        return None


def esta_duplicado(pais, archivo):
    # se compara sin espacios y sin importar mayusculas o minusculas
    pais = pais.strip().lower()
    try:
        with open (archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            for fila in lector:
                nombre = (fila.get("nombre") or "").strip().lower()
                if nombre == pais:
                    print("Pais duplicado")
                    return True
            return False
    except FileNotFoundError:
        print("El archivo no existe")
        return False
    except (OSError, csv.Error, UnicodeError):
        print("Error al leer el archivo")
        return False
#devuelve falso si el pais no esta duplicado, verifica en el csv si hay algun pais con el mismo nombre


def nombre_az(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return []
    try:
        ordenado_az = sorted(filas, key=lambda x: x['nombre'])
        #explicar key lambda
        return ordenado_az
    except (KeyError, TypeError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return []
#esta funcion sirve para los paises de la a-z


def nombre_za(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return []
    try:
        ordenado_za = sorted(filas, key=lambda x: x['nombre'], reverse=True)
        #explicar key lambda
        return ordenado_za
    except (KeyError, TypeError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return []
#esta funcion sirve para los paises de la z-a


def poblacion_masmenos(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return []
    try:
        poblacion_mastomenos = sorted(filas, key=lambda x: float(x['poblacion']), reverse=True)
        #explicar key lambda
        return poblacion_mastomenos
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return []
#esta funcion sirve para la poblacion de mayor a menor


def poblacion_menosmas(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return []
    try:
        poblacion_menostomas = sorted(filas, key=lambda x: float(x['poblacion']))
        #explicar key lambda
        return poblacion_menostomas
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return []
#esta funcion sirve para la poblacion de menor a mayor


def superficie_masmenos(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return []
    try:
        superficie_mastomenos = sorted(filas, key=lambda x: float(x['superficie']), reverse=True)
        #explicar key lambda
        return superficie_mastomenos
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return []
#esta funcion sirve para la superficie de mayor a menor


def superficie_menosmas(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return []
    try:
        superficie_menostomas = sorted(filas, key=lambda x: float(x['superficie']))
        #explicar key lambda
        return superficie_menostomas
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return []
#esta funcion sirve para la superficie de menor a mayor


def orden_paises(archivo):
    while True:
        print("1. Nombre")
        print("2. Poblacion")
        print("3. Superficie")
        print("4. Volver al menu principal")
        opcion = leer_entrada("¿Cual opcion desea elegir? (1-4): ").strip().lower()
        match opcion:
            case "1":
                print("1. A a la Z")
                print("2. Z a la A")
                cual_orden = leer_entrada("¿Que opcion prefiere? (1/2): ").strip()
                if cual_orden == "1":
                    lista_nombre = nombre_az(archivo)
                    if lista_nombre:
                        print(*[pais["nombre"] for pais in lista_nombre], sep="-")
                    break
                elif cual_orden == "2":
                    lista_nombre = nombre_za(archivo)
                    if lista_nombre:
                        print(*[pais["nombre"] for pais in lista_nombre], sep="-")
                    break
                else:
                    print("Ingrese 1 o 2")
                    continue
            case "2":
                print("1. Menor a mayor")
                print("2. Mayor a menor")
                cual_orden = leer_entrada("¿Que opcion prefiere? (1/2): ").strip()
                if cual_orden == "1":
                    lista_poblacion = poblacion_menosmas(archivo)
                    if lista_poblacion:
                        print(*[f"{pais['nombre']} ({pais['poblacion']})" for pais in lista_poblacion], sep="-")
                    break
                elif cual_orden == "2":
                    lista_poblacion = poblacion_masmenos(archivo)
                    if lista_poblacion:
                        print(*[f"{pais['nombre']} ({pais['poblacion']})" for pais in lista_poblacion], sep="-")
                    break
                else:
                    print("Ingrese 1 o 2")
                    continue
            case "3":
                print("1. Menor a mayor")
                print("2. Mayor a menor")
                cual_orden = leer_entrada("¿Que opcion prefiere? (1/2): ").strip()
                if cual_orden == "1":
                    lista_superficie = superficie_menosmas(archivo)
                    if lista_superficie:
                        print(*[f"{pais['nombre']} ({pais['superficie']})" for pais in lista_superficie], sep="-")
                    break
                elif cual_orden == "2":
                    lista_superficie = superficie_masmenos(archivo)
                    if lista_superficie:
                        print(*[f"{pais['nombre']} ({pais['superficie']})" for pais in lista_superficie], sep="-")
                    break
                else:
                    print("Ingrese 1 o 2")
                    continue
            case "4":
                print("Volviendo al menu principal...")
                break
            case _:
                print("Por favor, ingrese una opcion entre 1 y 4.")
#esta funcion decidi hacerla asi para que sea en cascada, entonces primero eligen que quieren ordenar y despues en que orden


def masymenos_poblacion(archivo):
    listas = leer_filas(archivo)
    if listas is None:
        return None
    if len(listas) == 0:
        print("No hay paises cargados")
        return None
    try:
        maxima_p = max(listas, key=lambda fila: float(fila["poblacion"]))
        minima_p = min(listas, key=lambda fila: float(fila["poblacion"]))
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return None
    print(f"El pais con mas poblacion es: {maxima_p['nombre']} ({maxima_p['poblacion']})")
    print(f"El pais con menos poblacion es: {minima_p['nombre']} ({minima_p['poblacion']})")
    return maxima_p, minima_p
#aca se muestra cual es el pais con mas habitantes y el que tiene menos


def promedio_poblacion(archivo):
    listas = leer_filas(archivo)
    if listas is None:
        return None
    if len(listas) == 0:
        print("No hay paises cargados")
        return None
    try:
        poblaciones = [float(fila["poblacion"]) for fila in listas]
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return None
    media_p = statistics.mean(poblaciones)
    print(f"El promedio de la poblacion es: {media_p:.2f}")
    return media_p
#calcula y printea el promedio de poblacion mundial


def promedio_superficie(archivo):
    listas = leer_filas(archivo)
    if listas is None:
        return None
    if len(listas) == 0:
        print("No hay paises cargados")
        return None
    try:
        superficie = [float(fila["superficie"]) for fila in listas]
    except (KeyError, TypeError, ValueError):
        print("Error: el archivo CSV tiene datos incorrectos")
        return None
    media_s = statistics.mean(superficie)
    print(f"El promedio de la superficie es: {media_s:.2f}")
    return media_s
#calcula y printea el promedio de superficie del territorio mundial


def cantidad_continente(archivo):
    filas = leer_filas(archivo)
    if filas is None:
        return {}

    conteo = {}
    for fila in filas:
        continente = (fila.get("continente") or "Sin dato").strip() or "Sin dato"
        conteo[continente] = conteo.get(continente, 0) + 1

    print("--- CANTIDAD DE PAISES POR CONTINENTE ---")
    for continente, cantidad in conteo.items():
        print(f"• {continente}: {cantidad} paises")
    return conteo
#devuelve cuantos paises hay por continente
