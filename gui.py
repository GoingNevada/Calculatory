

# IMPORTACION DE MODULOS 
import tkinter as tk
from tkinter import ttk, messagebox, OptionMenu, Label, StringVar, Entry, Button, Spinbox, IntVar, Tk
from matplotlib import backend_bases
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np
import sympy as sp
from calculadora import *
from db_graph import *

# DIRECCION DE ARCHIVOS ADICIONALES
icono = "Proyecto_calcgrf/resources/icono.ico"  # IMAGEN DE ICONO
img_login = "Proyecto_calcgrf/resources/login.png"  # IMAGEN DE LOGIN

# INICIALIZACIONES PRIORITARIAS
db_init()

# COLORES PREDETERMINADOS DE LA APLICACION
fondo = "#3D85C6"   # FONDO PARA LOGIN
fondo2 = "#134F5C"  # FONDO PARA FORM
fondo3 = "#434343"  # FONDO PARA CALCULADORA

# VARIABLES GLOBALES

teclas_aux = [['arc',   'hyp'    , '!'  ,    '%'      ],
              ['sin','sin\u207b¹','sinh','sinh\u207b¹'],
              ['cos','cos\u207b¹','cosh','cosh\u207b¹'],
              ['tan','tan\u207b¹','tanh','tanh\u207b¹'],
              ['csc','csc\u207b¹','csch','csch\u207b¹'],
              ['sec','sec\u207b¹','sech','sech\u207b¹'],
              ['cot','cot\u207b¹','coth','coth\u207b¹']]

teclas = [['\u21C4','x','y','C','\u232B'],
           ['sin','cos','tan','ans','÷'],
           ['x\u207F','(',')','|x|','*'],
           ['e','7','8','9','-'],
           ['\u207F\u221Ax','4','5','6','+'],
           ['log','1','2','3','\u21B5'],
           ['ln','\u03C0','0','.','_']]

historial = []

