

# LIBRERIAS UTILIZADAS PARA LA CONSTRUCCION DE VENTANA Y GRAFICACION
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import backend_bases
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import sympy as sp
from db_graph import *

# CARACTERES UTILIZADOS PARA EL DISEÑO DEL TECLADO DE VENTANA

backend_bases.NavigationToolbar2.toolitems = (
        ('Back', 'Back to  previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
      )

teclas = [['sin','cos','tan','C','\u232B'],
           ['x\u207F','x','y','ans','÷'],
           ['\u03C0','(',')','|x|','*'],
           ['e','7','8','9','-'],
           ['\u207F\u221Ax','4','5','6','+'],
           ['log','1','2','3','\u21B5'],
           ['ln','!','0','.','_']]

class CalculadoraGrafica(tk.Tk):
    def __init__(self): # CONSTRUCTOR DE LA CLASE
        super().__init__()  # FUNCION DE CLASE PARA EJECUTAR METODOS HIJOS
        self.title("Calculadora Gráfica")   # NOMBRE DE LA APLICACION
        self.iconbitmap("icono.ico")
        #self.geometry("800x600")    # DIMENSIONES INICIALES DE LA APLICACION
        self.menubar = tk.Menu(self)    # CREACION DE UN MENU EN LA BARRA SUPERIOR
        self.configure(menu=self.menubar, background="#434343")  # Cambiar color de fondo principal
        self.resizable(False,False)
        #----------------VARIABLES GLOBALES DE DE LA CLASE--------------#
        self.entrada = ''
        
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
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)

        #-------------CREACION DE FIGURA PRA GRAFICOS--------------#
        self.graficacion = tk.Canvas(self, width=50, height=50)
        self.graficacion.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

        self.figura = Figure(figsize=(4, 3), dpi=100)   # SE AGREGA FIGURA A LA VENTANA
        self.ax = self.figura.add_subplot(111)  # SE CREA EL LUGAR DE LA FIGURA
        #self.ax.spines['left'].set_position('center')
        #self.ax.spines['bottom'].set_position('center')
        self.ax.grid(True)
        #self.ax.set_xlim([-5, 5])
        #self.ax.set_xticks(range(-5, 5))
        #self.ax.set_ylim([-5, 5])
        #self.ax.set_yticks(range(-5, 5))


        self.canvas = FigureCanvasTkAgg(self.figura, master=self.graficacion)   
        self.canvas.draw()  # DIBUJADO INICIAL
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=1, fill=tk.BOTH)   # SE UBICA EN LA VENTANA
        self.tlb = NavigationToolbar2Tk(self.canvas, self.graficacion)
        self.tlb.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=1, fill=tk.BOTH)   # SE UBICA EN LA VENTANA"""


        #----------Etiqueta y entrada para la ecuación-------------#
        self.ecu = tk.Canvas(self, width=50, height=50, background="black")
        self.ecu.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=[0,5])

        self.ecu.columnconfigure(0, weight=1)
        self.ecu.columnconfigure(1, weight=3)
        self.ecu.rowconfigure(0, weight=1)

        self.etiqueta_ecuacion = tk.Label(self.ecu, text="f(x)", bg="#1155CC",  fg="black", font=('Harlow Solid Italic', 12), relief="flat", border=2)
        self.etiqueta_ecuacion.grid(row=0, column=0, sticky="nsew", columnspan=1)
        self.entrada_ecuacion = ttk.Entry(self.ecu, font=('Harlow Solid Italic', 12))
        self.entrada_ecuacion.grid(row=0, column=1, sticky="nsew")
        
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


        # Botón de sin
        self.boton_sin = ttk.Button(self, text=teclas[0][0], width=4, style="control.TButton", command=lambda: self.ing_teclado('sin('))
        self.boton_sin.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de cos
        self.boton_cos = ttk.Button(self, text=teclas[0][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('cos('))
        self.boton_cos.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de tan
        self.boton_tan = ttk.Button(self, text=teclas[0][2], width=4, style="control.TButton", command=lambda: self.ing_teclado('tan('))
        self.boton_tan.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de C
        self.boton_c = ttk.Button(self, text=teclas[0][3], width=4, style="del_button.TButton", command=self.limpiar)
        self.boton_c.grid(row=2, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de borrar
        self.boton_limpiar = ttk.Button(self, text=teclas[0][4], width=4, style="del_button.TButton", command=self.borrar)
        self.boton_limpiar.grid(row=2, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de x^n
        self.boton_potencia = ttk.Button(self, text=teclas[1][0], width=4, style="control.TButton", command=lambda: self.ing_teclado('^'))
        self.boton_potencia.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de x
        self.boton_x = ttk.Button(self, text=teclas[1][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('x'))
        self.boton_x.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de y
        self.boton_y = ttk.Button(self, text=teclas[1][2], width=4, style="control.TButton", command=lambda: self.ing_teclado('y'))
        self.boton_y.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de ans
        self.boton_ans = ttk.Button(self, text=teclas[1][3], width=4, style="oper_button.TButton", command=self.ans)
        self.boton_ans.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de /
        self.boton_division = ttk.Button(self, text=teclas[1][4], width=4, style="oper_button.TButton", command=lambda: self.ing_teclado('/'))
        self.boton_division.grid(row=3, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de pi
        self.boton_pi = ttk.Button(self, text=teclas[2][0], width=4, style="control.TButton", command=lambda: self.ing_teclado('\u03C0'))
        self.boton_pi.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de (
        self.boton_apare = ttk.Button(self, text=teclas[2][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('('))
        self.boton_apare.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
            
        # Botón de )
        self.boton_cpare = ttk.Button(self, text=teclas[2][2], width=4, style="control.TButton", command=lambda: self.ing_teclado(')'))
        self.boton_cpare.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de |x|
        self.boton_abs = ttk.Button(self, text=teclas[2][3], width=4, style="control.TButton", command=lambda: self.ing_teclado('abs('))
        self.boton_abs.grid(row=4, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de *
        self.boton_multi = ttk.Button(self, text=teclas[2][4], width=4, style="oper_button.TButton", command=lambda: self.ing_teclado('*'))
        self.boton_multi.grid(row=4, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de e
        self.boton_e = ttk.Button(self, text=teclas[3][0], width=4, style="control.TButton", command=lambda: self.ing_teclado('e'))
        self.boton_e.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 7
        self.boton_7 = ttk.Button(self, text=teclas[3][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('7'))
        self.boton_7.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 8
        self.boton_8 = ttk.Button(self, text=teclas[3][2], width=4, style="control.TButton", command=lambda: self.ing_teclado('8'))
        self.boton_8.grid(row=5, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 9
        self.boton_9 = ttk.Button(self, text=teclas[3][3], width=4, style="control.TButton", command=lambda: self.ing_teclado('9'))
        self.boton_9.grid(row=5, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de -
        self.boton_resta = ttk.Button(self, text=teclas[3][4], width=4, style="oper_button.TButton", command=lambda: self.ing_teclado('-'))
        self.boton_resta.grid(row=5, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de root
        self.boton_root = ttk.Button(self, text=teclas[4][0], width=4, style="control.TButton")
        self.boton_root.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 4
        self.boton_4 = ttk.Button(self, text=teclas[4][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('4'))
        self.boton_4.grid(row=6, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 5
        self.boton_5 = ttk.Button(self, text=teclas[4][2], width=4, style="control.TButton", command=lambda: self.ing_teclado('5'))
        self.boton_5.grid(row=6, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 6
        self.boton_6 = ttk.Button(self, text=teclas[4][3], width=4, style="control.TButton", command=lambda: self.ing_teclado('6'))
        self.boton_6.grid(row=6, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de +
        self.boton_suma = ttk.Button(self, text=teclas[4][4], width=4, style="oper_button.TButton", command=lambda: self.ing_teclado('+'))
        self.boton_suma.grid(row=6, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de log
        self.boton_log = ttk.Button(self, text=teclas[5][0], width=4, style="control.TButton", command=lambda: self.ing_teclado('log(b,x)'))
        self.boton_log.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 1
        self.boton_1 = ttk.Button(self, text=teclas[5][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('1'))
        self.boton_1.grid(row=7, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 2
        self.boton_2 = ttk.Button(self, text=teclas[5][2], width=4, style="control.TButton", command=lambda: self.ing_teclado('2'))
        self.boton_2.grid(row=7, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 3
        self.boton_3 = ttk.Button(self, text=teclas[5][3], width=4, style="control.TButton", command=lambda: self.ing_teclado('3'))
        self.boton_3.grid(row=7, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de enter
        self.boton_enter = ttk.Button(self, text=teclas[5][4], width=4, style="enter_button.TButton", command=self.graficar)
        self.boton_enter.grid(row=7, column=4, sticky="nsew", rowspan=2, padx=2, pady=2)
        
        # Botón de ln
        self.boton_ln = ttk.Button(self, text=teclas[6][0], width=4, style="control.TButton", command=lambda: self.ing_teclado('ln('))
        self.boton_ln.grid(row=8, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de !
        self.boton_punto = ttk.Button(self, text=teclas[6][1], width=4, style="control.TButton", command=lambda: self.ing_teclado('!'))
        self.boton_punto.grid(row=8, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 0
        self.boton_0 = ttk.Button(self, text=teclas[6][2], width=4, style="control.TButton", command=lambda: self.ing_teclado('0'))
        self.boton_0.grid(row=8, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de .
        self.boton_negativo = ttk.Button(self, text=teclas[6][3], width=4, style="control.TButton", command=lambda: self.ing_teclado('.'))
        self.boton_negativo.grid(row=8, column=3, sticky="nsew", padx=2, pady=2)

        self.historial = [] 
        
        db_init()


    def ing_teclado(self, tecla):
        ind = len(self.entrada_ecuacion.get())
        self.entrada_ecuacion.insert(ind, tecla)

    def graficar(self):
        ecuacion = self.entrada_ecuacion.get().strip()
        if not ecuacion:
            messagebox.showerror(message="Por favor ingrese una ecuación valida", title="Error en ecuación")
            return
        try:
            expr = sp.sympify(ecuacion)
            x = sp.symbols('x')
            if 'x' not in str(expr):
                raise ValueError("Error: La ecuación no contiene la variable 'x'.")

            #min_x, max_x = map(float, self.entrada_rango.get().split())
            #num_puntos = int(self.entrada_puntos.get())
            x_values = np.linspace(-20, 20, 1000)
            y_values = np.array([expr.subs(x, val) for val in x_values], dtype=float)

            self.ax.clear()
            self.ax.plot(x_values, y_values)
            self.ax.grid(True)
            self.ax.axhline(0, color='black', lw=0.5)
            self.ax.axvline(0, color='black', lw=0.5)
            self.canvas.draw()

            self.historial.append(self.entrada_ecuacion.get())
            
        except Exception as e:
            messagebox.showerror(message="Ecuación ingresada no valida", title="Error de ingreso")

    def ans(self):
        self.entrada_ecuacion.delete(0, tk.END)
        self.entrada_ecuacion.insert(0, self.entrada)
    
    def limpiar(self):
        self.entrada_ecuacion.delete(0, tk.END)
        self.ax.clear()
        self.ax.grid(True)
        self.canvas.draw()

    def borrar(self):
        self.entrada = self.entrada_ecuacion.get()
        ind = len(self.entrada_ecuacion.get())
        self.entrada_ecuacion.delete(ind-1)

    def guardar(self):
        user_creator(self.historial)