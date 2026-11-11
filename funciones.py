import csv
#Explicar uso del replace

def pedir_texto(texto):
    if texto == "":
        print("Campo obligatorio")
        return None
    elif not texto.replace(" ", "").isalpha():
        print("Ingrese solo texto")
        return None
    else:
        print(texto)
        return str(texto)
#pedir texto sirve para verificar si lo puesto es un texto, con la funcion replace permite poner nombres como 'Republica Dominicana'

def pedir_numero(entrada):
    try:
        if entrada=="":
            print("Campo obligatorio")
            return None
        numero=float(entrada.replace( ",", "."))
        print(numero)
    except ValueError:
        print("Ingrese solo numeros positivos")
        return None
#pedir numero verifica si lo puesto es un numero flotante, gracias a replace que permite las comas y puntos 

def esta_duplicado(pais, archivo,):
    try:
        with open (archivo, "r", encoding="utf-8") as r:
            lector=csv.DictReader(r)
            filas=list(lector)
            for fila in filas:
                if fila.get("paises") == pais:
                    #hay que cambair lo que va dentro de las comillas si ponen otro nombre en la cabecera de los paises 
                    print("Pais duplicado")
                    return True
    except FileNotFoundError:
        print("El archivo no existe")
    else:
        print("El pais no se encuntra en el archivo ")
        return False
#devuelve falso si el pais no esta duplicado, verifica en el csv si hay algun pais con el mismo nombre
