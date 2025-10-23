from flask import Blueprint, render_template, request, redirect, url_for
import requests
from datetime import datetime

# Crear el Blueprint de meta_proyecto
rutas_meta_proyecto = Blueprint("rutas_meta_proyecto", __name__)

# URL base de la API en C# que gestiona meta_proyecto
API_URL = "http://localhost:5031/api/meta_proyecto"
API_META_ESTRATEGICA = "http://localhost:5031/api/meta_estrategica"
API_PROYECTO = "http://localhost:5031/api/proyecto"

def formatear_fecha(fecha_str):
    """
    Convierte una fecha a formato YYYY-MM-DD compatible con <input type="date">.
    Acepta fechas como '2025-10-08', '08-10-2025' o '2025-10-08T00:00:00'.
    """
    if not fecha_str:
        return ""
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""

# ------------------- LISTAR meta_proyecto -------------------
@rutas_meta_proyecto.route("/meta_proyecto")
def meta_proyecto():
    try:
        metas_proyecto = requests.get(API_URL).json().get("datos", [])
        metas_estrategica = requests.get(API_META_ESTRATEGICA).json().get("datos", [])
        proyectos = requests.get(API_PROYECTO).json().get("datos", [])
    except Exception as e:
        metas_proyecto, metas_estrategica, proyectos= [], [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "meta_proyecto.html",
        metas_proyecto=metas_proyecto,
        meta_proyecto=None,
        metas_estrategica= metas_estrategica,
        proyectos=proyectos,
        modo="crear"
    )

# ------------------- BUSCAR meta_proyecto -------------------
@rutas_meta_proyecto.route("/meta_proyecto/buscar", methods=["POST"])
def buscar_meta_proyecto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id_meta/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    datos[0]["fecha_asociacion"] = formatear_fecha(datos[0].get("fecha_asociacion"))
                    meta_proyecto = datos[0]
                    metas_proyecto = requests.get(API_URL).json().get("datos", [])
                    metas_estrategica = requests.get(API_META_ESTRATEGICA).json().get("datos", [])
                    proyectos = requests.get(API_PROYECTO).json().get("datos", [])
                    return render_template(
                        "meta_proyecto.html",
                        metas_proyecto=metas_proyecto,
                        meta_proyecto=meta_proyecto,
                        metas_estrategica=metas_estrategica,
                        proyectos=proyectos,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    metas_proyecto = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "meta_proyecto.html",
        metas_proyecto=metas_proyecto,
        meta_proyecto=None,
        mensaje="Meta-Proyecto no encontrada",
        modo="crear"
    )

# ------------------- CREAR meta_proyecto -------------------
@rutas_meta_proyecto.route("/meta_proyecto/crear", methods=["POST"])
def crear_meta_proyecto():
    datos = {
        "id_meta": request.form.get("id_meta"),
        "id_proyecto": request.form.get("id_proyecto"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la relación meta-proyecto: {e}"

    return redirect(url_for("rutas_meta_proyecto.meta_proyecto"))

# ------------------- ACTUALIZAR meta_proyecto -------------------
@rutas_meta_proyecto.route("/meta_proyecto/actualizar", methods=["POST"])
def actualizar_meta_proyecto():
    codigo = request.form.get("id_meta")
    datos = {
        "id_meta": request.form.get("id_meta"),
        "id_proyecto": request.form.get("id_proyecto"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.put(f"{API_URL}/id_meta/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar la relación meta-proyecto: {e}"

    return redirect(url_for("rutas_meta_proyecto.meta_proyecto"))

# ------------------- ELIMINAR meta_proyecto -------------------
@rutas_meta_proyecto.route("/meta_proyecto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_meta_proyecto(codigo):
    try:
        requests.delete(f"{API_URL}/id_meta/{codigo}")
    except Exception as e:
        return f"Error al eliminar la relación meta-proyecto: {e}"

    return redirect(url_for("rutas_meta_proyecto.meta_proyecto"))
