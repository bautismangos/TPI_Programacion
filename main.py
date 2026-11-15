
import datos
import consultas
import funciones

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
