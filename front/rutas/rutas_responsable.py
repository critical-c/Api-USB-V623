from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_responsable = Blueprint("rutas_responsable", __name__)

# APIs en C#
API_RESPONSABLE_URL = "http://localhost:5031/api/responsable"
API_TIPO_RESPONSABLE_URL = "http://localhost:5031/api/tipo_responsable"
API_USUARIO_URL = "http://localhost:5031/api/usuario"

# ------------------- LISTAR responsables -------------------
@rutas_responsable.route("/responsable")
def responsable():
    try:
        responsables = requests.get(API_RESPONSABLE_URL).json().get("datos", [])
    except Exception as e:
        print("Error al cargar responsables:", e)
        responsables = []

    try:
        tipos_responsable = requests.get(API_TIPO_RESPONSABLE_URL).json().get("datos", [])
    except Exception:
        tipos_responsable = []

    try:
        usuarios = requests.get(API_USUARIO_URL).json().get("datos", [])
    except Exception:
        usuarios = []

    return render_template(
        "responsable.html",
        responsables=responsables,
        responsable=None,
        tipos_responsable=tipos_responsable,
        usuarios=usuarios,
        modo="crear"
    )

# ------------------- BUSCAR responsable -------------------
@rutas_responsable.route("/responsable/buscar", methods=["POST"])
def buscar_responsable():
    id_buscar = request.form.get("codigo_buscar")

    try:
        respuesta = requests.get(f"{API_RESPONSABLE_URL}/id/{id_buscar}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                responsable = datos[0]
                responsables = requests.get(API_RESPONSABLE_URL).json().get("datos", [])
                tipos_responsable = requests.get(API_TIPO_RESPONSABLE_URL).json().get("datos", [])
                usuarios = requests.get(API_USUARIO_URL).json().get("datos", [])
                return render_template(
                    "responsable.html",
                    responsables=responsables,
                    responsable=responsable,
                    tipos_responsable=tipos_responsable,
                    usuarios=usuarios,
                    modo="actualizar"
                )
    except Exception as e:
        print("Error al buscar responsable:", e)

    return redirect(url_for("rutas_responsable.responsable"))

# ------------------- CREAR responsable -------------------
@rutas_responsable.route("/responsable/crear", methods=["POST"])
def crear_responsable():
    datos = {
        "id_tipo_responsable": request.form.get("id_tipo_responsable"),
        "id_usuario": request.form.get("id_usuario"),
        "nombre": request.form.get("nombre")
    }

    try:
        requests.post(API_RESPONSABLE_URL, json=datos)
    except Exception as e:
        print("Error al crear responsable:", e)

    return redirect(url_for("rutas_responsable.responsable"))

# ------------------- ACTUALIZAR responsable -------------------
@rutas_responsable.route("/responsable/actualizar", methods=["POST"])
def actualizar_responsable():
    codigo = request.form.get("id")
    datos = {
        "id": codigo,
        "id_tipo_responsable": request.form.get("id_tipo_responsable"),
        "id_usuario": request.form.get("id_usuario"),
        "nombre": request.form.get("nombre")
    }

    try:
        requests.put(f"{API_RESPONSABLE_URL}/id/{codigo}", json=datos)
    except Exception as e:
        print("Error al actualizar responsable:", e)

    return redirect(url_for("rutas_responsable.responsable"))

# ------------------- ELIMINAR responsable -------------------
@rutas_responsable.route("/responsable/eliminar/<string:codigo>", methods=["POST"])
def eliminar_responsable(codigo):
    try:
        requests.delete(f"{API_RESPONSABLE_URL}/id/{codigo}")
    except Exception as e:
        print("Error al eliminar responsable:", e)

    return redirect(url_for("rutas_responsable.responsable"))
