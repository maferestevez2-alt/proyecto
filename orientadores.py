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
def orientadores():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)

    if query:
        sql = """
        SELECT * FROM orientadores
        WHERE no_empleado LIKE %s OR nombre LIKE %s OR apellido_paterno LIKE %s
        OR apellido_materno LIKE %s OR grupos_encargado LIKE %s
        """
        params = tuple(['%' + query + '%']*5)
        cursor.execute(sql, params)
    else:
        cursor.execute("SELECT * FROM orientadores")

    orientadores = cursor.fetchall()
    cursor.close()
    return render_template("orientadores.html", orientadores=orientadores, query=query)


# =========================
# AGREGAR ORIENTADOR
# =========================
@app.route("/agregar", methods=["POST"])
def agregar():
    no_empleado = request.form["no_empleado"]
    nombre = request.form["nombre"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    grupos_encargado = request.form["grupos_encargado"]

    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO orientadores (no_empleado, nombre, apellido_paterno, apellido_materno, grupos_encargado)
        VALUES (%s, %s, %s, %s, %s)
    """, (no_empleado, nombre, apellido_paterno, apellido_materno, grupos_encargado))
    conexion.commit()
    cursor.close()

    flash("Orientador agregado correctamente")
    return redirect(url_for("orientadores"))


# =========================
# EDITAR ORIENTADOR
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        no_empleado = request.form["no_empleado"]
        nombre = request.form["nombre"]
        apellido_paterno = request.form["apellido_paterno"]
        apellido_materno = request.form["apellido_materno"]
        grupos_encargado = request.form["grupos_encargado"]

        cursor.execute("""
            UPDATE orientadores
            SET no_empleado=%s, nombre=%s, apellido_paterno=%s, apellido_materno=%s, grupos_encargado=%s
            WHERE id=%s
        """, (no_empleado, nombre, apellido_paterno, apellido_materno, grupos_encargado, id))
        conexion.commit()
        cursor.close()
        flash("Orientador actualizado correctamente")
        return redirect(url_for("orientadores"))

    cursor.execute("SELECT * FROM orientadores WHERE id=%s", (id,))
    orientador = cursor.fetchone()
    cursor.close()
    return render_template("editar_orientador.html", orientador=orientador)


# =========================
# ELIMINAR ORIENTADOR
# =========================
@app.route("/eliminar/<int:id>")
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM orientadores WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    flash("Orientador eliminado correctamente")
    return redirect(url_for("orientadores"))


if __name__ == "__main__":
    app.run(debug=True)
