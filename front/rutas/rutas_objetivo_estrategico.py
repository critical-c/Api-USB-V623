from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint
rutas_objetivo_estrategico = Blueprint("rutas_objetivo_estrategico", __name__)

# URL base de la API en C# (asegúrate que esté corriendo)
API_URL = "http://localhost:5031/api/objetivo_estrategico"

# ------------------- LISTAR -------------------
@rutas_objetivo_estrategico.route("/objetivo_estrategico")
def objetivo_estrategico():
    try:
        respuesta = requests.get(API_URL)
        objetivos = respuesta.json().get("datos", [])
    except Exception as e:
        objetivos = []
        print("Error al conectar con la API:", e)

    return render_template(
        "objetivo_estrategico.html",
        objetivos=objetivos,
        objetivo=None,
        modo="crear"
    )

# ------------------- BUSCAR -------------------
@rutas_objetivo_estrategico.route("/objetivo_estrategico/buscar", methods=["POST"])
def buscar_objetivo_estrategico():
    id_buscar = request.form.get("id_buscar")

    if id_buscar:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id_buscar}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    objetivo = datos[0]
                    objetivos = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "objetivo_estrategico.html",
                        objetivos=objetivos,
                        objetivo=objetivo,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra
    try:
        objetivos = requests.get(API_URL).json().get("datos", [])
    except Exception:
        objetivos = []

    return render_template(
        "objetivo_estrategico.html",
        objetivos=objetivos,
        objetivo=None,
        mensaje="Objetivo estratégico no encontrado",
        modo="crear"
    )

# ------------------- CREAR -------------------
@rutas_objetivo_estrategico.route("/objetivo_estrategico/crear", methods=["POST"])
def crear_objetivo_estrategico():
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        respuesta = requests.post(API_URL, json=datos)
        if respuesta.status_code >= 400:
            print("Error al crear:", respuesta.text)
    except Exception as e:
        print("Error al conectar con la API:", e)

    return redirect(url_for("rutas_objetivo_estrategico.objetivo_estrategico"))

# ------------------- ACTUALIZAR -------------------
@rutas_objetivo_estrategico.route("/objetivo_estrategico/actualizar", methods=["POST"])
def actualizar_objetivo_estrategico():
    id_objetivo = request.form.get("id")
    datos = {
        "id": id_objetivo,
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        respuesta = requests.put(f"{API_URL}/id/{id_objetivo}", json=datos)
        if respuesta.status_code != 200:
            print("Error al actualizar:", respuesta.text)
    except Exception as e:
        print("Error al conectar con la API:", e)

    return redirect(url_for("rutas_objetivo_estrategico.objetivo_estrategico"))

# ------------------- ELIMINAR -------------------
@rutas_objetivo_estrategico.route("/objetivo_estrategico/eliminar/<string:id_objetivo>", methods=["POST"])
def eliminar_objetivo_estrategico(id_objetivo):
    try:
        respuesta = requests.delete(f"{API_URL}/id/{id_objetivo}")
        if respuesta.status_code >= 400:
            print("Error al eliminar:", respuesta.text)
    except Exception as e:
        print("Error al eliminar objetivo estratégico:", e)

    return redirect(url_for("rutas_objetivo_estrategico.objetivo_estrategico"))
