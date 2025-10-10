# ===============================================================
# Módulo: rutas_tipo_producto.py
# Descripción: Maneja las rutas para listar, crear, buscar,
# actualizar y eliminar tipos de producto. Se conecta a la API en C#.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_tipo_producto = Blueprint("rutas_tipo_producto", __name__)
API_URL = "http://localhost:5031/api/tipo_producto"  # Endpoint base de la API

# ===============================================================
# RUTA: LISTAR TIPOS DE PRODUCTO
# ===============================================================
@rutas_tipo_producto.route("/tipo_producto", methods=["GET"])
def listar_tipo_producto():
    try:
        respuesta = requests.get(API_URL)
        tipo_productos = respuesta.json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        tipo_productos = []

    return render_template("tipo_producto.html", tipo_productos=tipo_productos, tipo_producto=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR TIPO DE PRODUCTO POR ID
# ===============================================================
@rutas_tipo_producto.route("/tipo_producto/buscar", methods=["POST"])
def buscar_tipo_producto():
    codigo = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                tipo_producto = datos[0]
                tipo_productos = requests.get(API_URL).json().get("datos", [])
                return render_template("tipo_producto.html", tipo_productos=tipo_productos, tipo_producto=tipo_producto, modo="actualizar")
    except Exception as e:
        print("Error al buscar tipo de producto:", e)

    tipo_productos = requests.get(API_URL).json().get("datos", [])
    return render_template("tipo_producto.html", tipo_productos=tipo_productos, tipo_producto=None, mensaje="Tipo de producto no encontrado", modo="crear")


# ===============================================================
# RUTA: CREAR TIPO DE PRODUCTO
# ===============================================================
@rutas_tipo_producto.route("/tipo_producto", methods=["POST"])
def crear_tipo_producto():
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear tipo de producto: {e}"

    return redirect(url_for("rutas_tipo_producto.listar_tipo_producto"))


# ===============================================================
# RUTA: ACTUALIZAR TIPO DE PRODUCTO
# ===============================================================
@rutas_tipo_producto.route("/tipo_producto/actualizar/<int:id>", methods=["POST"])
def actualizar_tipo_producto(id):
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar tipo de producto: {e}"

    return redirect(url_for("rutas_tipo_producto.listar_tipo_producto"))


# ===============================================================
# RUTA: ELIMINAR TIPO DE PRODUCTO
# ===============================================================
@rutas_tipo_producto.route("/tipo_producto/eliminar/<int:id>", methods=["POST"])
def eliminar_tipo_producto(id):
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar tipo de producto: {e}"

    return redirect(url_for("rutas_tipo_producto.listar_tipo_producto"))
