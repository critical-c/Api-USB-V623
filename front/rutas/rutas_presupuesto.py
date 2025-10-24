from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de presupuesto
rutas_presupuesto = Blueprint("rutas_presupuesto", __name__)

# URLs base de las APIs en C#
API_PRESUPUESTO_URL = "http://localhost:5031/api/presupuesto"
API_PROYECTO_URL = "http://localhost:5031/api/proyecto"
API_ESTADO_URL = "http://localhost:5031/api/estado"

# ------------------- LISTAR presupuestos -------------------
@rutas_presupuesto.route("/presupuesto")
def presupuesto():
    try:
        respuesta = requests.get(API_PRESUPUESTO_URL)
        presupuestos = respuesta.json().get("datos", [])
    except Exception as e:
        presupuestos = []
        print("Error al conectar con la API de presupuesto:", e)

    # Obtener lista de proyectos
    try:
        proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
    except Exception as e:
        proyectos = []
        print("Error al conectar con la API de proyectos:", e)

    # Obtener lista de estados
    try:
        estados = requests.get(API_ESTADO_URL).json().get("datos", [])
    except Exception as e:
        estados = []
        print("Error al conectar con la API de estados:", e)

    return render_template(
        "presupuesto.html",
        presupuestos=presupuestos,
        presupuesto=None,
        proyectos=proyectos,
        estados=estados,
        modo="crear"
    )

# ------------------- BUSCAR presupuesto -------------------
@rutas_presupuesto.route("/presupuesto/buscar", methods=["POST"])
def buscar_presupuesto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_PRESUPUESTO_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    presupuesto = datos[0]
                    presupuestos = requests.get(API_PRESUPUESTO_URL).json().get("datos", [])
                    proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
                    estados = requests.get(API_ESTADO_URL).json().get("datos", [])
                    return render_template(
                        "presupuesto.html",
                        presupuestos=presupuestos,
                        presupuesto=presupuesto,
                        proyectos=proyectos,
                        estados=estados,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    presupuestos = requests.get(API_PRESUPUESTO_URL).json().get("datos", [])
    proyectos = requests.get(API_PROYECTO_URL).json().get("datos", [])
    estados = requests.get(API_ESTADO_URL).json().get("datos", [])

    return render_template(
        "presupuesto.html",
        presupuestos=presupuestos,
        presupuesto=None,
        proyectos=proyectos,
        estados=estados,
        mensaje="Presupuesto no encontrado",
        modo="crear"
    )

# ------------------- CREAR presupuesto -------------------
@rutas_presupuesto.route("/presupuesto/crear", methods=["POST"])
def crear_presupuesto():
    datos = {
        "id_proyecto": request.form.get("id_proyecto"),
        "estado": request.form.get("estado"),
        "monto_solicitado": request.form.get("monto_solicitado"),
        "monto_aprobado": request.form.get("monto_aprobado"),
        "periodo_anio": request.form.get("periodo_anio"),
        "fecha_solicitud": request.form.get("fecha_solicitud"),
        "fecha_aprobacion": request.form.get("fecha_aprobacion"),
        "observaciones": request.form.get("observaciones")
    }

    try:
        requests.post(API_PRESUPUESTO_URL, json=datos)
    except Exception as e:
        return f"Error al crear el presupuesto: {e}"

    return redirect(url_for("rutas_presupuesto.presupuesto"))

# ------------------- ACTUALIZAR presupuesto -------------------
@rutas_presupuesto.route("/presupuesto/actualizar", methods=["POST"])
def actualizar_presupuesto():
    codigo = request.form.get("id")
    datos = {
        "id": codigo,
        "id_proyecto": request.form.get("id_proyecto"),
        "estado": request.form.get("estado"),
        "monto_solicitado": request.form.get("monto_solicitado"),
        "monto_aprobado": request.form.get("monto_aprobado"),
        "periodo_anio": request.form.get("periodo_anio"),
        "fecha_solicitud": request.form.get("fecha_solicitud"),
        "fecha_aprobacion": request.form.get("fecha_aprobacion"),
        "observaciones": request.form.get("observaciones")
    }

    try:
        requests.put(f"{API_PRESUPUESTO_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar presupuesto: {e}"

    return redirect(url_for("rutas_presupuesto.presupuesto"))

# ------------------- ELIMINAR presupuesto -------------------
@rutas_presupuesto.route("/presupuesto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_presupuesto(codigo):
    try:
        requests.delete(f"{API_PRESUPUESTO_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar presupuesto: {e}"

    return redirect(url_for("rutas_presupuesto.presupuesto"))
