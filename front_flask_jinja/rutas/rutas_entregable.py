# ===============================================================
# Módulo: rutas_entregable.py
# Descripción: Maneja las rutas para listar, crear, buscar,
# actualizar y eliminar entregables. Se conecta a la API en C#.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_entregable = Blueprint("rutas_entregable", __name__)
API_URL = "http://localhost:5031/api/entregable"  # Endpoint base de la API

# ===============================================================
# RUTA: LISTAR ENTREGABLES
# ===============================================================
@rutas_entregable.route("/entregable", methods=["GET"])
def listar_entregable():
    try:
        respuesta = requests.get(API_URL)
        entregables = respuesta.json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        entregables = []

    return render_template("entregable.html", entregables=entregables, entregable=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR ENTREGABLE POR ID
# ===============================================================
@rutas_entregable.route("/entregable/buscar", methods=["POST"])
def buscar_entregable():
    codigo = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                entregable = datos[0]
                entregables = requests.get(API_URL).json().get("datos", [])
                return render_template("entregable.html", entregables=entregables, entregable=entregable, modo="actualizar")
    except Exception as e:
        print("Error al buscar entregable:", e)

    entregables = requests.get(API_URL).json().get("datos", [])
    return render_template("entregable.html", entregables=entregables, entregable=None, mensaje="Entregable no encontrado", modo="crear")


# ===============================================================
# RUTA: CREAR ENTREGABLE
# ===============================================================
@rutas_entregable.route("/entregable", methods=["POST"])
def crear_entregable():
    datos = {
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear entregable: {e}"

    return redirect(url_for("rutas_entregable.listar_entregable"))


# ===============================================================
# RUTA: ACTUALIZAR ENTREGABLE
# ===============================================================
@rutas_entregable.route("/entregable/actualizar/<int:id>", methods=["POST"])
def actualizar_entregable(id):
    datos = {
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar entregable: {e}"

    return redirect(url_for("rutas_entregable.listar_entregable"))


# ===============================================================
# RUTA: ELIMINAR ENTREGABLE
# ===============================================================
@rutas_entregable.route("/entregable/eliminar/<int:id>", methods=["POST"])
def eliminar_entregable(id):
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar entregable: {e}"

    return redirect(url_for("rutas_entregable.listar_entregable"))
