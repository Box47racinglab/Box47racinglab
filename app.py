from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# -----------------------------
# CONFIGURACIÓN DEL CORREO
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # tu correo
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # tu app password
app.config['MAIL_DEFAULT_SENDER'] = ('Box 47 Racing Lab', os.getenv('MAIL_USERNAME'))

mail = Mail(app)

# -----------------------------
# RUTA DE REGISTRO / CREACIÓN DE LICENCIA
# -----------------------------
@app.route('/crear_licencia', methods=['POST'])
def crear_licencia():
    try:
        # Datos del formulario
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        apodo = request.form['apodo']
        nivel = request.form['nivel']
        fecha_nacimiento = request.form['fecha_nacimiento']
        correo = request.form['correo']

        # Renderizamos la licencia en HTML
        html_licencia = render_template(
            "licencia.html",
            nombre=nombre,
            apellidos=apellidos,
            apodo=apodo,
            nivel=nivel,
            fecha_nacimiento=fecha_nacimiento,
            correo=correo,
            qr_base64=None  # si ya generas el QR, pásalo aquí
        )

        # Creamos el correo
        msg = Message(
            subject="Tu Licencia · Box 47 Racing Lab",
            recipients=[correo],
            html=html_licencia
        )

        # Enviar correo
        mail.send(msg)

        # También mostramos la licencia en la web
        return html_licencia

    except Exception as e:
        return f"❌ Error al procesar: {e}"

# -----------------------------
# RUTA PRINCIPAL (FORMULARIO)
# -----------------------------
@app.route('/')
def index():
    return render_template("registro.html")  # tu formulario de registro

# -----------------------------
# MAIN
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
