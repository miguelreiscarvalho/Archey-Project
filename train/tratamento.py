import cv2
import os

# Caminhos das pastas
input_folder = 'fotos'
output_folder = 'fotos_processadas'

# Verifique se a pasta de saída existe, se não, crie-a
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Carregar o classificador de rosto pré-treinado
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Percorre todas as imagens na pasta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Filtra por formatos de imagem
        image_path = os.path.join(input_folder, filename)

        # Ler a imagem
        image = cv2.imread(image_path)

        # Converter para escala de cinzas
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detectar rostos
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

        # Salvar imagens com rostos reconhecidos
        for (x, y, w, h) in faces:
            # Recorta o rosto da imagem
            face = gray_image[y:y + h, x:x + w]

            # Gera um nome para a imagem processada
            output_filename = os.path.join(output_folder, f"face_{filename}")
            cv2.imwrite(output_filename, face)

print("Processamento concluído!")
