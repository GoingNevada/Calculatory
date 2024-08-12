

# IMPORTACION DE MODULOS 
import tkinter as tk
from tkinter import ttk, messagebox, Label, Entry, Tk, Checkbutton, colorchooser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np
from calc_ctrl import *
from db_ctrl import *

# DIRECCION DE ARCHIVOS ADICIONALES
icono = "resources/icono.ico"  # IMAGEN DE ICONO
img_login = "resources/login.png"  # IMAGEN DE LOGIN

# INICIALIZACIONES PRIORITARIAS
db_init()

# COLORES PREDETERMINADOS DE LA APLICACION
fondo = "#3D85C6"   # FONDO PARA LOGIN
fondo2 = "#134F5C"  # FONDO PARA FORM
fondo3 = "#434343"  # FONDO PARA CALCULADORA

# VARIABLES GLOBALES
teclas = [ ['\u21C4','x','y','C','\u232B'],
           [ 'sin', 'cos','tan','ans','÷'],
           ['x\u207F', '(', ')','|x|','*'],
           [ 'e' , '7' , '8' , '9' , '-' ],
           ['\u207F\u221Ax','4','5','6','+'],
           [ 'log', '1', '2','3','\u21B5'],
           ['ln' ,'\u03C0' ,'0' ,'.' ,'_']]

historial = []

# VARIABLES DE CONFIGURACION
decimales = 'Flotante 6'
angulo = 'Radián'
formato = 'Normal'
grid_draw = True
lineas = "Ambos"
ejes = "Ambos"
xlim = [-10,10]
ylim = [-10,10]
line_color = "black"

name_dict = {
    "Ambos" : "both",
    "Mayor" : "major",
    "Menor" : "minor",
    "X" : "x",
    "Y" : "y"
}

