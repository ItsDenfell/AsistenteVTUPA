import requests
import os

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

def sintetizar_voz(texto):
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ELEVENLABS_API_KEY}"
    }
    data = {
        "text": texto,
        "voice_settings": {
            "gender": "female",
            "language": "es"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json().get("audio_url")
