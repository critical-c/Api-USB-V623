from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_ejecucion_presupuesto = Blueprint("rutas_ejecucion_presupuesto", __name__)

# URLs base
API_URL = "http://localhost:5031/api/ejecucion_presupuesto"
API_PRESUPUESTO = "http://localhost:5031/api/presupuesto"

# ------------------- LISTAR -------------------
@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto")
def ejecucion_presupuesto():
    try:
        ejecuciones = requests.get(API_URL).json().get("datos", [])
        presupuestos = requests.get(API_PRESUPUESTO).json().get("datos", [])
    except Exception as e:
        ejecuciones, presupuestos = [], []
        print("Error al conectar con la API:", e)

    return render_template(
        "ejecuciones_presupuesto.html",
        ejecuciones_presupuesto=ejecuciones,
        ejecucion_presupuesto=None,
        presupuestos=presupuestos,
        modo="crear"
    )

# ------------------- BUSCAR -------------------
@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/buscar", methods=["POST"])
def buscar_ejecucion_presupuesto():
    codigo = request.form.get("codigo_buscar")
    presupuestos = requests.get(API_PRESUPUESTO).json().get("datos", [])

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/id/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    ejecucion = datos[0]
                    ejecuciones = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "ejecuciones_presupuesto.html",
                        ejecuciones_presupuesto=ejecuciones,
                        ejecucion_presupuesto=ejecucion,
                        presupuestos=presupuestos,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    ejecuciones = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "ejecuciones_presupuesto.html",
        ejecuciones_presupuesto=ejecuciones,
        ejecucion_presupuesto=None,
        presupuestos=presupuestos,
        mensaje="Ejecución no encontrada",
        modo="crear"
    )

# ------------------- CREAR -------------------
@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/crear", methods=["POST"])
def crear_ejecucion_presupuesto():
    datos = {
        "presupuesto_id": int(request.form.get("presupuesto_id")),
        "anio": int(request.form.get("anio")),
        "monto_planeado": float(request.form.get("monto_planeado")),
        "monto_ejecutado": float(request.form.get("monto_ejecutado")),
        "observaciones": request.form.get("observaciones") or None
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear la ejecución: {e}"

    return redirect(url_for("rutas_ejecucion_presupuesto.ejecucion_presupuesto"))

# ------------------- ACTUALIZAR -------------------
@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/actualizar", methods=["POST"])
def actualizar_ejecucion_presupuesto():
    codigo = request.form.get("id")
    datos = {
        "presupuesto_id": int(request.form.get("presupuesto_id")),
        "anio": int(request.form.get("anio")),
        "monto_planeado": float(request.form.get("monto_planeado")),
        "monto_ejecutado": float(request.form.get("monto_ejecutado")),
        "observaciones": request.form.get("observaciones") or None
    }

    try:
        requests.put(f"{API_URL}/id/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar: {e}"

    return redirect(url_for("rutas_ejecucion_presupuesto.ejecucion_presupuesto"))

# ------------------- ELIMINAR -------------------
@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/eliminar/<string:codigo>", methods=["POST"])
def eliminar_ejecucion_presupuesto(codigo):
    try:
        requests.delete(f"{API_URL}/id/{codigo}")
    except Exception as e:
        return f"Error al eliminar: {e}"

    return redirect(url_for("rutas_ejecucion_presupuesto.ejecucion_presupuesto"))
