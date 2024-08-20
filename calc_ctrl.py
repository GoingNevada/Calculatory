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
import numpy as np  # modulo para el analisis vectorial y matricial
import sympy as sp
import re   # modulo para el manejo de expresiones regulares


teclas_aux = [['arc'  , '!'  ,    '%'    ],
              ['sin'  , 'cos',   'tan'   ],
              ['csc'  , 'sec',   'cot'   ],
              ['sin\u207b¹','cos\u207b¹','tan\u207b¹'],
              ['csc\u207b¹','sec\u207b¹','cot\u207b¹']]

teclas = [ ['\u21C4','x','y','C','\u232B'],
           [ 'sin', 'cos','tan','ans','÷'],
           ['x\u207F', '(', ')','|x|','*'],
           [ 'e' , '7' , '8' , '9' , '-' ],
           ['\u207F\u221Ax','4','5','6','+'],
           [ 'log', '1', '2','3','\u21B5'],
           ['ln' ,'\u03C0' ,'0' ,'.' ,'_']]

numeros = ['0','1','2','3','4','5','6','7','8','9']
signos = ['+','-','/','*','^']

# CONFIGURACION POR DEFECTO
angulo = 'Radian'   # Calculo de un angulo dado en Grado | Radian
formato = 'Normal'  # Formato de exponenciales Normal | Cientifico
digitos = 6         # Cantidad de digitos decimales a mostrar

def calc_config(data):
    digitos = data[0]
    angulo = data[1]
    formato = data[2]

def graph_config():
    pass

def is_int(num):  # FUNCION PARA LA COMPROBACION DE CONVERSION DE UN NUMERO A ENTERO
    try:        # UTILIZAMOS UN TRY PARA INTENTAR REALIZAR LA CONVERSION
        int(num)  # EN CASO DE EXITO, LA FUNCION RETORNARA UN VALOR 'TRUE'
        return True
    except ValueError:     # EN CASO DE CONTRARIO, RETORNARA UN VALOR 'FALSE'
        return False

def is_float(num):    # FUNCION PARA LA COMPROBACION DE CONVERSION DE UN NUMERO A DECIMAL
    try:            # UTILIZAMOS UN TRY PARA INTENTAR REALIZAR LA CONVERSION
        float(num)    # EN CASO DE EXITO, LA FUNCION RETORNARA UN VALOR 'TRUE'
        return True
    except ValueError:   # EN CASO DE CONTRARIO, RETORNARA UN VALOR 'FALSE'
        return False
    
def conv_num(num):  # FUNCION PARA LA CONVERSION DE UN NUMERO EN SU FORMA DIRECTA
    if is_int(num):      # SI EL NUMERO SE PUEDE CONVERTIR A ENTERO, RETORNARA SU VALOR ENTERO
        return int(num)
    elif is_float(num):  # SI EL NUMERO SE PUEDE CONVERTIR A REAL, RETORNARA SU VALOR REAL
        return float(num)
    else:
        return 'Error en conversion de caracter entrante'  # EN CASO CONTRARIO, RETORNARA UNA SEÑAL DE ERROR
    
def is_number(num):
    if is_int(num) or is_float(num):
        return True
    else:
        return False
    
def tokinize(expr): # CONVERSION DE LA CADENA ENTRANTE EN LISTA DE CARACTERES
    pattern = r'(\b\w*[\.]?\w+\b|\(|\)|\+|\-|\*|\/|\^|\!)'  # Patron de separacion
    tokens = re.findall(pattern, expr)  # Retorno de la lista de caracteres
    return tokens

def entry(entr, tecla):    # ANALIZADOR DE SINTAXIS
    if entr:    # PREGUNTAMOS SI LA CADENA NO ESTA VACIA
        ind = len(entr) # OBTENEMOS EL TAMAÑO DE LA CADENA DE ENTRADA
        if tecla in numeros:    # SI EL CARACTER ENTRANTE ES UN NUMERO, ENTONCES...
            return ind, tecla   # RETORNAMOS EL INDICE Y EL CARACTER QUE SE POSICIONARA
        elif tecla in signos:   # SI EL CARACTER ENTRANTE ES UN SIGNO, ENTONCES...
            if entr[ind-1] in signos:   # PREGUNTAMOS SI ANTERIORMENTE EXISTE UN SIGNO
                return ind-1, tecla     # SI EXISTE, ENTONCES REEMPLAZAMOS ESE SIGNO POR EL NUEVO QUE INGRESA
            else:
                return ind, tecla       # SI NO, ENTONCES SOLO SE RETORNA INDICE Y EL CARACTER
        elif tecla=='.':    # SI EL CARACTER ES '.', ENTONCES...
            if entr[ind-1] in numeros:  # PREGUNTAMOS SI HAY NUMEROS ANTERIORMENTE
                return ind, tecla   # SI EXISTE, ENTONCES SOLO SE RETRONA INDICE Y EL CARACTER (1.)
            elif entr[ind-1] in signos:
                return ind, '0.'
            else:                   
                return ind, '*0.'   # SI NO, ENTONCES SE RETRONA INDICE Y SE AGREGA '*0' AL CARACTER (*0.)
        else:
            if entr[ind-1] in signos:   # PREGUNTAMOS SI ANTERIORMENTE EXISTE UN SIGNO 
                return ind, tecla       # SI EXISTE, ENTONCES SOLO SE RETORNA INDICE Y EL CARACTER (+ sin(45))
            else:                       
                return ind, '*' + tecla  # SI NO, ENTONCES SE RETORNA EL INDICE Y "* + EL CARACTER"  (* sin(45))
    elif tecla in ['/','*','^','+','%']:
        messagebox.showerror(message="Formato invalido", title="Error de sintaxis")
        return -1,''
    elif tecla=='.':
        return 0, '0.'
    else:
        return 0, tecla # SI LA CADENA ESTA VACIA, SE RETORNA INDICE = 0 Y EL CARACTER
    
def const_replace(entrada):
    if '\u03C0' in entrada:
        entrada = entrada.replace('\u03C0','pi')
    if 'e' in entrada:
        entrada = entrada.replace('e','E')
    return entrada

def solver(entrada):
    if entrada:
        entrada = const_replace(entrada)
        expr = sp.sympify(entrada)
        if 'x' not in str(expr):
            return evaluate(expr)
        else:
            return graph(expr)
    else:
        messagebox.showerror(message="Por favor ingrese una ecuación valida", title="Error en ecuación")
        return 'SyntaxError'

def evaluate(entrada):
    try:
        res = str(entrada.evalf())
        if res == 'zoo':
            raise ZeroDivisionError
        else:
            return round(conv_num(res),6)
    except ZeroDivisionError:
        messagebox.showerror(message=f"No es posible realizar una division por cero", title="Error de division")
        return 'Indefinido'
    except Exception as ex:
        messagebox.showerror(message=f"Ecuación ingresada no valida, {type(ex)}", title="Error de ingreso")
        return 'SyntaxError'

def graph(entrada):
    x = sp.symbols('x')
    x_values = np.linspace(-50, 50, 10000)
    y_values = []
    try:
        for val in x_values:
            y = entrada.subs(x, val)
            if type(y) != sp.core.numbers.Float:
                y_values.append(None)
            else:
                y_values.append(y)
        y_values = np.array(y_values)
        return y_values
    except Exception as ex:
        messagebox.showerror(message=f"Ecuación ingresada no valida, {type(ex)}", title="Error de ingreso")
        return 'SyntaxError'
