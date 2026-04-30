from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

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
    # Al entrar a la URL pública, primero login
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        if usuario == "admin" and password == "admin":
            conn = get_db()
            turnos = conn.execute("SELECT * FROM turnos").fetchall()
            return render_template("index.html", turnos=turnos)
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")
    
@app.route("/agendar", methods=["POST"])
def agendar():
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    conn = get_db()
    conn.execute("INSERT INTO turnos (nombre, fecha) VALUES (?, ?)", (nombre, fecha))
    conn.commit()
    conn.close()
    return redirect(url_for("login"))
