import os

# Directorio de los PDFs
pdf_folder = 'pdfs_procedimientos'

# Renombrar archivos PDF
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        if 'Proc. Adm. (' in pdf_file:
            codigo = pdf_file.split('Proc. Adm. (')[1].split(')')[0]
        elif 'Proc. Adm. de Servicio (' in pdf_file:
            codigo = pdf_file.split('Proc. Adm. de Servicio (')[1].split(')')[0]
        else:
            continue

        new_name = f"{codigo}.pdf"
        old_path = os.path.join(pdf_folder, pdf_file)
        new_path = os.path.join(pdf_folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renombrado: {old_path} -> {new_path}")

print("Renombrado completado.")
