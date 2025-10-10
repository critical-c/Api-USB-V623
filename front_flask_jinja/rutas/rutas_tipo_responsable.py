# ===============================================================
# Módulo: rutas_tipo_responsable.py
# Descripción: Maneja las rutas para listar, crear, buscar,
# actualizar y eliminar tipos de responsable. Se conecta a la API en C#.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_tipo_responsable = Blueprint("rutas_tipo_responsable", __name__)
API_URL = "http://localhost:5031/api/tipo_responsable"  # Endpoint base de la API

# ===============================================================
# RUTA: LISTAR TIPOS DE RESPONSABLE
# ===============================================================
@rutas_tipo_responsable.route("/tipo_responsable", methods=["GET"])
def listar_tipo_responsable():
    try:
        respuesta = requests.get(API_URL)
        tipos = respuesta.json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        tipos = []

    return render_template("tipo_responsable.html", tipos=tipos, tipo=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR TIPO DE RESPONSABLE POR ID
# ===============================================================
@rutas_tipo_responsable.route("/tipo_responsable/buscar", methods=["POST"])
def buscar_tipo_responsable():
    codigo = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                tipo = datos[0]
                tipos = requests.get(API_URL).json().get("datos", [])
                return render_template("tipo_responsable.html", tipos=tipos, tipo=tipo, modo="actualizar")
    except Exception as e:
        print("Error al buscar tipo de responsable:", e)

    tipos = requests.get(API_URL).json().get("datos", [])
    return render_template("tipo_responsable.html", tipos=tipos, tipo=None, mensaje="Tipo de responsable no encontrado", modo="crear")


# ===============================================================
# RUTA: CREAR TIPO DE RESPONSABLE
# ===============================================================
@rutas_tipo_responsable.route("/tipo_responsable", methods=["POST"])
def crear_tipo_responsable():
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear tipo de responsable: {e}"

    return redirect(url_for("rutas_tipo_responsable.listar_tipo_responsable"))


# ===============================================================
# RUTA: ACTUALIZAR TIPO DE RESPONSABLE
# ===============================================================
@rutas_tipo_responsable.route("/tipo_responsable/actualizar/<int:id>", methods=["POST"])
def actualizar_tipo_responsable(id):
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar tipo de responsable: {e}"

    return redirect(url_for("rutas_tipo_responsable.listar_tipo_responsable"))


# ===============================================================
# RUTA: ELIMINAR TIPO DE RESPONSABLE
# ===============================================================
@rutas_tipo_responsable.route("/tipo_responsable/eliminar/<int:id>", methods=["POST"])
def eliminar_tipo_responsable(id):
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar tipo de responsable: {e}"

    return redirect(url_for("rutas_tipo_responsable.listar_tipo_responsable"))
