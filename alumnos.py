from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

# Listar alumnos + búsqueda
@app.route('/', methods=['GET'])
def alumnos():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)
    
    if query:
        sql = """
            SELECT * FROM alumnos
            WHERE nombre LIKE %s OR apellido_paterno LIKE %s OR apellido_materno LIKE %s
            OR no_control LIKE %s OR curp LIKE %s OR grupo LIKE %s OR turno LIKE %s OR semestre LIKE %s
        """
        params = tuple(['%' + query + '%']*8)
        cursor.execute(sql, params)
    else:
        cursor.execute("SELECT * FROM alumnos")
    
    alumnos = cursor.fetchall()
    cursor.close()
    return render_template("alumnos.html", alumnos=alumnos, query=query)

# Agregar alumno
@app.route('/agregar', methods=['POST'])
def agregar():
    no_control = request.form['no_control']
    curp = request.form['curp']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    grupo = request.form['grupo']
    turno = request.form['turno']
    semestre = request.form['semestre']

    cursor = conexion.cursor()
    sql = """
    INSERT INTO alumnos (no_control, curp, nombre, apellido_paterno, apellido_materno, grupo, turno, semestre)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    values = (no_control, curp, nombre, apellido_paterno, apellido_materno, grupo, turno, semestre)
    cursor.execute(sql, values)
    conexion.commit()
    cursor.close()
    return redirect(url_for("alumnos"))

# Editar alumno
@app.route('/editar/<int:id>')
def editar(id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos WHERE id=%s", (id,))
    alumno = cursor.fetchone()
    cursor.close()
    return render_template("editar_alumno.html", alumno=alumno)

# Actualizar alumno
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    no_control = request.form['no_control']
    curp = request.form['curp']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    grupo = request.form['grupo']
    turno = request.form['turno']
    semestre = request.form['semestre']

    cursor = conexion.cursor()
    sql = """
    UPDATE alumnos SET no_control=%s, curp=%s, nombre=%s, apellido_paterno=%s,
        apellido_materno=%s, grupo=%s, turno=%s, semestre=%s
    WHERE id=%s
    """
    values = (no_control, curp, nombre, apellido_paterno, apellido_materno, grupo, turno, semestre, id)
    cursor.execute(sql, values)
    conexion.commit()
    cursor.close()
    return redirect(url_for("alumnos"))

# Eliminar alumno
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    return redirect(url_for("alumnos"))

if __name__ == '__main__':
    app.run(debug=True)
