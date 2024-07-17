from llm import obtener_respuesta

def main():
    while True:
        pregunta = input("Haz tu pregunta sobre el TUPA (escribe 'salir' para terminar):\n")
        if pregunta.lower() == 'salir':
            break
        respuesta = obtener_respuesta(pregunta)
        print("Respuesta del asistente:")
        print(respuesta)

if __name__ == "__main__":
    main()
