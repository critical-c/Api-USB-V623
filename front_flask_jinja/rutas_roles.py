# ===============================================================
# Módulo: rutas_roles.py
# Descripción: Contiene las rutas del módulo de roles.
# Se comunica con la API externa (C#) para listar, buscar,
# crear, actualizar y eliminar roles.
# Incluye mensajes flash de confirmación o error.
# ===============================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

# ===============================================================
# Configuración del Blueprint
# ===============================================================
rutas_roles = Blueprint("rutas_roles", __name__)
API_URL = "http://localhost:5031/api/rol"  # URL base de la API para roles


# ===============================================================
# RUTA: LISTAR ROLES
# Método: GET
# ===============================================================
@rutas_roles.route("/roles", methods=["GET"])
def listar_roles():
    """
    Lista todos los roles disponibles obtenidos desde la API.
    """
    try:
        respuesta = requests.get(API_URL)
        roles = respuesta.json().get("datos", [])
    except Exception as e:
        roles = []
        flash("Error al conectar con la API de roles.", "error")
        print("Error al conectar con la API de roles:", e)

    return render_template("roles.html", roles=roles, rol=None, modo="crear")


# ===============================================================
# RUTA: BUSCAR ROL POR ID
# Método: POST (se usa formulario)
# ===============================================================
@rutas_roles.route("/roles/buscar", methods=["POST"])
def buscar_rol():
    """
    Busca un rol específico según su ID ingresado en el formulario.
    """
    id_rol = request.form.get("id_buscar")

    try:
        respuesta = requests.get(f"{API_URL}/id/{id_rol}")
        if respuesta.status_code == 200:
            datos = respuesta.json().get("datos", [])
            if datos:
                rol = datos[0]
                roles = requests.get(API_URL).json().get("datos", [])
                flash("Rol encontrado correctamente.", "exito")
                return render_template("roles.html", roles=roles, rol=rol, modo="actualizar")
            else:
                flash("Rol no encontrado.", "error")
        else:
            flash("Rol no encontrado.", "error")
    except Exception as e:
        flash("Error al buscar rol.", "error")
        print("Error al buscar rol:", e)

    roles = requests.get(API_URL).json().get("datos", [])
    return render_template("roles.html", roles=roles, rol=None, modo="crear")


# ===============================================================
# RUTA: CREAR NUEVO ROL
# Método: POST
# ===============================================================
@rutas_roles.route("/roles", methods=["POST"])
def crear_rol():
    """
    Crea un nuevo rol en la base de datos a través de la API.
    """
    datos = {"nombre": request.form.get("nombre")}

    try:
        respuesta = requests.post(API_URL, json=datos)
        if respuesta.status_code == 200:
            flash("Rol creado correctamente.", "exito")
        else:
            flash("Error al crear rol.", "error")
    except Exception as e:
        flash("Error al crear rol.", "error")
        print("Error al crear rol:", e)

    return redirect(url_for("rutas_roles.listar_roles"))


# ===============================================================
# RUTA: ACTUALIZAR ROL EXISTENTE
# Método: POST (por limitación de HTML)
# ===============================================================
@rutas_roles.route("/roles/actualizar/<int:id>", methods=["POST"])
def actualizar_rol(id):
    """
    Actualiza el nombre de un rol existente.
    """
    datos = {"nombre": request.form.get("nombre")}

    try:
        respuesta = requests.put(f"{API_URL}/id/{id}", json=datos)
        if respuesta.status_code == 200:
            flash("Rol actualizado correctamente.", "exito")
        else:
            flash("Error al actualizar rol.", "error")
    except Exception as e:
        flash("Error al actualizar rol.", "error")
        print("Error al actualizar rol:", e)

    return redirect(url_for("rutas_roles.listar_roles"))


# ===============================================================
# RUTA: ELIMINAR ROL EXISTENTE
# Método: POST (por limitación de HTML)
# ===============================================================
@rutas_roles.route("/roles/eliminar/<int:id>", methods=["POST"])
def eliminar_rol(id):
    """
    Elimina un rol según su ID.
    """
    try:
        respuesta = requests.delete(f"{API_URL}/id/{id}")
        if respuesta.status_code == 200:
            flash("Rol eliminado correctamente.", "exito")
        else:
            flash("Error al eliminar rol.", "error")
    except Exception as e:
        flash("Error al eliminar rol.", "error")
        print("Error al eliminar rol:", e)

    return redirect(url_for("rutas_roles.listar_roles"))
