from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 📌 CONEXIÓN A LA BD
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)


# ✅ MOSTRAR Y BUSCAR
@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        busqueda = request.form['busqueda']
        cursor.execute("""
            SELECT * FROM materias
            WHERE no_empleado LIKE %s docente LIKE %s OR materia LIKE %s
        """),((f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"))
    else:
        cursor.execute("SELECT * FROM materias")

    materias = cursor.fetchall()
    cursor.close()
    return render_template('materias.html', materias=materias)


# ✅ AGREGAR
@app.route('/agregar', methods=['POST'])
def agregar():
    no_empleado= request.form['no_empleado']
    docente = request.form['docente']
    materia = request.form['materia']

    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO materias (no_empleado,docente, materia)
        VALUES (%s, %s)
    """, (no_empleado,docente, materia))
    conexion.commit()
    cursor.close()
    
    return redirect(url_for('index'))


# ✅ EDITAR
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        no_empleado= request.form['no_empleado']
        docente = request.form['docente']
        materia = request.form['materia']

        cursor.execute("""
            UPDATE materias
            SET no_empleado=%s,docente=%s, materia=%s
            WHERE id=%s
        """, (docente, materia, id))
        conexion.commit()
        cursor.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM materias WHERE id=%s", (id,))
    materia = cursor.fetchone()
    cursor.close()

    return render_template('editar_materia.html', materia=materia)


# ✅ ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM materias WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
