from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "super_clave_segura"

# ------------------- CONEXIÓN BASE DE DATOS -------------------
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

# ==============================================================
#                      LOGIN / CUENTAS
# ==============================================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        rol = request.form["rol"]

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND rol=%s", (usuario, rol))
        user = cursor.fetchone()
        cursor.close()

        if user and user["password"] == password:
            session["usuario"] = usuario
            session["rol"] = rol
            return redirect(url_for("menu"))
        else:
            flash("Usuario, contraseña o rol incorrectos", "error")

    return render_template("login.html")


@app.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        rol = request.form["rol"]

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        if cursor.fetchone():
            flash("El usuario ya existe", "error")
        else:
            cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (%s, %s, %s)",
                           (usuario, password, rol))
            conexion.commit()
            flash("Cuenta creada correctamente", "info")
            return redirect(url_for("login"))
        cursor.close()

    return render_template("crear_cuenta.html")


@app.route("/recuperar_contrasena", methods=["GET", "POST"])
def recuperar_contrasena():
    if request.method == "POST":
        usuario = request.form["usuario"]
        new_password = request.form["new_password"]

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        if cursor.fetchone():
            cursor.execute("UPDATE usuarios SET password=%s WHERE usuario=%s", (new_password, usuario))
            conexion.commit()
            flash("Contraseña actualizada correctamente", "info")
            cursor.close()
            return redirect(url_for("login"))
        else:
            flash("El usuario no existe", "error")
            cursor.close()

    return render_template("recuperar_contrasena.html")


@app.route("/menu")
def menu():
    if "usuario" in session:
        return render_template("menu.html", usuario=session["usuario"], rol=session["rol"])
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==============================================================
#                      CRUD: ALUMNOS
# ==============================================================
@app.route("/alumnos", methods=["GET"])
def alumnos():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)

    if query:
        sql = """
            SELECT * FROM alumnos
            WHERE nombre LIKE %s OR apellido_paterno LIKE %s OR apellido_materno LIKE %s
            OR no_control LIKE %s OR curp LIKE %s OR grupo LIKE %s OR turno LIKE %s OR semestre LIKE %s
        """
        params = tuple(['%' + query + '%'] * 8)
        cursor.execute(sql, params)
    else:
        cursor.execute("SELECT * FROM alumnos")

    alumnos = cursor.fetchall()
    cursor.close()
    return render_template("alumnos.html", alumnos=alumnos, query=query)


@app.route("/alumnos/agregar", methods=["POST"])
def agregar_alumno():
    data = (
        request.form['no_control'],
        request.form['curp'],
        request.form['nombre'],
        request.form['apellido_paterno'],
        request.form['apellido_materno'],
        request.form['grupo'],
        request.form['turno'],
        request.form['semestre']
    )
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO alumnos (no_control, curp, nombre, apellido_paterno, apellido_materno, grupo, turno, semestre)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)
    conexion.commit()
    cursor.close()
    return redirect(url_for("alumnos"))


@app.route("/alumnos/editar/<int:id>", methods=["GET", "POST"])
def editar_alumno(id):
    cursor = conexion.cursor(dictionary=True)
    if request.method == "POST":
        data = (
            request.form['no_control'],
            request.form['curp'],
            request.form['nombre'],
            request.form['apellido_paterno'],
            request.form['apellido_materno'],
            request.form['grupo'],
            request.form['turno'],
            request.form['semestre'],
            id
        )
        cursor.execute("""
            UPDATE alumnos SET no_control=%s, curp=%s, nombre=%s, apellido_paterno=%s,
            apellido_materno=%s, grupo=%s, turno=%s, semestre=%s WHERE id=%s
        """, data)
        conexion.commit()
        cursor.close()
        return redirect(url_for("alumnos"))

    cursor.execute("SELECT * FROM alumnos WHERE id=%s", (id,))
    alumno = cursor.fetchone()
    cursor.close()
    return render_template("editar_alumno.html", alumno=alumno)


@app.route("/alumnos/eliminar/<int:id>")
def eliminar_alumno(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    return redirect(url_for("alumnos"))

# ==============================================================
#                      CRUD: DOCENTES
# ==============================================================
@app.route("/docentes", methods=["GET"])
def docentes():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)

    if query:
        cursor.execute("""
            SELECT * FROM docentes
            WHERE no_empleado LIKE %s OR nombre LIKE %s OR apellido_paterno LIKE %s
            OR apellido_materno LIKE %s OR materia LIKE %s
        """, tuple(['%' + query + '%'] * 5))
    else:
        cursor.execute("SELECT * FROM docentes")

    docentes = cursor.fetchall()
    cursor.close()
    return render_template("docentes.html", docentes=docentes, query=query)


@app.route("/docentes/agregar", methods=["POST"])
def agregar_docente():
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO docentes (no_empleado, nombre, apellido_paterno, apellido_materno, materia)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form["no_empleado"],
        request.form["nombre"],
        request.form["apellido_paterno"],
        request.form["apellido_materno"],
        request.form["materia"]
    ))
    conexion.commit()
    cursor.close()
    flash("Docente agregado correctamente")
    return redirect(url_for("docentes"))


