// grabador.js
let mediaRecorder;
let audioChunks = [];

function empezarGrabacion() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks);
                const formData = new FormData();
                formData.append('audio', audioBlob);

                fetch('/audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    mostrarRespuesta(data.texto);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 3000); // Grabación de 3 segundos
        });
}

function mostrarRespuesta(textoRespuesta) {
    const divRespuesta = document.getElementById('respuesta');
    divRespuesta.innerText = textoRespuesta;
}
