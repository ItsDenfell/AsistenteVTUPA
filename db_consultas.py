from models import db, ProcAdmin

def buscar_procedimientos_por_nombre(nombre):
    procedimientos = ProcAdmin.query.filter(ProcAdmin.nombre.contains(nombre)).all()
    print(f"Consulta SQL: {str(procedimientos)}")
    return procedimientos

def buscar_procedimientos_por_tipo(tipo):
    procedimientos = ProcAdmin.query.filter(ProcAdmin.nombre.contains(tipo)).all()
    print(f"Consulta SQL: {str(procedimientos)}")
    return procedimientos
