import cv2 as cv
import numpy as np
import mediapipe as mp
from pynput.mouse import Button, Controller
from tkinter import *
import threading
import time
import pyautogui as pa
from deepface import DeepFace
import win32api
import win32con
import keyboard


"""
REQUISITOS PARA FUNCIONAMENTO
Softwares necessários:
-IDE para execução do código (Pycharm, Visual Code)
-Python 3.8x
-Java JDK

-Será necessário criar uma maquina virtual na IDE.

Instalação:
# Execute cada linha abaixo uma por vez

pip install opencv-python
pip install numpy
pip install mediapipe
pip install pynput
pip install pyautogui



COMANDOS

CLICK - Levantar Sobrancelha
DUPLO CLICK - Manter Sobrancelha Levantada
PRESSIONAR - Abrir Boca
BOTÃO DIREITO - Sorrir

Teclado Virtual
https://apps.microsoft.com/detail/9nblggh35mpc?ocid=webpdpshare

#ATENÇÃO#
Ao executar o programa, mantenha-se como o rosto centralizado e NEUTRO, uma vez que o primeiro frame
será responsável por reconhecer a distáncia inicial entre os pontos no seu rosto. E por conseguinte
serão usadoos como fator de comparação para execução dos COMANDOS.
"""

root = Tk()

altura_monitor = root.winfo_screenheight()
largura_monitor = root.winfo_screenwidth()

print(altura_monitor, largura_monitor)

#  Aqui é definido o centro do monitor. Esse dado será usado futuramente para inicialização
#  do controle do mouse.

ponto_central_horizontlal = (0 + largura_monitor) * 0.5
ponto_central_vertical = (0 + altura_monitor) * 0.5

# OBS
# Parâmetro a ser tratado futuramente
# Motivo: Se tivermos um monitor muito grande, esses valores podem ser muito baixo para se percorrer
# todo o monitor, entretanto se o valor for aumentando em grande proporção, pode ficar muito instável.

sensibilidadeX = 7
sensibilidadeY = 10

mouse = Controller()

x, y = ponto_central_horizontlal, ponto_central_vertical

#  mp_face_mesh é responsável por coletar a solução que utiliza a malha do rosto.
mp_face_mesh = mp.solutions.face_mesh
PONTOS_OLHO_ESQUERDO = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# right eyes indices
PONTOS_OLHO_DIREITO = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

PONTOS_IRIS_DIREITA = [474, 475, 476, 477]
PONTOS_IRIS_ESQUERDA = [469, 470, 471, 472]
PONTOS_LABIO_SUPERIOR = [0, 72, 12, 302]
PONTOS_LABIO_INFERIOR = [15, 85, 16, 315]
SOBRANCELHA = [52, 65, 66, 66]
PONTOS_EXT_OLHO_ESQ = [61, 76, 62, 78]
PONTOS_EXT_OLHO_DIR = [308, 291, 308, 291]

PONTOS_CONTORNO_ROSTO = [
    10,  338,  297,  332,  284,  251,  389,  356,  454,  323,
    361,  288,  397,  365,  379,  378,  400,  377,  152,  148,
    176,  149,  150,  136,  172,  58,   132,  93,   234,  127,
    162,  21,   54,   103,  67,   109  # Lista dos pontos que contornam o rosto
]

cap = cv.VideoCapture(1)

Modulos_Iniciais = 0

# Usada para definir os valores iniciais Beginner, os quais serão usados como comparadores
# com os novos valores
on_off = 0

# Ativa as funções (defs) responsáveis por executar os COMANDOS
funcoes = 0
key = 0
action = ""
mode = 0


def detect_face():
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    face_rect = None
    step = 0

    while step <= 10:
        #  while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv.resize(frame, (840, 560), fx=0, fy=0, interpolation=cv.INTER_CUBIC)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=10,
            flags=cv.CASCADE_SCALE_IMAGE,
        )
        if len(faces) > 0:

            step += 1
            (x, y, w, h) = faces[0]
            # Desenhar o retângulo ao redor do rosto
            #cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostrar o frame com o retângulo desenhado
            #cv.imshow('Face Detection', frame)

            face_rect = (x, y, w, h)

        #cv.imshow('Face Detection', frame)

    return face_rect


face_rect = detect_face()


