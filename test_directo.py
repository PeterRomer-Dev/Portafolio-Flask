import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'sistema.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personas';")
    table = cursor.fetchone()
    if table:
        print("✅ TABLA ENCONTRADA: personas")
        cursor.execute("SELECT * FROM personas LIMIT 1")
        print("📊 DATOS:", cursor.fetchone())
    else:
        print("❌ ERROR: La tabla 'personas' no existe en el archivo.")
    conn.close()
except Exception as e:
    print("❌ ERROR DE CONEXIÓN:", e)
