from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime # Añade esto arriba con los otros imports

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
def crear_db():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    # Aseguramos que la tabla tenga todos los campos necesarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cedula TEXT,
            telefono TEXT,
            fecha_nac TEXT,
            correo TEXT
            fecha_registro TEXT  -- <--- Nueva columna
        )
    ''')
    conn.commit()
    conn.close()

# --- RUTAS PÚBLICAS (PORTAFOLIO Y REGISTRO) ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/guardar', methods=['POST'])
def guardar():

    # Capturamos la fecha y hora actual con un formato legible
    ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    datos = (
        request.form['nombre'],
        request.form['cedula'],
        request.form['telefono'],
        request.form['fecha_nac'],
        request.form['correo'],
        ahora # <--- Añadimos la variable automática aquí
    )
    
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO personas (nombre, cedula, telefono, fecha_nac, correo, fecha_registro) 
        VALUES (?,?,?,?,?,?)
    ''', datos)
    conn.commit()
    conn.close()
    
    return f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #121212; font-family: 'Poppins', sans-serif;">
        <div style="background: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0px 10px 30px rgba(0,255,0,0.1); width: 350px;">
            <div style="font-size: 50px; margin-bottom: 20px;">✅</div>
            <h2 style="color: #28a745; margin-top: 0;">¡Registro Exitoso!</h2>
            <p style="color: #333; margin-bottom: 30px;">Tus datos han sido almacenados correctamente en el sistema.</p>
            <a href="/" style="
                color: #28a745; 
                text-decoration: none; 
                font-weight: bold; 
                border: 2px solid #28a745; 
                padding: 10px 25px; 
                border-radius: 8px;
                transition: 0.3s;
            " onmouseover="this.style.background='#28a745'; this.style.color='white';" 
               onmouseout="this.style.background='transparent'; this.style.color='#28a745';">
                Continuar
            </a>
        </div>
    </div>
    """

# --- RUTAS PRIVADAS (ADMINISTRACIÓN) ---

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    clave_correcta = "Peter046"
    clave_ingresada = request.form['password']
    
    if clave_ingresada == clave_correcta:
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        
        # AQUÍ ESTA EL CAMBIO: Añadimos "ORDER BY id DESC"
        cursor.execute('SELECT * FROM personas ORDER BY id DESC')

        usuarios_registrados = cursor.fetchall()
        conn.close()
        return render_template('usuarios.html', lista=usuarios_registrados)
    else:
        # Generamos el HTML directamente desde Python para no crear otro archivo
        return f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #121212; font-family: sans-serif;">
            <div style="background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0px 0px 20px rgba(255,0,0,0.2);">
                <h2 style="color: red; margin-top: 0;">⚠️ Error de Acceso</h2>
                <p style="color: #333;">La clave introducida es incorrecta.</p>
                <br>
                <a href="/login" style="color: blue; text-decoration: none; font-weight: bold; border: 1px solid blue; padding: 8px 15px; border-radius: 5px;">Continuar</a>
            </div>
        </div>
        """

# --- INICIO DE LA APLICACIÓN ---
if __name__ == '__main__':
    crear_db()  # Crea la DB si no existe cada vez que inicias el servidor
    app.run(debug=True)

    # Fin de la jornada de hoy