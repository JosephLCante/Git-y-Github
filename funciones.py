# funciones.py (actualizado con validaciones)
from folium.map import Tooltip
import datos
from peewee import *
import os
import folium
import sqlite3
import webbrowser
import re
from datetime import datetime

# -----------------------
# Utilidades
# -----------------------
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def confirmar(prompt: str = "¿Confirmar? (s/n): ") -> bool:
    while True:
        r = input(prompt).strip().lower()
        if r in ("s", "si", "y", "yes"):
            return True
        if r in ("n", "no"):
            return False
        print("Responde 's' o 'n'.")

# -----------------------
# Validaciones
# -----------------------
def validar_texto(prompt: str, required: bool = True, max_len: int = 500) -> str:
    while True:
        valor = input(prompt).strip()
        if required and not valor:
            print("Este campo es obligatorio. Intenta de nuevo.")
            continue
        if not valor and not required:
            return ""
        if len(valor) > max_len:
            print(f"Demasiado largo (máx {max_len} caracteres).")
            continue
        return valor

def validar_nombre(prompt: str, required: bool = True) -> str:
    pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$")
    while True:
        valor = input(prompt).strip()
        if required and not valor:
            print("El nombre es obligatorio.")
            continue
        if not valor and not required:
            return ""
        if not pattern.match(valor):
            print("Nombre inválido: solo letras y espacios.")
            continue
        return valor

def validar_cedula(prompt: str, required: bool = True) -> str:
    # acepta solo dígitos entre 7 y 15
    pattern = re.compile(r"^\d{7,15}$")
    while True:
        valor = input(prompt).strip()
        if required and not valor:
            print("La cédula es obligatoria.")
            continue
        if not valor and not required:
            return ""
        if not pattern.match(valor):
            print("Cédula inválida. Debe contener solo dígitos (7-15).")
            continue
        return valor

def validar_fecha(prompt: str, required: bool = True, fmt: str = "%d/%m/%Y") -> str:
    while True:
        valor = input(prompt).strip()
        if required and not valor:
            print("La fecha es obligatoria.")
            continue
        if not valor and not required:
            return ""
        try:
            dt = datetime.strptime(valor, fmt)
            return dt.strftime(fmt)
        except ValueError:
            print(f"Formato inválido. Use {fmt} (ej: 31/12/2023).")

def validar_float(prompt: str, required: bool = True, minv: float = None) -> float:
    while True:
        valor = input(prompt).strip()
        if required and not valor:
            print("Este campo es obligatorio.")
            continue
        if not valor and not required:
            return None
        try:
            f = float(valor)
            if minv is not None and f < minv:
                print(f"El valor debe ser >= {minv}")
                continue
            return f
        except ValueError:
            print("Entrada inválida. Introduce un número (puede tener decimales).")

# -----------------------
# CRUD usando datos.robos (peewee)
# -----------------------
def Registrar():
    cls()
    print("=== Agregar caso ===")
    est = datos.robos()  

    # Validaciones claras antes de asignar
    est.Cedula = validar_cedula("Digite la cédula: ")
    est.Nombre = validar_nombre("Digite el nombre: ")
    est.fecha = validar_fecha("Digite la fecha (DD/MM/AAAA): ")
    est.que_se_robaron = validar_texto("Que se robaron: ")
    # valor monetario opcional, si se deja vacío se almacena como 0.0
    v = validar_float("Valor monetario (ej: 1500.50) - deja vacío si no aplica: ", required=False, minv=0.0)
    est.valor = v if v is not None else 0.0
    est.Direccion = validar_texto("Indique la direccion: ", required=False)

    # lat/lng son obligatorios aquí (si prefieres opcionales, cambia required=False)
    while True:
        try:
            lat_in = input("Digite la latitud (ej 18.5): ").strip()
            lng_in = input("Digite la longitud (ej -70.7): ").strip()
            if lat_in == "" or lng_in == "":
                print("Latitud y longitud son obligatorias. Si no las conoces, usa 0.0.")
                continue
            est.lat = float(lat_in)
            est.lng = float(lng_in)
            break
        except ValueError:
            print("Latitud/Longitud inválidas. Deben ser números (ej: 18.5, -70.7).")

    # Confirmación antes de guardar
    print("\nResumen del caso:")
    print(f" Cédula: {est.Cedula}")
    print(f" Nombre: {est.Nombre}")
    print(f" Fecha: {est.fecha}")
    print(f" Qué se robaron: {est.que_se_robaron}")
    print(f" Valor: {est.valor}")
    print(f" Dirección: {est.Direccion}")
    print(f" Lat: {est.lat} | Lng: {est.lng}")

    if confirmar("¿Guardar este caso? (s/n): "):
        try:
            est.save()
            print("Caso guardado correctamente.")
        except Exception as e:
            print("Error al guardar el caso:", e)
    else:
        print("Operación cancelada.")
    input("Presione Enter para continuar...")

