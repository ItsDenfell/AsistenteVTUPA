from flask import Flask, request, jsonify, render_template
from config import Config
from models import db, Area, SubArea, ProcAdmin, Pago
from transcriber import transcribir_audio
from tts import sintetizar_voz

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio', methods=['POST'])
def audio():
    archivo_audio = request.files['audio']
    texto = transcribir_audio(archivo_audio)
    respuesta = obtener_respuesta(texto)
    audio_sintetizado = sintetizar_voz(respuesta)
    return jsonify({
        'texto': respuesta,
        'archivo': audio_sintetizado
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
