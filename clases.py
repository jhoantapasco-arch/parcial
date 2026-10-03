import os
import re

import matplotlib.pyplot as plt

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
