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
