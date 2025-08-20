import os, io, base64, re
from datetime import date
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import qrcode

app = Flask(__name__)

# ---------- Config correo ----------
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")  # vacío por default
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")  # vacío por default
MAIL_DEFAULT_NAME = os.getenv("MAIL_DEFAULT_NAME", "Box 47 Racing Lab")
MAIL_DEFAULT_EMAIL = os.getenv("MAIL_DEFAULT_EMAIL", MAIL_USERNAME)

app.config.update(
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_USE_TLS=MAIL_USE_TLS,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
)

# Solo define DEFAULT_SENDER si hay email válido
if MAIL_DEFAULT_EMAIL:
    app.config["MAIL_DEFAULT_SENDER"] = (MAIL_DEFAULT_NAME, MAIL_DEFAULT_EMAIL)

mail = Mail(app)

# ---------- Utilidades ----------
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(addr: str) -> bool:
    return bool(addr) and EMAIL_RE.match(addr) is not None

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
        nombre = (request.form.get("nombre") or "").strip()
        ap_pat = (request.form.get("apellido_paterno") or "").strip()
        ap_mat = (request.form.get("apellido_materno") or "").strip()
        apodo = (request.form.get("apodo") or "").strip()
        correo = (request.form.get("correo") or "").strip()
        fecha_nacimiento = (request.form.get("fecha_nacimiento") or "").strip()
        nivel = (request.form.get("nivel") or "").strip()

        if not all([nombre, ap_pat, ap_mat, correo, fecha_nacimiento, nivel]):
            return "<h2>Faltan campos obligatorios.</h2>", 400

        apellidos = f"{ap_pat} {ap_mat}"
        fecha_emision = date.today().strftime("%Y-%m-%d")

        # 2) QR base64
        datos_qr = f"{nombre} {apellidos} | {apodo} | {correo} | Nivel: {nivel}"
        with io.BytesIO() as buf:
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

        # 4) Enviar correo SOLO si hay credenciales y correo válido
        if MAIL_USERNAME and MAIL_PASSWORD and is_valid_email(correo):
            try:
                msg = Message(
                    subject="Tu Licencia · Box 47 Racing Lab",
                    recipients=[correo],
                    html=html_licencia,
                )
                # From explícito si configuraste nombre/email
                if MAIL_DEFAULT_EMAIL:
                    msg.sender = (MAIL_DEFAULT_NAME, MAIL_DEFAULT_EMAIL)
                mail.send(msg)
            except Exception as mail_err:
                print(f"[WARN] Falló envío de correo: {mail_err}")
        else:
            print("[INFO] Correo NO enviado (sin credenciales o email inválido).")

        # 5) Mostrar licencia
        return html_licencia

    except Exception as e:
        print(f"[ERROR] crear_licencia: {e}")
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>", 400

# Solo en local; en Render usa gunicorn: `gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app`
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
