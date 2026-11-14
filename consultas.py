
import funciones

# ==========================================
# MODULO: CONSULTAS Y FILTROS DE PAISES
# ==========================================

# ------------------------------------------
# BUSCAR PAISES POR NOMBRE
# ------------------------------------------

def buscar_por_nombre(paises, nombre, exacta=False):
    resultados = []

    nombre = nombre.strip().lower()

    if nombre == "":
        print("Error: debe ingresar un nombre.")
        return resultados

    for pais in paises:
        nombre_pais = pais["nombre"].strip().lower()

        if exacta:
            if nombre_pais == nombre:
                resultados.append(pais)
        else:
            if nombre in nombre_pais:
                resultados.append(pais)

    return resultados

# ------------------------------------------
# FILTRAR PAISES POR CONTINENTE
# ------------------------------------------

def filtrar_por_continente(paises, continente):
    resultados = []

    continente = continente.strip().lower()

    if continente == "":
        print("Error: debe ingresar un continente.")
        return resultados

    for pais in paises:
        if pais["continente"].strip().lower() == continente:
            resultados.append(pais)

    return resultados

# ------------------------------------------
# FILTRAR PAISES POR POBLACION
# ------------------------------------------

def filtrar_por_poblacion(paises, minimo, maximo):
    resultados = []

    try:
        minimo = int(minimo)
        maximo = int(maximo)

        if minimo < 0 or maximo < 0:
            print("Error: la poblacion no puede ser negativa.")
            return resultados
        if minimo > maximo:
            print("Error: el minimo no puede ser mayor al maximo.")
            return resultados

    except ValueError:
        print("Error: debe ingresar valores numericos validos.")
        return resultados

    for pais in paises:

        poblacion = int(pais["poblacion"])

        if minimo <= poblacion <= maximo:
            resultados.append(pais)

    return resultados

# ------------------------------------------
# FILTRAR PAISES POR SUPERFICIE
# ------------------------------------------

def filtrar_por_superficie(paises, minimo, maximo):

    resultados = []

    try:
        minimo = float(minimo)
        maximo = float(maximo)

        if minimo < 0 or maximo < 0:
            print("Error: la superficie no puede ser negativa.")
            return resultados

        if minimo > maximo:
            print("Error: el minimo no puede ser mayor al maximo.")
            return resultados

    except ValueError:
        print("Error: debe ingresar valores numericos validos.")
        return resultados

    for pais in paises:

        superficie = float(pais["superficie"])

        if minimo <= superficie <= maximo:
            resultados.append(pais)

    return resultados


# ------------------------------------------
# MOSTRAR RESULTADOS DE LAS CONSULTAS
# ------------------------------------------

def mostrar_resultados(resultados):

    if len(resultados) == 0:

        print("\nNo se encontraron paises con esos criterios.")

    else:

        print("\n========== RESULTADOS ==========")

        for pais in resultados:

            print("-------------------------------")
            print("Nombre:", pais["nombre"])
            print("Continente:", pais["continente"])
            print("Poblacion:", pais["poblacion"])
            print("Superficie:", pais["superficie"])

        print("-------------------------------")
        print("Cantidad de paises encontrados:", len(resultados))


# ------------------------------------------
# MENU DE CONSULTAS
# ------------------------------------------

def menu_consultas(paises):

    opcion = ""

    while opcion != "5":

        print("\n======= CONSULTAS DE PAISES =======")
        print("1. Buscar pais por nombre")
        print("2. Filtrar por continente")
        print("3. Filtrar por poblacion")
        print("4. Filtrar por superficie")
        print("5. Volver al menu principal")

        opcion = funciones.leer_entrada("Seleccione una opcion: ").strip()

        if opcion == "1":

            nombre = funciones.leer_entrada("Ingrese el nombre del pais: ")

            print("\n1. Coincidencia exacta")
            print("2. Coincidencia parcial")

            tipo = funciones.leer_entrada("Seleccione el tipo de busqueda: ").strip()

            if tipo == "1":
                resultados = buscar_por_nombre(paises, nombre, True)

            elif tipo == "2":
                resultados = buscar_por_nombre(paises, nombre, False)

            else:
                print("Error: opcion de busqueda invalida.")
                continue

            mostrar_resultados(resultados)

        elif opcion == "2":

            continente = funciones.leer_entrada("Ingrese el continente: ")

            resultados = filtrar_por_continente(paises, continente)

            mostrar_resultados(resultados)

        elif opcion == "3":

            minimo = funciones.leer_entrada("Ingrese la poblacion minima: ")
            maximo = funciones.leer_entrada("Ingrese la poblacion maxima: ")

            resultados = filtrar_por_poblacion(paises, minimo, maximo)

            mostrar_resultados(resultados)

        elif opcion == "4":

            minimo = funciones.leer_entrada("Ingrese la superficie minima: ")
            maximo = funciones.leer_entrada("Ingrese la superficie maxima: ")

            resultados = filtrar_por_superficie(paises, minimo, maximo)

            mostrar_resultados(resultados)

        elif opcion == "5":

            print("Volviendo al menu principal...")

        else:

            print("Error: debe seleccionar una opcion valida.")
