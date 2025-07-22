
from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os
import pandas as pd

app = Flask(__name__)
DATA_FILE = 'licencias.csv'

@app.route('/', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apodo = request.form['apodo']
        correo = request.form['correo']
        nacimiento = request.form['nacimiento']
        nivel = request.form['nivel']
        url_licencia = url_for('licencia_virtual', nombre=nombre, _external=True)

        # Guardar CSV
        df = pd.DataFrame([[nombre, correo, nacimiento, nivel, url_licencia]],
                          columns=['Nombre', 'apodo', 'Correo', 'Nacimiento', 'Nivel', 'Licencia'])
        if os.path.exists(DATA_FILE):
            df.to_csv(DATA_FILE, mode='a', index=False, header=False)
        else:
            df.to_csv(DATA_FILE, index=False)

        # Crear QR
        img = qrcode.make(url_licencia)
        img.save(f'licencias/{nombre}.png')

        return redirect(url_licencia)
    return render_template('registro.html')

@app.route('/licencia/<nombre>')
def licencia_virtual(nombre):
    if not os.path.exists(DATA_FILE):
        return "Licencia no encontrada."
    df = pd.read_csv(DATA_FILE)
    user_data = df[df['Nombre'] == nombre].to_dict(orient='records')
    if not user_data:
        return "Piloto no encontrado."
    return render_template('licencia_virtual.html', datos=user_data[0])

if __name__ == '__main__':
    app.run()