@app.route("/docentes/editar/<int:id>", methods=["GET", "POST"])
def editar_docente(id):
    cursor = conexion.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            UPDATE docentes SET no_empleado=%s, nombre=%s, apellido_paterno=%s,
            apellido_materno=%s, materia=%s WHERE id=%s
        """, (
            request.form["no_empleado"],
            request.form["nombre"],
            request.form["apellido_paterno"],
            request.form["apellido_materno"],
            request.form["materia"],
            id
        ))
        conexion.commit()
        cursor.close()
        flash("Docente actualizado correctamente")
        return redirect(url_for("docentes"))

    cursor.execute("SELECT * FROM docentes WHERE id=%s", (id,))
    docente = cursor.fetchone()
    cursor.close()
    return render_template("editar_docente.html", docente=docente)


@app.route("/docentes/eliminar/<int:id>")
def eliminar_docente(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM docentes WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    flash("Docente eliminado correctamente")
    return redirect(url_for("docentes"))

# ==============================================================
#                      CRUD: ORIENTADORES
# ==============================================================

@app.route("/orientadores", methods=["GET"])
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
    return render_template("editarorientadores.html", orientador=orientador)


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

# ==============================================================
#                      CRUD: DIRECTIVOS
# ==============================================================
@app.route("/directivos", methods=["GET"])
def directivos():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)

    if query:
        cursor.execute("""
            SELECT * FROM directivos
            WHERE nombre LIKE %s OR apellido_paterno LIKE %s OR apellido_materno LIKE %s OR cargo LIKE %s
        """, tuple(['%' + query + '%'] * 4))
    else:
        cursor.execute("SELECT * FROM directivos")

    directivos = cursor.fetchall()
    cursor.close()
    return render_template("directivos.html", directivos=directivos, query=query)


@app.route("/directivos/agregar", methods=["POST"])
def agregar_directivo():
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO directivos (nombre, apellido_paterno, apellido_materno, cargo, correo)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form["nombre"],
        request.form["apellido_paterno"],
        request.form["apellido_materno"],
        request.form["cargo"],
        request.form["correo"]
    ))
    conexion.commit()
    cursor.close()
    flash("Directivo agregado correctamente")
    return redirect(url_for("directivos"))


@app.route("/directivos/editar/<int:id>", methods=["GET", "POST"])
def editar_directivo(id):
    cursor = conexion.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            UPDATE directivos SET nombre=%s, apellido_paterno=%s, apellido_materno=%s,
            cargo=%s, correo=%s WHERE id=%s
        """, (
            request.form["nombre"],
            request.form["apellido_paterno"],
            request.form["apellido_materno"],
            request.form["cargo"],
            request.form["correo"],
            id
        ))
        conexion.commit()
        cursor.close()
        flash("Directivo actualizado correctamente")
        return redirect(url_for("directivos"))

    cursor.execute("SELECT * FROM directivos WHERE id=%s", (id,))
    directivo = cursor.fetchone()
    cursor.close()
    return render_template("editardirectivo.html", directivo=directivo)


@app.route("/directivos/eliminar/<int:id>")
def eliminar_directivo(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM directivos WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    flash("Directivo eliminado correctamente")
    return redirect(url_for("directivos"))


# ==============================================================
#                      CRUD: MATERIA
# ==============================================================
@app.route("materias", methods=['GET', 'POST'])
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
@app.route('/agregar/materias', methods=['POST'])
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
    
    return redirect(url_for('materias'))


# ✅ EDITAR
@app.route('/editar/materias/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('materias'))

    cursor.execute("SELECT * FROM materias WHERE id=%s", (id,))
    materia = cursor.fetchone()
    cursor.close()

    return render_template('editar_materia.html', materia=materia)


# ✅ ELIMINAR
@app.route('/eliminar/materias/<int:id>')
def eliminar(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM materias WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()

    return redirect(url_for('materias'))


# ==============================================================
#                      CRUD: RECURSOS
# ==============================================================
@app.route("/recursos", methods=["GET"])
def recursos():
    query = request.args.get('q', '').strip()
    cursor = conexion.cursor(dictionary=True)

    if query:
        cursor.execute("""
            SELECT * FROM recursos
            WHERE nombre LIKE %s OR tipo LIKE %s OR descripcion LIKE %s
        """, tuple(['%' + query + '%'] * 3))
    else:
        cursor.execute("SELECT * FROM recursos")

    recursos = cursor.fetchall()
    cursor.close()
    return render_template("recursos.html", recursos=recursos, query=query)


@app.route("/recursos/agregar", methods=["POST"])
def agregar_recurso():
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO recursos (nombre, tipo, descripcion, cantidad)
        VALUES (%s, %s, %s, %s)
    """, (
        request.form["nombre"],
        request.form["tipo"],
        request.form["descripcion"],
        request.form["cantidad"]
    ))
    conexion.commit()
    cursor.close()
    flash("Recurso agregado correctamente")
    return redirect(url_for("recursos"))


@app.route("/recursos/editar/<int:id>", methods=["GET", "POST"])
def editar_recurso(id):
    cursor = conexion.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("""
            UPDATE recursos SET nombre=%s, tipo=%s, descripcion=%s, cantidad=%s WHERE id=%s
        """, (
            request.form["nombre"],
            request.form["tipo"],
            request.form["descripcion"],
            request.form["cantidad"],
            id
        ))
        conexion.commit()
        cursor.close()
        flash("Recurso actualizado correctamente")
        return redirect(url_for("recursos"))

    cursor.execute("SELECT * FROM recursos WHERE id=%s", (id,))
    recurso = cursor.fetchone()
    cursor.close()
    return render_template("editarrecurso.html", recurso=recurso)


@app.route("/recursos/eliminar/<int:id>")
def eliminar_recurso(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM recursos WHERE id=%s", (id,))
    conexion.commit()
    cursor.close()
    flash("Recurso eliminado correctamente")
    return redirect(url_for("recursos"))


if __name__ == "__main__":
    app.run(debug=True)