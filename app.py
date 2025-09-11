from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import psycopg2
import os
from werkzeug.utils import secure_filename

# Configuración de Flask
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="eventos_db",
        user="postgres",
        password="eliud"
    )

# Ruta principal: solo eventos futuros o actuales
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM eventos 
        WHERE (fecha > CURRENT_DATE) 
           OR (fecha = CURRENT_DATE AND hora >= CURRENT_TIME)
        ORDER BY fecha, hora;
    """)
    eventos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", eventos=eventos, mostrar_todos=False)

# Nueva ruta: muestra todos los eventos (activos e inactivos)
@app.route('/todos')
def todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM eventos ORDER BY fecha, hora;")
    eventos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", eventos=eventos, mostrar_todos=True)

# Crear nuevo evento
@app.route('/nuevo', methods=("GET", "POST"))
def nuevo():
    if request.method == "POST":
        creador = request.form["creador"]
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
        cur.execute(
            "INSERT INTO eventos (creador, nombre, fecha, hora, descripcion, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
            (creador, nombre, fecha, hora, descripcion, imagen),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    return render_template("form.html", evento=None)

# Editar evento
@app.route('/editar/<int:id>', methods=("GET", "POST"))
def editar(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        creador = request.form["creador"]
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

        if imagen:
            cur.execute(
                "UPDATE eventos SET creador=%s, nombre=%s, fecha=%s, hora=%s, descripcion=%s, imagen=%s WHERE id=%s",
                (creador, nombre, fecha, hora, descripcion, imagen, id),
            )
        else:
            cur.execute(
                "UPDATE eventos SET creador=%s, nombre=%s, fecha=%s, hora=%s, descripcion=%s WHERE id=%s",
                (creador, nombre, fecha, hora, descripcion, id),
            )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    cur.execute("SELECT * FROM eventos WHERE id=%s", (id,))
    evento = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("form.html", evento=evento)

# Eliminar evento
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM eventos WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

# Servir imágenes subidas
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

