import os
from sqlalchemy import create_engine, MetaData, Table, Column, String, LargeBinary, select, update
from sqlalchemy.exc import SQLAlchemyError

# Configuración de la base de datos
DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=' + \
    'DRIVER={ODBC Driver 17 for SQL Server};' + \
    'SERVER=DESKTOP-B340BGP\\SQLEXPRESS;' + \
    'DATABASE=DB_TUPA;' + \
    'Trusted_Connection=yes;'

# Crear el motor y reflejar la tabla
engine = create_engine(DATABASE_URI)
metadata = MetaData()

proc_admin_table = Table(
    'ProcAdmin', metadata,
    Column('idProcAdmin', String),
    Column('idSubArea', String),
    Column('nombre', String(500)),
    Column('codigo', String(10)),
    Column('pdf', LargeBinary),
    extend_existing=True
)
metadata.create_all(engine)

def update_pdf_content(pdf_folder):
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            codigo = pdf_file.split('.')[0]
            pdf_path = os.path.join(pdf_folder, pdf_file)
            
            with open(pdf_path, 'rb') as file:
                pdf_content = file.read()

            with engine.connect() as conn:
                trans = conn.begin()
                try:
                    select_stmt = select(proc_admin_table.c.codigo).where(proc_admin_table.c.codigo == codigo)
                    result = conn.execute(select_stmt).fetchone()

                    if result:
                        update_stmt = (
                            update(proc_admin_table)
                            .where(proc_admin_table.c.codigo == codigo)
                            .values(pdf=pdf_content)
                        )
                        conn.execute(update_stmt)
                        trans.commit()
                        print(f"Actualización exitosa para código: {codigo} con el contenido del PDF")
                    else:
                        trans.rollback()
                        print(f"No se encontró coincidencia para el código: {codigo}")
                except SQLAlchemyError as e:
                    trans.rollback()
                    print(f"Error al actualizar el código {codigo}: {e}")

pdf_folder = 'pdfs_procedimientos'
update_pdf_content(pdf_folder)

# Verificación de la actualización
try:
    with engine.connect() as conn:
        stmt = select([proc_admin_table.c.codigo, proc_admin_table.c.pdf])
        results = conn.execute(stmt).fetchall()
        for row in results:
            codigo, pdf_content = row
            if pdf_content:
                print(f"Código: {codigo}, PDF Content Length: {len(pdf_content)} bytes")
            else:
                print(f"Código: {codigo}, PDF Content: None")
except SQLAlchemyError as e:
    print(f"Error al verificar los datos: {e}")



