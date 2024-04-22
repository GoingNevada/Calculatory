
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#class db_graph():


def db_init():

    # Cargo el certificado de mi proyecto
    firebase_sdk = credentials.Certificate("graphic-calculator-db-firebase-adminsdk-i358v-e3aad94d63.json")

    # Hacemos referencia a la base de datos en tiempo real de firebase
    firebase_admin.initialize_app(firebase_sdk, {'databaseURL':'https://graphic-calculator-db-default-rtdb.firebaseio.com/'})

    # Creo una coleccion con el nombre de productos con un producto

    # Modificar un dato
    #self.ref = db.reference('Productos')
    #self.producto_ref = self.ref.child('-NtPAfD711oGpLZ68YLe')
    #self.producto_ref.update({'pulgadas':'10'})
    
def user_creator(data):
    ref = db.reference('/sacamo')
    ref.set({'user':'sacamo@unal.edu.co','password':'10212420','historial': data}) # Se sube a la base de datos

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
