
import datos
import consultas
import funciones


# ==========================================
# FUNCIONES DEL MENU PRINCIPAL
# ==========================================

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


# ==========================================
# MENU DE ESTADISTICAS
# ==========================================

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


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    # Cargamos los paises guardados en el archivo CSV
    paises = datos.cargar_paises()

    opcion = ""

    while opcion != "6":

        print("\n====================================")
        print("       SISTEMA DE GESTION DE PAISES")
        print("====================================")
        print("1. Agregar un pais")
        print("2. Actualizar un pais")
        print("3. Consultar paises")
        print("4. Ordenar paises")
        print("5. Estadisticas")
        print("6. Salir")
        print("====================================")

        opcion = input("Seleccione una opcion: ").strip()

        match opcion:

            case "1":
                agregar_nuevo_pais(paises)

            case "2":
                modificar_pais(paises)

            case "3":
                consultas.menu_consultas(paises)

            case "4":
                funciones.orden_paises("paises.csv")

            case "5":
                menu_estadisticas()

            case "6":
                print("\nGracias por utilizar el sistema.")

            case _:
                print("Error: debe seleccionar una opcion valida.")


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    menu_principal()
