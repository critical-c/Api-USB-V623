from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de archivo
rutas_archivo = Blueprint("rutas_archivo", __name__)

# URL base de la API en C# que gestiona los archivos
API_URL = "http://localhost:5031/api/archivo"

# ------------------- LISTAR archivo -------------------
@rutas_archivo.route("/archivo")
def archivo():
    try:
        respuesta = requests.get(API_URL)
        archivos = respuesta.json().get("datos", [])
    except Exception as e:
        archivos = []
        print("Error al conectar con la API:", e)

    return render_template(
        "archivos.html",
        archivos=archivos,
        archivo=None,
        modo="crear"
    )

# ------------------- BUSCAR archivo -------------------
@rutas_archivo.route("/archivo/buscar", methods=["POST"])
def buscar_archivo():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    archivo = datos[0]
                    archivos = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "archivos.html",
                        archivos=archivos,
                        archivo=archivo,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    archivos = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "archivos.html",
        archivos=archivos,
        archivo=None,
        mensaje="Archivo no encontrado",
        modo="crear"
    )

# ------------------- CREAR archivo -------------------
@rutas_archivo.route("/archivo/crear", methods=["POST"])
def crear_archivo():
    datos = {
        "id_usuario": request.form.get("id_usuario"),
        "ruta": request.form.get("ruta"),
        "nombre": request.form.get("nombre"),
        "tipo": request.form.get("tipo"),
        "fecha": request.form.get("fecha")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear el archivo: {e}"

    return redirect(url_for("rutas_archivo.archivo"))

# ------------------- ACTUALIZAR archivo -------------------
@rutas_archivo.route("/archivo/actualizar", methods=["POST"])
def actualizar_archivo():
    codigo = request.form.get("id")
    datos = {
        "id_usuario": request.form.get("id_usuario"),
        "ruta": request.form.get("ruta"),
        "nombre": request.form.get("nombre"),
        "tipo": request.form.get("tipo"),
        "fecha": request.form.get("fecha")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar archivo: {e}"

    return redirect(url_for("rutas_archivo.archivo"))

# ------------------- ELIMINAR archivo -------------------
@rutas_archivo.route("/archivo/eliminar/<string:codigo>", methods=["POST"])
def eliminar_archivo(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar archivo: {e}"

    return redirect(url_for("rutas_archivo.archivo"))
