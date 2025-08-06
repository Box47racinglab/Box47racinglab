from flask import Flask, render_template, request, redirect
import qrcode
import io
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("registro.html")

@app.route("/crear_licencia", methods=["POST"])
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

        # Crear texto para el QR
        datos_qr = f"{nombre} {apellido_paterno} {apellido_materno} | {apodo} | {correo} | Nivel: {nivel}"
        
        # Generar QR y convertir a base64
        qr = qrcode.make(datos_qr)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

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

if __name__ == "__main__":
    app.run(debug=True)
