from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de tipo_proyecto
rutas_tipo_proyecto = Blueprint("rutas_tipo_proyecto", __name__)

# URL base de la API en C# que gestiona los tipo_proyecto
API_URL = "http://localhost:5031/api/tipo_proyecto"

# ------------------- LISTAR tipo_proyecto -------------------
@rutas_tipo_proyecto.route("/tipo_proyecto")
def tipo_proyecto():

    try:
        respuesta = requests.get(API_URL)
        tipos_proyectos = respuesta.json().get("datos", [])
    except Exception as e:
        tipos_proyectos = []
        print("Error al conectar con la API:", e)

    return render_template(
        "tipo_proyectos.html",
        tipos_proyectos=tipos_proyectos,
        tipo_proyecto=None,
        modo="crear"
    )

# ------------------- BUSCAR tipo_proyecto -------------------
@rutas_tipo_proyecto.route("/tipo_proyecto/buscar", methods=["POST"])
def buscar_tipo_proyecto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    tipo_proyecto = datos[0]
                    tipos_proyectos = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "tipo_proyectos.html",
                        tipos_proyectos=tipos_proyectos,
                        tipo_proyecto=tipo_proyecto,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    tipos_proyectos = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "tipo_proyectos.html",
        tipos_proyectos=tipos_proyectos,
        tipo_proyecto=None,
        mensaje="Tipo de proyecto no encontrado",
        modo="crear"
    )

# ------------------- CREAR tipo_proyecto -------------------
@rutas_tipo_proyecto.route("/tipo_proyecto/crear", methods=["POST"])
def crear_tipo_proyecto():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el tipo de proyecto: {e}"

    return redirect(url_for("rutas_tipo_proyecto.tipo_proyecto"))

# ------------------- ACTUALIZAR tipo_proyecto -------------------
@rutas_tipo_proyecto.route("/tipo_proyecto/actualizar", methods=["POST"])
def actualizar_tipo_proyecto():
    codigo = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar tipo de proyecto: {e}"

    return redirect(url_for("rutas_tipo_proyecto.tipo_proyecto"))

# ------------------- ELIMINAR tipo_proyecto -------------------
@rutas_tipo_proyecto.route("/tipo_proyecto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_tipo_proyecto(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar tipo de proyecto: {e}"

    return redirect(url_for("rutas_tipo_proyecto.tipo_proyecto"))
