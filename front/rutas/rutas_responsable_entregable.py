from flask import Blueprint, render_template, request, redirect, url_for
import requests
from datetime import datetime

rutas_responsable_entregable = Blueprint("rutas_responsable_entregable", __name__)

API_RE = "http://localhost:5031/api/responsable_entregable"
API_RESPONSABLE = "http://localhost:5031/api/responsable"
API_ENTREGABLE = "http://localhost:5031/api/entregable"


def formatear_fecha(fecha_str):
    if not fecha_str:
        return ""
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


# ------------------- LISTAR asociaciones -------------------
@rutas_responsable_entregable.route("/responsable_entregable")
def responsable_entregable():
    try:
        asociaciones = requests.get(API_RE).json().get("datos", [])
        responsables = requests.get(API_RESPONSABLE).json().get("datos", [])
        entregables = requests.get(API_ENTREGABLE).json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        asociaciones, responsables, entregables = [], [], []

    return render_template(
        "responsable_entregable.html",
        asociaciones=asociaciones,
        responsables=responsables,
        entregables=entregables,
        modo="crear",
        asociacion=None,
        mensaje=None
    )


# ------------------- BUSCAR (solo por id_responsable) -------------------
@rutas_responsable_entregable.route("/responsable_entregable/buscar", methods=["POST"])
def buscar_responsable_entregable():
    id_responsable = request.form.get("id_responsable_buscar")

    try:
        asociaciones = requests.get(API_RE).json().get("datos", [])
        responsables = requests.get(API_RESPONSABLE).json().get("datos", [])
        entregables = requests.get(API_ENTREGABLE).json().get("datos", [])
    except Exception as e:
        print("Error al conectar con la API:", e)
        asociaciones, responsables, entregables = [], [], []

    if not id_responsable:
        return render_template(
            "responsable_entregable.html",
            asociaciones=asociaciones,
            responsables=responsables,
            entregables=entregables,
            asociacion=None,
            modo="crear"
        )

    # Buscar localmente en las asociaciones
    coincidencias = [a for a in asociaciones if str(a.get("id_responsable")) == str(id_responsable)]

    if coincidencias:
        asociacion = coincidencias[0]
        asociacion["fecha_asociacion"] = formatear_fecha(asociacion.get("fecha_asociacion"))
        return render_template(
            "responsable_entregable.html",
            asociaciones=asociaciones,
            responsables=responsables,
            entregables=entregables,
            asociacion=asociacion,
            modo="actualizar"
        )
    else:
        return render_template(
            "responsable_entregable.html",
            asociaciones=asociaciones,
            responsables=responsables,
            entregables=entregables,
            asociacion=None,
            modo="crear"
        )


# ------------------- CREAR -------------------
@rutas_responsable_entregable.route("/responsable_entregable/crear", methods=["POST"])
def crear_responsable_entregable():
    datos = {
        "id_responsable": request.form.get("id_responsable"),
        "id_entregable": request.form.get("id_entregable"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.post(API_RE, json=datos)
    except Exception as e:
        print("Error al crear asociación:", e)

    return redirect(url_for("rutas_responsable_entregable.responsable_entregable"))


# ------------------- ACTUALIZAR -------------------
@rutas_responsable_entregable.route("/responsable_entregable/actualizar", methods=["POST"])
def actualizar_responsable_entregable():
    id_responsable = request.form.get("id_responsable")
    id_entregable = request.form.get("id_entregable")

    datos = {
        "id_responsable": id_responsable,
        "id_entregable": id_entregable,
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        requests.put(f"{API_RE}/id/{id_responsable}/{id_entregable}", json=datos)
    except Exception as e:
        print("Error al actualizar asociación:", e)

    return redirect(url_for("rutas_responsable_entregable.responsable_entregable"))


# ------------------- ELIMINAR -------------------
@rutas_responsable_entregable.route("/responsable_entregable/eliminar/<int:id_responsable>/<int:id_entregable>", methods=["POST"])
def eliminar_responsable_entregable(id_responsable, id_entregable):
    try:
        requests.delete(f"{API_RE}/id/{id_responsable}/{id_entregable}")
    except Exception as e:
        print("Error al eliminar asociación:", e)

    return redirect(url_for("rutas_responsable_entregable.responsable_entregable"))
