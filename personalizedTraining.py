import cv2
import os
import json
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Dicionário de recomendações
instruction_texts = {
    "abriraboca": "Por favor, abra a boca. 😲",
    "sorrir": "Por favor, sorria. 😁",
    "mostraralingua": "Por favor, mostre a língua. 😝",
    "levantarassobrancelhas": "Por favor, levante as sobrancelhas.",
    "piscarosolhos": "Por favor, pisque um dos olhos. 😉"
}

# Função para carregar preferências do usuário
def load_user_preferences():
    with open('user_preferences.json', 'r', encoding='utf-8') as file:
        return json.load(file)

class CaptureApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Vamos realizar um treinamento personalizado para você,\n"
                                "para isso, siga as instruções que lhe forem passadas a seguir.",
                           font_size='20sp', halign='center', valign='middle')
        self.label.bind(size=self.label.setter('text_size'))
        self.start_button = Button(text="Iniciar", font_size='20sp')
        self.start_button.bind(on_press=self.start_capture)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.start_button)
        return self.layout

    def start_capture(self, instance):
        # Carregar preferências do usuário
        self.preferences = load_user_preferences()
        # Coletar as preferências em uma lista
        self.gestures = [
            self.preferences["Botão Direito"],
            self.preferences["Botão Esquerdo"],
            self.preferences["Pressionar Botão Esquerdo"]
        ]

        # Iniciar o processo de captura
        self.current_gesture_index = 0
        self.capture_next_gesture()

    def capture_next_gesture(self):
        if self.current_gesture_index < len(self.gestures):
            gesture = self.gestures[self.current_gesture_index]
            self.label.text = instruction_texts[gesture.lower()] + "\nPreparando para capturar em 5 segundos..."
            # Agendar a captura de imagens após 5 segundos
            Clock.schedule_once(lambda dt: self.capture_faces(gesture), 5)
            self.current_gesture_index += 1
        else:
            print("Captura concluída.")
            self.stop()  # Finaliza o aplicativo

    def capture_faces(self, subfolder_name):
        # Crie o diretório da subpasta dentro de 'dataset', se não existir
        dataset_dir = os.path.join('dataset', subfolder_name)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        # Inicialize a webcam
        cam = cv2.VideoCapture(0)

        # Espelhar a câmera
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print(f"Capturando faces para a subpasta '{subfolder_name}'. Olhe para a câmera e espere...")
        capturas = len(os.listdir(dataset_dir))
        count = 0
        while count < 100:
            ret, img = cam.read()

            # Espelha a imagem horizontalmente para uma visualização mais natural
            img = cv2.flip(img, 1)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                # Salve a imagem capturada no dataset/subpasta
                capturas += 1
                cv2.imwrite(f"{dataset_dir}/User.{capturas}.jpg", gray)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('image', img)

            # Interrompe o processo se capturar 30 fotos ou se o usuário pressionar 'q'
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Chama o próximo gesto após capturar as fotos
        # Certifique-se de que o próximo gesto só é chamado após a captura estar completa
        Clock.schedule_once(lambda dt: self.capture_next_gesture(), 1)  # Atrasar ligeiramente antes de chamar o próximo gesto


# Chama a função para iniciar a aplicação
if __name__ == '__main__':
    CaptureApp().run()
