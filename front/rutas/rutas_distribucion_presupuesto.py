from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de distribucion_presupuesto
rutas_distribucion_presupuesto = Blueprint("rutas_distribucion_presupuesto", __name__)

# URL base de la API en C# que gestiona las distribuciones de presupuesto
API_URL = "http://localhost:5031/api/distribucion_presupuesto"
API_PRESUPUESTO = "http://localhost:5031/api/presupuesto"
API_PROYECTO = "http://localhost:5031/api/proyecto"

# ------------------- LISTAR distribucion_presupuesto -------------------
@rutas_distribucion_presupuesto.route("/distribucion_presupuesto")
def distribucion_presupuesto():
    try:
        distribuciones_presupuesto = requests.get(API_URL).json().get("datos", [])
        presupuesto = requests.get(API_PRESUPUESTO).json().get("datos", [])
        proyectos = requests.get(API_PROYECTO).json().get("datos", [])
    except Exception as e:
        distribuciones_presupuesto, presupuesto = [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "distribuciones_presupuesto.html",
        distribuciones_presupuesto=distribuciones_presupuesto,
        distribucion_presupuesto=None,
        proyectos=proyectos,
        presupuesto=presupuesto,
        modo="crear"
    )

# ------------------- BUSCAR distribucion_presupuesto -------------------
@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/buscar", methods=["POST"])
def buscar_distribucion_presupuesto():
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    distribucion_presupuesto = datos[0]
                    distribuciones_presupuesto = requests.get(API_URL).json().get("datos", [])
                    presupuesto = requests.get(API_PRESUPUESTO).json().get("datos", [])
                    proyectos = requests.get(API_PROYECTO).json().get("datos", [])
                    return render_template(
                        "distribuciones_presupuesto.html",
                        distribuciones_presupuesto=distribuciones_presupuesto,
                        distribucion_presupuesto=distribucion_presupuesto,
                        proyectos=proyectos,
                        presupuesto=presupuesto,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    distribuciones_presupuesto = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "distribuciones_presupuesto.html",
        distribuciones_presupuesto=distribuciones_presupuesto,
        distribucion_presupuesto=None,
        mensaje="Distribución de presupuesto no encontrada",
        modo="crear"
    )

# ------------------- CREAR distribucion_presupuesto -------------------
@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/crear", methods=["POST"])
def crear_distribucion_presupuesto():
    datos = {
        "presupuesto_padre_id": request.form.get("presupuesto_padre_id"),
        "proyecto_hijo_id": request.form.get("proyecto_hijo_id"),
        "monto_asignado": float(request.form.get("monto_asignado"))
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la distribución de presupuesto: {e}"

    return redirect(url_for("rutas_distribucion_presupuesto.distribucion_presupuesto"))

# ------------------- ACTUALIZAR distribucion_presupuesto -------------------
@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/actualizar", methods=["POST"])
def actualizar_distribucion_presupuesto():
    codigo = request.form.get("id")
    datos = {
        "presupuesto_padre_id": request.form.get("presupuesto_padre_id"),
        "proyecto_hijo_id": request.form.get("proyecto_hijo_id"),
        "monto_asignado": float(request.form.get("monto_asignado"))
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar la distribución de presupuesto: {e}"

    return redirect(url_for("rutas_distribucion_presupuesto.distribucion_presupuesto"))

# ------------------- ELIMINAR distribucion_presupuesto -------------------
@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_distribucion_presupuesto(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar la distribución de presupuesto: {e}"

    return redirect(url_for("rutas_distribucion_presupuesto.distribucion_presupuesto"))
