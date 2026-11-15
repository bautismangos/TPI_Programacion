import csv
import statistics

# Agregar un pais nuevo
def agregar_nuevo_pais(paises):
    print("\n========== AGREGAR PAIS ==========")
    nombre = funciones.pedir_texto(input("Ingrese el nombre del pais: "))
    if nombre is None:
        return

    # Verificamos que el pais no exista
    if funciones.esta_duplicado(nombre, "paises.csv"):
        return

    continente = funciones.pedir_texto(input("Ingrese el continente: "))
    if continente is None:
        return

    # Pedimos la poblacion y verificamos que sea un numero entero positivo
    poblacion = pedir_entero_positivo("Ingrese la poblacion: ")
    if poblacion is None:
        return

    # Pedimos la superficie
    superficie = pedir_entero_positivo("Ingrese la superficie: ")
    if superficie is None:
        return

    # Llamamos a la funcion del modulo datos.py
    datos.agregar_pais(paises, nombre, poblacion, superficie, continente)

# Pedir numeros enteros positivos
def pedir_entero_positivo(mensaje):
    numero = funciones.pedir_numero(input(mensaje))
    if numero is None:
        return None
    if numero <= 0 or not numero.is_integer():
        print("Error: debe ingresar un numero entero mayor a cero.")
        return None
    return int(numero)

# Actualizar los datos de un pais
def modificar_pais(paises):
    print("\n========== ACTUALIZAR PAIS ==========")
    nombre = funciones.pedir_texto(input("Ingrese el nombre del pais que desea modificar: "))
    if nombre is None:
        return
    poblacion = pedir_entero_positivo("Ingrese la nueva poblacion: ")
    if poblacion is None:
        return
    superficie = pedir_entero_positivo("Ingrese la nueva superficie: ")
    if superficie is None:
        return

    # Llamamos a la funcion del modulo datos.py
    datos.actualizar_pais(paises, nombre, poblacion, superficie)

def menu_estadisticas():
    opcion = ""
    while opcion != "6":
        print("\n========== ESTADISTICAS ==========")
        print("1. Pais con mayor y menor poblacion")
        print("2. Promedio de poblacion")
        print("3. Promedio de superficie")
        print("4. Cantidad de paises por continente")
        print("5. Volver al menu principal")
        print("6. Salir de estadisticas")
        opcion = input("Seleccione una opcion: ").strip()
        match opcion:
            case "1":
                funciones.masymenos_poblacion("paises.csv")
            case "2":
                funciones.promedio_poblacion("paises.csv")
            case "3":
                funciones.promedio_superficie("paises.csv")
            case "4":
                funciones.cantidad_continente("paises.csv")
            case "5":
                print("Volviendo al menu principal...")
                break
            case "6":
                print("Saliendo de estadisticas...")
            case _:
                print("Error: seleccione una opcion valida.")

#Explicar uso del replace
def pedir_texto(texto):
    texto = texto.strip()
    if texto == "":
        print("Campo obligatorio")
        return None
    # replace saca los espacios, guiones y apostrofes para que la validacion
    # acepte nombres como 'Republica Dominicana', 'Timor-Leste' o "Cote d'Ivoire"
    elif not texto.replace(" ", "").replace("-", "").replace("'", "").isalpha():
        print("Ingrese solo texto")
        return None
    else:
        print(texto)
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
    if numero < 0:
        print("Ingrese solo numeros positivos")
        return None
    print(numero)
    return numero
#pedir numero verifica si lo puesto es un numero flotante, gracias a replace que permite las comas y puntos 

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
#devuelve falso si el pais no esta duplicado, verifica en el csv si hay algun pais con el mismo nombre

