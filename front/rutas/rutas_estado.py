from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de estado
rutas_estado = Blueprint("rutas_estado", __name__)

# URL base de la API en C# que gestiona los estados
API_URL = "http://localhost:5031/api/estado"

# ------------------- LISTAR estado -------------------
@rutas_estado.route("/estado")
def estado():
    try:
        respuesta = requests.get(API_URL)
        estados = respuesta.json().get("datos", [])
    except Exception as e:
        estados = []
        print("Error al conectar con la API:", e)

    return render_template(
        "estados.html",
        estados=estados,
        estado=None,
        modo="crear"
    )

# ------------------- BUSCAR estado -------------------
@rutas_estado.route("/estado/buscar", methods=["POST"])
def buscar_estado():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    estado = datos[0]
                    estados = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "estados.html",
                        estados=estados,
                        estado=estado,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    estados = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "estados.html",
        estados=estados,
        estado=None,
        mensaje="Estado no encontrado",
        modo="crear"
    )

# ------------------- CREAR estado -------------------
@rutas_estado.route("/estado/crear", methods=["POST"])
def crear_estado():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el estado: {e}"

    return redirect(url_for("rutas_estado.estado"))

# ------------------- ACTUALIZAR estado -------------------
@rutas_estado.route("/estado/actualizar", methods=["POST"])
def actualizar_estado():
    codigo = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar estado: {e}"

    return redirect(url_for("rutas_estado.estado"))

# ------------------- ELIMINAR estado -------------------
@rutas_estado.route("/estado/eliminar/<string:codigo>", methods=["POST"])
def eliminar_estado(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar estado: {e}"

    return redirect(url_for("rutas_estado.estado"))
