# 🕵️‍♂️ CRUD de Casos de Robos  
Sistema de registro, gestión y visualización de casos de robo usando **Python**, **SQLite**, **Peewee** y **Folium**.

Este proyecto forma parte de una práctica académica donde se implementa un **CRUD completo**, exportaciones HTML y mapas interactivos, además del uso de un flujo de trabajo **Git Flow**.

## Funcionalidades principales

### Registrar casos
Guarda información de:
- Cédula  
- Nombre de la víctima  
- Fecha  
- Qué se robaron  
- Valor monetario  
- Dirección  
- Ubicación (Latitud y Longitud)

Incluye **validaciones completas** para evitar datos inválidos.

---

### Borrar casos  
Permite eliminar un caso del sistema con confirmación previa.

---

### Exportar todos los casos (Mapa interactivo)
Genera un archivo `index.html` con un **mapa Folium**, mostrando:
- Marcadores por cada caso
- Tooltip con los datos del robo
- Popup con detalles del incidente

---

### Exportar un caso a HTML  
Crea un archivo HTML individual con diseño básico usando Bootstrap.

---

### Actualizar casos  
Permite modificar cualquier campo.  
Si dejas un campo en blanco, se mantiene el valor anterior.

## Dependencias

Es necesario contar con Python instalado en el equipo

Asi como las librerias:

pip install peewee folium
pip install peewee

