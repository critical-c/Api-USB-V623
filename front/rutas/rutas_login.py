from flask import Blueprint, render_template, request, redirect, url_for, session
import requests

rutas_login = Blueprint("rutas_login", __name__)
API_URL = "http://localhost:5031/api/usuario"

# ------------------- LOGIN -------------------
@rutas_login.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")

        try:
            respuesta = requests.get(API_URL)
            usuarios = respuesta.json().get("datos", [])
        except Exception as e:
            return render_template("login.html", error=f"Error conectando con la API: {e}")

        for user in usuarios:
            if user["email"] == email and user["contrasena"] == contrasena:
                session["usuario"] = user
                return redirect(url_for("inicio"))

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


# ------------------- LOGOUT -------------------
@rutas_login.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("rutas_login.login"))