class Calculadora(tk.Tk):
    def __init__(self): # CONSTRUCTOR DE LA CLASE
        super().__init__()  # FUNCION DE CLASE PARA EJECUTAR METODOS HIJOS
        self.title("Calculadora")   # NOMBRE DE LA APLICACION
        self.iconbitmap(icono)      # ICONO DE LA APLICACION
        self.menubar = tk.Menu(self)    # CREACION DE UN MENU EN LA BARRA SUPERIOR
        self.configure(menu=self.menubar, background=fondo3)  # Cambiar color de fondo principal
        self.resizable(False,False)
        #----------------VARIABLES GLOBALES DE DE LA CLASE--------------#
        self.entrada = ''
        self.estado_aux = False
        
        #----------------OPCIONES DE MENU--------------------#
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Nuevo")
        self.filemenu.add_command(label="Abrir")
        self.filemenu.add_command(label="Guardar", command= self.guardar)
        self.filemenu.add_command(label="Cerrar")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Salir", command=self.quit)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Cortar")
        self.editmenu.add_command(label="Copiar")
        self.editmenu.add_command(label="Pegar")

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Ayuda")
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Acerca de...")

        self.menubar.add_cascade(label="Archivo", menu=self.filemenu)
        self.menubar.add_cascade(label="Editar", menu=self.editmenu)
        self.menubar.add_cascade(label="Ayuda", menu=self.helpmenu)
        
        #------------CONFIGURACION DE LA DISTRIBUCION DE LA VENTANA-------------#
        # NUMERO DE COLUMNAS CON SU PESO
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        
        # NUMERO DE FILAS CON SU PESO
        self.rowconfigure(0, weight=1) # PARA GRAFICA WEIGHT=10
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)

        #----------Etiqueta y entrada para la ecuación-------------#
        self.entrada_ecuacion = ttk.Entry(self, font=('Arial', 18))
        self.entrada_ecuacion.grid(row=0, column=0, sticky="nsew", columnspan=5, padx=5, pady=5)

        #-------------BLOQUE DE SALIDA DE RESULTADOS--------------#
        self.ecuacion = tk.StringVar()
        self.resultado = ttk.Label(self, textvariable=self.ecuacion, font=('Arial', 18), justify='right')
        self.resultado.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=[0,5])
        self.graficacion = tk.Canvas(self, width=50, height=50)

        #---------BLOQUE DE BOTONES CON FUNCIONALIDADES-------#
        estilo = ttk.Style()
        estilo.theme_use('clam')

        delt_button = ttk.Style()
        delt_button.configure("del_button.TButton", font="consolas 12 bold", background="#000000", relief="flat", foreground="#FF0000")
        delt_button.map('del_button.TButton', background=[('active', '#262626')])

        oper_button = ttk.Style()
        oper_button.configure("oper_button.TButton", font="consolas 12 bold", background="#000000", relief="flat", foreground="#34A853")
        oper_button.map('oper_button.TButton', background=[('active', '#262626')])
        
        norm_button = ttk.Style()
        norm_button.configure("control.TButton", font="consolas 12 bold", background="#000000", relief="flat", foreground="#FFFFFF")
        norm_button.map('control.TButton', background=[('active', '#262626')])

        enter_button = ttk.Style()
        enter_button.configure("enter_button.TButton", font="consolas 12 bold", background="#34A853", relief="flat", foreground="#FFFFFF")
        norm_button.map('enter_button.TButton', background=[('active', '#11742B')])

        pulse_button = ttk.Style()
        pulse_button.configure("pulse_button.TButton", font="consolas 12 bold", background="#660000", relief="flat", foreground="#FFFFFF")
        pulse_button.map('pulse_button.TButton', background=[('active', '#990000')])

        # Boton de cambio
        self.boton_change = ttk.Button(self, text=teclas[0][0], width=5, style="control.TButton", command=self.aux_button)
        self.boton_change.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)

        # Botón de x
        self.boton_x = ttk.Button(self, text=teclas[0][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('x'))
        self.boton_x.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de y
        self.boton_y = ttk.Button(self, text=teclas[0][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('y'))
        self.boton_y.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de C
        self.boton_c = ttk.Button(self, text=teclas[0][3], width=5, style="del_button.TButton", command=self.limpiar)
        self.boton_c.grid(row=2, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de borrar
        self.boton_limpiar = ttk.Button(self, text=teclas[0][4], width=5, style="del_button.TButton", command=self.borrar)
        self.boton_limpiar.grid(row=2, column=4, sticky="nsew", padx=2, pady=2)

        # Botón de sin
        self.boton_sin = ttk.Button(self, text=teclas[1][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('sin('))
        self.boton_sin.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de cos
        self.boton_cos = ttk.Button(self, text=teclas[1][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('cos('))
        self.boton_cos.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de tan
        self.boton_tan = ttk.Button(self, text=teclas[1][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('tan('))
        self.boton_tan.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de ans
        self.boton_ans = ttk.Button(self, text=teclas[1][3], width=5, style="oper_button.TButton", command=self.ans)
        self.boton_ans.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de /
        self.boton_division = ttk.Button(self, text=teclas[1][4], width=5, style="oper_button.TButton", command=lambda: self.ing_teclado('/'))
        self.boton_division.grid(row=3, column=4, sticky="nsew", padx=2, pady=2)

        # Botón de x^n
        self.boton_potencia = ttk.Button(self, text=teclas[2][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('^'))
        self.boton_potencia.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de (
        self.boton_apare = ttk.Button(self, text=teclas[2][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('('))
        self.boton_apare.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
            
        # Botón de )
        self.boton_cpare = ttk.Button(self, text=teclas[2][2], width=5, style="control.TButton", command=lambda: self.ing_teclado(')'))
        self.boton_cpare.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de |x|
        self.boton_abs = ttk.Button(self, text=teclas[2][3], width=5, style="control.TButton", command=lambda: self.ing_teclado('abs('))
        self.boton_abs.grid(row=4, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de *
        self.boton_multi = ttk.Button(self, text=teclas[2][4], width=5, style="oper_button.TButton", command=lambda: self.ing_teclado('*'))
        self.boton_multi.grid(row=4, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de e
        self.boton_e = ttk.Button(self, text=teclas[3][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('e'))
        self.boton_e.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 7
        self.boton_7 = ttk.Button(self, text=teclas[3][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('7'))
        self.boton_7.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 8
        self.boton_8 = ttk.Button(self, text=teclas[3][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('8'))
        self.boton_8.grid(row=5, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 9
        self.boton_9 = ttk.Button(self, text=teclas[3][3], width=5, style="control.TButton", command=lambda: self.ing_teclado('9'))
        self.boton_9.grid(row=5, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de -
        self.boton_resta = ttk.Button(self, text=teclas[3][4], width=5, style="oper_button.TButton", command=lambda: self.ing_teclado('-'))
        self.boton_resta.grid(row=5, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de root
        self.boton_root = ttk.Button(self, text=teclas[4][0], width=5, style="control.TButton")
        self.boton_root.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 4
        self.boton_4 = ttk.Button(self, text=teclas[4][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('4'))
        self.boton_4.grid(row=6, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 5
        self.boton_5 = ttk.Button(self, text=teclas[4][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('5'))
        self.boton_5.grid(row=6, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 6
        self.boton_6 = ttk.Button(self, text=teclas[4][3], width=5, style="control.TButton", command=lambda: self.ing_teclado('6'))
        self.boton_6.grid(row=6, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de +
        self.boton_suma = ttk.Button(self, text=teclas[4][4], width=5, style="oper_button.TButton", command=lambda: self.ing_teclado('+'))
        self.boton_suma.grid(row=6, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de log
        self.boton_log = ttk.Button(self, text=teclas[5][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('log(b,x)'))
        self.boton_log.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 1
        self.boton_1 = ttk.Button(self, text=teclas[5][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('1'))
        self.boton_1.grid(row=7, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 2
        self.boton_2 = ttk.Button(self, text=teclas[5][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('2'))
        self.boton_2.grid(row=7, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 3
        self.boton_3 = ttk.Button(self, text=teclas[5][3], width=5, style="control.TButton", command=lambda: self.ing_teclado('3'))
        self.boton_3.grid(row=7, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de enter
        self.boton_enter = ttk.Button(self, text=teclas[5][4], width=5, style="enter_button.TButton", command=self.solve)
        self.boton_enter.grid(row=7, column=4, sticky="nsew", rowspan=2, padx=2, pady=2)
        
        # Botón de ln
        self.boton_ln = ttk.Button(self, text=teclas[6][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('ln('))
        self.boton_ln.grid(row=8, column=0, sticky="nsew", padx=2, pady=2)

        # Botón de pi
        self.boton_pi = ttk.Button(self, text=teclas[6][1], width=5, style="control.TButton", command=lambda: self.ing_teclado('\u03C0'))
        self.boton_pi.grid(row=8, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 0
        self.boton_0 = ttk.Button(self, text=teclas[6][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('0'))
        self.boton_0.grid(row=8, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de .
        self.boton_negativo = ttk.Button(self, text=teclas[6][3], width=5, style="control.TButton", command=lambda: self.ing_teclado('.'))
        self.boton_negativo.grid(row=8, column=3, sticky="nsew", padx=2, pady=2)

        self.btns_state = [False,False]  # ESTADO DEL BOTON ASOCIADO A CAMBIO

    def chg_state(self, ind):

        self.btns_state[ind] = not(self.btns_state[ind])

        print(self.btns_state)

        if self.btns_state==[True,False]:
            self.boton_arc.configure(style="pulse_button.TButton")
            self.boton_hyp.configure(style="control.TButton")
            self.boton_nsin.configure(text=teclas_aux[1][1], command=lambda: self.ing_teclado('asin('))
            self.boton_ncos.configure(text=teclas_aux[2][1], command=lambda: self.ing_teclado('acos('))
            self.boton_ntan.configure(text=teclas_aux[3][1], command=lambda: self.ing_teclado('atan('))
            self.boton_csc.configure(text=teclas_aux[4][1], command=lambda: self.ing_teclado('acsc('))
            self.boton_sec.configure(text=teclas_aux[5][1], command=lambda: self.ing_teclado('asec('))
            self.boton_cot.configure(text=teclas_aux[6][1], command=lambda: self.ing_teclado('acot('))

        elif self.btns_state==[False,True]:
            self.boton_hyp.configure(style="pulse_button.TButton")
            self.boton_arc.configure(style="control.TButton")
            self.boton_nsin.configure(text=teclas_aux[1][2], command=lambda: self.ing_teclado('sinh('))
            self.boton_ncos.configure(text=teclas_aux[2][2], command=lambda: self.ing_teclado('cosh('))
            self.boton_ntan.configure(text=teclas_aux[3][2], command=lambda: self.ing_teclado('tanh('))
            self.boton_csc.configure(text=teclas_aux[4][2], command=lambda: self.ing_teclado('csch('))
            self.boton_sec.configure(text=teclas_aux[5][2], command=lambda: self.ing_teclado('sech('))
            self.boton_cot.configure(text=teclas_aux[6][2], command=lambda: self.ing_teclado('coth('))
        
        elif self.btns_state==[True,True]:
            self.boton_hyp.configure(style="pulse_button.TButton")
            self.boton_arc.configure(style="pulse_button.TButton")
            self.boton_nsin.configure(text=teclas_aux[1][3], command=lambda: self.ing_teclado('asinh('))
            self.boton_ncos.configure(text=teclas_aux[2][3], command=lambda: self.ing_teclado('acosh('))
            self.boton_ntan.configure(text=teclas_aux[3][3], command=lambda: self.ing_teclado('atanh('))
            self.boton_csc.configure(text=teclas_aux[4][3], command=lambda: self.ing_teclado('acsch('))
            self.boton_sec.configure(text=teclas_aux[5][3], command=lambda: self.ing_teclado('asech('))
            self.boton_cot.configure(text=teclas_aux[6][3], command=lambda: self.ing_teclado('acoth('))
        
        else:
            self.boton_hyp.configure(style="control.TButton")
            self.boton_arc.configure(style="control.TButton")
            self.boton_nsin.configure(text=teclas_aux[1][0], command=lambda: self.ing_teclado('sin('))
            self.boton_ncos.configure(text=teclas_aux[2][0], command=lambda: self.ing_teclado('cos('))
            self.boton_ntan.configure(text=teclas_aux[3][0], command=lambda: self.ing_teclado('tan('))
            self.boton_csc.configure(text=teclas_aux[4][0], command=lambda: self.ing_teclado('csc('))
            self.boton_sec.configure(text=teclas_aux[5][0], command=lambda: self.ing_teclado('sec('))
            self.boton_cot.configure(text=teclas_aux[6][0], command=lambda: self.ing_teclado('cot('))
            

    def aux_button(self):
        print(self.estado_aux)
        self.estado_aux = not(self.estado_aux)
        print(self.estado_aux)
        if self.estado_aux == True:
            self.boton_change.configure(style="pulse_button.TButton")
            # ---------BOTONES AUXILIARES----------------------#
            self.boton_nsin = ttk.Button(self,text=teclas_aux[1][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('sin('))
            self.boton_ncos = ttk.Button(self,text=teclas_aux[2][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('cos('))
            self.boton_ntan = ttk.Button(self,text=teclas_aux[3][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('tan('))
            self.boton_csc =  ttk.Button(self,text=teclas_aux[4][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('csc('))
            self.boton_sec =  ttk.Button(self,text=teclas_aux[5][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('sec('))
            self.boton_cot =  ttk.Button(self,text=teclas_aux[6][0], width=5, style="control.TButton", command=lambda: self.ing_teclado('cot('))
            self.boton_arc =  ttk.Button(self,text=teclas_aux[0][0], width=5, style="control.TButton", command=lambda: self.chg_state(0))
            self.boton_hyp =  ttk.Button(self,text=teclas_aux[0][1], width=5, style="control.TButton", command=lambda: self.chg_state(1))
            self.boton_fac =  ttk.Button(self,text=teclas_aux[0][2], width=5, style="control.TButton", command=lambda: self.ing_teclado('!'))
            self.boton_porc = ttk.Button(self,text=teclas_aux[0][3], width=5, style="control.TButton", command=lambda: self.ing_teclado('%'))
            self.boton_arc.configure(style="control.TButton")
            self.boton_hyp.configure(style="control.TButton")
            self.boton_nsin.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_ncos.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
            self.boton_ntan.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
            self.boton_csc.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_sec.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
            self.boton_cot.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
            self.boton_arc.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_hyp.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_fac.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_porc.grid(row=8, column=0, sticky="nsew", padx=2, pady=2)
            self.btns_state[0]=False
            self.btns_state[1]=False
        else:
            self.boton_change.configure(style="control.TButton")
            self.boton_nsin.destroy()
            self.boton_ncos.destroy()
            self.boton_ntan.destroy()
            self.boton_csc.destroy()
            self.boton_sec.destroy()
            self.boton_cot.destroy()
            self.boton_arc.destroy()
            self.boton_hyp.destroy()
            self.boton_fac.destroy()
            self.boton_porc.destroy()
            self.btns_state[0]=False
            self.btns_state[1]=False

    def is_int(self,n):  # Funcion de comprobacion de numero entero positivo
        try:            # Uitlizamos un try - catch para realizar la comporbacion
            int(n)
            return True     # Si cumple las condiciones, se retorna True
        except Exception:
            return False        # Si no, envia un False


    def ing_teclado(self, tecla):
        ind = len(self.entrada_ecuacion.get())
        self.entrada_ecuacion.insert(ind, tecla)

    def solve(self):
        resultado = resolver(self.entrada_ecuacion.get().strip())
        if self.is_int(resultado):
            self.graficacion.destroy()
            self.resultado = ttk.Label(self, textvariable=self.ecuacion, font=('Arial', 18), justify='right')
            self.resultado.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=[0,5])
            self.ecuacion.set(resultado)
        else:
            self.graficacion = tk.Canvas(self, width=50, height=50)
            self.graficacion.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
            self.figura = Figure(figsize=(4, 3), dpi=100)   # SE AGREGA FIGURA A LA VENTANA
            self.ax = self.figura.add_subplot(111)  # SE CREA EL LUGAR DE LA FIGURA
            #self.ax.spines['left'].set_position('center')
            #self.ax.spines['bottom'].set_position('center')
            self.ax.grid(True)
            self.ax.set_xlim([-5, 5])
            #self.ax.set_xticks(range(-5, 5))
            self.ax.set_ylim([-5, 5])
            #self.ax.set_yticks(range(-5, 5))

            self.canvas = FigureCanvasTkAgg(self.figura, master=self.graficacion)   
            self.canvas.draw()  # DIBUJADO INICIAL
            self.canvas.get_tk_widget().pack(side=tk.TOP, expand=1, fill=tk.BOTH)   # SE UBICA EN LA VENTANA
            self.tlb = NavigationToolbar2Tk(self.canvas, self.graficacion)
            self.tlb.update()
            self.canvas.get_tk_widget().pack(side=tk.TOP, expand=1, fill=tk.BOTH)   # SE UBICA EN LA VENTANA"""
            x_values = np.linspace(-20, 20, 1000)
            self.ax.clear()
            self.ax.plot(x_values, resultado)
            #self.ax.grid(True)
            self.ax.axhline(0, color='black', lw=0.5)
            self.ax.axvline(0, color='black', lw=0.5)
            self.canvas.draw()

    def ans(self):
        self.entrada_ecuacion.delete(0, tk.END)
        self.entrada_ecuacion.insert(0, self.entrada)
    
    def limpiar(self):
        self.entrada_ecuacion.delete(0, tk.END)
        self.ecuacion.set('')
        #self.ax.clear()
        self.graficacion.destroy()
        self.resultado = ttk.Label(self, textvariable=self.ecuacion, font=('Arial', 18), justify='right')
        self.resultado.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=[0,5])

    def borrar(self):
        self.entrada = self.entrada_ecuacion.get()
        ind = len(self.entrada_ecuacion.get())
        self.entrada_ecuacion.delete(ind-1)

    def guardar(self):
        user_edit("sacamo@unal.edu.co", historial)

class Login(tk.Tk):
    def __init__(self):
        super().__init__()

        # CONFIGURACION DE LA VENTANA Y SU ESTRUCTURA
        self.title('Calculadora (Login)')
        self.iconbitmap(icono)
        self.configure(bg=fondo, padx=5)
        self.resizable(False,False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # IMAGEN DE LOGIN
        self.img = Image.open(img_login) # CARGAMOS LA IMAGEN A UTILIZAR
        self.img = self.img.resize((160,160)) # LA REDIMENSIONAMOS PARA ACOPLAR A LA VENTANA
        self.img = ImageTk.PhotoImage(self.img) # OBTENEMOS LA IMAGEN COMO UN OBJETO IMAGETK
        self.fondo = tk.Label(self, image= self.img, bg = fondo) # CONFIGURAMOS LA IMAGEN EN UN LABEL
        self.fondo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=[5,10]) # POSICIONAMOS LA IMAGEN EN LA PRIMERA FILA
        
        # INGRESO DE DATOS DE USUARIO
        self.label_user = tk.Label(self,
                                    text="Usuario:",
                                    font=("Arial", 14),
                                    bg=fondo,
                                    fg="black")
        self.label_user.grid(row=1, column=0, padx=10, sticky="we", pady=[10,5])

        self.entry_user = ttk.Entry(self,
                                      width=22,
                                      font=("Arial",14))
        self.entry_user.grid(row=1, column=1, columnspan=2, padx=5, sticky="we", pady=[10,5])

        # INGRESO DE DATOS DE CONTRASEÑA
        self.label_password = tk.Label(self,
                                      text="Contraseña:",
                                      font=("Arial", 14),
                                      bg=fondo,
                                      fg="black")
        self.label_password.grid(row=2, column=0, padx=10, sticky="we", pady=[0,10])

        self.entry_password = ttk.Entry(self,
                                      width=15,
                                      font=("Arial",14),
                                      show="*")
        self.entry_password.grid(row=2, column=1, columnspan=2, padx=5, sticky="w", pady=[0,10])


        # CREACION DE ESTILO PARA BOTONES TEMATICOS
        button_style = ttk.Style()
        button_style.configure("button_style.TButton", font=("Arial",12), background=fondo)

        # BOTON DE OLVIDE CONTRASEÑA
        self.forg_pass = ttk.Button(self,
                                    text="Olvide mi contraseña",
                                    style="button_style.TButton",
                                    command=self.forg_passw)
        self.forg_pass.grid(row=3, column=0, sticky="e", padx=5, pady=[5,30])

        # BOTON DE INGRESAR
        self.ing_button = ttk.Button(self,
                                    text="Ingresar",
                                    style="button_style.TButton",
                                    command=self.entrar)
        self.ing_button.grid(row=3, column=1, sticky="we", padx=5, pady=[5,30])

        # BOTON DE REGISTRARSE
        self.reg_button = ttk.Button(self,
                                    text="Registrarse",
                                    style="button_style.TButton",
                                    command=self.reg_user)
        self.reg_button.grid(row=4, column=0, sticky="we", padx=5, pady=5)

        # BOTON DE INVITADO 
        self.invitado = ttk.Button(self,
                                    text="Ingresar como Anonimo",
                                    style="button_style.TButton",
                                    command=self.inv_entrar)
        self.invitado.grid(row=4, column=1, sticky="we", padx=5, pady=5)


    def entrar(self):
        user = self.entry_user.get()
        password = self.entry_password.get() 
        if user_check(email=user, password=password):
            messagebox.showinfo("Acceso Correcto", "Usuario verificado")
            self.destroy()
            Calculadora()
        else:
            messagebox.showinfo("Acceso Incorrecto", "Los datos ingresados no son correctos")

    def forg_passw(self):
        pass

    def reg_user(self):
        self.destroy()
        Form()

    def inv_entrar(self):
        self.destroy()
        Calculadora()

class Form(Tk):
    def __init__(self):
        super().__init__()

        # CONFIGURACION DE LA VENTANA Y SU ESTRUCTURA
        self.title('Calculadora (Registro)')
        self.iconbitmap(icono)
        self.configure(bg=fondo2, padx=5)
        self.resizable(False,False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)


        # INGRESO DE DATOS DEL USUARIO

        self.etq_email = Label(self, text="Correo electronico:", bg=fondo2, fg="white", font=("Arial", 12))
        self.etq_email.grid(row=0, column=0, sticky="nsew", pady=[20,10])

        self.etq_password = Label(self, text="Contraseña:", bg=fondo2, fg="white", font=("Arial", 12))
        self.etq_password.grid(row=1, column=0, sticky="nsew", pady=[0,10])

        self.etq2_password = Label(self, text="Confirmar Contraseña:", bg=fondo2, fg="white", font=("Arial", 12))
        self.etq2_password.grid(row=2, column=0, sticky="nsew", pady=[0,10])

        self.entry_email = Entry(self, font=("Arial", 12))
        self.entry_email.grid(row=0,column=1, sticky="we", pady=[20,10])

        self.entry_pass1 = Entry(self, font=("Arial", 12), show="*")
        self.entry_pass1.grid(row=1,column=1, sticky="we", pady=[0,10])

        self.entry_pass2 = Entry(self, font=("Arial", 12), show="*")
        self.entry_pass2.grid(row=2,column=1, sticky="we", pady=[0,10])

        # BOTONES DE AGREGAR Y REGRESAR
        button_style = ttk.Style()
        button_style.configure("button_style.TButton", background=fondo2, font=("Arial", 12))

        self.boton_ing = ttk.Button(self, text="Agregar", cursor="hand2", command=self.registrar, style="button_style.TButton")
        self.boton_ing.grid(row=3, column=0, sticky="nsew", pady=[0, 10])

        self.boton_reg= ttk.Button(self, text="Regresar", cursor="hand2", command=self.regresar, style="button_style.TButton")
        self.boton_reg.grid(row=3, column=1, sticky="nsew", pady=[0, 10])


    def registrar(self):
        email = self.entry_email.get()
        password = self.entry_pass1.get()
        if password == self.entry_pass2.get():
            if user_creator(email, password): 
                messagebox.showinfo("Registro de usuario", f"Se ha registrado al usuario {email}, exitosamente")
                self.destroy()
                Login()
            else:
                messagebox.showerror("Registro de usuario", "No se pudo registrar al usuario")
        else:
            messagebox.showinfo("Registro de usuario", "Las contraseñas no coinciden")

    def regresar(self):
        self.destroy()
        Login()