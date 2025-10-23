from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de actividad
rutas_actividad = Blueprint("rutas_actividad", __name__)

# URL base de la API en C# que gestiona las actividades
API_URL = "http://localhost:5031/api/actividad"

# ------------------- LISTAR actividad -------------------
@rutas_actividad.route("/actividad")
def actividad():
    try:
        respuesta = requests.get(API_URL)
        actividades = respuesta.json().get("datos", [])
    except Exception as e:
        actividades = []
        print("Error al conectar con la API:", e)

    return render_template(
        "actividades.html",
        actividades=actividades,
        actividad=None,
        modo="crear"
    )

# ------------------- BUSCAR actividad -------------------
@rutas_actividad.route("/actividad/buscar", methods=["POST"])
def buscar_actividad():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    actividad = datos[0]
                    actividades = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "actividades.html",
                        actividades=actividades,
                        actividad=actividad,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    actividades = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "actividades.html",
        actividades=actividades,
        actividad=None,
        mensaje="Actividad no encontrada",
        modo="crear"
    )

# ------------------- CREAR actividad -------------------
@rutas_actividad.route("/actividad/crear", methods=["POST"])
def crear_actividad():
    datos = {
        "id_entregable": request.form.get("id_entregable"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion"),
        "prioridad": int(request.form.get("prioridad")),
        "porcentaje_avance": int(request.form.get("porcentaje_avance"))
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la actividad: {e}"

    return redirect(url_for("rutas_actividad.actividad"))

# ------------------- ACTUALIZAR actividad -------------------
@rutas_actividad.route("/actividad/actualizar", methods=["POST"])
def actualizar_actividad():
    codigo = request.form.get("id")
    datos = {
        "id_entregable": request.form.get("id_entregable"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion"),
        "prioridad": int(request.form.get("prioridad")),
        "porcentaje_avance": int(request.form.get("porcentaje_avance"))
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar actividad: {e}"

    return redirect(url_for("rutas_actividad.actividad"))

# ------------------- ELIMINAR actividad -------------------
@rutas_actividad.route("/actividad/eliminar/<string:codigo>", methods=["POST"])
def eliminar_actividad(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar actividad: {e}"

    return redirect(url_for("rutas_actividad.actividad"))
