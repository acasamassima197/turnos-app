from flask import Flask, request, render_template
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
def index():
    conn = get_db()
    turnos = conn.execute("SELECT * FROM turnos").fetchall()
    return render_template("index.html", turnos=turnos)

@app.route("/agendar", methods=["POST"])
def agendar():
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    conn = get_db()
    conn.execute("INSERT INTO turnos (nombre, fecha) VALUES (?, ?)", (nombre, fecha))
    conn.commit()
    return "Turno agendado correctamente"
