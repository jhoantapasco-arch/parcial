import os
import re

import matplotlib.pyplot as plt
import pandas as pd

plt.ion()

CARPETA = "graficos"        # carpeta donde se guardan las imagenes



def validarEntero(t):
    while True:
        try:
            return int(t)
        except (ValueError, TypeError):
            t = input("Ingrese un numero entero: ")


def validarRango(t, minimo, maximo):
    t = validarEntero(t)
    while t < minimo or t > maximo:
        t = validarEntero(input("Ingrese un valor entre {} y {}: ".format(minimo, maximo)))
    return t


def nombreSeguro(texto):
    """Deja solo letras, numeros, guion y guion bajo para usar en nombres de archivo."""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(texto)).strip("_")


def guardarFigura(nombre):
    """Guarda la figura activa (png) dentro de CARPETA y devuelve la ruta."""
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, nombre)
    plt.savefig(ruta, dpi=150)
    return ruta


class ArchivoCSV:
    def __init__(self, ruta):
        self.__ruta = ruta
        self.__tiempo = "Tiempo"
        self.__condicion = "Condición"
        tabla = pd.read_csv(ruta, sep=None, engine="python")
        # En los archivos del parcial las columnas se llaman time_ms y condition
        tabla = tabla.rename(columns={"time_ms": self.__tiempo, "condition": self.__condicion})

        # El tiempo pasa a ser el indice de las filas
        self.__tabla = tabla.set_index(self.__tiempo)
        self.__columnas = self.__tabla.columns

    def verTabla(self):
        return self.__tabla

    def verCol(self):
        return self.__tabla.columns

    def verCondiciones(self):
        return self.__tabla[self.__condicion].unique().tolist()

    def verCanales(self):
        """Columnas del CSV que son canales (sin la condicion ni el sujeto)."""
        canales = []
        for c in self.__tabla.columns:
            if c != self.__condicion and c != "subject":
                canales.append(c)
        return canales