class Calculadora(tk.Tk):
    i = 0
    def __init__(self, user): # CONSTRUCTOR DE LA CLASE
        super().__init__()  # FUNCION DE CLASE PARA EJECUTAR METODOS PADRE (TKINTER)
        self.title("Calculadora")   # NOMBRE DE LA APLICACION
        self.iconbitmap(icono)      # ICONO DE LA APLICACION
        self.menubar = tk.Menu(self)    # CREACION DE UN MENU EN LA BARRA SUPERIOR
        self.configure(menu=self.menubar, background=fondo3)  # CONFIGURACION DE LA VENTANA
        #self.resizable(False,False)

        #----------------VARIABLES GLOBALES DE DE LA CLASE--------------#
        self.entrada = ''
        self.res = 0
        self.estado_aux = False
        self.usuario = user
        self.tema = ''
        
        #----------------OPCIONES DE MENU--------------------#
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Abrir desde json")
        self.filemenu.add_command(label="Guardar json", command=self.guardar)
        self.filemenu.add_command(label="Sincronizar en DB", command=self.syncr, state= 'active' if self.usuario != 'None' else 'disabled')
        self.filemenu.add_command(label="Cerrar", command=self.cerrar)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Salir", command=self.quit)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Configuración de graficos", command=self.cfg_graph)
        self.editmenu.add_command(label="Configuración de calculo", command=self.cfg_calc)
        self.editmenu.add_command(label="Limpiar historial", command=self.del_hist)

        self.theme = tk.Menu(self.menubar, tearoff=0)
        self.tema_sel = tk.IntVar()
        self.tema_sel.set(1)  # Opción seleccionada por defecto ("Claro").
        self.theme.add_radiobutton(label="Claro", variable=self.tema_sel, value=1)
        self.theme.add_radiobutton(label="Oscuro", variable=self.tema_sel, value=2)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Ayuda")
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Acerca de...")

        self.menubar.add_cascade(label="Archivo", menu=self.filemenu)
        self.menubar.add_cascade(label="Opciones", menu=self.editmenu)
        self.menubar.add_cascade(label="Tema", menu=self.theme)
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
        self.entrada_ecuacion = ttk.Combobox(self, font=('Arial', 18))
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
        
        dark_style = ttk.Style()
        dark_style.configure("dark_button.TButton", font="consolas 12 bold", background="#000000", relief="flat", foreground="#FFFFFF")
        dark_style.map('dark_button.TButton', background=[('active', '#262626')])

        light_style = ttk.Style()
        light_style.configure("light_button.TButton", font="consolas 12 bold", background="#ECEBDD", relief="flat", foreground="#000000")
        light_style.map('light_button.TButton', background=[('active', '#D0D3D4')])

        enter_button = ttk.Style()
        enter_button.configure("enter_button.TButton", font="consolas 12 bold", background="#34A853", relief="flat", foreground="#FFFFFF")
        enter_button.map('enter_button.TButton', background=[('active', '#11742B')])

        pulse_button = ttk.Style()
        pulse_button.configure("pulse_button.TButton", font="consolas 12 bold", background="#660000", relief="flat", foreground="#FFFFFF")
        pulse_button.map('pulse_button.TButton', background=[('active', '#990000')])

        # Boton de cambio
        self.boton_change = ttk.Button(self, text=teclas[0][0], width=6, style="light_button.TButton", command=self.aux_button)
        self.boton_change.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)

        # Botón de x
        self.boton_x = ttk.Button(self, text=teclas[0][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('x'))
        self.boton_x.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de y
        self.boton_y = ttk.Button(self, text=teclas[0][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('y'))
        self.boton_y.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de C
        self.boton_c = ttk.Button(self, text=teclas[0][3], width=6, style="del_button.TButton", command=self.limpiar)
        self.boton_c.grid(row=2, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de borrar
        self.boton_limpiar = ttk.Button(self, text=teclas[0][4], width=6, style="del_button.TButton", command=self.borrar)
        self.boton_limpiar.grid(row=2, column=4, sticky="nsew", padx=2, pady=2)

        # Botón de sin
        self.boton_sin = ttk.Button(self, text=teclas[1][0], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('sin('))
        self.boton_sin.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de cos
        self.boton_cos = ttk.Button(self, text=teclas[1][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('cos('))
        self.boton_cos.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de tan
        self.boton_tan = ttk.Button(self, text=teclas[1][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('tan('))
        self.boton_tan.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de ans
        self.boton_ans = ttk.Button(self, text=teclas[1][3], width=6, style="oper_button.TButton", command=self.ans)
        self.boton_ans.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de /
        self.boton_division = ttk.Button(self, text=teclas[1][4], width=6, style="oper_button.TButton", command=lambda: self.ing_teclado('/'))
        self.boton_division.grid(row=3, column=4, sticky="nsew", padx=2, pady=2)

        # Botón de x^n
        self.boton_potencia = ttk.Button(self, text=teclas[2][0], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('^'))
        self.boton_potencia.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de (
        self.boton_apare = ttk.Button(self, text=teclas[2][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('('))
        self.boton_apare.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
            
        # Botón de )
        self.boton_cpare = ttk.Button(self, text=teclas[2][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado(')'))
        self.boton_cpare.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de |x|
        self.boton_abs = ttk.Button(self, text=teclas[2][3], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('abs('))
        self.boton_abs.grid(row=4, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de *
        self.boton_multi = ttk.Button(self, text=teclas[2][4], width=6, style="oper_button.TButton", command=lambda: self.ing_teclado('*'))
        self.boton_multi.grid(row=4, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de e
        self.boton_e = ttk.Button(self, text=teclas[3][0], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('e'))
        self.boton_e.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 7
        self.boton_7 = ttk.Button(self, text=teclas[3][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('7'))
        self.boton_7.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 8
        self.boton_8 = ttk.Button(self, text=teclas[3][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('8'))
        self.boton_8.grid(row=5, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 9
        self.boton_9 = ttk.Button(self, text=teclas[3][3], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('9'))
        self.boton_9.grid(row=5, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de -
        self.boton_resta = ttk.Button(self, text=teclas[3][4], width=6, style="oper_button.TButton", command=lambda: self.ing_teclado('-'))
        self.boton_resta.grid(row=5, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de root
        self.boton_root = ttk.Button(self, text=teclas[4][0], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('root(x,i)'))
        self.boton_root.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 4
        self.boton_4 = ttk.Button(self, text=teclas[4][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('4'))
        self.boton_4.grid(row=6, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 5
        self.boton_5 = ttk.Button(self, text=teclas[4][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('5'))
        self.boton_5.grid(row=6, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 6
        self.boton_6 = ttk.Button(self, text=teclas[4][3], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('6'))
        self.boton_6.grid(row=6, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de +
        self.boton_suma = ttk.Button(self, text=teclas[4][4], width=6, style="oper_button.TButton", command=lambda: self.ing_teclado('+'))
        self.boton_suma.grid(row=6, column=4, sticky="nsew", padx=2, pady=2)
        
        # Botón de log
        self.boton_log = ttk.Button(self, text=teclas[5][0], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('log(x,b)'))
        self.boton_log.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
        
        # Botón de 1
        self.boton_1 = ttk.Button(self, text=teclas[5][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('1'))
        self.boton_1.grid(row=7, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 2
        self.boton_2 = ttk.Button(self, text=teclas[5][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('2'))
        self.boton_2.grid(row=7, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de 3
        self.boton_3 = ttk.Button(self, text=teclas[5][3], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('3'))
        self.boton_3.grid(row=7, column=3, sticky="nsew", padx=2, pady=2)
        
        # Botón de enter
        self.boton_enter = ttk.Button(self, text=teclas[5][4], width=6, style="enter_button.TButton", command=self.result)
        self.boton_enter.grid(row=7, column=4, sticky="nsew", rowspan=2, padx=2, pady=2)
        
        # Botón de ln
        self.boton_ln = ttk.Button(self, text=teclas[6][0], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('ln('))
        self.boton_ln.grid(row=8, column=0, sticky="nsew", padx=2, pady=2)

        # Botón de pi
        self.boton_pi = ttk.Button(self, text=teclas[6][1], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('\u03C0'))
        self.boton_pi.grid(row=8, column=1, sticky="nsew", padx=2, pady=2)
        
        # Botón de 0
        self.boton_0 = ttk.Button(self, text=teclas[6][2], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('0'))
        self.boton_0.grid(row=8, column=2, sticky="nsew", padx=2, pady=2)
        
        # Botón de .
        self.boton_negativo = ttk.Button(self, text=teclas[6][3], width=6, style="light_button.TButton", command=lambda: self.ing_teclado('.'))
        self.boton_negativo.grid(row=8, column=3, sticky="nsew", padx=2, pady=2)

        self.btns_state = False  # ESTADO DEL BOTON ASOCIADO A CAMBIO

    def chg_state(self):
        self.btns_state = not(self.btns_state)
        if self.btns_state==True:
            self.boton_arc.configure(style="pulse_button.TButton")
            self.boton_nsin.configure(text='sin\u207b¹', command=lambda: self.ing_teclado('asin('))
            self.boton_ncos.configure(text='cos\u207b¹', command=lambda: self.ing_teclado('acos('))
            self.boton_ntan.configure(text='tan\u207b¹', command=lambda: self.ing_teclado('atan('))
            self.boton_csc.configure(text='csc\u207b¹', command=lambda: self.ing_teclado('acsc('))
            self.boton_sec.configure(text='sec\u207b¹', command=lambda: self.ing_teclado('asec('))
            self.boton_cot.configure(text='cot\u207b¹', command=lambda: self.ing_teclado('acot('))
        else:
            self.boton_arc.configure(style="light_button.TButton")
            self.boton_nsin.configure(text='sin', command=lambda: self.ing_teclado('sin('))
            self.boton_ncos.configure(text='cos', command=lambda: self.ing_teclado('cos('))
            self.boton_ntan.configure(text='tan', command=lambda: self.ing_teclado('tan('))
            self.boton_csc.configure(text='csc', command=lambda: self.ing_teclado('csc('))
            self.boton_sec.configure(text='sec', command=lambda: self.ing_teclado('sec('))
            self.boton_cot.configure(text='cot', command=lambda: self.ing_teclado('cot('))
            
    def aux_button(self):
        self.estado_aux = not(self.estado_aux)
        if self.estado_aux == True:
            self.boton_change.configure(style="pulse_button.TButton")
            # ---------BOTONES AUXILIARES----------------------#
            self.boton_nsin = ttk.Button(self,text='sin', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('sin('))
            self.boton_ncos = ttk.Button(self,text='cos', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('cos('))
            self.boton_ntan = ttk.Button(self,text='tan', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('tan('))
            self.boton_csc =  ttk.Button(self,text='csc', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('csc('))
            self.boton_sec =  ttk.Button(self,text='sec', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('sec('))
            self.boton_cot =  ttk.Button(self,text='cot', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('cot('))
            self.boton_fac =  ttk.Button(self,text='!', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('!'))
            self.boton_porc = ttk.Button(self,text='%', width=6, style="light_button.TButton", command=lambda: self.ing_teclado('%'))
            self.boton_arc =  ttk.Button(self,text='arc', width=6, style="light_button.TButton", command= self.chg_state)
            self.boton_arc.configure(style="light_button.TButton")
            self.boton_nsin.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_ncos.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
            self.boton_ntan.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
            self.boton_csc.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_sec.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
            self.boton_cot.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
            self.boton_arc.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_fac.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
            self.boton_porc.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
        else:
            self.boton_change.configure(style="light_button.TButton")
            self.boton_nsin.destroy()
            self.boton_ncos.destroy()
            self.boton_ntan.destroy()
            self.boton_csc.destroy()
            self.boton_sec.destroy()
            self.boton_cot.destroy()
            self.boton_arc.destroy()
            self.boton_fac.destroy()
            self.boton_porc.destroy()
        self.btns_state = False

    def ing_teclado(self, tecla):   # METODO DE INGRESO DE CARACTERES
        ind, tecla = entry(self.entrada_ecuacion.get(),tecla)   # LLAMADO A LA FUNCION ENTRY, RETORNA INDICE Y CARACTER A POSTEAR
        self.entrada_ecuacion.delete(ind)   # SE ELIMINA EL CARACTER QUE ESTE EN LA POSICION RETORNADA
        self.entrada_ecuacion.insert(ind, tecla)    # SE INSERTA EN LA POSICION INDICADA EL CARACTER DE RETORNO

    def result(self):
        ecu = self.entrada_ecuacion.get().strip() # OBTENEMOS EL STRING EN ENTRADA Y ELIMINAMOS LOS ESPACIOS EN BLANCO
        res = solver(ecu)
        if type(res) is int or type(res) is float:
            self.graficacion.destroy()
            self.columnconfigure(5, weight=0)
            self.resultado = ttk.Label(self, textvariable=self.ecuacion, font=('Arial', 18), justify='left')
            self.resultado.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=[0,5])
            self.ecuacion.set(res)
            if self.entrada_ecuacion.get() not in historial:
                historial.append(self.entrada_ecuacion.get())
            self.obtener_info()
            self.res = res
        elif type(res) is np.ndarray:
            self.res = ecu
            #-------------CONSTRUCCION DEL ESPACIO DE GRAFICACION-----------------------#
            #self.resultado.destroy()    # DESTRUIMOS EL LABEL DE RESULTADOS
            self.columnconfigure(5, weight=15)
            self.graficacion.destroy() # DESTRUIMOS EL LABEL DE GRAFICACION POR SI EXISTE UNO ANTERIORMENTE CREADO
            self.graficacion = tk.Canvas(self, width=100, height=100) # CONTRUIMOS EL ESPACIO PARA LA FIGURA A GENERAR
            self.graficacion.grid(row=0, column=5, rowspan=9, sticky="nsew", padx=5, pady=5) # SE UBICA DENTRO DE LA VENTANA
            self.figura = Figure(figsize=(4, 3), dpi=100)   # SE AGREGA FIGURA AL CANVAS GENERADO
            self.ax = self.figura.add_subplot(111)  # SE CONFIGURA LA DISPOSICION DE LA FIGURA DENTRO DEL CANVAS
            self.canvas = FigureCanvasTkAgg(self.figura, master=self.graficacion)   
            self.canvas.get_tk_widget().pack(side=tk.TOP, expand=1, fill=tk.BOTH)   # SE UBICA EN LA VENTANA
            self.tlb = NavigationToolbar2Tk(self.canvas, self.graficacion)  # AGREGAMOS LAS OPCIONES DE FIGURA DENTRO DEL CANVAS
            self.tlb.update()   # ACTUALIZAMOS LAS CONFIGURACIONES REALIZADAS

            #--------------DUBUJADO DE LA FIGURA GENERADA-------------------------------#
            x_values = np.linspace(-100, 100, 1000) # GENERAMOS LA LISTA DE LOS PUNTOS EN X PARA F(X)
            self.ax.plot(x_values, res, color=line_color) # DIBUJAMOS LA FIGURA
            self.ax.grid(grid_draw, which=name_dict[lineas], axis=name_dict[ejes])  # SE ACTIVA LA GRILLA
            self.ax.axhline(0, color='black', lw=0.5)
            self.ax.axvline(0, color='black', lw=0.5)
            self.ax.spines[["left", "bottom"]].set_position(("data", 0))
            self.ax.spines[["top", "right"]].set_visible(False)
            self.ax.set_xlim([xlim[0], xlim[1]])
            self.ax.set_ylim([ylim[0], ylim[1]])
            self.ax.set_xticks(range(int(xlim[0]), int(xlim[1])+1, 1))
            self.ax.set_yticks(range(int(ylim[0]), int(ylim[1])+1, 1))
            #self.ax.set_adjustable('datalim')
            
            self.canvas.draw()
            if self.entrada_ecuacion.get() not in historial:
                historial.append(self.entrada_ecuacion.get())
            self.obtener_info()
        else:
            self.ecuacion.set(res)

    def ans(self):
        ind, tecla = entry(self.entrada_ecuacion.get(),self.res)   # LLAMADO A LA FUNCION ENTRY, RETORNA INDICE Y CARACTER A POSTEAR
        self.entrada_ecuacion.delete(ind)   # SE ELIMINA EL CARACTER QUE ESTE EN LA POSICION RETORNADA
        self.entrada_ecuacion.insert(ind, tecla)    # SE INSERTA EN LA POSICION INDICADA EL CARACTER DE RETORNO
    
    def limpiar(self):
        self.entrada_ecuacion.delete(0, tk.END)
        self.graficacion.destroy()
        self.columnconfigure(5, weight=0)
        self.ecuacion.set('')
        self.resultado = ttk.Label(self, textvariable=self.ecuacion, font=('Arial', 18), justify='right')
        self.resultado.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=[0,5])

    def borrar(self):
        self.entrada = self.entrada_ecuacion.get()
        ind = len(self.entrada_ecuacion.get())
        self.entrada_ecuacion.delete(ind-1)

    def guardar(self):
        user = self.usuario.split('@') # OBTENEMOS EL USUARIO DEL EMAIL INGRESADO
        json_generator(user[0], historial)
    
    def syncr(self):
        user = self.usuario.split('@') # OBTENEMOS EL USUARIO DEL EMAIL INGRESADO
        user_edit(user[0], historial)

    def del_hist(self):
        historial.clear()
        self.entrada_ecuacion.configure(values=historial)
    
    def cerrar(self):
        self.destroy()
        Login()

    def cfg_calc(self):
        confg_calc()
        cfg = [decimales,angulo,formato] 
        calc_config(cfg)

    def cfg_graph(self):
        confg_graph()

    def obtener_info(self):
        print(historial)
        if len(historial)<=5:
            self.entrada_ecuacion.configure(values=historial)
        else:
            self.i+=1
            self.entrada_ecuacion.configure(values=historial[0+self.i:])
    
    def menu_tema_presionado(self):
        tema = self.tema_sel.get()
        if tema == 1:
            self.tema = 'light_button.TButton'
        elif tema == 2:
            self.tema = 'dark_button.TButton'

class Login(tk.Tk):
    def __init__(self):
        super().__init__()  # LA FUNCION SUPER() SIRVE PARA UTILIZAR METODOS DE LA CLASE PADRE, EN ESTE CASO DE LA CLASE Tk 

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
            Calculadora(user)
        else:
            messagebox.showinfo("Acceso Incorrecto", "Los datos ingresados no son correctos")

    def forg_passw(self):
        pass

    def reg_user(self):
        self.destroy()
        Form()

    def inv_entrar(self):
        self.destroy()
        Calculadora('None')

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


class confg_calc(Tk):
    def __init__(self):
        super().__init__()

        global angulo, formato, decimales
        # CONFIGURACION DE LA VENTANA Y SU ESTRUCTURA
        self.title('Configuración de calculo')
        self.configure(padx=5)
        self.iconbitmap(icono)
        self.resizable(False,False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # ZONA DE CAMBIOS DE CONFIGURACION
        self.etq_digitos = Label(self, text="Mostrar dígitos", fg="black", font=("Arial", 12))
        self.etq_digitos.grid(row=0, column=0, sticky="nsew", columnspan=2, pady=[10,5])

        self.etq_angulo = Label(self, text="Ángulo", fg="black", font=("Arial", 12))
        self.etq_angulo.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=[0,5])

        self.etq_formato = Label(self, text="Formato exponencial", fg="black", font=("Arial", 12))
        self.etq_formato.grid(row=2, column=0, sticky="nsew", columnspan=2, pady=[0,5])

        self.entry_digitos = ttk.Combobox(self, font=("Arial", 12), width=10, state="readonly", values=['Flotante 1','Flotante 2','Flotante 3',
                                                                                                        'Flotante 4','Flotante 5','Flotante 6',
                                                                                                        'Flotante 7','Flotante 8','Flotante 9',
                                                                                                        'Flotante 10','Flotante 11','Flotante 12'])
        self.entry_digitos.set(decimales)
        self.entry_digitos.grid(row=0,column=2, pady=[10,10])

        self.entry_angulo = ttk.Combobox(self, font=("Arial", 12), state="readonly", values=['Radián','Grado'], width=10)
        self.entry_angulo.set(angulo)
        self.entry_angulo.grid(row=1,column=2, pady=[0,10])
        
        self.entry_formato = ttk.Combobox(self, font=("Arial", 12), state="readonly", values=['Normal','Científico'], width=10)
        self.entry_formato.set(formato)
        self.entry_formato.grid(row=2,column=2, pady=[0,10])

        # BOTONES DE ACEPTAR O CANCELAR CONFIGURACION
        button_style2 = ttk.Style()
        button_style2.configure("button_style2.TButton", font=("Arial", 12))

        self.boton_rest = ttk.Button(self, text="Restaurar", cursor="hand2", style="button_style2.TButton", command=self.restore)
        self.boton_rest.grid(row=3, column=0, sticky="nsew", pady=[0, 5])

        self.boton_acep = ttk.Button(self, text="Aceptar", cursor="hand2", style="button_style2.TButton", command=self.confirm)
        self.boton_acep.grid(row=3, column=1, sticky="nsew", pady=[0, 5])

        self.boton_canc = ttk.Button(self, text="Cancelar", cursor="hand2", style="button_style2.TButton", command=self.destroy)
        self.boton_canc.grid(row=3, column=2, sticky="nsew", pady=[0, 5])

    def restore(self):
        self.entry_digitos.set("Flotante 6")
        self.entry_angulo.set("Radián")
        self.entry_formato.set("Normal")

    def confirm(self):
        global decimales, angulo, formato
        decimales = self.entry_digitos.get()
        angulo = self.entry_angulo.get()
        formato = self.entry_formato.get()
        self.destroy()


class confg_graph(Tk):
    def __init__(self):
        super().__init__()

        # CONFIGURACION DE LA VENTANA Y SU ESTRUCTURA
        self.title('Configuración de graficos')
        self.configure(padx=8)
        self.iconbitmap(icono)
        self.resizable(False,False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)

        # CONFIGURACION DE ESTILOS DE WIDGETS
        button_style2 = ttk.Style()
        button_style2.configure("button_style2.TButton", font=("Arial", 12))
        
        # CONFIGURACION DE GRILLA
        self.etq_grilla = Label(self, text="Grilla", fg= "black", font=("Arial", 14))
        self.etq_grilla.grid(row=0, column=0, sticky="nsew", columnspan=2, pady=[10,5])

        self.etq_mostrar = Label(self, text="Mostrar grilla", fg= "black", font=("Arial", 12))
        self.etq_mostrar.grid(row=1, column=0, sticky="nsew", pady=[0,5])

        self.etq_lineas = Label(self, text="Lineas", fg= "black", font=("Arial", 12))
        self.etq_lineas.grid(row=2, column=0, sticky="nsew", pady=[0,5])

        self.etq_ejes = Label(self, text="Ejes", fg= "black", font=("Arial", 12))
        self.etq_ejes.grid(row=3, column=0, sticky="nsew", pady=[0,5])

        self.chkbox_value = tk.BooleanVar(self)
        self.chkbox_value.set(grid_draw)
        self.chkbox_mostrar = Checkbutton(self, anchor="center", variable=self.chkbox_value)
        self.chkbox_mostrar.grid(row=1, column=1, sticky="nsew", pady=[0,5])

        self.entry_lineas = ttk.Combobox(self, font=("Arial", 12), state="readonly", values=['Mayor','Menor','Ambos'], width=10)
        self.entry_lineas.set(lineas)
        self.entry_lineas.grid(row=2, column=1, sticky="nsew", pady=[0,10])
        
        self.entry_ejes = ttk.Combobox(self, font=("Arial", 12), state="readonly", values=['X','Y','Ambos'], width=10)
        self.entry_ejes.set(ejes)
        self.entry_ejes.grid(row=3, column=1, sticky="nsew", pady=[0,10])
        
        # CONFIGURACION DE EJES
        self.etq_limites = Label(self, text="Limites de ejes", fg= "black", font=("Arial", 14))
        self.etq_limites.grid(row=4, column=0, sticky="nsew", columnspan=2, pady=[2,5])

        self.xframe = tk.Frame(self, background="gray")
        self.xframe.grid(row=5, column=0, sticky="nsew", pady=[0,5], columnspan=2)
        self.xframe.rowconfigure(0, weight=1)
        self.xframe.columnconfigure(0, weight=1)
        self.xframe.columnconfigure(1, weight=1)
        self.xframe.columnconfigure(2, weight=1)
        self.xframe.columnconfigure(3, weight=1)
        
        self.etq_xmin = Label(self.xframe, text="Xmin", fg= "black", font=("Arial", 12))
        self.etq_xmin.grid(row=0, column=0, sticky="nsew")

        self.entry_xmin_val = tk.DoubleVar(self.xframe, value=xlim[0])
        self.entry_xmin = Entry(self.xframe, font=("Arial", 12), textvariable=self.entry_xmin_val, width=4)
        self.entry_xmin.grid(row=0, column=1, sticky="nsew")

        self.etq_xmax = Label(self.xframe, text="Xmax", fg= "black", font=("Arial", 12))
        self.etq_xmax.grid(row=0, column=2, sticky="nsew")

        self.entry_xmax_val = tk.DoubleVar(self.xframe, value=xlim[1])
        self.entry_xmax = Entry(self.xframe, font=("Arial", 12), textvariable=self.entry_xmax_val, width=4)
        self.entry_xmax.grid(row=0, column=3, sticky="nsew")


        self.yframe = tk.Frame(self)
        self.yframe.grid(row=6, column=0, sticky="nsew", pady=[0,5], columnspan=2)
        self.yframe.rowconfigure(0, weight=1)
        self.yframe.columnconfigure(0, weight=1)
        self.yframe.columnconfigure(1, weight=1)
        self.yframe.columnconfigure(2, weight=1)
        self.yframe.columnconfigure(3, weight=1)

        self.etq_ymin = Label(self.yframe, text="Ymin", fg= "black", font=("Arial", 12))
        self.etq_ymin.grid(row=0, column=0, sticky="nsew")

        self.entry_ymin_val = tk.DoubleVar(self.yframe, value=ylim[0])
        self.entry_ymin = Entry(self.yframe, font=("Arial", 12), textvariable=self.entry_ymin_val, width=4)
        self.entry_ymin.grid(row=0, column=1, sticky="nsew")

        self.etq_ymax = Label(self.yframe, text="Ymax", fg= "black", font=("Arial", 12))
        self.etq_ymax.grid(row=0, column=2, sticky="nsew")

        self.entry_ymax_val = tk.DoubleVar(self.yframe, value=ylim[1])
        self.entry_ymax = Entry(self.yframe, font=("Arial", 12), textvariable=self.entry_ymax_val, width=4)
        self.entry_ymax.grid(row=0, column=3, sticky="nsew")
        
        # CONFIGURACION DE LINEA
        self.etq_estilo = Label(self, text="Estilo de linea", fg= "black", font=("Arial", 14))
        self.etq_estilo.grid(row=7, column=0, sticky="nsew", columnspan=2, pady=[2,5])

        self.font_color = tk.Frame(self)
        self.font_color.grid(row=8, column=0, sticky="nsew", pady=[0,5], columnspan=2)
        self.font_color.rowconfigure(0, weight=1)
        self.font_color.columnconfigure(0, weight=1)
        self.font_color.columnconfigure(1, weight=1)
        self.font_color.columnconfigure(2, weight=1)

        self.etq_color = Label(self.font_color, text="Color de trazo", fg= "black", font=("Arial", 12), width=5)
        self.etq_color.grid(row=0, column=0, sticky="nsew")

        self.lab_color = Label(self.font_color, fg= "black", background=line_color, relief="raised", height=1)
        self.lab_color.grid(row=0, column=1, sticky="nsew", padx=2, pady=5)

        self.button_color = ttk.Button(self.font_color, text="Cambiar", style="button_style2.TButton", command=self.pick_color, width=2)
        self.button_color.grid(row=0, column=2, sticky="nsew")

        # BOTONES DE ACEPTAR O CANCELAR CONFIGURACION
        self.font_boton = tk.Frame(self)
        self.font_boton.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=[0,5])
        self.font_boton.rowconfigure(0, weight=1)
        self.font_boton.columnconfigure(0, weight=1)
        self.font_boton.columnconfigure(1, weight=1)
        self.font_boton.columnconfigure(2, weight=1)

        self.boton_rest = ttk.Button(self.font_boton, text="Restaurar", cursor="hand2", style="button_style2.TButton", command=self.restore, width=12)
        self.boton_rest.grid(row=0,column=0, sticky="nsew")

        self.boton_acep = ttk.Button(self.font_boton, text="Aceptar", cursor="hand2", style="button_style2.TButton", command=self.confirm, width=12)
        self.boton_acep.grid(row=0,column=1, sticky="nsew")

        self.boton_canc = ttk.Button(self.font_boton, text="Cancelar", cursor="hand2", style="button_style2.TButton", command=self.destroy, width=12)
        self.boton_canc.grid(row=0,column=2, sticky="nsew")

    def pick_color(self):
        global line_color
        self.color = colorchooser.askcolor()[1]  # Ask the user to choose a color and get the hex code
        if self.color:
            self.lab_color.config(background=self.color)  # Set the foreground color of the Label
            line_color = self.color

    def restore(self):
        self.chkbox_value.set(True)
        self.entry_lineas.set("Ambos")
        self.entry_ejes.set("Ambos")
        self.entry_xmin_val.set(-20.0)
        self.entry_xmax_val.set(20.0)
        self.entry_ymin_val.set(-20.0)
        self.entry_ymax_val.set(20.0)
        self.lab_color.config(background="black")

    def confirm(self):
        global grid_draw, lineas, ejes, xlim, ylim, line_color
        grid_draw = self.chkbox_value.get()
        lineas = self.entry_lineas.get()
        ejes = self.entry_ejes.get()
        xlim[0] = self.entry_xmin_val.get()
        xlim[1] = self.entry_xmax_val.get()
        ylim[0] = self.entry_ymin_val.get()
        ylim[1] = self.entry_ymax_val.get()
        self.destroy()