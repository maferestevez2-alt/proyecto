from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_por_otra_muy_secreta"  # cámbiala en producción

# Usuario "en base de datos" (hardcoded para el ejemplo).
# Guardamos el hash de la contraseña "12345"
USUARIOS = {
    "mafer_13": generate_password_hash("12345")
}

@app.route('/')
def index():
    if session.get("user"):
        return redirect(url_for("Menu"))
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if usuario in USUARIOS and check_password_hash(USUARIOS[usuario], password):
            session['user'] = usuario
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return render_template('login.html', username=usuario)
    # GET
    return render_template('login.html')

@app.route('/menu')
def menu():
    usuario = session.get('user')
    if not usuario:
        flash("Por favor inicia sesión primero.", "warning")
        return redirect(url_for('login'))
    return render_template('Menu.html', usuario=usuario)



@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Cerraste sesión.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
