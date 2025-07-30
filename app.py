from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("formulario.html")  # tu formulario de registro

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

if __name__ == "__main__":
    app.run(debug=True)
