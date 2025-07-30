from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def registro():
    return render_template('registro.html')

@app.route('/crear_licencia', methods=['POST'])
def crear_licencia():
    datos = {
        'nombre': request.form['nombre'],
        'segundo nombre': request.form['segundo nombre'],
        'apellido': request.form['apellido'],
        'segundo apellido': request.form['segundo apellido'],
        'apodo': request.form['apodo'],
        'correo': request.form['correo'],
        'nacimiento': request.form['nacimiento'],
        'nivel': request.form['nivel']
    }
    return render_template('licencia_virtual.html', licencia=datos)

if __name__ == '__main__':
    app.run(debug=True)
