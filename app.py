\from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    try:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        email = request.form['email']

        return render_template('licencia_virtual.html',
                               nombre=nombre,
                               apellido=apellido,
                               edad=edad,
                               email=email)
    except Exception as e:
        return f"<h1>Error al procesar el formulario:</h1><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
