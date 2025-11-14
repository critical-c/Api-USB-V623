from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de archivo_entregable
rutas_archivo_entregable = Blueprint("rutas_archivo_entregable", __name__)

# URL base de la API en C# que gestiona los archivo_entregable
API_URL = "http://localhost:5031/api/archivo_entregable"
API_ARCHIVO = "http://localhost:5031/api/archivo"
API_ENTREGABLE = "http://localhost:5031/api/entregable"
API_ARCHIVOS_ENTREGABLES = "http://localhost:5031/api/view_archivo_entregable"

# ------------------- LISTAR archivo_entregable -------------------
@rutas_archivo_entregable.route("/archivo_entregable")
def archivo_entregable():
    try:
        archivos_entregables = requests.get(API_URL).json().get("datos", [])
        archivo = requests.get(API_ARCHIVO).json().get("datos", [])
        entregable = requests.get(API_ENTREGABLE).json().get("datos", [])
        archivos_vista = requests.get(API_ARCHIVOS_ENTREGABLES).json().get("datos", [])
    except Exception as e:
        archivos_entregables, archivo, entregable,  archivos_vista= [], [], [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "archivos_entregables.html",
        archivos_vista=archivos_vista,
        archivos_entregables=archivos_entregables,
        archivo_entregable=None,
        archivo=archivo,
        entregable=entregable,
        modo="crear"
    )

# ------------------- BUSCAR archivo_entregable -------------------
@rutas_archivo_entregable.route("/archivo_entregable/buscar", methods=["POST"])
def buscar_archivo_entregable():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id_archivo/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    archivo_entregable = datos[0]
                    archivos_entregables = requests.get(API_URL).json().get("datos", [])
                    archivo = requests.get(API_ARCHIVO).json().get("datos", [])
                    entregable = requests.get(API_ENTREGABLE).json().get("datos", [])
                    archivos_vista = requests.get(API_ARCHIVOS_ENTREGABLES).json().get("datos", [])
                    return render_template(
                        "archivos_entregables.html",
                        archivos_vista=archivos_vista,
                        archivos_entregables=archivos_entregables,
                        archivo_entregable=archivo_entregable,
                        archivo=archivo,
                        entregable=entregable,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    archivos_entregables = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "archivos_entregables.html",
        archivos_entregables=archivos_entregables,
        archivo_entregable=None,
        mensaje="Relación Archivo-Entregable no encontrada",
        modo="crear"
    )

# ------------------- CREAR archivo_entregable -------------------
@rutas_archivo_entregable.route("/archivo_entregable/crear", methods=["POST"])
def crear_archivo_entregable():
    datos = {
        "id_archivo": request.form.get("id_archivo"),
        "id_entregable": request.form.get("id_entregable")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la relación archivo-entregable: {e}"

    return redirect(url_for("rutas_archivo_entregable.archivo_entregable"))

# ------------------- ACTUALIZAR archivo_entregable -------------------
@rutas_archivo_entregable.route("/archivo_entregable/actualizar", methods=["POST"])
def actualizar_archivo_entregable():
    codigo = request.form.get("id_archivo")
    datos = {
        "id_archivo": request.form.get("id_archivo"),
        "id_entregable": request.form.get("id_entregable")
    }

    try:
        requests.put(f"{API_URL}/id_archivo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar la relación archivo-entregable: {e}"

    return redirect(url_for("rutas_archivo_entregable.archivo_entregable"))

# ------------------- ELIMINAR archivo_entregable -------------------
@rutas_archivo_entregable.route("/archivo_entregable/eliminar/<string:codigo>", methods=["POST"])
def eliminar_archivo_entregable(codigo):
    try:
        requests.delete(f"{API_URL}/id_archivo/{codigo}")
    except Exception as e:
        return f"Error al eliminar la relación archivo-entregable: {e}"

    return redirect(url_for("rutas_archivo_entregable.archivo_entregable"))
