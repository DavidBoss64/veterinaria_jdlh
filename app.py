from flask import Flask,request,url_for,render_template
import sqlite3


app = Flask(__name__)

def init_database():

    conn = sqlite3.connect("citas.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS pacientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
""")

    conn.commit()
    conn.close()
init_database()

@app.route('/')
def index():
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row

    cursor.execute("""
    SELECT * FROM pacientes
""")
    pacientes=cursor.fetchall()
    conn.commit()
    conn.close()

    return render_template("index.html",pacientes=pacientes)


if __name__ =="__main__":
    app.run(debug=True)