def borrar():
    cls()
    print("=== Borrar caso ===")
    casos = datos.robos.select()
    if casos.count() == 0:
        input("No hay casos para borrar. Enter para continuar...")
        return

    for dat in casos:
        print(f"{dat.id}) {dat.Nombre}")

    while True:
        idx = input("Digite el ID del caso a eliminar: ").strip()
        if not idx.isdigit():
            print("ID inválido. Debe ser un número.")
            continue
        idx_int = int(idx)
        try:
            caso = datos.robos.get(datos.robos.id == idx_int)
        except datos.robos.DoesNotExist:
            print("No existe un caso con ese ID.")
            continue

        print(f"Has seleccionado: {caso.id}) {caso.Nombre} - {caso.que_se_robaron}")
        if confirmar("¿Desea borrar este caso definitivamente? (s/n): "):
            try:
                datos.robos.delete().where(datos.robos.id == idx_int).execute()
                print("Caso eliminado.")
            except Exception as e:
                print("Error al eliminar:", e)
        else:
            print("Operación cancelada.")
        break

    input("Enter para continuar...")

def exportall():
    cls()
    print("=== Exportar todos los casos (mapa) ===")
    mapa = folium.Map(location=[18.952389810390983, -70.54906852736485], zoom_start=8, control_scale=True)

    casos = datos.robos.select()
    if casos.count() == 0:
        print("No hay casos para exportar.")
        input("Enter para continuar...")
        return

    errores = 0
    for r in casos:
        try:
            lat = float(r.lat)
            lng = float(r.lng)
            dat = (f"Cedula: {r.Cedula}<br>Nombre: {r.Nombre}<br>Fecha: {r.fecha}<br>"
                   f"Que se robaron: {r.que_se_robaron}<br>Valor: {r.valor}<br>Direccion: {r.Direccion}")
            folium.Marker([lat, lng], popup=dat, tooltip=Tooltip(dat)).add_to(mapa)
        except Exception:
            errores += 1
            # saltar si lat/lng no son válidos

    filename = "index.html"
    mapa.save(filename)
    try:
        webbrowser.open(filename)
        print(f"Mapa generado en {filename}. (Errores en {errores} registros de ubicación)")
    except Exception as e:
        print("Mapa generado, pero no se pudo abrir automáticamente:", e)
    input("Enter para continuar...")

