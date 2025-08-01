from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, send_file
import qrcode
import io
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("formulario.html")  # tu formulario de registro
def registro():
    return render_template("registro.html")

@app.route("/crear_licencia", methods=["POST"])
def crear_licencia():
    # Recibir datos del formulario
    nombre = request.form["nombre"]
    segundo_nombre = request.form["segundo_nombre"]
    apellido = request.form["apellido"]
    segundo_apellido = request.form["segundo_apellido"]
    apodo = request.form["apodo"]
    correo = request.form["correo"]
    nacimiento = request.form["nacimiento"]
    nivel = request.form["nivel"]

    # Crear diccionario de licencia
    licencia = {
        "nombre": nombre,
        "segundo_nombre": segundo_nombre,
        "apellido": apellido,
        "segundo_apellido": segundo_apellido,
        "apodo": apodo,
        "correo": correo,
        "nacimiento": nacimiento,
        "nivel": nivel
    }

    # Renderizar plantilla de licencia
    return render_template("licencia.html", licencia=licencia)
    nombre = request.form.get("nombre")
    segundo_nombre = request.form.get("segundo nombre")
    primer_apellido = request.form.get("primer apellido")
    segundo_apellido = request.form.get("segundo apellido")
    apodo = request.form.get("apodo")
    correo = request.form.get("correo")
    nacimiento = request.form.get("nacimiento")
    nivel = request.form.get("nivel")

    # Validación rápida para evitar errores
    if not all([nombre, primer_apellido, apodo, correo, nacimiento, nivel]):
        return "Faltan datos requeridos", 400

    # Crear string del QR
    datos_qr = f"Nombre: {nombre} {segundo_nombre or ''} {primer_apellido} {segundo_apellido or ''}\nApodo: {apodo}\nCorreo: {correo}\nNacimiento: {nacimiento}\nNivel: {nivel}"

    qr = qrcode.make(datos_qr)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_data = buffer.getvalue()
    buffer.seek(0)

    # Pasar datos a plantilla
    return render_template("licencia.html", nombre=nombre, apodo=apodo, correo=correo,
                           nacimiento=nacimiento, nivel=nivel, qr=qr_data)

@app.route("/qr.png")
def mostrar_qr():
    return send_file(io.BytesIO(qr_data), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
            
