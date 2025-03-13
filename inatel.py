import cv2 as cv
import numpy as np
import mediapipe as mp
from pynput.mouse import Button, Controller
from tkinter import *
import threading
import time
import pyautogui as pa

root = Tk()

altura_monitor = root.winfo_screenheight()
largura_monitor = root.winfo_screenwidth()

pmmx = (0 + largura_monitor) * 0.5
pmmy = (0 + altura_monitor) * 0.5

print(pmmx, pmmy)

sensi_x = 7
sensi_y = 10

mouse = Controller()

x, y = 1, 1

mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# right eyes indices
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
mouth1 = [0, 72, 12, 302]
mouth2 = [15, 85, 16, 315]
eyebrow = [52, 65, 66, 66]
llc = [61, 76, 62, 78]
rlc = [308, 291, 308, 291]
nard = [107, 107, 107, 107]
nare = [336, 336, 336, 336]

cap = cv.VideoCapture(1)

first_value_y = []
first_value_x = []
on_off = 0
beginnerclick = 0
beginnerpress = 0
music_beginner = 0
ganhox = None
ganhoy = None

var1 = 0
var2 = 0
var3 = 0

def main():
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.1,
            min_tracking_confidence=0
    ) as face_mesh:
        while True:
            #  Variavies Globais
            global var1, var2, var3, beginnerclick, on_off, ganhox, ganhoy, beginnerpress, beginnernar, music_beginner

            ret, frame = cap.read()

            if not ret:

                var1 = 6
                var2 = 6
                var3 = 6
                break

            frame = cv.flip(frame, 1)
            frame = frame[80:400, 150:500]
            frame = cv.resize(frame, (840, 525), fx=0, fy=0, interpolation=cv.INTER_CUBIC)

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                # print(results.multi_face_landmarks[0].landmark)
                mesh_points = np.array(
                    [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in
                     results.multi_face_landmarks[0].landmark])

                (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                (m_cx, m_cy), m_radius = cv.minEnclosingCircle(mesh_points[mouth1])
                (m2_cx, m2_cy), m2_radius = cv.minEnclosingCircle(mesh_points[mouth2])
                (px, py), p_radius = cv.minEnclosingCircle(mesh_points[eyebrow])
                (llcx, llcy), llc_radius = cv.minEnclosingCircle(mesh_points[llc])
                (rlcx, rlcy), rlc_radius = cv.minEnclosingCircle(mesh_points[rlc])
                (nardx, nardy), nard_radius = cv.minEnclosingCircle(mesh_points[nard])
                (narex, narey), nare_radius = cv.minEnclosingCircle(mesh_points[nare])

                point_m = (np.array([m_cx, m_cy], dtype=np.int32))
                point_m2 = (np.array([m2_cx, m2_cy], dtype=np.int32))
                pp = (np.array([px, py], dtype=np.int32))
                cllc = (np.array([llcx, llcy], dtype=np.int32))
                crlc = (np.array([rlcx, rlcy], dtype=np.int32))
                cnard = (np.array([nardx, nardy], dtype=np.int32))
                cnare = (np.array([narex, narey], dtype=np.int32))

                center_left = (np.array([l_cx, l_cy], dtype=np.int32))
                center_right = (np.array([r_cx, r_cy], dtype=np.int32))

                cv.circle(frame, center_left, int(l_radius * 0.1), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, center_right, int(r_radius * 0.1), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, point_m, int(l_radius * 0.3), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, point_m2, int(l_radius * 0.3), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, pp, int(p_radius * 0.3), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, cllc, int(llc_radius), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, crlc, int(rlc_radius), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, cnard, int(nard_radius), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, cnare, int(nare_radius), (255, 0, 255), 1, cv.LINE_AA)

                pointfor = cnare[0] - cnard[0]
                pointclick = center_right[1] - pp[1]
                pointpress = point_m2[1] - point_m[1]
                pointright = crlc[0] - cllc[0]

                if beginnerclick == 0:

                    beginnerpar = pointfor
                    beginnerpoint = pointclick
                    beginnerright = pointright
                    beginnerpress = pointpress
                    beginnerclick = 1

                #  Comando o click 1
                """if pointclick >= beginnerpoint + 12:
                    var1 = 1

                else:
                    var1 = 0"""

                sf = (beginnerpar - pointfor)*1.2

                print(sf)


                #  print(f"nariz: {pointfor} cima: {pointpress} lado: {pointright} multiplicador: {sf}")

                #  Comando pressionar 2

                if pointpress >= beginnerpress+25:
                    var2 = 2

                #  Comando soltar 3
                elif pointpress < beginnerpress+25:
                    var2 = 3

                else:
                    var2 = 0

                #  Comando botão direito 4

                if pointright >= beginnerright+20 - sf:
                    var3 = 1

                # Comando Esc 5
                elif pointright <= beginnerright-20 - sf:
                    var3 = 5

                else:
                    var3 = 0

                cv.line(frame, point_m, point_m2, (255, 0, 0), 1)
                cv.line(frame, cllc, crlc, (255, 0, 0), 1)
                cv.line(frame, center_right, pp, (255, 0, 0), 1)
                cv.line(frame, cnard, cnare, (255, 0, 0), 1)

            x = ((l_cx + r_cx) * 0.5)
            y = ((l_cy + r_cy) * 0.5)

            if on_off == 0:
                first_value_x = x
                first_value_y = y
                on_off = 1

            if x < first_value_x and y < first_value_y:
                ganhox = first_value_x - x
                ganhoy = first_value_y - y

                x1 = (pmmx - (ganhox * sensi_x))
                y2 = (pmmy - (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            if x < first_value_x and y > first_value_y:
                ganhox = first_value_x - x
                ganhoy = y - first_value_y

                x1 = (pmmx - (ganhox * sensi_x))
                y2 = (pmmy + (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            if x > first_value_x and y < first_value_y:
                ganhox = x - first_value_x
                ganhoy = first_value_y - y

                x1 = (pmmx + (ganhox * sensi_x))
                y2 = (pmmy - (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            if x > first_value_x and y > first_value_y:
                ganhox = x - first_value_x
                ganhoy = y - first_value_y
                x1 = (pmmx + (ganhox * sensi_x))
                y2 = (pmmy + (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            cv.imshow('img', frame)
            key = cv.waitKey(1)

            if key == 27:
                cap.release()
                cv.destroyAllWindows()
                var1 = 6
                var2 = 6
                var3 = 6
                break


dict_rv = [["desligar", "desativar", "Desligar programa", "interromper programa", "Fechar programa" ],
           ["pressionar", "segurar", "Personare", "personagem"], ["soltar", "largar", "despertar"], ["apertar"],
           ["abrir", "expandir"], ["enviar", "mandar"], ["escrever", "digitar"], ["espaço"]]


key_acess = 0
key_acess2 = 0

def pressionar():
    global key_acess, key_acess2
    while True:
        try:
            # Gastar memoria
            print("", end="")

            if key_acess2 == 0:
                if var2 == 2:

                    time.sleep(0.5)

                    if var2 == 2:
                        print("Pressionou")
                        key_acess = 1
                        key_acess2 = 1
                        pa.mouseDown()

                    else:
                        pass

                elif var2 == 6:
                    break

            elif key_acess == 1:

                if var2 == 3:
                    time.sleep(0.5)

                    if var2 == 3:
                        print("Soltou")
                        key_acess = 0
                        key_acess2 = 0
                        pa.mouseUp()

                    elif var2 == 6:
                        break

                    else:
                        pass

                elif var2 == 6:
                    break

        except:
            print("Falhou")
            pass


def click():
    while True:

        try:
            # Gastar memoria
            print("", end="")

            if var3 == 1:

                time.sleep(0.1)

                if var3 == 1:
                    print("Clicou")
                    pa.click()
                    time.sleep(0.3)

                else:
                    pass

            elif var3 == 6:
                break

        except:

            pass


def button_right():
    while True:

        try:
            # Gastar memoria
            print("", end="")

            if var3 == 5:
                time.sleep(0.5)
                if var3 == 5:
                    print("Click Direito")
                    pa.click(button="right")

                else:
                    pass

            elif var3 == 9:
                time.sleep(0.5)
                if var3 == 9:
                    print("Esc")
                    pa.press('esc')

                else:
                    pass

            elif var3 == 6:
                break

        except:
            pass



threading.Thread(target=main).start()
#  recvoice()

time.sleep(0.5)
threading.Thread(target=click).start()

time.sleep(0.5)
pressionar()
