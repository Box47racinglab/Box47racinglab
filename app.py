from flask import Flask, render_template, request
import qrcode
import io
import base64
from flask_mail import Mail, Message

app = Flask(__name__)

# -----------------------------
# CONFIGURACIÓN DEL CORREO
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tucorreo@gmail.com'  # 👈 cámbialo
app.config['MAIL_PASSWORD'] = 'tu_app_password'     # 👈 cámbialo
app.config['MAIL_DEFAULT_SENDER'] = ('Box 47 Racing Lab', 'tucorreo@gmail.com')

mail = Mail(app)


# -----------------------------
# RUTA PRINCIPAL (FORMULARIO)
# -----------------------------
@app.route("/")
def home():
    return render_template("registro.html")


# -----------------------------
# RUTA CREAR LICENCIA
# -----------------------------
@app.route("/crear_licencia", methods=["POST"])
def crear_licencia():
    try:
        # 1. Obtener datos del formulario
        nombre = request.form["nombre"]
        apellido_paterno = request.form["apellido_paterno"]
        apellido_materno = request.form["apellido_materno"]
        apodo = request.form["apodo"]
        correo = request.form["correo"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        nivel = request.form["nivel"]

        apellidos = f"{apellido_paterno} {apellido_materno}"

        # 2. Generar QR
        datos_qr = f"{nombre} {apellidos} | {apodo} | {correo} | Nivel: {nivel}"
        qr = qrcode.make(datos_qr)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # 3. Renderizar HTML de licencia
        html = render_template(
            "licencia.html",
            nombre=nombre,
            apellidos=apellidos,
            apodo=apodo,
            nivel=nivel,
            fecha_nacimiento=fecha_nacimiento,
            correo=correo,
            qr_base64=qr_base64
        )

        # 4. Enviar correo con la licencia en HTML
        msg = Message(
            subject="Tu Licencia Box 47 Racing Lab",
            recipients=[correo],
            html=html
        )
        mail.send(msg)

        # 5. También mostrar la licencia en navegador
        return html

    except Exception as e:
        return f"<h1>Error al procesar el formulario:</h1><pre>{str(e)}</pre>", 400


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
