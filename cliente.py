

import socket  # Importa la biblioteca socket para la comunicación de red
import cv2  # Importa la biblioteca OpenCV para el procesamiento de imágenes y videos
import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas eficientes

SERVER_ADDRESS = "127.0.0.1"  # Dirección IP del servidor
SERVER_PORT = 9090  # Puerto del servidor

s = socket.socket()  # Crea un objeto socket para la comunicación
s.connect((SERVER_ADDRESS, SERVER_PORT))  # Establece una conexión con el servidor

print("Conectado al servidor en " + str((SERVER_ADDRESS, SERVER_PORT)))  # Imprime un mensaje de conexión exitosa

video_frames = []  # Lista para almacenar los frames de video recibidos

while True:  # Bucle infinito para recibir y mostrar los frames del video
    frame_size = s.recv(4)  # Recibe los primeros 4 bytes que representan el tamaño del siguiente frame de video

    if not frame_size:  # Verifica si no se recibió ningún dato en frame_size
        print("Fin de la transmisión del video")
        break  # Rompe el bucle si no se recibieron más frames

    frame_size = int.from_bytes(frame_size, byteorder='big')  # Convierte los bytes a un entero (orden big-endian)

    frame_bytes = b""  # Crea una cadena de bytes vacía para almacenar los bytes del frame de video
    remaining_bytes = frame_size  # Almacena el número de bytes que quedan por recibir

    while remaining_bytes > 0:  # Bucle para recibir todos los bytes del frame de video
        chunk = s.recv(min(remaining_bytes, 4096))  # Recibe un fragmento de bytes del frame de video (tamaño máximo de 4096 bytes)

        if not chunk:  # Verifica si no se recibió ningún dato en chunk
            print("Error al recibir los bytes del frame")
            break  # Rompe el bucle si no se recibieron más bytes del frame

        frame_bytes += chunk  # Concatena los bytes recibidos al conjunto de bytes del frame
        remaining_bytes -= len(chunk)  # Resta la longitud del fragmento recibido a los bytes restantes por recibir

    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)  # Convierte los bytes del frame en un array NumPy de tipo uint8
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)  # Decodifica el array de bytes en una imagen OpenCV en color
    cv2.imshow("Video del servidor", frame)  # Muestra la imagen del frame en una ventana llamada "Video del servidor"
    video_frames.append(frame)  # Agrega el frame a la lista de frames de video

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Espera durante 1 ms y verifica si la tecla 'q' ha sido presionada
        break  # Rompe el bucle si se presionó la tecla 'q'

s.close()  # Cierra la conexión del socket
cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas por OpenCV
