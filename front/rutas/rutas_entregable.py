# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests
from datetime import datetime

# Crear el Blueprint de entregables
rutas_entregable = Blueprint("rutas_entregable", __name__)

# URL base de la API en C# que gestiona los entregables
API_URL = "http://localhost:5031/api/entregable"


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
# ------------------- LISTAR entregable -------------------
@rutas_entregable.route("/entregable")
def entregable():
    try:
        respuesta = requests.get(API_URL)
        entregables = respuesta.json().get("datos", [])
    except Exception as e:
        entregables = []
        print("Error al conectar con la API:", e)

    return render_template(
        "entregables.html",
        entregables=entregables,
        entregable=None,
        modo="crear"
    )


# ------------------- BUSCAR entregable -------------------
@rutas_entregable.route("/entregable/buscar", methods=["POST"])
def buscar_entregable():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    entregable = datos[0]
                    entregable["fecha_inicio"] = formatear_fecha(entregable.get("fecha_inicio"))
                    entregable["fecha_fin_prevista"] = formatear_fecha(entregable.get("fecha_fin_prevista"))
                    entregable["fecha_modificacion"] = formatear_fecha(entregable.get("fecha_modificacion"))
                    entregable["fecha_finalizacion"] = formatear_fecha(entregable.get("fecha_finalizacion"))
                    entregables = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "entregables.html",
                        entregables=entregables,
                        entregable=entregable,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    entregables = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "entregables.html",
        entregables=entregables,
        entregable=None,
        mensaje="Entregable no encontrado",
        modo="crear"
    )

# ------------------- CREAR entregable -------------------
@rutas_entregable.route("/entregable/crear", methods=["POST"])
def crear_entregable():
    datos = {
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el entregable: {e}"

    return redirect(url_for("rutas_entregable.entregable"))

# ------------------- ACTUALIZAR entregable -------------------
@rutas_entregable.route("/entregable/actualizar", methods=["POST"])
def actualizar_entregable():
    codigo = request.form.get("id")
    datos = {
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": datetime.now().strftime("%Y-%m-%d"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar entregable: {e}"

    return redirect(url_for("rutas_entregable.entregable"))

# ------------------- ELIMINAR entregable -------------------
@rutas_entregable.route("/entregable/eliminar/<string:codigo>", methods=["POST"])
def eliminar_entregable(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar entregable: {e}"

    return redirect(url_for("rutas_entregable.entregable"))
