from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Crear la aplicación Flask y configurar la base de datos
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Definir un modelo simple para probar la conexión
class Area(db.Model):
    __tablename__ = 'Area'
    idArea = db.Column(db.Integer, primary_key=True)
    nombreArea = db.Column(db.String)
    abreviatura = db.Column(db.String)

def test_db_connection():
    with app.app_context():
        try:
            # Realizar una consulta simple
            areas = Area.query.all()
            print(f"Conexión exitosa! Se encontraron {len(areas)} áreas.")
            for area in areas:
                print(f"ID: {area.idArea}, Nombre: {area.nombreArea}, Abreviatura: {area.abreviatura}")
        except Exception as e:
            print(f"Error al conectarse a la base de datos: {e}")

if __name__ == '__main__':
    test_db_connection()
