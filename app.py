from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/crear_licencia', methods=['POST'])
def crear_licencia():
    try:
        # Recoger datos del formulario
        nombre = request.form.get('nombre')
        segundo_nombre = request.form.get('segundo nombre')  # opcional
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        apodo = request.form.get('apodo')
        correo = request.form.get('correo')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        nivel = request.form.get('nivel')

        # Renderizar plantilla de licencia con los datos
        return render_template(
            'licencia.html',
            nombre=nombre,
            segundo_nombre=segundo_nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            apodo=apodo,
            correo=correo,
            fecha_nacimiento=fecha_nacimiento,
            nivel=nivel
        )
    
    except Exception as e:
        # Mostrar el error en pantalla si algo falla
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>"

# Ejecutar localmente
if __name__ == '__main__':
    app.run(debug=True)
