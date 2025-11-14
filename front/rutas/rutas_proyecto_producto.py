from flask import Blueprint, render_template, request, redirect, url_for
import requests
from datetime import datetime

rutas_proyecto_producto = Blueprint("rutas_proyecto_producto", __name__)

# APIs C#
API_PROYECTO_PRODUCTO_URL = "http://localhost:5031/api/proyecto_producto"
API_PROYECTO_URL = "http://localhost:5031/api/proyecto"
API_PRODUCTO_URL = "http://localhost:5031/api/producto"
API_PROYECTO_PRODUCTO_VIEW = "http://localhost:5031/api/view_proyecto_producto"


def formatear_fecha(fecha_str):
    if not fecha_str:
        return ""
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


# ------------------- LISTAR asociaciones -------------------
@rutas_proyecto_producto.route("/proyecto_producto")
def proyecto_producto():
    try:
        asociaciones = requests.get(API_PROYECTO_PRODUCTO_URL).json().get("datos", [])
    except Exception as e:
        print("Error al cargar asociaciones:", e)
        asociaciones = []

    try:
        proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
    except Exception:
        proyectos = []

    try:
        productos = requests.get(API_PRODUCTO_URL).json().get("datos", [])
    except Exception:
        productos = []
        
    try:
        proyecto_producto_view = requests.get(API_PROYECTO_PRODUCTO_VIEW).json().get("datos", [])
    except Exception:
        proyecto_producto_view = []

    return render_template(
        "proyecto_producto.html",
        proyecto_producto_view=proyecto_producto_view,
        asociaciones=asociaciones,
        asociacion=None,
        proyectos=proyectos,
        productos=productos,
        modo="crear"
    )


# ------------------- BUSCAR asociación -------------------
@rutas_proyecto_producto.route("/proyecto_producto/buscar", methods=["POST"])
def buscar_proyecto_producto():
    id_buscar = request.form.get("codigo_buscar")

    try:
        respuesta = requests.get(f"{API_PROYECTO_PRODUCTO_URL}/id_proyecto/{id_buscar}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                asociacion = datos[0]
                asociacion["fecha_asociacion"] = formatear_fecha(asociacion.get("fecha_asociacion"))
                asociaciones = requests.get(API_PROYECTO_PRODUCTO_URL).json().get("datos", [])
                proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
                productos = requests.get(API_PRODUCTO_URL).json().get("datos", [])
                proyecto_producto_view = requests.get(API_PROYECTO_PRODUCTO_VIEW).json().get("datos", [])
                return render_template(
                    "proyecto_producto.html",
                    proyecto_producto_view=proyecto_producto_view,
                    asociaciones=asociaciones,
                    asociacion=asociacion,
                    proyectos=proyectos,
                    productos=productos,
                    modo="actualizar"
                )
    except Exception as e:
        print("Error al buscar asociación:", e)

    return redirect(url_for("rutas_proyecto_producto.proyecto_producto"))


# ------------------- CREAR asociación -------------------
@rutas_proyecto_producto.route("/proyecto_producto/crear", methods=["POST"])
def crear_proyecto_producto():
    datos = {
        "id_proyecto": request.form.get("id_proyecto"),
        "id_producto": request.form.get("id_producto"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.post(API_PROYECTO_PRODUCTO_URL, json=datos)
    except Exception as e:
        print("Error al crear asociación:", e)

    return redirect(url_for("rutas_proyecto_producto.proyecto_producto"))


# ------------------- ACTUALIZAR asociación -------------------
@rutas_proyecto_producto.route("/proyecto_producto/actualizar", methods=["POST"])
def actualizar_proyecto_producto():
    codigo = request.form.get("id_proyecto")
    datos = {
        "id_proyecto": codigo,
        "id_producto": request.form.get("id_producto"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.put(f"{API_PROYECTO_PRODUCTO_URL}/id_proyecto/{codigo}", json=datos)
    except Exception as e:
        print("Error al actualizar asociación:", e)

    return redirect(url_for("rutas_proyecto_producto.proyecto_producto"))


# ------------------- ELIMINAR asociación -------------------
@rutas_proyecto_producto.route("/proyecto_producto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_proyecto_producto(codigo):
    try:
        requests.delete(f"{API_PROYECTO_PRODUCTO_URL}/id_proyecto/{codigo}")
    except Exception as e:
        print("Error al eliminar asociación:", e)

    return redirect(url_for("rutas_proyecto_producto.proyecto_producto"))
