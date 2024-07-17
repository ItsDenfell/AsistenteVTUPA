import os
from sqlalchemy import create_engine, MetaData, Table, select, Column, String, LargeBinary
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
proc_admin_table = Table('ProcAdmin', metadata,
    Column('codigo', String(10), nullable=False),
    Column('pdf', LargeBinary),
    autoload_with=engine
)

# Verificación del contenido PDF
def verify_pdf_content(codigo):
    try:
        with engine.connect() as conn:
            stmt = select(proc_admin_table.c.codigo, proc_admin_table.c.pdf).where(proc_admin_table.c.codigo == codigo)
            result = conn.execute(stmt).fetchone()
            if result:
                codigo, pdf_content = result
                if pdf_content:
                    # Crear la carpeta 'verificados' si no existe
                    os.makedirs('verificados', exist_ok=True)
                    
                    pdf_path = os.path.join('verificados', f"{codigo}.pdf")
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_content)
                    print(f"PDF verificado y guardado como: {pdf_path}")
                else:
                    print(f"Código: {codigo}, PDF Content: None")
            else:
                print(f"No se encontró coincidencia para el código: {codigo}")
    except SQLAlchemyError as e:
        print(f"Error al verificar los datos: {e}")

# Verificar un archivo PDF específico por su código
codigo_a_verificar = 'PA1203DDB8_1'  # Reemplaza esto con el código que deseas verificar
verify_pdf_content(codigo_a_verificar)
