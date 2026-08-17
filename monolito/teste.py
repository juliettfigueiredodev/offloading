import cv2
import torch
import time
from ultralytics import YOLO

print(f"CUDA disponivel: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Usando GPU: {torch.cuda.is_available()}")
else:
    print("AVISO: Rodando em CPU. A inferência pode ser lenta.")

model = YOLO('yololln.pt')
source_path = "video.mp4"
cap = cv2.VideoCapture(source_path)

vehicle_classes = [2, 3, 5, 7]

ultimo_tempo_log = time.time()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_redimensionado = cv2.resize(frame, (1280, 720))

    results = model.predict(frame_redimensionado, conf=0.5, classes=vehicle_classes, device='cpu', verbose=False)

    tempo_atual = time.time()

    if tempo_atual - ultimo_tempo_log >= 1.0:
        quantidade_veiculos = len(results[0].boxes)

        hora_formatada = time.strftime("%H:%M:%S", time.localtime(tempo_atual))

        print(f"[{hora_formatada}] Veículos detectados na tela: {quantidade_veiculos}")

        ultimo_tempo_log = tempo_atual

    annotated_frame = results[0].plot()

    cv2.imshow("Detecção de Veículos Local", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()