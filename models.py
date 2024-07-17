from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Area(db.Model):
    __tablename__ = 'Area'
    idArea = db.Column(db.Integer, primary_key=True)
    nombreArea = db.Column(db.String)
    abreviatura = db.Column(db.String)

class SubArea(db.Model):
    __tablename__ = 'SubAreas'
    idSubArea = db.Column(db.Integer, primary_key=True)
    idArea = db.Column(db.Integer, db.ForeignKey('Area.idArea'))
    nombreSubArea = db.Column(db.String)
    abreviatura = db.Column(db.String)

class ProcAdmin(db.Model):
    __tablename__ = 'ProcAdmin'
    idProcAdmin = db.Column(db.Integer, primary_key=True)
    idSubArea = db.Column(db.Integer, db.ForeignKey('SubAreas.idSubArea'))
    nombre = db.Column(db.String)
    codigo = db.Column(db.String)
    pdf = db.Column(db.LargeBinary)

class Pago(db.Model):
    __tablename__ = 'Pago'
    idPago = db.Column(db.Integer, primary_key=True)
    idProcAdmin = db.Column(db.Integer, db.ForeignKey('ProcAdmin.idProcAdmin'))
    monto = db.Column(db.Float)
    descripcion = db.Column(db.String)
