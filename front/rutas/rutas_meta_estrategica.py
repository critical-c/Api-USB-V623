from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de meta_estrategica
rutas_meta_estrategica = Blueprint("rutas_meta_estrategica", __name__)

# URL base de la API en C# que gestiona las metas estratégicas
API_URL = "http://localhost:5031/api/meta_estrategica"
API_OBJETIVO_ESTRATEGICO = "http://localhost:5031/api/objetivo_estrategico"

# ------------------- LISTAR meta_estrategica -------------------
@rutas_meta_estrategica.route("/meta_estrategica")
def meta_estrategica():
    try:
        metas_estrategicas = requests.get(API_URL).json().get("datos", [])
        objetivo_estrategico = requests.get(API_OBJETIVO_ESTRATEGICO).json().get("datos", [])
    except Exception as e:
        metas_estrategicas, objetivo_estrategico = [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "meta_estrategica.html",
        metas_estrategicas=metas_estrategicas,
        meta_estrategica=None,
        objetivo_estrategico=objetivo_estrategico,
        modo="crear"
    )

# ------------------- BUSCAR meta_estrategica -------------------
@rutas_meta_estrategica.route("/meta_estrategica/buscar", methods=["POST"])
def buscar_meta_estrategica():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    meta_estrategica = datos[0]
                    metas_estrategicas = requests.get(API_URL).json().get("datos", [])
                    objetivo_estrategico = requests.get(API_OBJETIVO_ESTRATEGICO).json().get("datos", [])
                    return render_template(
                        "meta_estrategica.html",
                        metas_estrategicas=metas_estrategicas,
                        meta_estrategica=meta_estrategica,
                        objetivo_estrategico=objetivo_estrategico,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    metas_estrategicas = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "meta_estrategica.html",
        metas_estrategicas=metas_estrategicas,
        meta_estrategica=None,
        mensaje="Meta estratégica no encontrada",
        modo="crear"
    )

# ------------------- CREAR meta_estrategica -------------------
@rutas_meta_estrategica.route("/meta_estrategica/crear", methods=["POST"])
def crear_meta_estrategica():
    datos = {
        "id_obj": request.form.get("id_obj"),
        "titulo": request.form.get("titulo")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la meta estratégica: {e}"

    return redirect(url_for("rutas_meta_estrategica.meta_estrategica"))

# ------------------- ACTUALIZAR meta_estrategica -------------------
@rutas_meta_estrategica.route("/meta_estrategica/actualizar", methods=["POST"])
def actualizar_meta_estrategica():
    codigo = request.form.get("id")
    datos = {
        "id_obj": request.form.get("id_obj"),
        "titulo": request.form.get("titulo")
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar la meta estratégica: {e}"

    return redirect(url_for("rutas_meta_estrategica.meta_estrategica"))

# ------------------- ELIMINAR meta_estrategica -------------------
@rutas_meta_estrategica.route("/meta_estrategica/eliminar/<string:codigo>", methods=["POST"])
def eliminar_meta_estrategica(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar la meta estratégica: {e}"

    return redirect(url_for("rutas_meta_estrategica.meta_estrategica"))
