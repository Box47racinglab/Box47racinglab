from flask import Flask, render_template, request, redirect
import qrcode
import io
import base64
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("registro.html")
# Configura tu correo (ejemplo Gmail, pero puedes usar otro SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tucorreo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña_o_app_password'  # usa app password de Gmail
app.config['MAIL_DEFAULT_SENDER'] = ('Box 47 Racing Lab', 'tucorreo@gmail.com')

@app.route("/crear_licencia", methods=["POST"])
mail = Mail(app)

@app.route('/crear_licencia', methods=['POST'])
def crear_licencia():
    try:
        # Obtener datos del formulario
        nombre = request.form["nombre"]
        apellido_paterno = request.form["apellido_paterno"]
        apellido_materno = request.form["apellido_materno"]
        apodo = request.form["apodo"]
        correo = request.form["correo"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        nivel = request.form["nivel"]
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    apodo = request.form['apodo']
    nivel = request.form['nivel']
    fecha_nacimiento = request.form['fecha_nacimiento']

        # Crear texto para el QR
        datos_qr = f"{nombre} {apellido_paterno} {apellido_materno} | {apodo} | {correo} | Nivel: {nivel}"
        
        # Generar QR y convertir a base64
        qr = qrcode.make(datos_qr)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
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

        # Renderizar la licencia con datos y el QR
        return render_template(
            "licencia_virtual.html",
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            apodo=apodo,
            correo=correo,
            fecha_nacimiento=fecha_nacimiento,
            nivel=nivel,
            qr_code=qr_base64
        )
    
    except Exception as e:
        return f"<h1>Error al procesar el formulario:</h1><pre>{str(e)}</pre>", 400
    # Enviar email
    msg = Message(
        subject="Tu Licencia Box 47 Racing Lab",
        recipients=[correo],
        html=html
    )
    mail.send(msg)

if __name__ == "__main__":
    app.run(debug=True)
    return html  # también se muestra en el navegador
