# =================== rutas/rutas_usuarios.py ===================
from flask import Blueprint, render_template, request, redirect, url_for
import requests
# Importar la función para encriptar contraseñas
from werkzeug.security import generate_password_hash  

rutas_usuario = Blueprint("rutas_usuario", __name__)
API_URL = "http://localhost:5031/api/usuario"


# ------------------- LISTAR USUARIO -------------------
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


# ------------------- BUSCAR USUARIO -------------------
@rutas_usuario.route("/usuario/buscar", methods=["POST"])
def buscar_usuario():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
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

    usuarios = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "usuarios.html",
        usuarios=usuarios,
        usuario=None,
        mensaje="Usuario no encontrado",
        modo="crear"
    )


# ------------------- CREAR USUARIO -------------------
@rutas_usuario.route("/usuario/crear", methods=["POST"])
def crear_usuario():
    contrasena_plana = request.form.get("contrasena")
    #Almacenamos la contraseña encriptada
    contrasena_hash = generate_password_hash(contrasena_plana)  

    datos = {
        "email": request.form.get("email"),
        "contrasena": contrasena_hash, #Contraseña encriptada
        "ruta_avatar": request.form.get("ruta_avatar") or None,
        "activo": request.form.get("activo")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el usuario: {e}"

    return redirect(url_for("rutas_usuario.usuario"))


# ------------------- ACTUALIZAR USUARIO -------------------
@rutas_usuario.route("/usuario/actualizar", methods=["POST"])
def actualizar_usuario():
    codigo = request.form.get("id")
    contrasena_plana = request.form.get("contrasena")
    contrasena_hash = generate_password_hash(contrasena_plana)  # 🔒 re-encriptar

    datos = {
        "email": request.form.get("email"),
        "contrasena": contrasena_hash,
        "ruta_avatar": request.form.get("ruta_avatar") or None,
        "activo": request.form.get("activo")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar usuario: {e}"

    return redirect(url_for("rutas_usuario.usuario"))


# ------------------- ELIMINAR USUARIO -------------------
@rutas_usuario.route("/usuario/eliminar/<string:codigo>", methods=["POST"])
def eliminar_usuario(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar usuario: {e}"

    return redirect(url_for("rutas_usuario.usuario"))
