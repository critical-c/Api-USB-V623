# ===============================================================
# Módulo: rutas_variable_estrategica.py
# Descripción: Maneja las rutas para listar, crear, buscar,
# actualizar y eliminar variables estratégicas. Se conecta a la API en C#.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_variable_estrategica = Blueprint("rutas_variable_estrategica", __name__)
API_URL = "http://localhost:5031/api/variable_estrategica"  # Endpoint base de la API

# ===============================================================
# RUTA: LISTAR VARIABLES ESTRATÉGICAS
# ===============================================================
@rutas_variable_estrategica.route("/variable_estrategica", methods=["GET"])
def listar_variable_estrategica():
    try:
        respuesta = requests.get(API_URL)
        variables = respuesta.json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        variables = []

    return render_template("variable_estrategica.html", variables=variables, variable=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR VARIABLE ESTRATÉGICA POR ID
# ===============================================================
@rutas_variable_estrategica.route("/variable_estrategica/buscar", methods=["POST"])
def buscar_variable_estrategica():
    codigo = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                variable = datos[0]
                variables = requests.get(API_URL).json().get("datos", [])
                return render_template("variable_estrategica.html", variables=variables, variable=variable, modo="actualizar")
    except Exception as e:
        print("Error al buscar variable estratégica:", e)

    variables = requests.get(API_URL).json().get("datos", [])
    return render_template("variable_estrategica.html", variables=variables, variable=None, mensaje="Variable estratégica no encontrada", modo="crear")


# ===============================================================
# RUTA: CREAR VARIABLE ESTRATÉGICA
# ===============================================================
@rutas_variable_estrategica.route("/variable_estrategica", methods=["POST"])
def crear_variable_estrategica():
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear variable estratégica: {e}"

    return redirect(url_for("rutas_variable_estrategica.listar_variable_estrategica"))


# ===============================================================
# RUTA: ACTUALIZAR VARIABLE ESTRATÉGICA
# ===============================================================
@rutas_variable_estrategica.route("/variable_estrategica/actualizar/<int:id>", methods=["POST"])
def actualizar_variable_estrategica(id):
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar variable estratégica: {e}"

    return redirect(url_for("rutas_variable_estrategica.listar_variable_estrategica"))


# ===============================================================
# RUTA: ELIMINAR VARIABLE ESTRATÉGICA
# ===============================================================
@rutas_variable_estrategica.route("/variable_estrategica/eliminar/<int:id>", methods=["POST"])
def eliminar_variable_estrategica(id):
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar variable estratégica: {e}"

    return redirect(url_for("rutas_variable_estrategica.listar_variable_estrategica"))
