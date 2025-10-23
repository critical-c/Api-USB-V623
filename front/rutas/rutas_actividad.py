from flask import Blueprint, render_template, request, redirect, url_for
import requests
from datetime import datetime

# Crear el Blueprint de actividad
rutas_actividad = Blueprint("rutas_actividad", __name__)

# URL base de la API en C# que gestiona las actividades
API_URL = "http://localhost:5031/api/actividad"
API_ENTREGABLE = "http://localhost:5031/api/entregable"

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

# ------------------- LISTAR actividad -------------------
@rutas_actividad.route("/actividad")
def actividad():
    try:
        actividades = requests.get(API_URL).json().get("datos", [])
        entregable = requests.get(API_ENTREGABLE).json().get("datos", [])
    except Exception as e:
        actividades, entregable = [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "actividades.html",
        actividades=actividades,
        actividad=None,
        entregable=entregable,
        modo="crear"
    )

# ------------------- BUSCAR actividad -------------------
@rutas_actividad.route("/actividad/buscar", methods=["POST"])
def buscar_actividad():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    actividad = datos[0]
                    actividad["fecha_inicio"] = formatear_fecha(datos[0].get("fecha_inicio"))
                    actividad["fecha_fin_prevista"] = formatear_fecha(datos[0].get("fecha_fin_prevista"))
                    actividad["fecha_modificacion"] = formatear_fecha(datos[0].get("fecha_modificacion"))
                    actividad["fecha_finalizacion"] = formatear_fecha(datos[0].get("fecha_finalizacion"))
                    actividades = requests.get(API_URL).json().get("datos", [])
                    entregable = requests.get(API_ENTREGABLE).json().get("datos", [])
                    return render_template(
                        "actividades.html",
                        actividades=actividades,
                        actividad=actividad,
                        entregable=entregable,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    actividades = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "actividades.html",
        actividades=actividades,
        actividad=None,
        mensaje="Actividad no encontrada",
        modo="crear"
    )

# ------------------- CREAR actividad -------------------
@rutas_actividad.route("/actividad/crear", methods=["POST"])
def crear_actividad():
    datos = {
        "id_entregable": request.form.get("id_entregable"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio") or None,
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista") or None,
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None,
        "prioridad": request.form.get("prioridad") or None,
        "porcentaje_avance": request.form.get("porcentaje_avance")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la actividad: {e}"

    return redirect(url_for("rutas_actividad.actividad"))

# ------------------- ACTUALIZAR actividad -------------------
@rutas_actividad.route("/actividad/actualizar", methods=["POST"])
def actualizar_actividad():
    codigo = request.form.get("id")
    datos = {
        "id_entregable": request.form.get("id_entregable"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion") or None,
        "fecha_inicio": request.form.get("fecha_inicio") or None,
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista") or None,
        "fecha_modificacion": datetime.now().strftime("%Y-%m-%d"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None,
        "prioridad": request.form.get("prioridad") or None,
        "porcentaje_avance": request.form.get("porcentaje_avance")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar actividad: {e}"

    return redirect(url_for("rutas_actividad.actividad"))

# ------------------- ELIMINAR actividad -------------------
@rutas_actividad.route("/actividad/eliminar/<string:codigo>", methods=["POST"])
def eliminar_actividad(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar actividad: {e}"

    return redirect(url_for("rutas_actividad.actividad"))
