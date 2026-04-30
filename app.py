from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "clave-secreta"  # Necesario para manejar sesiones

# Función de conexión a PostgreSQL en Render
def get_db():
    conn = psycopg2.connect(
        host="dpg-d7podgr7uimc73deuhc0-a.oregon-postgres.render.com",
        database="turnosdb_jfsx",
        user="alete",
        password="Vbdlit1kUITFobBM6w365X3SpzbCmA6s",
        port="5432"
    )
    return conn

@app.route("/")
def root():
    # Si el usuario está logueado, mostrar la agenda
    if "usuario" in session:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM turnos ORDER BY id DESC")
        turnos = cur.fetchall()
        conn.close()
        return render_template("index.html", turnos=turnos)
    # Si no está logueado, redirigir al login
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        # Login fijo: admin/admin
        if usuario == "admin" and password == "admin":
            session["usuario"] = usuario
            conn = get_db()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM turnos ORDER BY id DESC")
            turnos = cur.fetchall()
            conn.close()
            return render_template("index.html", turnos=turnos)
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/agendar", methods=["POST"])
def agendar():
    if "usuario" not in session:
        return redirect(url_for("login"))
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO turnos (nombre, fecha) VALUES (%s, %s)", (nombre, fecha))
    conn.commit()
    cur.close()
    conn.close()
    # Volver a la agenda mostrando todos los turnos
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM turnos ORDER BY id DESC")
    turnos = cur.fetchall()
    conn.close()
    return render_template("index.html", turnos=turnos)
