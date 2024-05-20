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
import Proyecto_calcgrf.libraries.calculadora as cal
import re   # modulo para el manejo de expresiones regulares


config = {                # CONFIGURACION POR DEFECTO
    'Angulo': ['Grado','Radian'],    # Calculo de un angulo dado en Grado | Radian
    'Formato exponecial': ['Normal','Cientifico'],  # Formato de exponenciales Normal | Cientifico
    'Mostrar Digitos': 3    # Cantidad de digitos decimales a mostrar
}

angulo = config['Angulo'][0]    # Angulo configurado en grados

numeros = ['0','1','2','3','4','5','6','7','8','9']
funciones = ['sin(','cos(','tan(','ln(','log(x,b)','root(x,i)','abs(','e','\u03C0']
signos = ['+','-','/','*','^']

def entry(entr, tecla):    # ANALIZADOR DE SINTAXIS
    if entr:    # PREGUNTAMOS SI LA CADENA NO ESTA VACIA
        ind = len(entr) # OBTENEMOS EL TAMAÑO DE LA CADENA DE ENTRADA
        if tecla in numeros:    # SI EL CARACTER ENTRANTE ES UN NUMERO, ENTONCES...
            return ind, tecla   # RETORNAMOS EL INDICE Y EL CARACTER SE QUE POSICIONARA
        elif tecla in funciones:    # SI EL CARACTER ENTRANTE ES UNA FUNCION, ENTONCES...
            if entr[ind-1] in signos:   # PREGUNTAMOS SI ANTERIORMENTE EXISTE UN SIGNO 
                return ind, tecla       # SI EXISTE, ENTONCES SOLO SE RETORNA INDICE Y EL CARACTER (+ sin(45))
            else:                       
                return ind, '*' + tecla  # SI NO, ENTONCES SE RETORNA EL INDICE Y "* + EL CARACTER"  (* sin(45))
        elif tecla in signos:   # SI EL CARACTER ENTRANTE ES UN SIGNO, ENTONCES...
            if entr[ind-1] in signos:   # PREGUNTAMOS SI ANTERIORMENTE EXISTE UN SIGNO
                return ind-1, tecla     # SI EXISTE, ENTONCES REEMPLAZAMOS ESE SIGNO POR EL NUEVO QUE INGRESA
            else:
                return ind, tecla       # SI NO, ENTONCES SOLO SE RETORNA INDICE Y EL CARACTER
        elif tecla=='.':    # SI EL CARACTER ES '.', ENTONCES...
            if entr[ind-1] in numeros:  # PREGUNTAMOS SI HAY NUMEROS ANTERIORMENTE
                return ind, tecla   # SI EXISTE, ENTONCES SOLO SE RETRONA INDICE Y EL CARACTER (1.)
            else:                   
                return ind, '*0.'   # SI NO, ENTONCES SE RETRONA INDICE Y SE AGREGA '*0' AL CARACTER (*0.)
        else:
            return ind, tecla
    elif tecla in ['/','*','^','+','%']:
        messagebox.showerror(message="Formato invalido", title="Error de sintaxis")
        return -1,''
    elif tecla=='.':
        return 0, '0.'
    else:
        return 0, tecla # SI LA CADENA ESTA VACIA, SE RETORNA INDICE = 0 Y EL CARACTER

def resolver(entrada):
    ecuacion = entrada
    if not ecuacion:
        messagebox.showerror(message="Por favor ingrese una ecuación valida", title="Error en ecuación")
        return 'e'
    try:
        expr = sp.sympify(ecuacion)
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
