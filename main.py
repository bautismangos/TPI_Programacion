
import datos
import consultas
import funciones



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
        print("6. Salir de estadisticas")

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

            case "6":
                print("Saliendo de estadisticas...")
                return

            case _:
                print("Error: seleccione una opcion valida.")


# ==========================================
# MENU PRINCIPAL
# ==========================================

# Vuelve a leer el CSV para ver los cambios hechos por el importador u otro programa.
# Devuelve False si no se pudo leer, para no seguir operando con datos viejos.
def recargar_paises(paises):

    actuales = datos.cargar_paises()

    if actuales is None:
        return False

    paises.clear()
    paises.extend(actuales)
    return True


def menu_principal():

    # Ruta absoluta al CSV, sin depender del directorio desde donde se ejecuta
    ruta_csv = datos.RUTA_CSV

    paises = []

    while True:

        # Recargamos el archivo en cada vuelta: la API puede haberlo modificado.
        # Si esta corrupto, cerramos para no sobrescribir datos que no pudimos leer.
        if not recargar_paises(paises):
            print("No se puede continuar: revise el archivo de datos.")
            return

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

        opcion = funciones.leer_entrada("Seleccione una opcion: ").strip()

        try:
            match opcion:

                case "1":
                    agregar_nuevo_pais(paises)

                case "2":
                    modificar_pais(paises)

                case "3":
                    consultas.menu_consultas(paises)

                case "4":
                    funciones.orden_paises(ruta_csv)

                case "5":
                    menu_estadisticas(ruta_csv)

                case "6":
                    print("\nGracias por utilizar el sistema.")
                    return

                case _:
                    print("Error: debe seleccionar una opcion valida.")

        except Exception as error:
            # Red de seguridad: un error inesperado no cierra todo el programa
            print(f"Ocurrio un error inesperado: {error}")
            print("Volviendo al menu principal...")


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")
