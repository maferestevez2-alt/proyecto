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

@app.route('/', methods=['GET'])
def directivos():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)
    
    if query:
        sql = """
        SELECT * FROM directivos
        WHERE no_empleado LIKE %s OR nombre LIKE %s OR apellido_paterno LIKE %s
        OR apellido_materno LIKE %s OR puesto LIKE %s
        """
        params = tuple(['%' + query + '%']*5)
        cursor.execute(sql, params)
    else:
        cursor.execute("SELECT * FROM directivos")
    
    directivos = cursor.fetchall()
    cursor.close()
    return render_template("directivos.html", directivos=directivos, query=query)


# ==========
# AGREGAR
# ==========
@app.route('/agregar', methods=['POST'])
def agregar():
    no_empleado = request.form['no_empleado']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    puesto = request.form['puesto']

    cursor = conexion.cursor()
    sql = """
    INSERT INTO directivos (no_empleado, nombre, apellido_paterno, apellido_materno, puesto)
    VALUES (%s,%s,%s,%s,%s)
    """
    values = (no_empleado, nombre, apellido_paterno, apellido_materno, puesto)
    cursor.execute(sql, values)
    conexion.commit()
    cursor.close()
    return redirect(url_for("directivos"))


# ==========
# EDITAR
# ==========
@app.route('/editar/<int:id>')
def editar(id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM directivos WHERE id=%s", (id,))
    directivo = cursor.fetchone()
    cursor.close()
    return render_template("editardirectivo.html", directivo=directivo)


# ==========
# ACTUALIZAR
# ==========
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    no_empleado = request.form['no_empleado']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    puesto = request.form['puesto']

    cursor = conexion.cursor()
    sql = """
    UPDATE directivos
    SET no_empleado=%s, nombre=%s, apellido_paterno=%s, apellido_materno=%s, puesto=%s
    WHERE id=%s
    """
    values = (no_empleado, nombre, apellido_paterno, apellido_materno, puesto, id)
    cursor.execute(sql, values)
    conexion.commit()
    cursor.close()
    return redirect(url_for("directivos"))


# ==========
# ELIMINAR
# ==========
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM directivos WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    return redirect(url_for("directivos"))


if __name__ == '__main__':
    app.run(debug=True)
