from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de estado_proyecto
rutas_estado_proyecto = Blueprint("rutas_estado_proyecto", __name__)

# URL base de la API en C# que gestiona estado_proyecto
API_URL = "http://localhost:5031/api/estado_proyecto"
API_PROYECTO = "http://localhost:5031/api/proyecto"
API_ESTADO = "http://localhost:5031/api/estado"
API_ESTADO_PROYECTO = "http://localhost:5031/api/view_estado_proyecto"

# ------------------- LISTAR estado_proyecto -------------------
@rutas_estado_proyecto.route("/estado_proyecto")
def estado_proyecto():
    try:
        estado_proyectos = requests.get(API_URL).json().get("datos", [])
        proyectos = requests.get(API_PROYECTO).json().get("datos", [])
        estado = requests.get(API_ESTADO).json().get("datos", [])
        estado_view = requests.get(API_ESTADO_PROYECTO).json().get("datos", [])
    except Exception as e:
        estado_proyectos, proyectos, estado, estado_view= [], [], [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "estado_proyecto.html",
        estado_view=estado_view,
        estado_proyectos=estado_proyectos,
        estado_proyecto=None,
        proyectos=proyectos,
        estado=estado,
        modo="crear"
    )

# ------------------- BUSCAR estado_proyecto -------------------
@rutas_estado_proyecto.route("/estado_proyecto/buscar", methods=["POST"])
def buscar_estado_proyecto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id_proyecto/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    estado_proyecto = datos[0]
                    estado_proyectos = requests.get(API_URL).json().get("datos", [])
                    proyectos = requests.get(API_PROYECTO).json().get("datos", [])
                    estado = requests.get(API_ESTADO).json().get("datos", [])
                    estado_view = requests.get(API_ESTADO_PROYECTO).json().get("datos", [])
                    return render_template(
                        "estado_proyecto.html",
                        estado_view=estado_view,
                        estado_proyecto=estado_proyecto,
                        proyectos=proyectos,
                        estado=estado,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"
    estado_proyectos = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "estado_proyecto.html",
        estado_proyectos=estado_proyectos,
        estado_proyecto=None,
        modo="crear"
    )

# ------------------- CREAR estado_proyecto -------------------
@rutas_estado_proyecto.route("/estado_proyecto/crear", methods=["POST"])
def crear_estado_proyecto():
    datos = {
        "id_proyecto": request.form.get("id_proyecto"),
        "id_estado": request.form.get("id_estado")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la relación estado-proyecto: {e}"

    return redirect(url_for("rutas_estado_proyecto.estado_proyecto"))

# ------------------- ACTUALIZAR estado_proyecto -------------------
@rutas_estado_proyecto.route("/estado_proyecto/actualizar", methods=["POST"])
def actualizar_estado_proyecto():
    codigo = request.form.get("id_proyecto")
    datos = {
        "id_proyecto": request.form.get("id_proyecto"),
        "id_estado": request.form.get("id_estado")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar la relación estado-proyecto: {e}"

    return redirect(url_for("rutas_estado_proyecto.estado_proyecto"))

# ------------------- ELIMINAR estado_proyecto -------------------
@rutas_estado_proyecto.route("/estado_proyecto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_estado_proyecto(codigo):
    try:
        requests.delete(f"{API_URL}/id_proyecto/{codigo}")
    except Exception as e:
        return f"Error al eliminar la relación estado-proyecto: {e}"

    return redirect(url_for("rutas_estado_proyecto.estado_proyecto"))
