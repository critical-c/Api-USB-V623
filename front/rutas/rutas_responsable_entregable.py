from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_responsable_entregable = Blueprint("rutas_responsable_entregable", __name__)

# URLs de la API (ajusta host/puerto si tu API usa otro)
API_RE = "http://localhost:5031/api/responsable_entregable"
API_RESPONSABLE = "http://localhost:5031/api/responsable"
API_ENTREGABLE = "http://localhost:5031/api/entregable"


# ------------------- LISTAR asociaciones -------------------
@rutas_responsable_entregable.route("/responsable_entregable")
def responsable_entregable():
    try:
        asociaciones = requests.get(API_RE, timeout=10).json().get("datos", [])
    except Exception as e:
        print("Error al cargar asociaciones:", e)
        asociaciones = []

    try:
        responsables = requests.get(API_RESPONSABLE, timeout=10).json().get("datos", [])
    except Exception as e:
        print("Error al cargar responsables:", e)
        responsables = []

    try:
        entregables = requests.get(API_ENTREGABLE, timeout=10).json().get("datos", [])
    except Exception as e:
        print("Error al cargar entregables:", e)
        entregables = []

    return render_template(
        "responsable_entregable.html",
        responsables=responsables,
        entregables=entregables,
        asociaciones=asociaciones,
        modo="crear",
        asociacion=None,
        mensaje=None
    )


# ------------------- BUSCAR asociación (por clave compuesta) -------------------
@rutas_responsable_entregable.route("/responsable_entregable/buscar", methods=["POST"])
def buscar_responsable_entregable():
    id_responsable = request.form.get("id_responsable_buscar")
    id_entregable = request.form.get("id_entregable_buscar")

    # recargar listas para renderizar en cualquier caso
    try:
        asociaciones = requests.get(API_RE, timeout=10).json().get("datos", [])
    except Exception:
        asociaciones = []
    try:
        responsables = requests.get(API_RESPONSABLE, timeout=10).json().get("datos", [])
    except Exception:
        responsables = []
    try:
        entregables = requests.get(API_ENTREGABLE, timeout=10).json().get("datos", [])
    except Exception:
        entregables = []

    if not id_responsable or not id_entregable:
        return render_template(
            "responsable_entregable.html",
            responsables=responsables,
            entregables=entregables,
            asociaciones=asociaciones,
            modo="crear",
            asociacion=None,
            mensaje="Debe proporcionar ambos IDs para buscar (responsable y entregable)."
        )

    try:
        # Supongo que tu API admite ruta /id/{id_responsable}/{id_entregable}
        respuesta = requests.get(f"{API_RE}/id/{id_responsable}/{id_entregable}", timeout=10)
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                asociacion = datos[0]  # registro encontrado
                return render_template(
                    "responsable_entregable.html",
                    responsables=responsables,
                    entregables=entregables,
                    asociaciones=asociaciones,
                    modo="actualizar",
                    asociacion=asociacion,
                    mensaje="Asociación encontrada."
                )
            else:
                mensaje = "No se encontró la asociación."
        else:
            mensaje = f"No encontrado (status {respuesta.status_code})."
    except Exception as e:
        print("Error en búsqueda:", e)
        mensaje = "Error al consultar la API."

    return render_template(
        "responsable_entregable.html",
        responsables=responsables,
        entregables=entregables,
        asociaciones=asociaciones,
        modo="crear",
        asociacion=None,
        mensaje=mensaje
    )


# ------------------- CREAR asociación -------------------
@rutas_responsable_entregable.route("/responsable_entregable/crear", methods=["POST"])
def crear_responsable_entregable():
    datos = {
        "id_responsable": request.form.get("id_responsable"),
        "id_entregable": request.form.get("id_entregable"),
        "fecha_asociacion": request.form.get("fecha_asociacion")
    }

    try:
        resp = requests.post(API_RE, json=datos, timeout=10)
        if resp.status_code not in (200, 201):
            print("Error al crear asociación:", resp.status_code, resp.text)
    except Exception as e:
        print("Error al crear asociación:", e)

    return redirect(url_for("rutas_responsable_entregable.responsable_entregable"))


# ------------------- ACTUALIZAR asociación (solo fecha) -------------------
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
        # suponiendo endpoint PUT /id/{id_responsable}/{id_entregable}
        resp = requests.put(f"{API_RE}/id/{id_responsable}/{id_entregable}", json=datos, timeout=10)
        if resp.status_code not in (200, 204):
            print("Error al actualizar asociación:", resp.status_code, resp.text)
    except Exception as e:
        print("Error al actualizar asociación:", e)

    return redirect(url_for("rutas_responsable_entregable.responsable_entregable"))


# ------------------- ELIMINAR asociación (clave compuesta) -------------------
@rutas_responsable_entregable.route("/responsable_entregable/eliminar/<int:id_responsable>/<int:id_entregable>", methods=["POST"])
def eliminar_responsable_entregable(id_responsable, id_entregable):
    try:
        # suponiendo endpoint DELETE /id/{id_responsable}/{id_entregable}
        resp = requests.delete(f"{API_RE}/id/{id_responsable}/{id_entregable}", timeout=10)
        if resp.status_code not in (200, 204):
            print("Error al eliminar asociación:", resp.status_code, resp.text)
    except Exception as e:
        print("Error al eliminar asociación:", e)

    return redirect(url_for("rutas_responsable_entregable.responsable_entregable"))
