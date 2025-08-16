from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect
import qrcode
import io
import base64
from io import BytesIO

app = Flask(__name__)

# Ruta GET: muestra el formulario
@app.route('/')
def mostrar_formulario():
    return render_template('registro.html')
@app.route("/")
def home():
    return render_template("registro.html")

# Ruta POST: procesa el formulario y genera la licencia
@app.route('/crear_licencia', methods=['POST'])
@app.route("/crear_licencia", methods=["POST"])
def crear_licencia():
    try:
        nombre = request.form['nombre']
        segundo_nombre = request.form['segundo_nombre']
        primer_apellido = request.form['primer_apellido']
        segundo_apellido = request.form['segundo_apellido']
        apodo = request.form['apodo']
        correo = request.form['correo']
        nacimiento = request.form['nacimiento']
        nivel = request.form['nivel']
        # Obtener datos del formulario
        nombre = request.form["nombre"]
        apellido_paterno = request.form["apellido_paterno"]
        apellido_materno = request.form["apellido_materno"]
        apodo = request.form["apodo"]
        correo = request.form["correo"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        nivel = request.form["nivel"]

        # Generar código QR con el correo (puedes cambiar por otra info si prefieres)
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(correo)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        # Crear texto para el QR
        datos_qr = f"{nombre} {apellido_paterno} {apellido_materno} | {apodo} | {correo} | Nivel: {nivel}"
        
        # Generar QR y convertir a base64
        qr = qrcode.make(datos_qr)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Convertir la imagen a base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_data = base64.b64encode(buffer.getvalue()).decode()

        return render_template('licencia.html',
                               nombre=nombre,
                               segundo_nombre=segundo_nombre,
                               primer_apellido=primer_apellido,
                               segundo_apellido=segundo_apellido,
                               apodo=apodo,
                               correo=correo,
                               nacimiento=nacimiento,
                               nivel=nivel,
                               qr_data=qr_data)
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
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>"
        return f"<h1>Error al procesar el formulario:</h1><pre>{str(e)}</pre>", 400

if __name__ == '__main__':
if __name__ == "__main__":
    app.run(debug=True)
