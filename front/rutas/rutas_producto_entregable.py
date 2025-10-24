from flask import Blueprint, render_template, request, redirect, url_for
import requests
from datetime import datetime

rutas_producto_entregable = Blueprint("rutas_producto_entregable", __name__)

# URLs de las APIs (ajusta los puertos o nombres si es necesario)
API_PRODUCTO_ENTREGABLE_URL = "http://localhost:5031/api/producto_entregable"
API_PRODUCTO_URL = "http://localhost:5031/api/producto"
API_ENTREGABLE_URL = "http://localhost:5031/api/entregable"

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
# ------------------- LISTAR asociaciones -------------------
@rutas_producto_entregable.route("/producto_entregable")
def producto_entregable():
    try:
        asociaciones = requests.get(API_PRODUCTO_ENTREGABLE_URL).json().get("datos", [])
        productos = requests.get(API_PRODUCTO_URL).json().get("datos", [])
        entregables = requests.get(API_ENTREGABLE_URL).json().get("datos", [])
    except Exception as e:
        asociaciones, productos, entregables = [], [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "producto_entregable.html",
        asociaciones=asociaciones,
        asociacion=None,
        productos=productos,
        entregables=entregables,
        modo="crear"
    )


# ------------------- BUSCAR -------------------
@rutas_producto_entregable.route("/producto_entregable/buscar", methods=["POST"])
def buscar_producto_entregable():
    id_buscar = request.form.get("codigo_buscar")

    try:
        respuesta = requests.get(f"{API_PRODUCTO_ENTREGABLE_URL}/id_producto/{id_buscar}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                asociacion = datos[0]
                asociacion["fecha_asociacion"] = formatear_fecha(asociacion.get("fecha_asociacion"))
                asociaciones = requests.get(API_PRODUCTO_ENTREGABLE_URL).json().get("datos", [])
                productos = requests.get(API_PRODUCTO_URL).json().get("datos", [])
                entregables = requests.get(API_ENTREGABLE_URL).json().get("datos", [])
                return render_template(
                    "producto_entregable.html",
                    asociaciones=asociaciones,
                    asociacion=asociacion,
                    productos=productos,
                    entregables=entregables,
                    modo="actualizar"
                )
    except Exception as e:
        print("Error al buscar asociación:", e)

    return redirect(url_for("rutas_producto_entregable.producto_entregable"))


# ------------------- CREAR -------------------
@rutas_producto_entregable.route("/producto_entregable/crear", methods=["POST"])
def crear_producto_entregable():
    datos = {
        "id_producto": request.form.get("id_producto"),
        "id_entregable": request.form.get("id_entregable"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.post(API_PRODUCTO_ENTREGABLE_URL, json=datos)
    except Exception as e:
        print("Error al crear asociación:", e)

    return redirect(url_for("rutas_producto_entregable.producto_entregable"))


# ------------------- ACTUALIZAR -------------------
@rutas_producto_entregable.route("/producto_entregable/actualizar", methods=["POST"])
def actualizar_producto_entregable():
    codigo = request.form.get("id_producto")
    datos = {
        "id_producto": codigo,
        "id_entregable": request.form.get("id_entregable"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.put(f"{API_PRODUCTO_ENTREGABLE_URL}/id/{codigo}", json=datos)
    except Exception as e:
        print("Error al actualizar asociación:", e)

    return redirect(url_for("rutas_producto_entregable.producto_entregable"))


# ------------------- ELIMINAR -------------------
@rutas_producto_entregable.route("/producto_entregable/eliminar/<string:codigo>", methods=["POST"])
def eliminar_producto_entregable(codigo):
    try:
        requests.delete(f"{API_PRODUCTO_ENTREGABLE_URL}/id/{codigo}")
    except Exception as e:
        print("Error al eliminar asociación:", e)

    return redirect(url_for("rutas_producto_entregable.producto_entregable"))
