import socket
import cv2

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 9090

s = socket.socket()
s.bind((SERVER_ADDRESS, SERVER_PORT))

s.listen(100)
print("Escuchando al servidor en " + str((SERVER_ADDRESS, SERVER_PORT)))

while True:
    c, addr = s.accept()
    print("Cliente conectado: " + str(addr))

    video_path = "C:\\Users\\User\\Videos\\videoplayback.mp4"  # Ruta del video a cargar
    video = cv2.VideoCapture(video_path)

    frame_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            print("Fin de la transmisión del video")
            break
        # Codificar el frame como bytes para enviarlo
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        # Enviar el tamaño del frame al cliente
        frame_size = len(frame_bytes).to_bytes(4, byteorder='big')
        c.send(frame_size)

        # Enviar el frame al cliente
        c.send(frame_bytes)

        frame_count += 1
        print("Enviando frame {} al cliente".format(frame_count))

    video.release()
    c.close()
