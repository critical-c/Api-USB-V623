from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint
rutas_producto = Blueprint("rutas_producto", __name__)

# URLs base de las APIs en C#
API_URL_PRODUCTO = "http://localhost:5031/api/producto"
API_URL_TIPO_PRODUCTO = "http://localhost:5031/api/tipo_producto"


# ------------------- LISTAR PRODUCTOS -------------------
@rutas_producto.route("/producto")
def producto():
    try:
        productos = requests.get(API_URL_PRODUCTO).json().get("datos", [])
    except Exception as e:
        productos = []
        print("Error al conectar con la API de productos:", e)

    try:
        tipos = requests.get(API_URL_TIPO_PRODUCTO).json().get("datos", [])
    except Exception as e:
        tipos = []
        print("Error al conectar con la API de tipos de producto:", e)

    return render_template(
        "producto.html",
        productos=productos,
        producto=None,
        tipos=tipos,
        modo="crear"
    )


# ------------------- BUSCAR PRODUCTO -------------------
@rutas_producto.route("/producto/buscar", methods=["POST"])
def buscar_producto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL_PRODUCTO}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    producto = datos[0]
                    productos = requests.get(API_URL_PRODUCTO).json().get("datos", [])
                    tipos = requests.get(API_URL_TIPO_PRODUCTO).json().get("datos", [])
                    return render_template(
                        "producto.html",
                        productos=productos,
                        producto=producto,
                        tipos=tipos,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    productos = requests.get(API_URL_PRODUCTO).json().get("datos", [])
    tipos = requests.get(API_URL_TIPO_PRODUCTO).json().get("datos", [])
    return render_template(
        "producto.html",
        productos=productos,
        producto=None,
        tipos=tipos,
        mensaje="Producto no encontrado",
        modo="crear"
    )


# ------------------- CREAR PRODUCTO -------------------
@rutas_producto.route("/producto/crear", methods=["POST"])
def crear_producto():
    datos = {
        "id_tipo_producto": request.form.get("id_tipo_producto"),
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "ruta_logo": request.form.get("ruta_logo")
    }

    try:
        requests.post(API_URL_PRODUCTO, json=datos)
    except Exception as e:
        return f"Error al crear producto: {e}"

    return redirect(url_for("rutas_producto.producto"))


# ------------------- ACTUALIZAR PRODUCTO -------------------
@rutas_producto.route("/producto/actualizar", methods=["POST"])
def actualizar_producto():
    codigo = request.form.get("id")
    datos = {
        "id": codigo,
        "id_tipo_producto": request.form.get("id_tipo_producto"),
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
        requests.put(f"{API_URL_PRODUCTO}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar producto: {e}"

    return redirect(url_for("rutas_producto.producto"))


# ------------------- ELIMINAR PRODUCTO -------------------
@rutas_producto.route("/producto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_producto(codigo):
    try:
        requests.delete(f"{API_URL_PRODUCTO}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar producto: {e}"

    return redirect(url_for("rutas_producto.producto"))
