from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.clock import Clock
import json  # Para salvar as preferências em um arquivo JSON
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

# Opções para o menu seletor
gesture_options = ['Abrir a boca', 'Sorrir', 'Mostrar a língua', 'Levantar \nas Sobrancelhas', 'Piscar os olhos']
dic = {
    'Abrir a boca': 'Abriraboca',
    'Sorrir': 'Sorrir',
    'Mostrar a língua': 'Mostraralingua',
    'Levantar \nas Sobrancelhas': 'LevantarasSobrancelhas',
    'Piscar os olhos': 'Piscarosolhos'
}

# Primeira tela de boas-vindas
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.welcome_label = Label(
            text='Seja bem-vindo ao ARCHEY!',
            font_size='30sp',
            bold=True,
            color=(1, 1, 1, 1),  # Texto branco
            opacity=0  # Invisível no início
        )
        layout.add_widget(self.welcome_label)
        self.add_widget(layout)

    def on_enter(self, *args):
        # Quando a tela é exibida, inicia a animação de fade-in
        self.welcome_label.opacity = 1
        Clock.schedule_once(self.switch_to_next, 3)

    def switch_to_next(self, dt):
        # Troca automaticamente para a próxima tela (descrição)
        self.manager.current = 'description'


# Segunda tela com mais descrições
class DescriptionScreen(Screen):
    def __init__(self, **kwargs):
        super(DescriptionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Label com mais descrições sobre o software, centralizado
        self.description_label = Label(
            text='Um software pensado para você, trazendo maior acessibilidade\n'
                 'através da solução que permite controlar o computador de \n'
                 'uma forma intuitiva e divertida.',
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1),  # Texto branco
            opacity=0,  # Invisível no início
            halign='center',  # Centralizar horizontalmente
            valign='middle',  # Centralizar verticalmente
            text_size=(self.width, None)  # Ajusta o tamanho do texto ao widget
        )

        layout.add_widget(self.description_label)
        self.add_widget(layout)

        # Para garantir o redimensionamento correto
        self.description_label.bind(size=self._update_text_size)

    def _update_text_size(self, *args):
        # Define o tamanho de texto para centralizar dentro do Label
        self.description_label.text_size = (self.description_label.width, None)

    def on_enter(self, *args):
        # Animação de fade-in ao entrar na tela
        self.description_label.opacity = 1
        Clock.schedule_once(self.switch_to_next, 6)

    def switch_to_next(self, dt):
        # Troca automaticamente para a próxima tela (personalização)
        self.manager.current = 'customization'


# Terceira tela com as opções de personalização
class CustomizationScreen(Screen):
    def __init__(self, **kwargs):
        super(CustomizationScreen, self).__init__(**kwargs)

        # Layout principal usando FloatLayout
        layout = FloatLayout()

        # Texto no topo centralizado
        top_label = Label(
            text="Vamos personalizar sua experiência",
            font_size='25sp',
            bold=True,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        layout.add_widget(top_label)

        # Texto de instrução centralizado
        instruction_label = Label(
            text="Escolha quais gestos você irá utilizar para executar as funções do mouse.",
            font_size='17sp',
            size_hint=(None, None),
            size=(600, 50),
            pos_hint={'center_x': 0.5, 'top': 0.85}
        )
        layout.add_widget(instruction_label)

        # Funções do mouse com menus seletores em um GridLayout
        mouse_layout = GridLayout(cols=2, spacing=10, size_hint=(None, None), size=(400, 200), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        mouse_layout.bind(minimum_height=mouse_layout.setter('height'))

        # Armazenar seleções do usuário
        self.selections = {'Botão Direito': None, 'Botão Esquerdo': None, 'Pressionar Botão Esquerdo': None}
        self.spinners = {}  # Guardar referências dos spinners

        # Adicionar opções com menus para cada função do mouse
        for mouse_button in self.selections:
            mouse_label = Label(
                text=f"{mouse_button}:",
                size_hint_y=None,
                height=50,
                halign='right',
                valign='middle',
                size_hint_x=None,
                width=200  # Ajuste a largura do label
            )
            mouse_label.bind(size=mouse_label.setter('text_size'))
            mouse_layout.add_widget(mouse_label)

            # Menu seletor (Spinner)
            spinner = Spinner(
                text="Selecione...",
                values=gesture_options,
                size_hint=(None, None),  # Personaliza o tamanho
                size=(150, 40),  # Tamanho semelhante ao select do HTML
                background_color=(1, 1, 1, 1),  # Fundo branco
                color=(0, 0, 0, 1)  # Texto preto
            )
            spinner.bind(text=self.on_selection)
            mouse_layout.add_widget(spinner)
            self.spinners[mouse_button] = spinner

        layout.add_widget(mouse_layout)

        # Botão "Aplicar" para salvar as escolhas
        apply_button = Button(
            text="Aplicar",
            size_hint=(0.3, None),  # Define a largura como 30% da tela
            height=50,
            pos_hint={'center_x': 0.5, 'y': 0.05},  # Centraliza na parte inferior
            on_press=self.save_preferences
        )
        layout.add_widget(apply_button)

        # ScrollView para o conteúdo se a tela for pequena
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def on_selection(self, spinner, text):
        # Garantir que o gesto seja único
        for key, sp in self.spinners.items():
            if sp != spinner and sp.text == text:
                sp.text = "Selecione..."
        # Atualizar seleção atual
        for key, sp in self.spinners.items():
            if sp == spinner:
                self.selections[key] = text

    def save_preferences(self, instance):
        # Verificar se todas as opções foram selecionadas
        if None in self.selections.values():
            popup = Popup(title="Erro", content=Label(text="Por favor, selecione um gesto para cada função."),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            # Salvar as preferências usando os valores selecionados
            preferences = {
                'Botão Direito': dic[self.selections['Botão Direito']],  # Gesto selecionado para o botão direito
                'Botão Esquerdo': dic[self.selections['Botão Esquerdo']],  # Gesto correspondente ao botão esquerdo
                'Pressionar Botão Esquerdo': dic[self.selections['Pressionar Botão Esquerdo']]
                # Gesto correspondente ao pressionar
            }

            # Salvar as preferências em um arquivo JSON
            with open('user_preferences.json', 'w', encoding='utf-8') as json_file:
                json.dump(preferences, json_file, ensure_ascii=False, indent=4)

            # Cria um popup de sucesso
            self.popup = Popup(title="Sucesso", content=Label(text="Preferências salvas com sucesso!"),
                               size_hint=(None, None), size=(400, 200))
            self.popup.bind(on_dismiss=self.on_popup_dismiss)

            # Abre o popup
            self.popup.open()

            # Fecha o popup automaticamente após 3 segundos
            Clock.schedule_once(self.close_popup, 3)

    def close_popup(self, dt):
        self.popup.dismiss()  # Fecha o popup

    def on_popup_dismiss(self, instance):
        App.get_running_app().stop()


class SlideApp(App):
    def build(self):
        self.title = "ARCHEY Inc."
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(DescriptionScreen(name='description'))
        sm.add_widget(CustomizationScreen(name='customization'))

        return sm


if __name__ == '__main__':
    SlideApp().run()