def nombre_az(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            ordenado_az= sorted(filas, key=lambda x: x['nombre'])
            #explicar key lambda
            return ordenado_az
    except FileNotFoundError:
        print("El archivo no existe")
        return []
#esta funcion sirve para los paises de la a-z

def nombre_za(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            ordenado_za= sorted(filas, key=lambda x: x['nombre'],reverse=True)
            #explicar key lambda
            return ordenado_za
    except FileNotFoundError:
        print("El archivo no existe")
        return []
#esta funcion sirve para los paises de la z-a

def poblacion_masmenos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            poblacion_mastomenos= sorted(filas, key=lambda x: float(x['poblacion']), reverse=True)
            #explicar key lambda
            return poblacion_mastomenos
    except FileNotFoundError:
        print("El archivo no existe")
        return []
#esta funcion sirve para la poblacion de mayor a menor 

def poblacion_menosmas(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            poblacion_menostomas= sorted(filas, key=lambda x: float(x['poblacion']))
            #explicar key lambda
            return poblacion_menostomas
    except FileNotFoundError:
        print("El archivo no existe")
        return []
#esta funcion sirve para la poblacion de menor a mayor 

def superficie_masmenos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            superficie_mastomenos= sorted(filas, key=lambda x: float(x['superficie']), reverse=True)
            #explicar key lambda
            return superficie_mastomenos
    except FileNotFoundError:
        print("El archivo no existe")
        return []
#esta funcion sirve para la superficie de mayor a menor 

def superficie_menosmas(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            superficie_menostomas= sorted(filas, key=lambda x: float(x['superficie']))
            #explicar key lambda
            return superficie_menostomas
    except FileNotFoundError:
        print("El archivo no existe")
        return []
#esta funcion sirve para la superficie de menor a mayor 

def orden_paises(archivo):
    while True:
        print("""1.Nombre
            2.Poblacion
            3.Superficie
            4.Volver al menú principal""")
        opcion=input("¿Cual opcion desea elegir? (1-4): ").strip().lower()
        match opcion:
            case "1":
                print("""1.A a la Z
                    2.Z a la A""")
                cual_orden=input("¿Que opcion prefiere? (1/2): ").strip()
                if cual_orden == "1":
                    lista_nombre=nombre_az(archivo)
                    if lista_nombre:
                        print(*[pais["nombre"] for pais in lista_nombre],sep="-")
                    break
                elif cual_orden== "2":
                    lista_nombre=nombre_za(archivo)
                    if lista_nombre:
                        print(*[pais["nombre"] for pais in lista_nombre],sep="-")
                    break
                else:
                    print("Ingrese 1 o 2")
                    continue
            case "2":
                print("""1.Menor a mayor
                    2.Mayor a menor""")
                cual_orden=input("¿Que opcion prefiere? (1/2): ").strip()
                if cual_orden == "1":
                    lista_poblacion=poblacion_menosmas(archivo)
                    if lista_poblacion:
                        print(*[f"{pais['nombre']} ({pais['poblacion']})" for pais in lista_poblacion],sep="-")
                    break
                elif cual_orden== "2":
                    lista_poblacion=poblacion_masmenos(archivo)
                    if lista_poblacion:
                        print(*[f"{pais['nombre']} ({pais['poblacion']})" for pais in lista_poblacion],sep="-")
                    break
                else:
                    print("Ingrese 1 o 2")
                    continue
            case "3":
                print("""1.Menor a mayor
                    2.Mayor a menor""")
                cual_orden=input("¿Que opcion prefiere? (1/2): ").strip()
                if cual_orden == "1":
                    lista_superficie=superficie_menosmas(archivo)
                    if lista_superficie:
                        print(*[f"{pais['nombre']} ({pais['superficie']})" for pais in lista_superficie],sep="-")
                    break
                elif cual_orden== "2":
                    lista_superficie=superficie_masmenos(archivo)
                    if lista_superficie:
                        print(*[f"{pais['nombre']} ({pais['superficie']})" for pais in lista_superficie],sep="-")
                    break
                else:
                    print("Ingrese 1 o 2")
                    continue
            case "4":
                print("Sera enviado al menú principal")
                break
            case  _:
                print("Porfavor ingrese alguna de las opciones dadas entre 1-4")
#esta funcion decidi hacerla asi para que sea en cascada, entonces primero eligen que quieren ordenar y despues en que orden

def masymenos_poblacion(archivo):
    try:
        with open (archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            listas=list(lector)
        if len(listas) == 0:
            print("No hay paises cargados")
            return None
        maxima_p=max(listas, key=lambda fila: float(fila["poblacion"]))
        minima_p=min(listas, key=lambda fila: float(fila["poblacion"]))
        print(f"El pais con mas poblacion es: {maxima_p['nombre']} ({maxima_p['poblacion']})")
        print(f"El pais con menos poblacion es: {minima_p['nombre']} ({minima_p['poblacion']})")
        return maxima_p, minima_p
    except FileNotFoundError:
        print("El archivo no existe")
        return None
#aca se muestra cual es la ciudad con mas habitantes y la que tines menos
def promedio_poblacion(archivo):
    try:
        with open (archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            listas=list(lector)
        if len(listas) == 0:
            print("No hay paises cargados")
            return None
        poblaciones = [float(fila["poblacion"]) for fila in listas]
        media_p = statistics.mean(poblaciones)
        print(f"El promedio de la poblacion es: {media_p:.2f}")
        return media_p
    except FileNotFoundError:
        print("El archivo no existe")
        return None
#calcula y printea el promedio de poblacion mundial
def promedio_superficie(archivo):
    try:
        with open (archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            listas=list(lector)
        if len(listas) == 0:
            print("No hay paises cargados")
            return None
        superficie = [float(fila["superficie"]) for fila in listas]
        media_s = statistics.mean(superficie)
        print(f"El promedio de la superficie es: {media_s:.2f}")
        return media_s
    except FileNotFoundError:
        print("El archivo no existe")
        return None
#calcula y printea el promedio de superficie del territorio mundial
def cantidad_continente(archivo):
    try:
        with open(archivo, "r", encoding="utf-8-sig") as r:
            lector=csv.DictReader(r)
            conteo = {}
            for fila in lector:
                continente = fila.get("continente") or "Sin dato"
                conteo[continente] = conteo.get(continente, 0) + 1
        print("--- CANTIDAD DE PAÍSES POR CONTINENTE ---")
        for continente, cantidad in conteo.items():
            print(f"• {continente}: {cantidad} países")
        return conteo
    except FileNotFoundError:
        print("El archivo no existe")
        return {}
#devuelve cuantos paises hay por continente
