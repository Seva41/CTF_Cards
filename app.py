'''
CTF 2 - Seguridad en TI
TICS413 2024-2 Viña del Mar - Santiago

Hecho por: Sebastián Dinator
https://sebadinator.com/
Noviembre 2024

Python 3.10.11
'''

from flask import (
    Flask,
    render_template,
    request,
    session,
    send_from_directory,
    g,
    abort,
)
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import sqlite3
import hashlib
import os
import base64
import logging
from logging.handlers import RotatingFileHandler
import re
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria para las sesiones
csrf = CSRFProtect(app)  # Protección CSRF

# Configuración de cookies seguras
app.config["SESSION_COOKIE_SECURE"] = True  # Solo permite cookies en HTTPS
app.config["SESSION_COOKIE_HTTPONLY"] = (
    True  # No permite acceso a las cookies desde JavaScript
)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Previene CSRF
app.config["SESSION_PERMANENT"] = True  # Sesiones persistentes
app.config["SESSION_TYPE"] = "filesystem"  # Almacena sesiones en el sistema de archivos

app.permanent_session_lifetime = timedelta(
    minutes=90
)  # Sesiones expiran después de 90 minutos
Session(app)

if not app.debug:
    file_handler = RotatingFileHandler("error.log", maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


limiter = Limiter(
    key_func=get_remote_address,
)
limiter.init_app(app)


# Inicialización del estado de los desafíos
@app.before_request
def initialize_session():
    if "challenge_status" not in session:
        session["challenge_status"] = {
            "crofie1": False,
            "inform2": False,
            "hcact3": False,
            "cifch4": False,
        }
    if "final_status" not in session:
        session["final_status"] = {
            "finalboss5": False,
        }


# Generación de nonce para Content-Security-Policy
@app.before_request
def generate_nonce():
    g.nonce = base64.b64encode(os.urandom(16)).decode()


# Configuración de headers de seguridad
@app.after_request
def set_security_headers(response):
    nonce = getattr(g, "nonce", None)
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains; preload"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{g.nonce}' https://cdn.jsdelivr.net; "
        f"style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    )
    return response


# Manejo seguro de archivos estáticos
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


# Manejo de errores
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("429.html"), 429


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template("403.html"), 403


# Definición de banderas
flag1 = "segti{XSS_SUCCESS}"
flag2 = "segti{INJECTION_DONE}"
flag3 = "segti{GOT_HASHED}"
flag4 = "segti{DECRYPTED_ONE}"
flag5 = "segti{H4CKER_W1N}"


# Ruta de inicio
@app.route("/")
def index():
    if "challenge_status" not in session:
        session["challenge_status"] = {
            "crofie1": False,
            "inform2": False,
            "hcact3": False,
            "cifch4": False,
        }
    if "final_status" not in session:
        session["final_status"] = {
            "finalboss5": False,
        }
    all_completed = all(session["challenge_status"].values())
    return render_template(
        "index.html",
        challenge_status=session["challenge_status"],
        all_completed=all_completed,
        final_status=session["final_status"],
    )


# Challenge 1: XSS
@app.route("/crofie1", methods=["GET", "POST"])
@limiter.limit("300 per minute")
def crofie1():
    success_message = None
    error_message = None

    ACCEPTED_XSS_PAYLOADS = [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert('xss')>",
        "<svg/onload=alert('xss')>",
        "<iframe src='javascript:alert(\"xss\")'></iframe>",
        "<div onclick=\"alert('xss')\">Click me</div>",
        "<a href='javascript:alert(\"xss\")'>Click me</a>",
        "<body onload=alert('xss')>",
        "<img src=\"javascript:alert('xss')\">",
        "<svg onload=alert('xss')>",
        "<script>ALERT('xss')</script>",
        '<a href="javascript:alert(’¡Hola, has sido hackeado!’);">Click me!</a>',
        "<a href='javascript:alert(’¡Hola, has sido hackeado!’);'>Click me!</a>",
        "<script>alert('Mensaje 1')</script>",
        '<script>alert("Mensaje 1")</script>',
    ]

    # Función para verificar si el comentario contiene un payload XSS aceptado
    def is_valid_xss(comment):
        for payload in ACCEPTED_XSS_PAYLOADS:
            if payload.lower() in comment.lower():
                return True
        return False

    # Mostrar bandera si ya está completado
    if session["challenge_status"]["crofie1"]:
        success_message = f"¡Bandera encontrada! {flag1}"
    elif request.method == "POST":
        comment = request.form.get("comment")
        if (
            re.search(r"<script>", comment, re.IGNORECASE)
            or re.search(r"onload", comment, re.IGNORECASE)
            or re.search(r"svg", comment, re.IGNORECASE)
            or re.search(r"iframe", comment, re.IGNORECASE)
            or re.search(r"onclick", comment, re.IGNORECASE)
            or re.search(r"href", comment, re.IGNORECASE)
        ):
            if is_valid_xss(comment):
                session["challenge_status"]["crofie1"] = True
                session.modified = True  # Asegura que la sesión se actualice
                success_message = f"¡Bandera encontrada! {flag1}"
            else:
                error_message = "El comentario no es correcto. Intenta de nuevo."
        else:
            error_message = "El comentario parece no adecuado para este foro."

    return render_template(
        "crofie1.html", success_message=success_message, error_message=error_message
    )


# Challenge 2: SQL Injection
@app.route("/inform2", methods=["GET", "POST"])
@limiter.limit("300 per minute")
def inform2():
    success_message = None
    error_message = None
    result = None  # Inicializar result

    # Mostrar bandera si ya está completado
    if session["challenge_status"]["inform2"]:
        success_message = f"¡Bandera encontrada! {flag2}"
    elif request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            # Consulta SQL vulnerable a inyección
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            # print(query)
            try:
                cur.execute(query)
                result = cur.fetchone()
            except sqlite3.Error as e:
                error_message = "Error al acceder a la base de datos."
                app.logger.error(f"SQL Error: {e}")
            finally:
                con.close()

            # Si se encuentra un resultado, marcar como completado
            if result:
                session["challenge_status"]["inform2"] = True
                session.modified = True
                success_message = f"¡Bandera encontrada! {flag2}"
            else:
                if not error_message:
                    error_message = "Credenciales incorrectas. Intenta de nuevo."

        except Exception as e:
            error_message = (
                "Ocurrió un error inesperado. Por favor, intenta de nuevo más tarde."
            )
            app.logger.error(f"Error en inform2: {e}")

    return render_template(
        "inform2.html", success_message=success_message, error_message=error_message
    )


# Challenge 3: Hashing
@app.route("/hcact3", methods=["GET", "POST"])
@limiter.limit("300 per minute")
def hcact3():
    success_message = None
    error_message = None
    p = "pikachu1234"
    hashed_password = hashlib.sha256(p.encode()).hexdigest()

    # Mostrar bandera si ya está completado
    if session["challenge_status"]["hcact3"]:
        success_message = f"¡Bandera encontrada! {flag3}"
    elif request.method == "POST":
        password = request.form.get("password")
        if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
            session["challenge_status"]["hcact3"] = True
            session.modified = True
            success_message = f"¡Bandera encontrada! {flag3}"
        else:
            error_message = "Mensaje incorrecto. Intenta de nuevo."

    return render_template(
        "hcact3.html",
        success_message=success_message,
        error_message=error_message,
        hashed_password=hashed_password,
    )


# Challenge 4: Cifrado
@app.route("/cifch4", methods=["GET", "POST"])
@limiter.limit("300 per minute")
def cifch4():
    success_message = None
    error_message = None
    encrypted_message = "h3rg3i_a4cvj4v3"  # ROT15

    # Mostrar bandera si ya está completado
    if session["challenge_status"]["cifch4"]:
        success_message = f"¡Bandera encontrada! {flag4}"
    elif request.method == "POST":
        decrypted_message = request.form.get("decrypted_message")
        if decrypted_message == "s3cr3t_l4ngu4g3":
            session["challenge_status"]["cifch4"] = True
            session.modified = True
            success_message = f"¡Bandera encontrada! {flag4}"
        else:
            error_message = "El mensaje es incorrecto. Intenta de nuevo."

    return render_template(
        "cifch4.html",
        success_message=success_message,
        error_message=error_message,
        encrypted_message=encrypted_message,
    )


@app.route("/finalboss5", methods=["GET", "POST"])
@limiter.limit("300 per minute")
def finalboss5():
    if not all(session["challenge_status"].values()):
        abort(403)  # Prohibir acceso si no ha completado todos los desafíos previos.
    success_message = None
    error_message = None

    out = "8d9850c884aa4e8a4b73ca422ebb0195"
    key = "02672469526323625526541869952461"
    IV = "84532186251485468562186856456566"
    conf = "HEXHEXCBCRAWHEX"

    # Lógica para el quinto desafío
    if session["final_status"]["finalboss5"]:
        success_message = f"¡Bandera encontrada! {flag5}"
    elif request.method == "POST":
        answer = request.form.get("answer")
        if answer == "B055_D3F34T3D":  # Cambia esto por tu lógica real
            session["final_status"]["finalboss5"] = True
            session.modified = True
            success_message = f"¡Bandera encontrada! {flag5}"
        else:
            error_message = "Respuesta incorrecta. Intenta de nuevo."

    return render_template(
        "finalboss5.html",
        success_message=success_message,
        error_message=error_message,
        key=key,
        out=out,
        IV=IV,
        conf=conf,
    )


# Ejecución de la aplicación
if __name__ == "__main__":
    app.run(debug=False)
