import os
import io
import base64
from datetime import date

from flask import Flask, render_template, request
from flask_mail import Mail, Message
import qrcode

app = Flask(__name__)

# -------------------------------
# Configuración de correo
# (pon tus credenciales o usa variables de entorno en Render)
# -------------------------------
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "tucorreo@gmail.com")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "tu_app_password")
app.config["MAIL_DEFAULT_SENDER"] = (
    os.getenv("MAIL_DEFAULT_NAME", "Box 47 Racing Lab"),
    os.getenv("MAIL_DEFAULT_EMAIL", os.getenv("MAIL_USERNAME", "tucorreo@gmail.com")),
)

mail = Mail(app)

# -------------------------------
# Rutas
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    # Muestra tu registro.html (el que pegaste)
    return render_template("registro.html")

@app.route("/crear_licencia", methods=["POST"])
def crear_licencia():
    try:
        # 1) Recibir datos del formulario (coinciden con tus name=)
        nombre = request.form.get("nombre", "").strip()
        apellido_paterno = request.form.get("apellido_paterno", "").strip()
        apellido_materno = request.form.get("apellido_materno", "").strip()
        apodo = request.form.get("apodo", "").strip()
        correo = request.form.get("correo", "").strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento", "").strip()
        nivel = request.form.get("nivel", "").strip()

        # Validación mínima
        if not all([nombre, apellido_paterno, apellido_materno, correo, fecha_nacimiento, nivel]):
            return "<h2>Faltan campos obligatorios.</h2>", 400

        apellidos = f"{apellido_paterno} {apellido_materno}"
        fecha_emision = date.today().strftime("%Y-%m-%d")

        # 2) Generar QR (base64) con datos clave
        datos_qr = f"{nombre} {apellidos} | {apodo} | {correo} | Nivel: {nivel}"
        qr_img = qrcode.make(datos_qr)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # 3) Render de la licencia (HTML que también verás en el navegador)
        html_licencia = render_template(
            "licencia.html",
            nombre=nombre,
            apellidos=apellidos,
            apodo=apodo,
            nivel=nivel,
            fecha_nacimiento=fecha_nacimiento,
            correo=correo,
            fecha_emision=fecha_emision,
            qr_base64=qr_base64,
            licencia_id=None, codigo=None, id_licencia=None,
        )

        # 4) Enviar correo con la licencia en HTML (si hay credenciales)
        try:
            if app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"]:
                msg = Message(
                    subject="Tu Licencia · Box 47 Racing Lab",
                    recipients=[correo],
                    html=html_licencia,
                )
                mail.send(msg)
        except Exception as e:
            # Si falla el correo, no rompemos la vista
            print(f"[WARN] Falló envío de correo: {e}")

        # 5) Mostrar la licencia en el navegador
        return html_licencia

    except Exception as e:
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>", 400


if __name__ == "__main__":
    # En local: python app.py
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
