import os, io, base64
from datetime import date
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import qrcode

app = Flask(__name__)

# ---------- Config correo (opcionales) ----------
# Si no defines MAIL_USERNAME/MAIL_PASSWORD en Render, NO intentará enviar (evita caídas).
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "")  # vacío por default
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "")  # vacío por default
app.config["MAIL_DEFAULT_SENDER"] = (
    os.getenv("MAIL_DEFAULT_NAME", "Box 47 Racing Lab"),
    os.getenv("MAIL_DEFAULT_EMAIL", os.getenv("MAIL_USERNAME", "")),
)
mail = Mail(app)

# ---------- Rutas ----------
@app.route("/health")
def health():
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return render_template("registro.html")

@app.route("/crear_licencia", methods=["POST"])
def crear_licencia():
    try:
        # 1) Datos
        nombre = request.form.get("nombre", "").strip()
        ap_pat = request.form.get("apellido_paterno", "").strip()
        ap_mat = request.form.get("apellido_materno", "").strip()
        apodo = request.form.get("apodo", "").strip()
        correo = request.form.get("correo", "").strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento", "").strip()
        nivel = request.form.get("nivel", "").strip()

        if not all([nombre, ap_pat, ap_mat, correo, fecha_nacimiento, nivel]):
            return "<h2>Faltan campos obligatorios.</h2>", 400

        apellidos = f"{ap_pat} {ap_mat}"
        fecha_emision = date.today().strftime("%Y-%m-%d")

        # 2) QR base64
        datos_qr = f"{nombre} {apellidos} | {apodo} | {correo} | Nivel: {nivel}"
        buf = io.BytesIO()
        qrcode.make(datos_qr).save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # 3) Render licencia
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

        # 4) Enviar correo SOLO si hay credenciales reales
        try:
            if app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"]:
                msg = Message(
                    subject="Tu Licencia · Box 47 Racing Lab",
                    recipients=[correo],
                    html=html_licencia,
                )
                mail.send(msg)
        except Exception as mail_err:
            # No tiramos el servicio por fallo de SMTP
            print(f"[WARN] Falló envío de correo: {mail_err}")

        # 5) Mostrar licencia
        return html_licencia

    except Exception as e:
        # Muestra el error en pantalla y en logs
        print(f"[ERROR] crear_licencia: {e}")
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>", 400

# Solo se usa en local. En Render arrancamos con gunicorn.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
