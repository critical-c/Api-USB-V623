# ===============================================================
# Módulo: rutas_estado.py
# Descripción: Maneja las rutas para listar, crear, buscar,
# actualizar y eliminar estados. Se conecta a la API en C#.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_estado = Blueprint("rutas_estado", __name__)
API_URL = "http://localhost:5031/api/estado"  # Endpoint base de la API

# ===============================================================
# RUTA: LISTAR ESTADOS
# ===============================================================
@rutas_estado.route("/estado", methods=["GET"])
def listar_estado():
    try:
        respuesta = requests.get(API_URL)
        estados = respuesta.json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        estados = []

    return render_template("estado.html", estados=estados, estado=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR ESTADO POR ID
# ===============================================================
@rutas_estado.route("/estado/buscar", methods=["POST"])
def buscar_estado():
    codigo = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                estado = datos[0]
                estados = requests.get(API_URL).json().get("datos", [])
                return render_template("estado.html", estados=estados, estado=estado, modo="actualizar")
    except Exception as e:
        print("Error al buscar estado:", e)

    estados = requests.get(API_URL).json().get("datos", [])
    return render_template("estado.html", estados=estados, estado=None, mensaje="Estado no encontrado", modo="crear")


# ===============================================================
# RUTA: CREAR ESTADO
# ===============================================================
@rutas_estado.route("/estado", methods=["POST"])
def crear_estado():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear estado: {e}"

    return redirect(url_for("rutas_estado.listar_estado"))


# ===============================================================
# RUTA: ACTUALIZAR ESTADO
# ===============================================================
@rutas_estado.route("/estado/actualizar/<int:id>", methods=["POST"])
def actualizar_estado(id):
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar estado: {e}"

    return redirect(url_for("rutas_estado.listar_estado"))


# ===============================================================
# RUTA: ELIMINAR ESTADO
# ===============================================================
@rutas_estado.route("/estado/eliminar/<int:id>", methods=["POST"])
def eliminar_estado(id):
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar estado: {e}"

    return redirect(url_for("rutas_estado.listar_estado"))
