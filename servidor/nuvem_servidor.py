import socket
import cv2
import numpy as np
import json
from ultralytics import YOLO

model = YOLO('yolo11n.pt')
vehicle_classes = [2, 3, 5, 7]

sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_servidor.bind(('', 9000))

print("[*] Servidor Cloud de IA aguardando streams de video...")

while True:
    dados_bytes, endereco_cliente = sock_servidor.recvfrom(65535)

    np_arr = np.frombuffer(dados_bytes, dtype=np.uint8)

    frame_recebido = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame_recebido is not None:
        results = model.predict(frame_recebido, conf=0.5, classes=vehicle_classes, verbose=False)
        contagem = len(results[0].boxes)
        
        print(f"[*] Frame recebido de {endereco_cliente[0]} -> {contagem} veiculo(s) detectado(s)")

        payload = {"carros": contagem}
        json_str = json.dumps(payload)
        dados_resposta = json_str.encode()

        dest = (endereco_cliente[0], 9001)
        sock_servidor.sendto(dados_resposta, dest)