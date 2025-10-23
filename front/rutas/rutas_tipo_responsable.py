from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de tipo_responsable
rutas_tipo_responsable = Blueprint("rutas_tipo_responsable", __name__)

# URL base de la API en C# que gestiona los tipo_responsable
API_URL = "http://localhost:5031/api/tipo_responsable"

# ------------------- LISTAR tipo_responsable -------------------
@rutas_tipo_responsable.route("/tipo_responsable")
def tipo_responsable():

    try:
        respuesta = requests.get(API_URL)
        tipos_responsables = respuesta.json().get("datos", [])
    except Exception as e:
        tipos_responsables = []
        print("Error al conectar con la API:", e)

    return render_template(
        "tipo_responsables.html",
        tipos_responsables=tipos_responsables,
        tipo_responsable=None,
        modo="crear"
    )

# ------------------- BUSCAR tipo_responsable -------------------
@rutas_tipo_responsable.route("/tipo_responsable/buscar", methods=["POST"])
def buscar_tipo_responsable():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    tipo_responsable = datos[0]
                    tipos_responsables = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "tipo_responsables.html",
                        tipos_responsables=tipos_responsables,
                        tipo_responsable=tipo_responsable,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    tipos_responsables = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "tipo_responsables.html",
        tipos_responsables=tipos_responsables,
        tipo_responsable=None,
        mensaje="Tipo de responsable no encontrado",
        modo="crear"
    )

# ------------------- CREAR tipo_responsable -------------------
@rutas_tipo_responsable.route("/tipo_responsable/crear", methods=["POST"])
def crear_tipo_responsable():
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el tipo de responsable: {e}"

    return redirect(url_for("rutas_tipo_responsable.tipo_responsable"))

# ------------------- ACTUALIZAR tipo_responsable -------------------
@rutas_tipo_responsable.route("/tipo_responsable/actualizar", methods=["POST"])
def actualizar_tipo_responsable():
    codigo = request.form.get("id")
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar tipo de responsable: {e}"

    return redirect(url_for("rutas_tipo_responsable.tipo_responsable"))

# ------------------- ELIMINAR tipo_responsable -------------------
@rutas_tipo_responsable.route("/tipo_responsable/eliminar/<string:codigo>", methods=["POST"])
def eliminar_tipo_responsable(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar tipo de responsable: {e}"

    return redirect(url_for("rutas_tipo_responsable.tipo_responsable"))
