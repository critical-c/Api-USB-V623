# ===============================================================
# Módulo: rutas_tipo_proyecto.py
# Descripción: Maneja las rutas para listar, crear, buscar,
# actualizar y eliminar tipos de proyecto. Se conecta a la API en C#.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_tipo_proyecto = Blueprint("rutas_tipo_proyecto", __name__)
API_URL = "http://localhost:5031/api/tipo_proyecto"  # Endpoint base de la API

# ===============================================================
# RUTA: LISTAR TIPOS DE PROYECTO
# ===============================================================
@rutas_tipo_proyecto.route("/tipo_proyecto", methods=["GET"])
def listar_tipo_proyecto():
    try:
        respuesta = requests.get(API_URL)
        tipos = respuesta.json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        tipos = []

    return render_template("tipo_proyecto.html", tipos=tipos, tipo=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR TIPO DE PROYECTO POR ID
# ===============================================================
@rutas_tipo_proyecto.route("/tipo_proyecto/buscar", methods=["POST"])
def buscar_tipo_proyecto():
    codigo = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                tipo = datos[0]
                tipos = requests.get(API_URL).json().get("datos", [])
                return render_template("tipo_proyecto.html", tipos=tipos, tipo=tipo, modo="actualizar")
    except Exception as e:
        print("Error al buscar tipo de proyecto:", e)

    tipos = requests.get(API_URL).json().get("datos", [])
    return render_template("tipo_proyecto.html", tipos=tipos, tipo=None, mensaje="Tipo de proyecto no encontrado", modo="crear")


# ===============================================================
# RUTA: CREAR TIPO DE PROYECTO
# ===============================================================
@rutas_tipo_proyecto.route("/tipo_proyecto", methods=["POST"])
def crear_tipo_proyecto():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear tipo de proyecto: {e}"

    return redirect(url_for("rutas_tipo_proyecto.listar_tipo_proyecto"))


# ===============================================================
# RUTA: ACTUALIZAR TIPO DE PROYECTO
# ===============================================================
@rutas_tipo_proyecto.route("/tipo_proyecto/actualizar/<int:id>", methods=["POST"])
def actualizar_tipo_proyecto(id):
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar tipo de proyecto: {e}"

    return redirect(url_for("rutas_tipo_proyecto.listar_tipo_proyecto"))


# ===============================================================
# RUTA: ELIMINAR TIPO DE PROYECTO
# ===============================================================
@rutas_tipo_proyecto.route("/tipo_proyecto/eliminar/<int:id>", methods=["POST"])
def eliminar_tipo_proyecto(id):
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar tipo de proyecto: {e}"

    return redirect(url_for("rutas_tipo_proyecto.listar_tipo_proyecto"))
