import cv2
import socket
import json

SERVER_IP = '127.0.0.1'
SERVER_PORT_VIDEO = 9000
SERVER_PORT_JSON = 9001 # O cliente vai escutar o retorno nessa porta

# TODO: Crie e configures DOIS sockests UDP. Um para enviar o video, outro para receber o JSON.
# DICA: Faça o bind() no socket de recebimento 

sock_envio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # AF_INET indica IPv4 
sock_recebimento = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM define o protocolo UDP

# Associa o socket de recebimento ao IP local e à porta 9001
sock_recebimento.bind((SERVER_IP, SERVER_PORT_JSON))

# Tempo máximo de espera pelo JSON
# Evita que o programa fique travado/bloqueado esperando dados e congele a exibição do vídeo.
sock_recebimento.settimeout(0.01)

cap = cv2.VideoCapture('video.mp4')     # Abre o arquivo de vídeo indicado

quantidade_veiculos = 0

while cap.isOpened(): 
    sucess, frame = cap.read()  # Lê quadro a quadro do vídeo
    if not sucess:
        break

    # 1. Reduzir a resolução para caber no pacote UDP 
    frame_redimensionado = cv2.resize(frame, (480, 320))

    # 2. Comprimir o frame para o formato JPEG
    # Encode_param define a qualidade. 80 é um bom equilibrio entre tamanho e visibilidade para a IA.
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
    result, encimg = cv2.imencode('.jpg', frame_redimensionado, encode_param)

    # 3. Converter para bytes puros
    dados_bytes = encimg.tobytes()

    # Verificação de segurança: O pacote tem menos de 65KB?

    if len(dados_bytes) < 65000:
        # TODO: Envie 'dados_bytes'  usando sock_envio par o IP e Porta do Servidor
        sock_envio.sendto(dados_bytes, (SERVER_IP, SERVER_PORT_VIDEO))

    else:
        print('Quadro grande demais para UDP!')


    # ----------------------------------------------------------------
    # TODO: RECEBER O RETORNO DA NUVEM (JSON)
    # Como o UDP não é bloqueante se configurarmos um timeout pequeno,
    # tente receber o JSON do servidor aqui.
    try:
        msg, _ = sock_recebimento.recvfrom(1024)
        dados_json = json.loads(msg.decode())

        quantidade_veiculos = dados_json.get("carros", 0)

    except socket.timeout: 
        pass

    # -----------------------------------------------------------------
    # TODO: MOSTRAR O RESULTADO NA TELA
    # Se você recebeu o JSON, use cv2.putText() para desenhar a quantidade
    # de carros detectados no canto do 'frame_redimensionado'.
    # -----------------------------------------------------------------
    
    cv2.putText(frame_redimensionado, f'Veiculos detectados: {quantidade_veiculos}',
        (10,30),    # Posição (x, y) do texto
        cv2.FONT_HERSHEY_SIMPLEX,       # Fonte
        0.8,        # Tamanho da fonte
        (0, 255, 0),        # Cor em BGR (Verde)
        2       # Espessura das linhas do texto
    )

    cv2.imshow("Dashcam - Visão do Motorista", frame_redimensionado)
    if cv2.waitKey(30) & 0xFF == ord('q'): # O 30 simula ~30fps na leitura local
        break

cap.release()
cv2.destroyAllWindows()