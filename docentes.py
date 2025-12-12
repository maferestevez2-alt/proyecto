from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

@app.route("/", methods=["GET"])
def docentes():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)

    if query:
        sql = """
        SELECT * FROM docentes
        WHERE no_empleado LIKE %s OR nombre LIKE %s OR apellido_paterno LIKE %s
        OR apellido_materno LIKE %s OR materia LIKE %s
        """
        params = tuple(['%' + query + '%']*5)
        cursor.execute(sql, params)
    else:
        cursor.execute("SELECT * FROM docentes")

    docentes = cursor.fetchall()
    cursor.close()
    return render_template("docentes.html", docentes=docentes, query=query)


@app.route("/agregar", methods=["POST"])
def agregar():
    no_empleado = request.form["no_empleado"]
    nombre = request.form["nombre"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    materia = request.form["materia"]

    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO docentes (no_empleado, nombre, apellido_paterno, apellido_materno, materia)
        VALUES (%s, %s, %s, %s, %s)
    """, (no_empleado, nombre, apellido_paterno, apellido_materno, materia))
    conexion.commit()
    cursor.close()

    flash("Docente agregado correctamente")
    return redirect(url_for("docentes"))


@app.route("/editar/<id>")
def editar(id):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM docentes WHERE id = %s", (id,))
    docente = cursor.fetchone()
    cursor.close()
    return render_template("editar_docente.html", docente=docente)

@app.route("/actualizar/<id>", methods=["POST"])
def actualizar(id):
    no_empleado = request.form["no_empleado"]
    nombre = request.form["nombre"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    materia = request.form["materia"]

    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE docentes
        SET no_empleado=%s, nombre=%s, apellido_paterno=%s,
        apellido_materno=%s, materia=%s
        WHERE id=%s
    """, (no_empleado, nombre, apellido_paterno, apellido_materno, materia, id))
    conexion.commit()
    cursor.close()

    flash("Docente actualizado correctamente")
    return redirect(url_for("docentes"))

@app.route("/eliminar/<id>")
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM docentes WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()

    flash("Docente eliminado correctamente")
    return redirect(url_for("docentes"))


if __name__ == "__main__":
    app.run(debug=True)
