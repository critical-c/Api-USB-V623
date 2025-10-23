# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de variables estratégicas
rutas_variable_estrategica = Blueprint("rutas_variable_estrategica", __name__)

# URL base de la API en C# que gestiona las variables estratégicas
API_URL = "http://localhost:5031/api/variable_estrategica"

# ------------------- LISTAR variable_estrategica -------------------
@rutas_variable_estrategica.route("/variable_estrategica")
def variable_estrategica():
    try:
        respuesta = requests.get(API_URL)
        variables_estrategicas = respuesta.json().get("datos", [])
    except Exception as e:
        variables_estrategicas = []
        print("Error al conectar con la API:", e)

    return render_template(
        "variables_estrategicas.html",
        variables_estrategicas=variables_estrategicas,
        variable_estrategica=None,
        modo="crear"
    )

# ------------------- BUSCAR variable_estrategica -------------------
@rutas_variable_estrategica.route("/variable_estrategica/buscar", methods=["POST"])
def buscar_variable_estrategica():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    variable_estrategica = datos[0]
                    variables_estrategicas = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "variables_estrategicas.html",
                        variables_estrategicas=variables_estrategicas,
                        variable_estrategica=variable_estrategica,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    variables_estrategicas = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "variables_estrategicas.html",
        variables_estrategicas=variables_estrategicas,
        variable_estrategica=None,
        mensaje="Variable estratégica no encontrada",
        modo="crear"
    )

# ------------------- CREAR variable_estrategica -------------------
@rutas_variable_estrategica.route("/variable_estrategica/crear", methods=["POST"])
def crear_variable_estrategica():
    datos = {
        "titulo": request.form.get("titulo"),
        "description": request.form.get("description")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la variable estratégica: {e}"

    return redirect(url_for("rutas_variable_estrategica.variable_estrategica"))

# ------------------- ACTUALIZAR variable_estrategica -------------------
@rutas_variable_estrategica.route("/variable_estrategica/actualizar", methods=["POST"])
def actualizar_variable_estrategica():
    codigo = request.form.get("id")
    datos = {
        "titulo": request.form.get("titulo"),
        "description": request.form.get("description")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar la variable estratégica: {e}"

    return redirect(url_for("rutas_variable_estrategica.variable_estrategica"))

# ------------------- ELIMINAR variable_estrategica -------------------
@rutas_variable_estrategica.route("/variable_estrategica/eliminar/<string:codigo>", methods=["POST"])
def eliminar_variable_estrategica(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar la variable estratégica: {e}"

    return redirect(url_for("rutas_variable_estrategica.variable_estrategica"))
