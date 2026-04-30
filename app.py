from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave-secreta"  # Necesario para manejar sesiones

DB_FILE = "turnos.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()

# Siempre inicializar la base al arrancar
init_db()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def root():
    # Si el usuario está logueado, mostrar agenda
    if "usuario" in session:
        conn = get_db()
        turnos = conn.execute("SELECT * FROM turnos").fetchall()
        return render_template("index.html", turnos=turnos)
    # Si no, ir al login
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        if usuario == "admin" and password == "admin":
            session["usuario"] = usuario
            conn = get_db()
            turnos = conn.execute("SELECT * FROM turnos").fetchall()
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
    conn.execute("INSERT INTO turnos (nombre, fecha) VALUES (?, ?)", (nombre, fecha))
    conn.commit()
    conn.close()
    # Volver a la agenda sin pedir login de nuevo
    conn = get_db()
    turnos = conn.execute("SELECT * FROM turnos").fetchall()
    return render_template("index.html", turnos=turnos)
