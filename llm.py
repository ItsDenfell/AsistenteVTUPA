import openai
# openai es el API de asistente
# Asistente: IA diseñada específicamente para este propósito que utiliza los modelos y las herramientas de llamadas de OpenAI
import os
from langchain_openai import ChatOpenAI
# ChatOpenAI es el modelo de IA
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from db_consultas import buscar_procedimientos_por_nombre, buscar_procedimientos_por_tipo
from app import app  # Importar la aplicación Flask para usar el contexto de la aplicación


openai.api_key = os.getenv('OPENAI_API_KEY')

# VAARIABLE DONDE ESTA ALMACENADO EL MODELO
# Configurar el modelo GPT-3.5 Turbo
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Definir el template del prompt
# PromtTemplate: plantillas de prompts) son estructuras predefinidas que ayudan a formular solicitudes (prompts) para modelos de lenguaje de manera consistente y efectiva. Estas plantillas se utilizan para guiar la interacción con el modelo, proporcionando una estructura que el modelo puede seguir para generar respuestas relevantes y precisas.
prompt_template = PromptTemplate(
    input_variables=["consulta"],
    template="Eres un asistente virtual que responde preguntas sobre el TUPA. {consulta}"
)


# Crear el LLMChain
chain = LLMChain(prompt=prompt_template, llm=llm)

def obtener_respuesta(consulta):
    respuesta_db = None

    with app.app_context():  # Asegurarse de que las consultas a la base de datos se realicen dentro del contexto de la aplicación
        # Verificar si la consulta es sobre procedimientos específicos en la base de datos
        if "procedimiento" in consulta.lower():
            nombre_procedimiento = consulta.lower().split("procedimiento de")[-1].strip()
            procedimientos = buscar_procedimientos_por_nombre(nombre_procedimiento)
            if procedimientos:
                respuesta_db = f"En el TUPA actualmente se encuentran los siguientes procedimientos relacionados con '{nombre_procedimiento}':\n"
                for proc in procedimientos:
                    respuesta_db += f"ID: {proc.idProcAdmin}, Nombre: {proc.nombre}, Código: {proc.codigo}\n"
                return respuesta_db

        # Verificar si la consulta es sobre el número de procedimientos
        if "cuántos procedimientos" in consulta.lower():
            tipo_procedimiento = consulta.lower().split("procedimientos de")[-1].strip()
            procedimientos = buscar_procedimientos_por_tipo(tipo_procedimiento)
            if procedimientos:
                respuesta_db = f"En el TUPA hay {len(procedimientos)} procedimientos de '{tipo_procedimiento}'.\n"
                return respuesta_db

    # Utilizar LangChain para gestionar el prompt y generar una respuesta
    respuesta_gpt = chain.run({"consulta": consulta})

    return respuesta_gpt