# Importar la clase principal de Flask y la función para renderizar plantillas
from flask import Flask, render_template

# Importar el Blueprint que contiene las rutas de productos

from rutas.rutas_usuarios import rutas_usuarios
from rutas.rutas_tipo_responsable import rutas_tipo_responsable
from rutas.rutas_tipo_proyecto import rutas_tipo_proyecto
from rutas.rutas_estado import rutas_estado
from rutas.rutas_tipo_producto import rutas_tipo_producto
from rutas.rutas_entregable import rutas_entregable
from rutas.rutas_variable_estrategica import rutas_variable_estrategica

# Crear la instancia de la aplicación Flask
aplicacion = Flask(__name__)
# Clave secreta utilizada por Flask para firmar las sesiones y permitir el uso de mensajes flash.
# Es obligatoria cuando se usan sesiones o funciones como flash() y debe mantenerse privada.
aplicacion.secret_key = "clave-secreta-12345"


# ------------------- Registro de Blueprints -------------------
# Registrar el Blueprint de productos en la aplicación principal

aplicacion.register_blueprint(rutas_usuarios)
aplicacion.register_blueprint(rutas_tipo_responsable)
aplicacion.register_blueprint(rutas_tipo_proyecto)
aplicacion.register_blueprint(rutas_estado)
aplicacion.register_blueprint(rutas_tipo_producto)
aplicacion.register_blueprint(rutas_entregable)
aplicacion.register_blueprint(rutas_variable_estrategica)




# ------------------- Rutas principales -------------------

@aplicacion.route("/")
def inicio():
    """
    Función asociada a la ruta principal (/).
    Retorna la plantilla index.html.
    """
    return render_template("index.html")


@aplicacion.route("/acerca")
def acerca():
    """
    Función asociada a la ruta /acerca.
    Retorna la plantilla acerca.html con información sobre el proyecto.
    """
    return render_template("acerca.html")

# ---------------------------------------------------------
# ===============================================================
# MANEJO DE ERRORES
# ===============================================================
from flask import render_template

# Error 404 - Página no encontrada
@aplicacion.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("error.html", codigo=404, mensaje="Página no encontrada."), 404

# Error 500 - Error interno del servidor
@aplicacion.errorhandler(500)
def error_interno(e):
    return render_template("error.html", codigo=500, mensaje="Error interno del servidor."), 500

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Ejecutar la aplicación en modo depuración, en el puerto 5000
    # host="0.0.0.0" permite que la app sea accesible desde la red local
    # debug=True permite reinicio automático ante cambios
    aplicacion.run(host="0.0.0.0", port=5000, debug=True)
