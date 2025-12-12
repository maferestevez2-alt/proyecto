from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secreto_super_seguro"

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

# -------------------
# LOGIN
# -------------------
@app.route("/", methods=["GET","POST"])
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

# -------------------
# CREAR CUENTA
# -------------------
@app.route("/crear_cuenta", methods=["GET","POST"])
def crear_cuenta():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        rol = request.form["rol"]

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        if cursor.fetchone():
            flash("El usuario ya existe", "error")
            cursor.close()
        else:
            cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (%s, %s, %s)", 
                           (usuario, password, rol))
            conexion.commit()
            cursor.close()
            flash("Cuenta creada correctamente", "info")
            return redirect(url_for("login"))

    return render_template("crear_cuenta.html")

# -------------------
# RECUPERAR CONTRASEÑA
# -------------------
@app.route("/recuperar_contrasena", methods=["GET","POST"])
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

# -------------------
# MENU
# -------------------
@app.route("/menu")
def menu():
    if "usuario" in session:
        return render_template("menu.html", usuario=session["usuario"], rol=session["rol"])
    return redirect(url_for("login"))

# -------------------
# CERRAR SESIÓN
# -------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)