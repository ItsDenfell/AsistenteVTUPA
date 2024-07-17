import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import pickle

def extraer_texto_pdf(ruta_pdf):
    texto_completo = ""
    documento = fitz.open(ruta_pdf)
    for pagina in documento:
        texto_completo += pagina.get_text()
    return texto_completo

def crear_embeddings(texto):
    modelo_embeddings = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = modelo_embeddings.encode(texto, convert_to_tensor=True)
    return embeddings

def guardar_embeddings(embeddings, textos, archivo):
    with open(archivo, 'wb') as f:
        pickle.dump({'embeddings': embeddings, 'textos': textos}, f)

def cargar_embeddings(archivo):
    with open(archivo, 'rb') as f:
        embeddings = pickle.load(f)
    return embeddings

# Ejemplo de uso
ruta_pdf = 'pdftupa/TUPA Procedimientos Administrativos.pdf'
texto_pdf = extraer_texto_pdf(ruta_pdf)
embeddings_pdf = crear_embeddings(texto_pdf)
guardar_embeddings(embeddings_pdf, [texto_pdf], 'embeddings_pdf.pkl')
