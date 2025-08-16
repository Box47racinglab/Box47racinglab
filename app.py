from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configura tu correo (ejemplo Gmail, pero puedes usar otro SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tucorreo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña_o_app_password'  # usa app password de Gmail
app.config['MAIL_DEFAULT_SENDER'] = ('Box 47 Racing Lab', 'tucorreo@gmail.com')

mail = Mail(app)

@app.route('/crear_licencia', methods=['POST'])
def crear_licencia():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    apodo = request.form['apodo']
    nivel = request.form['nivel']
    fecha_nacimiento = request.form['fecha_nacimiento']

    # Generar la licencia en HTML (puedes incluir QR aquí)
    html = render_template(
        "licencia.html",
        nombre=nombre,
        apellidos=apellidos,
        apodo=apodo,
        nivel=nivel,
        fecha_nacimiento=fecha_nacimiento,
        correo=correo,
        qr_base64=None,   # si ya generas QR, pásalo aquí
    )

    # Enviar email
    msg = Message(
        subject="Tu Licencia Box 47 Racing Lab",
        recipients=[correo],
        html=html
    )
    mail.send(msg)

    return html  # también se muestra en el navegador
