from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Función para crear la tabla SQL con tus campos
def crear_db():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cedula TEXT,
            telefono TEXT,
            fecha_nac TEXT,
            correo TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    # Capturamos los datos del formulario
    datos = (
        request.form['nombre'],
        request.form['cedula'],
        request.form['telefono'],
        request.form['fecha_nac'],
        request.form['correo']
    )
    
    # Insertamos en SQL
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO personas (nombre, cedula, telefono, fecha_nac, correo) VALUES (?,?,?,?,?)', datos)
    conn.commit()
    conn.close()
    
    return "<h1>¡Usuario registrado con éxito en la base de datos!</h1><a href='/'>Volver al inicio</a>"

if __name__ == '__main__':
    crear_db()
    app.run(debug=True)