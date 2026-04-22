from flask import Flask,request,url_for,render_template, redirect
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

@app.route('/agendar')
def agendar():
    return render_template("agendar.html")

@app.route('/agendar/agregar',methods = ['POST'])
def agregar():
    conn = sqlite3.connect("citas.db")
    conn.row_factory=sqlite3.Row

    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']

    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO pacientes(mascota,propietario,especie)
    VALUES(?,?,?)
""",(mascota,propietario,especie))
    
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = sqlite3.connect("citas.db")
    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()

    cursor.execute("""
        SELECT * FROM pacientes
        WHERE id = ?
""",(id,))
    
    paciente = cursor.fetchone()

    conn.commit()
    conn.close()
    return render_template("editar.html",paciente=paciente)

@app.route('/guardar_editar', methods = ['POST'])
def guardar_editar():

    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    id_m = request.form['id']

    conn = sqlite3.connect("citas.db")
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE pacientes SET 
            mascota = ?,
            propietario = ?,
            especie = ?
        WHERE id = ?
""",(mascota,propietario,especie,id_m))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ =="__main__":
    app.run(debug=True)