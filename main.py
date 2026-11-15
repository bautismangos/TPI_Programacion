
import datos
import consultas
import funciones

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
                    funciones.agregar_nuevo_pais(paises)

                case "2":
                    funciones.modificar_pais(paises)

                case "3":
                    consultas.menu_consultas(paises)

                case "4":
                    funciones.orden_paises(ruta_csv)

                case "5":
                    funciones.menu_estadisticas(ruta_csv)

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
