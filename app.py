from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

# Ruta GET: muestra el formulario
@app.route('/')
def mostrar_formulario():
    return render_template('registro.html')

# Ruta POST: procesa el formulario y genera la licencia
@app.route('/crear_licencia', methods=['POST'])
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

        # Generar código QR con el correo (puedes cambiar por otra info si prefieres)
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(correo)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

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
    except Exception as e:
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
