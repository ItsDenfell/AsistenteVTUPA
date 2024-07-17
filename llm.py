import openai
import os
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from db_consultas import buscar_procedimientos_por_nombre, buscar_procedimientos_por_tipo

openai.api_key = os.getenv('OPENAI_API_KEY')

# Configurar el modelo GPT-3.5 Turbo
llm = OpenAI(model="gpt-3.5-turbo")

def obtener_respuesta(consulta):
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

    # Si no se encuentra en la base de datos, usar GPT-3.5 Turbo para generar una respuesta
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente virtual que responde preguntas sobre el TUPA."},
            {"role": "user", "content": consulta}
        ]
    )
    respuesta_gpt = response.choices[0].message.content.strip()
    return respuesta_gpt
