import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def transcribir_audio(archivo_audio):
    transcripcion = openai.Audio.transcribe("whisper-1", archivo_audio)
    return transcripcion['text']
