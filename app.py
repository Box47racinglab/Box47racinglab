from flask import Flask, render_template, request, redirect, url_for, send_file
import qrcode
import io
from datetime import datetime

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    return render_template("formulario.html")

# Crear licencia
@app.route("/crear_licencia", methods=["POST"])
def crear_licencia():
    # Recibir datos
    nombre = request.form.get("nombre")
    segundo_nombre = request.form.get("segundo_nombre")
    primer_apellido = request.form.get("apellido")
    segundo_apellido = request.form.get("segundo_apellido")
    apodo = request.form.get("apodo")
    correo = request.form.get("correo")
    nacimiento = request.form.get("nacimiento")
    nivel = request.form.get("nivel")

    # Validación simple
    if not all([nombre, primer_apellido, apodo, correo, nacimiento, nivel]):
        return "Faltan datos requeridos", 400

    # Crear datos de QR
    datos_qr = (
        f"Nombre: {nombre} {segundo_nombre or ''} {primer_apellido} {segundo_apellido or ''}\n"
        f"Apodo: {apodo}\nCorreo: {correo}\nNacimiento: {nacimiento}\nNivel: {nivel}"
    )

    # Generar QR
    qr = qrcode.make(datos_qr)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Renderizar licencia con QR como imagen base64
    import base64
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template(
        "licencia.html",
        nombre=nombre,
        segundo_nombre=segundo_nombre,
        primer_apellido=primer_apellido,
        segundo_apellido=segundo_apellido,
        apodo=apodo,
        correo=correo,
        nacimiento=nacimiento,
        nivel=nivel,
        qr_data=qr_base64
    )

if __name__ == "__main__":
    app.run(debug=True)
           
