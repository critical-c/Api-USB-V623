# ===============================================================
# Módulo: rutas_productos.py
# Descripción: Maneja las rutas RESTful del módulo de productos.
# Cada ruta se comunica con la API externa (C#) que gestiona los productos.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for
import requests  # Se usa para llamar a la API REST externa

# ---------------------------------------------------------------
# Configuración del Blueprint
# ---------------------------------------------------------------
rutas_productos = Blueprint("rutas_productos", __name__)

# Dirección base de la API
API_URL = "http://localhost:5031/api/producto"


# ---------------------------------------------------------------
# GET /productos → listar todos los productos
# ---------------------------------------------------------------
@rutas_productos.route("/productos", methods=["GET"])
def listar_productos():
    """Obtiene y muestra la lista completa de productos"""
    try:
        respuesta = requests.get(API_URL)
        productos = respuesta.json().get("datos", [])
    except Exception as e:
        productos = []
        print("Error al conectar con la API:", e)

    return render_template("productos.html",
                           productos=productos,
                           producto=None,
                           modo="crear")


# ---------------------------------------------------------------
# GET /productos/buscar → buscar producto por código
# (El formulario envía GET con ?codigo=123)
# ---------------------------------------------------------------
@rutas_productos.route("/productos/buscar", methods=["GET"])
def buscar_producto():
    """Busca un producto específico según su código"""
    codigo = request.args.get("codigo")

    if not codigo:
        return redirect(url_for("rutas_productos.listar_productos"))

    try:
        respuesta = requests.get(f"{API_URL}/codigo/{codigo}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                producto = datos[0]
                productos = requests.get(API_URL).json().get("datos", [])
                return render_template("productos.html",
                                       productos=productos,
                                       producto=producto,
                                       modo="actualizar")
    except Exception as e:
        print("Error al buscar producto:", e)

    # Si no existe, recarga la lista
    productos = requests.get(API_URL).json().get("datos", [])
    return render_template("productos.html",
                           productos=productos,
                           producto=None,
                           mensaje="Producto no encontrado",
                           modo="crear")


# ---------------------------------------------------------------
# POST /productos → crear producto
# ---------------------------------------------------------------
@rutas_productos.route("/productos", methods=["POST"])
def crear_producto():
    """Crea un nuevo producto"""
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "valorunitario": int(request.form.get("valorunitario", 0)),
        "stock": int(request.form.get("stock", 0))
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear producto: {e}"

    return redirect(url_for("rutas_productos.listar_productos"))


# ---------------------------------------------------------------
# POST /productos/actualizar → actualizar producto existente
# (El formulario usa POST, pero Flask hace PUT hacia la API)
# ---------------------------------------------------------------
@rutas_productos.route("/productos/actualizar", methods=["POST"])
def actualizar_producto():
    """Actualiza un producto existente"""
    codigo = request.form.get("codigo")
    datos = {
        "nombre": request.form.get("nombre"),
        "valorunitario": int(request.form.get("valorunitario", 0)),
        "stock": int(request.form.get("stock", 0))
    }

    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar producto: {e}"

    return redirect(url_for("rutas_productos.listar_productos"))


# ---------------------------------------------------------------
# POST /productos/eliminar → eliminar producto
# (El formulario usa POST, pero Flask hace DELETE hacia la API)
# ---------------------------------------------------------------
@rutas_productos.route("/productos/eliminar", methods=["POST"])
def eliminar_producto():
    """Elimina un producto según su código"""
    codigo = request.form.get("codigo")
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar producto: {e}"

    return redirect(url_for("rutas_productos.listar_productos"))
