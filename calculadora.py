
import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import math

def resolver(entrada):
    ecuacion = entrada
    if not ecuacion:
        messagebox.showerror(message="Por favor ingrese una ecuación valida", title="Error en ecuación")
        return 0
    try:
        expr = sp.sympify(ecuacion)
        x = sp.symbols('x')
        if 'x' not in str(expr):
            try:
                expr = eval(ecuacion)
                return expr
            except Exception:
                messagebox.showerror(message="Ecuación ingresada no se puede calcular", title="Error de calculo")
        else:
            #min_x, max_x = map(float, self.entrada_rango.get().split())
            #num_puntos = int(self.entrada_puntos.get())
            x_values = np.linspace(-20, 20, 1000)
            y_values = np.array([expr.subs(x, val) for val in x_values], dtype=float)

            

            #self.historial.append(self.entrada_ecuacion.get())
            return y_values
    except Exception:
        messagebox.showerror(message="Ecuación ingresada no valida", title="Error de ingreso")
