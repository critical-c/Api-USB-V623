from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de tipo_producto
rutas_tipo_producto = Blueprint("rutas_tipo_producto", __name__)

# URL base de la API en C# que gestiona los tipos de producto
API_URL = "http://localhost:5031/api/tipo_producto"

# ------------------- LISTAR tipo_producto -------------------
@rutas_tipo_producto.route("/tipo_producto")
def tipo_producto():
    try:
        respuesta = requests.get(API_URL)
        tipos_productos = respuesta.json().get("datos", [])
    except Exception as e:
        tipos_productos = []
        print("Error al conectar con la API:", e)

    return render_template(
        "tipo_productos.html",
        tipos_productos=tipos_productos,
        tipo_producto=None,
        modo="crear"
    )

# ------------------- BUSCAR tipo_producto -------------------
@rutas_tipo_producto.route("/tipo_producto/buscar", methods=["POST"])
def buscar_tipo_producto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    tipo_producto = datos[0]
                    tipos_productos = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "tipo_productos.html",
                        tipos_productos=tipos_productos,
                        tipo_producto=tipo_producto,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    tipos_productos = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "tipo_productos.html",
        tipos_productos=tipos_productos,
        tipo_producto=None,
        mensaje="Tipo de producto no encontrado",
        modo="crear"
    )

# ------------------- CREAR tipo_producto -------------------
@rutas_tipo_producto.route("/tipo_producto/crear", methods=["POST"])
def crear_tipo_producto():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el tipo de producto: {e}"

    return redirect(url_for("rutas_tipo_producto.tipo_producto"))

# ------------------- ACTUALIZAR tipo_producto -------------------
@rutas_tipo_producto.route("/tipo_producto/actualizar", methods=["POST"])
def actualizar_tipo_producto():
    codigo = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar tipo de producto: {e}"

    return redirect(url_for("rutas_tipo_producto.tipo_producto"))

# ------------------- ELIMINAR tipo_producto -------------------
@rutas_tipo_producto.route("/tipo_producto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_tipo_producto(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar tipo de producto: {e}"

    return redirect(url_for("rutas_tipo_producto.tipo_producto"))
