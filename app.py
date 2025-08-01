from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')  # Tu formulario de registro

@app.route('/crear_licencia', methods=['POST'])
def crear_licencia():
    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    segundo_nombre = request.form.get('segundo_nombre')
    apellido = request.form.get('apellido')
    segundo_apellido = request.form.get('segundo_apellido')
    apodo = request.form.get('apodo')
    correo = request.form.get('correo')
    nacimiento = request.form.get('nacimiento')
    nivel = request.form.get('nivel')

    # Validar que no falte nada importante
    if not all([nombre, apellido, correo, nacimiento, nivel]):
        return "Faltan datos requeridos", 400

    # Datos que irán en el QR
    datos_qr = f'''
Nombre: {nombre} {segundo_nombre or ""}
Apellido: {apellido} {segundo_apellido or ""}
Apodo: {apodo or ""}
Correo: {correo}
Nacimiento: {nacimiento}
Nivel: {nivel}
'''.strip()

    # Generar QR
    qr_img = qrcode.make(datos_qr)
    buffered = io.BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Mostrar la licencia
    return render_template("licencia.html",
                           nombre=nombre,
                           segundo_nombre=segundo_nombre,
                           apellido=apellido,
                           segundo_apellido=segundo_apellido,
                           apodo=apodo,
                           correo=correo,
                           nacimiento=nacimiento,
                           nivel=nivel,
                           qr_base64=qr_base64)

if __name__ == '__main__':
    app.run(debug=True)
