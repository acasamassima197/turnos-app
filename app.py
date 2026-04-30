import sqlite3

def init_db():
    conn = sqlite3.connect("turnos.db")
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()

# Llamar a init_db() al inicio
init_db()
