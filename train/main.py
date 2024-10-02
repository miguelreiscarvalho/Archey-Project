import cv2
import numpy as np
from PIL import Image
import os


def train_model():
    dataset_dir = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Dicionário para mapear expressões faciais a um ID numérico
    expression_labels = {}
    current_id = 0
    face_samples = []
    ids = []

    # Função para obter as imagens e os rótulos do dataset com subpastas
    def get_images_and_labels(path):
        for expression in os.listdir(path):
            expression_path = os.path.join(path, expression)
            if not os.path.isdir(expression_path):
                continue

            # Verifica se a expressão já foi mapeada
            if expression not in expression_labels:
                expression_labels[expression] = current_id
                current_id += 1

            # Pega o ID associado à expressão
            expression_id = expression_labels[expression]

            for image_file in os.listdir(expression_path):
                image_path = os.path.join(expression_path, image_file)
                pil_img = Image.open(image_path).convert('L')  # Converta para escala de cinza
                img_numpy = np.array(pil_img, 'uint8')

                # Detecta as faces na imagem
                faces = face_detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    face_samples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(expression_id)

    # Chama a função para carregar as imagens e os rótulos
    get_images_and_labels(dataset_dir)

    print(f"Treinando o modelo de reconhecimento facial para {len(expression_labels)} expressões faciais. Aguarde...")

    # Treina o reconhecedor LBPH com as faces e seus rótulos
    recognizer.train(face_samples, np.array(ids))

    # Salve o modelo treinado
    recognizer.write('expression_trainer.yml')

    # Exibe os rótulos das expressões mapeadas
    print("Expressões faciais mapeadas:")
    for expression, id_ in expression_labels.items():
        print(f"ID: {id_} - Expressão: {expression}")


# Treine o modelo
train_model()