def check_exit_key():
    if keyboard.is_pressed('f12'):  # Detecta se a tecla 'F12' foi pressionada
        return True
    return False


def main():
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.1,
            min_tracking_confidence=0
    ) as face_mesh:

        global ponto_central_horizontlal, ponto_central_vertical
        x1 = ponto_central_horizontlal
        y2 = ponto_central_vertical

        X, Y, W, H = face_rect

        while True:

            #  Variavies Globais
            global funcoes, Modulos_Iniciais, on_off

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv.flip(frame, 1)
            frame = frame[Y-100:Y+H+20, X-90:X+W+60]
            frame = cv.resize(frame, (840, 560), fx=0, fy=0, interpolation=cv.INTER_CUBIC)
            #  frame = cv.resize(frame, (360, 240))
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                # print(results.multi_face_landmarks[0].landmark)
                mesh_points = np.array(
                    [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in
                     results.multi_face_landmarks[0].landmark])

                cv.circle(frame, mesh_points[4], 5, color=(255, 0, 0), thickness=2)
                narizX, narizY = mesh_points[4]

                #  Coleta de pontos no eixo x, y e o raio do circulo criado
                (olho_direitoX, olho_direitoY), olho_direitoRaio = cv.minEnclosingCircle(mesh_points[PONTOS_IRIS_DIREITA])
                (olho_esquerdoX, olho_esquerdoY), olho_esquerdoRaio = cv.minEnclosingCircle(mesh_points[PONTOS_IRIS_ESQUERDA])
                (labio_superiorX, labio_superiorY), labio_superiorRaio = cv.minEnclosingCircle(mesh_points[PONTOS_LABIO_SUPERIOR])
                (labio_inferiorX, labio_inferiorY), labio_inferiorRaio = cv.minEnclosingCircle(mesh_points[PONTOS_LABIO_INFERIOR])
                (sobrancelhaX, sobrancelhaY), sobrancelhaRaio = cv.minEnclosingCircle(mesh_points[SOBRANCELHA])
                (ext_boca_esqX, ext_boca_esqY), Ext_Boca_Esq_Raio = cv.minEnclosingCircle(mesh_points[PONTOS_EXT_OLHO_ESQ])
                (ext_boca_direitoX, ext_boca_direitoY), Ext_Boca_Dir_Raio = cv.minEnclosingCircle(mesh_points[PONTOS_EXT_OLHO_DIR])

                Eixo_Labio_Superior = (np.array([labio_superiorX, labio_superiorY], dtype=np.int32))
                Eixo_Labio_Inferior = (np.array([labio_inferiorX, labio_inferiorY], dtype=np.int32))
                Eixo_Sobrancelha = (np.array([sobrancelhaX, sobrancelhaY], dtype=np.int32))
                Eixo_Ext_Boca_Esquerdo = (np.array([ext_boca_esqX, ext_boca_esqY], dtype=np.int32))
                Eixo_Ext_Boca_Direito = (np.array([ext_boca_direitoX, ext_boca_direitoY], dtype=np.int32))

                centro_olho_dir = (np.array([olho_direitoX, olho_direitoY], dtype=np.int32))

                Eixo_centro_olho_esq = (np.array([olho_esquerdoX, olho_esquerdoY], dtype=np.int32))
                #  Parte gráfica/visual dos pontos utilizados no algoritmo
                #  circle(imagem, coordenadas, tamanho, cor, espessura, tipo)


                #  Olho Direito
                cv.circle(frame, centro_olho_dir, int(olho_direitoRaio * 0.3), (255, 0, 255), 1, cv.LINE_AA)

                #  Olho Esquerdo
                cv.circle(frame, Eixo_centro_olho_esq, int(olho_esquerdoRaio * 0.3), (255, 0, 255), 1, cv.LINE_AA)

                #  Ponto Central Lábio Superior
                cv.circle(frame, Eixo_Labio_Superior, int(olho_direitoRaio * 0.3), (255, 0, 255), 1, cv.LINE_AA)

                #  Ponto Central Lábio Inferior
                cv.circle(frame, Eixo_Labio_Inferior, int(olho_direitoRaio * 0.3), (255, 0, 255), 1, cv.LINE_AA)

                # Ponto Central Sobrancelha Esquerda
                cv.circle(frame, Eixo_Sobrancelha, int(sobrancelhaRaio * 0.3), (255, 0, 255), 1, cv.LINE_AA)

                # Ponto da Extremidadde Esquerda dos Lábios
                cv.circle(frame, Eixo_Ext_Boca_Esquerdo, int(Ext_Boca_Esq_Raio), (255, 0, 255), 1, cv.LINE_AA)  # Click

                # Ponto da Extremidade Direita dos Lábios
                cv.circle(frame, Eixo_Ext_Boca_Direito, int(Ext_Boca_Dir_Raio), (255, 0, 255), 1, cv.LINE_AA)  # Click

                cv.line(frame, Eixo_Labio_Superior, Eixo_Labio_Inferior, (255, 0, 0), 1)
                cv.line(frame, Eixo_Ext_Boca_Esquerdo, Eixo_Ext_Boca_Direito, (255, 0, 0), 1)
                cv.line(frame, Eixo_centro_olho_esq, Eixo_Sobrancelha, (255, 0, 0), 1)


            #  x = ((olho_direitoX + olho_esquerdoX) * 0.5)
            #  y = ((olho_direitoY + olho_esquerdoY) * 0.5)

            if mode == 1:
                x = ((olho_direitoX + olho_esquerdoX) * 0.5)
                y = ((olho_direitoY + olho_esquerdoY) * 0.5)

            else:
                x = narizX
                y = narizY

            if on_off == 0:
                first_value_x = x
                first_value_y = y
                on_off = 1

            campo_livrex = 20
            campo_livrey = 20

            velocidade = 3

            distancia_cp = [abs(first_value_x - x), abs(first_value_y - y)]
            #  distancia_cp = [ponto_central_horizontlal, ponto_central_vertical]
            #  print(distancia_cp)

            fator_movimento = 0.3

            cv.rectangle(frame, [first_value_x - campo_livrex, first_value_y - campo_livrey],
                         [first_value_x + campo_livrex, first_value_y + campo_livrey]
                         , (0, 255, 0),
                         2
                         )

            #  print((x1, y2))
            if mode == 0 and x < first_value_x - campo_livrex:
                if x1 >= 0:
                    x1 -= (velocidade + distancia_cp[0] * 0.1) * fator_movimento
                #  first_value_x -= 1

                mouse.position = (x1, y2)

            if mode == 0 and y < first_value_y - campo_livrey:
                if y2 >= 0:
                    y2 -= (velocidade + distancia_cp[1] * 0.1) * fator_movimento
                #  first_value_y -= 1
                mouse.position = (x1, y2)

            if mode == 0 and x > first_value_x + campo_livrex:
                if x1 <= largura_monitor:
                    x1 += (velocidade + distancia_cp[0] * 0.1) * fator_movimento
                #  first_value_x += 1
                mouse.position = (x1, y2)

            if mode == 0 and y > first_value_y + campo_livrey:
                if y2 <= altura_monitor:
                    y2 += (velocidade + distancia_cp[1] * 0.1) * fator_movimento
                #  first_value_y += 1
                mouse.position = (x1, y2)

            """
            if mode != 0 and not mode_press:
                ponto_central_vertical = y2
                ponto_central_horizontlal = x1
                mode_press = True

            elif mode == 0:
                mode_press = False

            if mode != 0 and x < first_value_x and y < first_value_y:
                ganhox = first_value_x - x
                ganhoy = first_value_y - y

                x1 = (ponto_central_horizontlal - (ganhox * sensibilidadeX))
                y2 = (ponto_central_vertical - (ganhoy * sensibilidadeY))

                mouse.position = (x1, y2)

            elif mode != 0 and x < first_value_x and y > first_value_y:
                ganhox = first_value_x - x
                ganhoy = y - first_value_y

                x1 = (ponto_central_horizontlal - (ganhox * sensibilidadeX))
                y2 = (ponto_central_vertical + (ganhoy * sensibilidadeY))

                mouse.position = (x1, y2)

            elif mode != 0 and x > first_value_x and y < first_value_y:
                ganhox = x - first_value_x
                ganhoy = first_value_y - y

                x1 = (ponto_central_horizontlal + (ganhox * sensibilidadeX))
                y2 = (ponto_central_vertical - (ganhoy * sensibilidadeY))

                mouse.position = (x1, y2)

            elif mode != 0 and x > first_value_x and y > first_value_y:


                ganhox = x - first_value_x
                ganhoy = y - first_value_y
                x1 = (ponto_central_horizontlal + (ganhox * sensibilidadeX))
                y2 = (ponto_central_vertical + (ganhoy * sensibilidadeY))

                mouse.position = (x1, y2)
                
            """

            # Funções
            Modulo_Click = Eixo_centro_olho_esq[1] - Eixo_Sobrancelha[1]
            Modulo_Press = Eixo_Labio_Inferior[1] - Eixo_Labio_Superior[1]
            Modulo_Direito = Eixo_Ext_Boca_Direito[0] - Eixo_Ext_Boca_Esquerdo[0]

            #  print(Modulo_Click, Modulo_Press, Modulo_Direito)

            if Modulos_Iniciais == 0:
                Modulo_Click_Inicial = Modulo_Click
                Modulo_Direito_Inicial = Modulo_Direito
                Modulo_Press_Inicial = Modulo_Press
                Modulos_Iniciais = 1

            if distancia_cp[0] <= 15 and distancia_cp[1] <= 7:


                # print(f"CLick - {Modulo_Click_Inicial} - {Modulo_Click}")
                # print(f"Press - {Modulo_Press_Inicial} - {Modulo_Press}")
                # print(f"Direito - {Modulo_Direito_Inicial} - {Modulo_Direito}")

                if Modulo_Click >= Modulo_Click_Inicial + 13:

                    funcoes = 1

                elif Modulo_Direito >= Modulo_Direito_Inicial + 8:
                #    print("Press")
                    funcoes = 2

                else:
                    funcoes = 0

            else:
                funcoes = 0

            frame = cv.resize(frame, (352, 288), fx=0, fy=0, interpolation=cv.INTER_CUBIC)
            cv.imshow('img', frame)

            key = cv.waitKey(1)

            if check_exit_key():

                funcoes = 6
                break

    cap.release()
    cv.destroyAllWindows()

