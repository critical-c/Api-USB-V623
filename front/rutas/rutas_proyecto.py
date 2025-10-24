from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_proyecto = Blueprint("rutas_proyecto", __name__)

# URLs base de las APIs en C#
API_PROYECTO_URL = "http://localhost:5031/api/proyecto"
API_TIPO_PROYECTO_URL = "http://localhost:5031/api/tipo_proyecto"
API_USUARIO_URL = "http://localhost:5031/api/usuario"

# ------------------- LISTAR PROYECTOS -------------------
@rutas_proyecto.route("/proyecto")
def proyecto():
    try:
        proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
    except Exception as e:
        print("Error al obtener proyectos:", e)
        proyectos = []

    try:
        tipos = requests.get(API_TIPO_PROYECTO_URL).json().get("datos", [])
    except:
        tipos = []

    try:
        usuarios = requests.get(API_USUARIO_URL).json().get("datos", [])
    except:
        usuarios = []

    return render_template(
        "proyecto.html",
        proyectos=proyectos,
        proyecto=None,
        tipos=tipos,
        usuarios=usuarios,
        modo="crear"
    )

# ------------------- BUSCAR PROYECTO -------------------
@rutas_proyecto.route("/proyecto/buscar", methods=["POST"])
def buscar_proyecto():
    id_buscar = request.form.get("id_buscar")

    if id_buscar:
        try:
            respuesta = requests.get(f"{API_PROYECTO_URL}/id/{id_buscar}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    proyecto = datos[0]
                    proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
                    tipos = requests.get(API_TIPO_PROYECTO_URL).json().get("datos", [])
                    usuarios = requests.get(API_USUARIO_URL).json().get("datos", [])
                    return render_template(
                        "proyecto.html",
                        proyectos=proyectos,
                        proyecto=proyecto,
                        tipos=tipos,
                        usuarios=usuarios,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
    return render_template(
        "proyecto.html",
        proyectos=proyectos,
        proyecto=None,
        mensaje="Proyecto no encontrado",
        modo="crear"
    )

# ------------------- CREAR PROYECTO -------------------
@rutas_proyecto.route("/proyecto/crear", methods=["POST"])
def crear_proyecto():
    datos = {
        "id_proyecto_padre": request.form.get("id_proyecto_padre"),
        "id_responsable": request.form.get("id_responsable"),
        "id_tipo_proyecto": request.form.get("id_tipo_proyecto"),
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion"),
        "ruta_logo": request.form.get("ruta_logo")
    }

    try:
        requests.post(API_PROYECTO_URL, json=datos)
    except Exception as e:
        return f"Error al crear proyecto: {e}"

    return redirect(url_for("rutas_proyecto.proyecto"))

# ------------------- ACTUALIZAR PROYECTO -------------------
@rutas_proyecto.route("/proyecto/actualizar", methods=["POST"])
def actualizar_proyecto():
    codigo = request.form.get("id")

    datos = {
        "id": codigo,
        "id_proyecto_padre": request.form.get("id_proyecto_padre"),
        "id_responsable": request.form.get("id_responsable"),
        "id_tipo_proyecto": request.form.get("id_tipo_proyecto"),
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion"),
        "ruta_logo": request.form.get("ruta_logo")
    }

    try:
        requests.put(f"{API_PROYECTO_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar proyecto: {e}"

    return redirect(url_for("rutas_proyecto.proyecto"))

# ------------------- ELIMINAR PROYECTO -------------------
@rutas_proyecto.route("/proyecto/eliminar/<string:id>", methods=["POST"])
def eliminar_proyecto(id):
    try:
        requests.delete(f"{API_PROYECTO_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar proyecto: {e}"

    return redirect(url_for("rutas_proyecto.proyecto"))
