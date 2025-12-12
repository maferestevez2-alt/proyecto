from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 📌 CONEXIÓN A LA BASE DE DATOS
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

# ✅ LISTAR Y BUSCAR
@app.route('/', methods=['GET', 'POST'])
def recursos():
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        busqueda = request.form['busqueda']
        cursor.execute("""
            SELECT * FROM recursos 
            WHERE no_control LIKE %s 
            OR nombre LIKE %s
            OR materia LIKE %s
            OR tipo LIKE %s
        """, (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"))
    else:
        cursor.execute("SELECT * FROM recursos")

    recursos = cursor.fetchall()
    cursor.close()
    return render_template('recursos.html', recursos=recursos)


# ✅ AGREGAR RECURSO
@app.route('/agregar', methods=['POST'])
def agregar():
    no_control = request.form['no_control']
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    estadisticas = request.form['estadisticas']
    materia = request.form['materia']
    tipo = request.form['tipo']

    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO recursos (no_control, fecha, nombre, estadisticas, materia, tipo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (no_control, fecha, nombre, estadisticas, materia, tipo))
    conexion.commit()
    cursor.close()
    return redirect(url_for('recursos'))


# ✅ EDITAR RECURSO
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        no_control = request.form['no_control']
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        estadisticas = request.form['estadisticas']
        materia = request.form['materia']
        tipo = request.form['tipo']

        cursor.execute("""
            UPDATE recursos
            SET no_control=%s, fecha=%s, nombre=%s, estadisticas=%s, materia=%s, tipo=%s
            WHERE id=%s
        """, (no_control, fecha, nombre, estadisticas, materia, tipo, id))
        conexion.commit()
        cursor.close()
        return redirect(url_for('recursos'))

    cursor.execute("SELECT * FROM recursos WHERE id=%s", (id,))
    recurso = cursor.fetchone()
    cursor.close()
    return render_template('editarrecursos.html', recurso=recurso)


# ✅ ELIMINAR RECURSO
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM recursos WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    return redirect(url_for('recursos'))


if __name__ == '__main__':
    app.run(debug=True)
