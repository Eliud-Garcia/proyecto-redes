from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date, datetime
import psycopg2
import os

# -------------------------------------
# ⚙️ CONFIGURACIÓN GENERAL
# -------------------------------------
app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # cámbiala en producción

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

DB_CONFIG = {
    "dbname": "eventos_db",
    "user": "postgres",
    "password": "eliud",
    "host": "localhost",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Mostrar año actual en el footer
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# -------------------------------------
# 🔐 AUTENTICACIÓN
# -------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, rol FROM usuarios WHERE username=%s", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["rol"] = user[3]
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)",
                (username, hashed)
            )
            conn.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("El usuario ya existe.", "danger")
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("index"))

# -------------------------------------
# 🎟️ EVENTOS
# -------------------------------------
@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, creador, nombre, fecha, hora, descripcion, imagen
        FROM eventos
        WHERE activo = TRUE AND fecha >= %s
        ORDER BY fecha ASC
    """, (date.today(),))
    eventos = cur.fetchall()
    conn.close()
    return render_template("index.html", eventos=eventos, usuario=session.get("username"), rol=session.get("rol"))

@app.route("/eventos_todos")
def eventos_todos():
    if "user_id" not in session:
        flash("Debes iniciar sesión para ver todos los eventos.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, creador, nombre, fecha, hora, descripcion, imagen
        FROM eventos
        ORDER BY fecha DESC
    """)
    eventos = cur.fetchall()
    conn.close()

    return render_template("eventos_todos.html", eventos=eventos, current_date=date.today())

# ➕ AGREGAR EVENTO
@app.route("/agregar", methods=["GET", "POST"])
def agregar_evento():
    if "user_id" not in session:
        flash("Debes iniciar sesión para agregar un evento.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        creador = session["username"]
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"]

        imagen = None
        if "imagen" in request.files:
            file = request.files["imagen"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                imagen = filename

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO eventos (creador, nombre, fecha, hora, descripcion, imagen, activo)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
        """, (creador, nombre, fecha, hora, descripcion, imagen))
        conn.commit()
        conn.close()

        flash("Evento agregado correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("agregar.html")

# ✏️ EDITAR EVENTO
@app.route("/editar/<int:evento_id>", methods=["GET", "POST"])
def editar_evento(evento_id):
    if "user_id" not in session:
        flash("Debes iniciar sesión para editar un evento.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, creador, nombre, fecha, hora, descripcion, imagen FROM eventos WHERE id = %s", (evento_id,))
    evento = cur.fetchone()

    if not evento:
        flash("Evento no encontrado.", "danger")
        conn.close()
        return redirect(url_for("index"))

    # Validar permisos
    if evento[1] != session["username"] and session["rol"] != "admin":
        flash("No tienes permiso para editar este evento.", "danger")
        conn.close()
        return redirect(url_for("index"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"]

        imagen = evento[6]  # mantener la existente si no se cambia
        if "imagen" in request.files:
            file = request.files["imagen"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                imagen = filename

        cur.execute("""
            UPDATE eventos SET nombre=%s, fecha=%s, hora=%s, descripcion=%s, imagen=%s WHERE id=%s
        """, (nombre, fecha, hora, descripcion, imagen, evento_id))
        conn.commit()
        conn.close()

        flash("Evento actualizado correctamente.", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("editar.html", evento=evento)

# ❌ ELIMINAR EVENTO
@app.route("/eliminar/<int:evento_id>", methods=["POST"])
def eliminar_evento(evento_id):
    if "user_id" not in session:
        flash("Debes iniciar sesión para eliminar un evento.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT creador FROM eventos WHERE id = %s", (evento_id,))
    evento = cur.fetchone()

    if not evento:
        flash("Evento no encontrado.", "danger")
        conn.close()
        return redirect(url_for("index"))

    if evento[0] != session["username"] and session["rol"] != "admin":
        flash("No tienes permiso para eliminar este evento.", "danger")
        conn.close()
        return redirect(url_for("index"))

    cur.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
    conn.commit()
    conn.close()

    flash("Evento eliminado correctamente.", "success")
    return redirect(url_for("index"))

# 📸 SERVIR IMÁGENES
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# -------------------------------------
# 🚀 MAIN
# -------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
