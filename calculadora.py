"""
Autor: Santiago Camargo Molina

Descripcion: Modulo de integracion de funciones en cuanto al analisis sintactico de la expresion de entrada
para identificar funciones especiales como las trigonometricas, logaritmicas, exponeciales y radicales, para 
su respectivo calculo.

En este archivo se describen todas las funciones utilizadas para obtener un resultado final de una expresion
matematica dada, apoyandose en el algoritmo de Shutting Yard para el calculo de las mismas, obedeciendo a la
jerarquia de operadores
"""

#-----IMPORTACION DE MODULOS----
from tkinter import messagebox  # tkinter para el uso de cajas de mensajes
import sympy as sp  # modulo para el analisis matematico de expresiones complejas
import numpy as np  # modulo para el analisis vectorial y matricial
import Proyecto_calcgrf.Pruebas.calculadora as cal
import re   # modulo para el manejo de expresiones regulares


config = {                # CONFIGURACION POR DEFECTO
    'Angulo': ['Grado','Radian'],    # Calculo de un angulo dado en Grado | Radian
    'Formato exponecial': ['Normal','Cientifico'],  # Formato de exponenciales Normal | Cientifico
    'Mostrar Digitos': 3    # Cantidad de digitos decimales a mostrar
}

angulo = config['Angulo'][0]    # Angulo configurado en grados


def entry(entrada):    # ANALIZADOR SINTÁCTICO
    entrada = entrada.lower()   # CONVERSION DE CARACTERES A MINUSCULAS
    if entrada.find("x") == -1: # Si retorna -1, significa que no encontro ninguna x en la cadena
        pass

def resolver(entrada):
    ecuacion = entrada
    if not ecuacion:
        messagebox.showerror(message="Por favor ingrese una ecuación valida", title="Error en ecuación")
        return 'e'
    try:
        expr = sp.sympify(ecuacion)
        sp.evalf
        x = sp.symbols('x')
        if 'x' not in str(expr):
            try:
                expr = eval(ecuacion)
                return expr
            except Exception:
                messagebox.showerror(message="Ecuación ingresada no se puede calcular", title="Error de calculo")
                return 'e'
        else:
            #min_x, max_x = map(float, entrada_rango.get().split())
            #num_puntos = int(entrada_puntos.get())
            x_values = np.linspace(-20, 20, 1000)
            y_values = np.array([expr.subs(x, val) for val in x_values], dtype=float)
            #historial.append(entrada_ecuacion.get())
            return y_values
    except Exception:
        messagebox.showerror(message="Ecuación ingresada no valida", title="Error de ingreso")
        return 'e'

def graficator():
    pass
