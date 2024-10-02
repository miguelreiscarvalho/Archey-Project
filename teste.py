import cv2

def recognize_expressions():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('expression_trainer.yml')  # Carrega o modelo treinado
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Dicionário de expressões faciais (precisa ser igual ao usado no treinamento)
    expression_labels = {0: "Abrir a Boca", 1: "Levantar as Sobrancelhas", 2: "Mostrar Lingua",
                         3:"Neutral", 4:"Piscar os olhos", 5:"Sorrir"}  # Ajuste conforme seu dataset

    cam = cv2.VideoCapture(0)

    while True:
        ret, img = cam.read()

        # Espelhda a câmera
        img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, flags=cv2.CASCADE_SCALE_IMAGE)


        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # Verifica se o reconhecimento é confiável
            print(id_, confidence)
            if confidence < 100:
                expression = expression_labels.get(id_, "Desconhecido")
                confidence_text = f"  {round(100 - confidence)}%"
            else:
                expression = "Desconhecido"
                confidence_text = f"  {round(100 - confidence)}%"

            # Exibe a expressão facial e o nível de confiança
            cv2.putText(img, str(expression), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence_text), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Reconhecimento de Expressões', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# Executa o reconhecimento em tempo real
recognize_expressions()