"""
def emotions():
    print("agora")
    frame_skip = 15  # Analisar a cada 5 frames
    frame_count = 0
    print("agora")
    while True:


        #  Variavies Globais
        global action, funcoes
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            break

        #  frame = cv.flip(frame, 1)
        #  img_h, img_w = frame.shape[:2]
        # results = face_mesh.process(rgb_frame)
        if frame_count % frame_skip == 0:

            try:
                frame_resized = cv.resize(frame, (224, 224))  # Redimensione para 224x224 ou um tamanho apropriado
                result = DeepFace.analyze(frame_resized, actions=['emotion'])

                # print("Result:", result)
                print(result)

                if isinstance(result, list) and len(result) > 0:

                    first_result = result[0]

                    dominant_emotion = first_result['dominant_emotion']
                    # emotion_scores = first_result['emotion']

                    print(dominant_emotion)

                    # COMANDOS
                    if dominant_emotion == 'happy':
                        action = "press"

                    elif dominant_emotion == 'surprise':
                        action = "right"

                    else:
                        action = ""

            except:
                pass

        if funcoes == 6:
            break
"""

key_acess = 0

def gestosPontos():
    global funcoes

    comando = 0
    ativo = True

    print("Comando Atual: Click")
    while True:
        try:

            # Gastar memoria
            print("", end="")

            if funcoes == 1:

                time.sleep(0.05)

                if funcoes == 1:

                    if comando == 0:
                        print("Clicou")
                        pa.click()
                        time.sleep(0.3)

                    if comando == 1:

                        if ativo:
                            print("Pressionou")
                            pa.mouseDown()
                            time.sleep(0.5)
                            ativo = False

                        else:
                            print("Soltou")
                            pa.mouseUp()
                            time.sleep(0.5)
                            ativo = True

                    if comando == 2:
                        print("Click Direito")
                        pa.click(button="right")
                        time.sleep(0.2)

            elif funcoes == 2:

                time.sleep(0.5)

                if funcoes == 2:

                    comando += 1
                    if comando >= 3:
                        comando = 0

                    if comando == 0:
                        print("Click Ativado")

                    elif comando == 1:
                        print("Pressionar Ativado")

                    elif comando == 2:
                        print("Click Direito Ativado")

            elif funcoes == 6:
                break

        except:
            pass


threading.Thread(target=main).start()
time.sleep(0.5)
gestosPontos()
