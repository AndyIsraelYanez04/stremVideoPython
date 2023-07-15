import socket  # Importar el módulo socket para la comunicación de red
import cv2  # Importar el módulo OpenCV para el procesamiento de imágenes y video

SERVER_ADDRESS = "127.0.0.1"  # Dirección IP del servidor (localhost)
SERVER_PORT = 9090  # Puerto del servidor

s = socket.socket()  # Crear un objeto de socket
s.bind((SERVER_ADDRESS, SERVER_PORT))  # Vincular el socket a la dirección y puerto del servidor

s.listen(100)  # Escuchar conexiones entrantes con un tamaño de cola de 100
print("Escuchando al servidor en " + str((SERVER_ADDRESS, SERVER_PORT)))  # Imprimir mensaje de escucha

while True:  # Bucle infinito para aceptar conexiones entrantes
    c, addr = s.accept()  # Aceptar la conexión entrante y obtener el objeto de socket y la dirección del cliente
    print("Cliente conectado: " + str(addr))  # Imprimir la dirección del cliente conectado

    video_path = "C:\\Users\\User\\Videos\\videoplayback.mp4"  # Ruta del video a cargar
    video = cv2.VideoCapture(video_path)  # Crear un objeto de captura de video para el video en la ruta especificada

    frame_count = 0  # Contador de fotogramas

    while True:  # Bucle infinito para enviar fotogramas del video al cliente
        ret, frame = video.read()  # Leer un fotograma del video
        if not ret:  # Si no se pudo leer un fotograma, se llegó al final del video
            print("Fin de la transmisión del video")
            break  # Salir del bucle

        # Codificar el fotograma como bytes para enviarlo
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        # Enviar el tamaño del fotograma al cliente
        frame_size = len(frame_bytes).to_bytes(4, byteorder='big')
        c.send(frame_size)

        # Enviar el fotograma al cliente
        c.send(frame_bytes)

        frame_count += 1  # Incrementar el contador de fotogramas
        print("Enviando frame {} al cliente".format(frame_count))  # Imprimir el número de fotograma enviado

    video.release()  # Liberar el objeto de captura de video
    c.close()  # Cerrar la conexión con el cliente


# para instalar pip install opencv-python
