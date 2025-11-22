from folium.map import Tooltip
import datos
from peewee import *
import os
import folium
import os
import sqlite3
import webbrowser

def cls():
     os.system('cls')

def Registrar():
    cls()
    print("Agregar caso  ") 
    est = datos.robos()  
    est.Cedula = input("Digite la cedula: ")
    est.Nombre = input("Digite el nombre: ")
    est.fecha= (input("Digite la fecha: "))
    est.que_se_robaron = input("Que se robaron: ")
    est.valor =  (input('Valor monetario: '))
    est.Direccion = (input("Indique la direccion: "))
    est.lat = (float(input("Digite la latidud: ")))
    est.lng = (float(input("Digite la longitud: ")))
    input("Listo,presione enter para continuar ")
    est.save()

def borrar():
    cls()
    for dat in datos.robos.select():
        print (f"{dat.id}) {dat.Nombre}")
    idx = input ("Digite el codigo del caso a eliminar : ")
    datos.robos.delete().where(datos.robos.id == idx).execute()
    input ("Eliminada!")

def exportall():
    mapa = folium.Map(location = [18.952389810390983, -70.54906852736485], zoom_start=8, control_scale=True )

    for robos in datos.robos.select():
        dat = (f"Cedula: {robos.Cedula}<br>Nombre: {robos.Nombre}<br>Fecha: {robos.fecha}<br>Que se robaron :{robos.que_se_robaron}<br>Valor:{robos.valor}<br>Direccion:{robos.Direccion} ")
        folium.Marker(
        [(f"{robos.lat}"),(f"{robos.lng}")], popup=dat, tooltip=dat).add_to(mapa)

    mapa.save("index.html")
    os.system('index.html')

def exportar():
    cls()
    for robos in datos.robos.select():
        print(f"{robos.id}){robos.Nombre}")
    idx = input ("Seleccione el usuario que quiera exportar")
    
    est = datos.robos.get(datos.robos.id == idx)
    cedula = est.Cedula
    nombre = est.Nombre
    Fecha = est.fecha
    que_roba = est.que_se_robaron
    valor = est.valor
    direccion = est.Direccion

    html2 = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Document</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class='container'>
            <h1><i>Caso de robo<i></h1>
            <h2><i>Nombre:{nombre}</i></h2>
            <h2><i>Cedula:{cedula}</i></h2>
            <h2><i>Fecha:{Fecha}</i></h2>
            <h2><i>Que se robaron:{que_roba}</i></h2>
            <h2><i>Valor:{valor}</i></h2>
            <h2><i>Direccion:{direccion}</i></h2>
        </div>
    </body>
    </html>
    """
    a = open('exportar1.html','w')     
    a.write(html2)
    a.close()
    webbrowser.open('exportar1.html')

def Actualizar():
    cls()
    print("=== Actualizar caso ===\n")

    casos = datos.robos.select()

    if casos.count() == 0:
        input("No hay casos registrados. Enter para continuar.")
        return

    for c in casos:
        print(f"{c.id}) {c.Nombre}")

    idx = input("\nDigite el ID del caso a actualizar: ")

    try:
        caso = datos.robos.get(datos.robos.id == idx)
    except:
        input("ID no válido. Enter para continuar.")
        return

    print("\n*** Deje en blanco para mantener el valor actual ***\n")

    def pedir(etiqueta, valor_actual):
        nuevo = input(f"{etiqueta} (actual: {valor_actual}): ")
        return valor_actual if nuevo == "" else nuevo

    caso.Cedula = pedir("Cédula", caso.Cedula)
    caso.Nombre = pedir("Nombre", caso.Nombre)
    caso.fecha = pedir("Fecha", caso.fecha)
    caso.que_se_robaron = pedir("Qué se robaron", caso.que_se_robaron)
    caso.valor = pedir("Valor", caso.valor)
    caso.Direccion = pedir("Dirección", caso.Direccion)

    try:
        caso.lat = float(pedir("Latitud", caso.lat))
        caso.lng = float(pedir("Longitud", caso.lng))
    except:
        pass

    caso.save()

    input("Caso actualizado correctamente. Enter para continuar.")
