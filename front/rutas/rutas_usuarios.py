# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de productos
# "rutas_productos" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_usuario = Blueprint("rutas_usuario", __name__)

# URL base de la API en C# que gestiona los productos
API_URL = "http://localhost:5031/api/usuario"

# ------------------- LISTAR usuario -------------------
@rutas_usuario.route("/usuario")
def usuario():

    try:
        respuesta = requests.get(API_URL)
        usuarios = respuesta.json().get("datos", [])
    except Exception as e:
        usuarios = []
        print("Error al conectar con la API:", e)


    return render_template(
        "usuarios.html",
        usuarios=usuarios,
        usuario=None,
        modo="crear"
    )

# ------------------- BUSCAR usuario -------------------
@rutas_usuario.route("/usuario/buscar", methods=["POST"])
def buscar_usuario():

    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    # Si la API retorna datos, se asume que es una lista
                    usuario = datos[0]
                    usuarios = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "usuarios.html",
                        usuarios=usuarios,
                        usuario=usuario,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra, recargar la lista completa
    usuarios = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "usuarios.html",
        usuarios=usuarios,
        usuario=None,
        mensaje="Usuario no encontrado",
        modo="crear"
    )

# ------------------- CREAR usuario -------------------
@rutas_usuario.route("/usuario/crear", methods=["POST"])
def crear_usuario():
    datos = {
        "email": request.form.get("email"),
        "contrasena": request.form.get("contrasena"),
        "ruta_avatar": request.form.get("ruta_avatar") or None,
        "activo": request.form.get("activo")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el usuario: {e}"

    return redirect(url_for("rutas_usuario.usuario"))

# ------------------- ACTUALIZAR usuario -------------------
@rutas_usuario.route("/usuario/actualizar", methods=["POST"])
def actualizar_usuario():

    codigo = request.form.get("id")
    datos = {
        "email": request.form.get("email"),
        "contrasena": request.form.get("contrasena"),
        "ruta_avatar": request.form.get("ruta_avatar") or None,
        "activo": request.form.get("activo")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar usuario: {e}"

    return redirect(url_for("rutas_usuario.usuario"))

# ------------------- ELIMINAR usuario -------------------
@rutas_usuario.route("/usuario/eliminar/<string:codigo>", methods=["POST"])
def eliminar_usuario(codigo):
    """
    Ruta para eliminar un producto de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar usuario: {e}"

    return redirect(url_for("rutas_usuario.usuario"))


