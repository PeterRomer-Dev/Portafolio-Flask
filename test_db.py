from app import app, db
from sqlalchemy import text
with app.app_context():
    try:
        res = db.session.execute(text('SELECT * FROM personas'))
        print("✅ CONEXIÓN EXITOSA. Datos encontrados:", res.fetchall())
    except Exception as e:
        print("❌ ERROR REAL:", e)
