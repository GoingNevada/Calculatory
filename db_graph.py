
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# DIRECCION DE ARCHIVOS ADICIONALES
key = "Proyecto_calcgrf/resources/graphic-calculator-db-firebase-adminsdk-i358v-e3aad94d63.json"
url = 'https://graphic-calculator-db-default-rtdb.firebaseio.com/'

def db_init():  # FUNCION DE INICIO DE LA DB
    # CARGO EL CERTIFICADO .JSON DE LA BD
    firebase_sdk = credentials.Certificate(key)
    # Hacemos referencia a la base de datos en tiempo real de firebase
    firebase_admin.initialize_app(firebase_sdk, {'databaseURL': url})
    
def user_creator(email,password): # FUNCION CREATE DE LA DB
    user = email.split('@')
    dir = "/"+user[0]  # CREAMOS UNA NUEVA COLECCION EN LA DB PARA EL NUEVO USUARIO
    ref = db.reference(dir) # ESPECIFICAMOS EN QUE DIRECCION VAMOS A ESCRIBIR
    ref.set({'user':email,'password':password,'historial': None}) # SUBIMOS LOS DATOS A LA BD
    return True

def user_check(email,password): # FUNCION READ DE LA DB
    ref = db.reference('/') # ESPECIFICAMOS EN QUE DIRECCION VAMOS A POSICIONARNOS
    data = ref.get() # OBTENERMOS LA INFORMACION DE LA DIRECCION SELECCIONADA
    user = email.split('@') # OBTENEMOS EL USUARIO DEL EMAIL INGRESADO
    for usuario in data:    # ITERAMOS EN EL DICCIONARIO OBTENIDO EN DATA PARA BUSCAR SI EXISTE EL USUARIO
        if usuario==user[0]:    # SI EL USUARIO EXISTE ENTONCES:
            if data[usuario]["user"]==email and data[usuario]["password"]==password: # CONFIRMAMOS LOS DATOS INGRESADOS
                return True # RETORNAMOS TRUE PARA CONFIRMAR EXITO EN EL INGRESO
            else:
                return False # RETORNAMOS FALSE PARA AVISAR DEL ERROR DE INGRESO

def user_edit(user, data):  # FUNCION UPDATE DE LA DB
    # Modificar un dato
    #self.ref = db.reference('Productos')
    #self.producto_ref = self.ref.child('-NtPAfD711oGpLZ68YLe')
    #self.producto_ref.update({'pulgadas':'10'})
    pass

def user_delete(user, data):  # FUNCION DELETE DE LA DB
    pass

def json_generator(data):
    # generamos un archivo
    archivo = 'file.json'

    datos = {}  # Declarar datos como un diccionario
    datos["sacamo"] = []    # lista dentro del diccionario
    datos["sacamo"].append({
        "user" : "sacamo@unal.edu.co",
        "password" : "abcdefg",
        "historial" : data
    })

    #datos["sacamo"][0]["ecuaciones"] = ["ecuacion 1", "ecuacion 2"]

    #ref = db.reference('/sacamo')
    #user_ref = ref.child('historial')
    #ref.update(["ecuacion 1", "ecuacion 2"])

    with open(archivo, "w") as file:
        json.dump(datos, file, indent=4)