def exportar():
    cls()
    print("=== Exportar caso individual (HTML) ===")
    casos = datos.robos.select()
    if casos.count() == 0:
        input("No hay casos para exportar. Enter para continuar...")
        return

    for r in casos:
        print(f"{r.id}) {r.Nombre}")

    while True:
        idx = input("Seleccione el ID del usuario que quiera exportar: ").strip()
        if not idx.isdigit():
            print("ID inválido.")
            continue
        idx_int = int(idx)
        try:
            est = datos.robos.get(datos.robos.id == idx_int)
            break
        except datos.robos.DoesNotExist:
            print("No se encontró el caso con ese ID.")

    cedula = est.Cedula
    nombre = est.Nombre
    Fecha = est.fecha
    que_roba = est.que_se_robaron
    valor = est.valor
    direccion = est.Direccion

    html2 = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8"/>
        <title>Caso de robo - {nombre}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class='container py-4'>
            <h1>Caso de robo</h1>
            <hr/>
            <h4>Nombre: <small class="text-muted">{nombre}</small></h4>
            <h4>Cédula: <small class="text-muted">{cedula}</small></h4>
            <h4>Fecha: <small class="text-muted">{Fecha}</small></h4>
            <h4>Qué se robaron: <small class="text-muted">{que_roba}</small></h4>
            <h4>Valor: <small class="text-muted">{valor}</small></h4>
            <h4>Dirección: <small class="text-muted">{direccion}</small></h4>
        </div>
    </body>
    </html>
    """
    filename = f"caso_{idx_int}.html"
    try:
        with open(filename, "w", encoding="utf-8") as a:
            a.write(html2)
        webbrowser.open(filename)
        print(f"Caso exportado a {filename}")
    except Exception as e:
        print("Error al exportar:", e)
    input("Enter para continuar...")

def Actualizar():
    cls()
    print("=== Actualizar caso ===\n")

    casos = datos.robos.select()
    
    if casos.count() == 0:
        input("No hay casos registrados. Enter para continuar.")
        return

    for c in casos:
        print(f"{c.id}) {c.Nombre}")

    while True:
        idx = input("\nDigite el ID del caso a actualizar: ").strip()
        if not idx.isdigit():
            print("ID inválido. Debe ser numérico.")
            continue
        idx_int = int(idx)
        try:
            caso = datos.robos.get(datos.robos.id == idx_int)
            break
        except datos.robos.DoesNotExist:
            print("ID no válido. Intenta otra vez.")

    print("\n*** Deje en blanco para mantener el valor actual ***\n")

    def pedir_validado_nombre(etiqueta, valor_actual):
        nuevo = input(f"{etiqueta} (actual: {valor_actual}): ").strip()
        if nuevo == "":
            return valor_actual
        # validar formato nombre
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$")
        if not pattern.match(nuevo):
            print("Nombre inválido. Se mantiene el valor actual.")
            return valor_actual
        return nuevo

    def pedir_fecha(etiqueta, valor_actual):
        nuevo = input(f"{etiqueta} (actual: {valor_actual}): ").strip()
        if nuevo == "":
            return valor_actual
        try:
            dt = datetime.strptime(nuevo, "%d/%m/%Y")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            print("Formato de fecha inválido. Se mantiene el valor actual.")
            return valor_actual

    def pedir_float_opt(etiqueta, valor_actual):
        nuevo = input(f"{etiqueta} (actual: {valor_actual}): ").strip()
        if nuevo == "":
            return valor_actual
        try:
            f = float(nuevo)
            return f
        except ValueError:
            print("Valor numérico inválido. Se mantiene el valor actual.")
            return valor_actual

    def pedir_texto(etiqueta, valor_actual):
        nuevo = input(f"{etiqueta} (actual: {valor_actual}): ").strip()
        return valor_actual if nuevo == "" else nuevo

    # actualizar campos
    caso.Cedula = validar_cedula("Cédula (dejar en blanco para mantener): ", required=False) or caso.Cedula
    caso.Nombre = pedir_validado_nombre("Nombre", caso.Nombre)
    caso.fecha = pedir_fecha("Fecha (DD/MM/AAAA)", caso.fecha)
    caso.que_se_robaron = pedir_texto("Qué se robaron", caso.que_se_robaron)
    caso.valor = pedir_float_opt("Valor monetario", caso.valor)
    caso.Direccion = pedir_texto("Dirección", caso.Direccion)

    # lat/lng: intentar convertir, si invalido, mantener
    lat_input = input(f"Latitud (actual: {caso.lat}): ").strip()
    lng_input = input(f"Longitud (actual: {caso.lng}): ").strip()
    try:
        if lat_input != "":
            caso.lat = float(lat_input)
        if lng_input != "":
            caso.lng = float(lng_input)
    except ValueError:
        print("Lat/Long inválidas. Se mantienen los valores actuales.")

    try:
        caso.save()
        print("Caso actualizado correctamente.")
    except Exception as e:
        print("Error al guardar los cambios:", e)

    input("Enter para continuar...")

