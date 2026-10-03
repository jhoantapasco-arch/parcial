import io
import os
import re

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio

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

    # ---------- informacion ----------
    def __str__(self):
        buffer = io.StringIO()
        self.__tabla.info(buf=buffer)                 # info() escribe en el buffer
        return ("\n===== INFORMACION DEL ARCHIVO CSV =====\n"
                "Archivo: {}\n"
                "{}\n"
                "===== ESTADISTICOS (describe) =====\n"
                "{}\n\n"
                "Condiciones: {}\n"
                "Canales disponibles: {}".format(
                    self.__ruta,
                    buffer.getvalue(),
                    self.__tabla.describe().to_string(),
                    self.verCondiciones(),
                    self.verCanales()))

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


class ArchivoMAT:
    def __init__(self, ruta):
        self.__ruta = ruta
        self.__datos = sio.loadmat(ruta)
        self.__variables = sio.whosmat(ruta)
        self.__llaves = list(self.__datos.keys())
        self.__matriz = None
        self.__nombreVar = None

    def __str__(self):
        ancho = max([len(v[0]) for v in self.__variables] + [8])
        linea = "-" * (ancho + 44)
        texto = "\n===== VARIABLES DEL ARCHIVO MAT =====\n"
        texto += "Archivo: {}\n".format(self.__ruta)
        texto += linea + "\n"
        texto += "{:<4}{:<{w}}  {:<18}{}\n".format("N°", "Variable", "Dimensiones", "Tipo", w=ancho)
        texto += linea + "\n"
        for i, v in enumerate(self.__variables):
            texto += "{:<4}{:<{w}}  {:<18}{}\n".format(i, v[0], str(v[1]), v[2], w=ancho)
        texto += linea + "\n"
        texto += "Llaves del diccionario: {}".format(self.__llaves)
        return texto

    def verLlaves(self):
        return self.__llaves

    def verVariables(self):
        return self.__variables

    def cargarMatriz(self, numero):
        nombre = self.__variables[numero][0]
        matriz = self.__datos[nombre]
        if not isinstance(matriz, np.ndarray) or not np.issubdtype(matriz.dtype, np.number):
            raise ValueError("La variable '{}' no es una matriz numerica.".format(nombre))
        self.__matriz = matriz
        self.__nombreVar = nombre
        return self.__matriz

    def verMatriz(self):
        return self.__matriz

    def verNombreVariable(self):
        return self.__nombreVar

class Sistema:
    def __init__(self):
        self.__archivos = {}

    def ingresarArchivo(self, nombre, archivo):
        self.__archivos[nombre] = archivo

    def verArchivo(self, nombre):
        return self.__archivos.get(nombre, None)

    def verArchivos(self):
        return self.__archivos

    def buscarPorTipo(self, tipo):
        """Devuelve los nombres de los archivos que son de la clase indicada."""
        return [n for n, a in self.__archivos.items() if isinstance(a, tipo)]

