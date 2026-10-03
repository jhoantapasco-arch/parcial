from clases import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio


def limpiarRuta(ruta):
    """Quita espacios y comillas (al copiar la ruta en Windows suele traer comillas)."""
    return ruta.strip().strip('"').strip("'")


def pedirArchivo(sis, tipo, etiqueta):
    """Pide el nombre de un archivo cargado y verifica que exista y sea del tipo correcto."""
    if len(sis.buscarPorTipo(tipo)) == 0:
        print("No hay archivos {} cargados. Use la opcion 1.".format(etiqueta))
        return None

    print("Archivos {} cargados: {}".format(etiqueta, sis.buscarPorTipo(tipo)))
    nombre = input("Ingrese el nombre del archivo {}: ".format(etiqueta)).strip()
    archivo = sis.verArchivo(nombre)

    if archivo is None:
        print("Archivo no encontrado.")
        return None
    if not isinstance(archivo, tipo):
        print("Ese archivo no es de tipo {}.".format(etiqueta))
        return None
    return archivo


def elegirDeLista(lista, mensaje):
    """Muestra una lista numerada y devuelve el elemento elegido por el usuario."""
    for i in range(len(lista)):
        print("{}- {}".format(i, lista[i]))
    return lista[validarRango(input(mensaje), 0, len(lista) - 1)]


def main():
    sis = Sistema()

    while True:
        menu = validarRango(input(
            "\n\t>>>>> MENU PPAL <<<<<\n"
            "1- Ingresar archivo\n"
            "2- Ver informacion CSV\n"
            "3- Graficar CSV por condicion\n"
            "4- Diferencia interhemisferica CSV\n"
            "5- Ver informacion y cargar variable MAT\n"
            "6- Operar 4 canales MAT\n"
            "7- Estadisticos matriz 3D MAT\n"
            "8- Ver archivos cargados\n"
            "9- Salir\n"
            "--> "), 1, 9)

      