from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from arithmetic import Arithmetic

import webbrowser
import random


#############################################################################
class KivyTutorRoot(BoxLayout):
    """Root of all Widgets"""

    math_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(KivyTutorRoot, self).__init__(**kwargs)
        # List of previous screens
        self.screen_list = []
        self.is_mix = False

    def changeScreen(self, next_screen):
        operations = ("addition subtraction division "
                      "multiplication division".split())
        question = None

        if self.ids.kivy_screen_manager.current not in self.screen_list:
            self.screen_list.append(self.ids.kivy_screen_manager.current)

        if next_screen == "about this app":
            self.ids.kivy_screen_manager.current = "about screen"
        else:
            if next_screen == "mix!":
                self.is_mix = True
                index = random.randint(0, len(operations - 1))
                next_screen = operations[index]
            else:
                self.is_mix = False
            for operation in operations:
                if next_screen == operation:
                    question = f"self.math_screen.get_{operation}_question"
            self.math_screen.question_text.text = KivyTutorRoot.prepQuestion(
                eval(question) if question is not None else None
            )
            self.ids.kivy_screen_manager.current = "math_screen"

    @staticmethod
    def prepQuestion(question):
        """Prepara uma quest~ao com markup"""
        if question is None:
            return "ERROR"
        text_list = question.split()
        text_list.insert(2, "[b]")
        text_list.insert(len(text_list), "[/b]")
        return " ".join(text_list)

    def onBackButton(self):
        # check if there are any screen to go back to
        if self.screen_list:
            # returns the last item of the list and remove it
            self.ids.kivy_screen_manager.current = self.screen_list.pop()
            # we don't close the app
            return True
        # no more screens to go back to, close app
        return False


#############################################################################
class MathScreen(Screen, Arithmetic):
    """Widget que contém a tela e as funções das perguntas matemáticas"""

    def __init__(self, *args, **kwargs):
        super(MathScreen, self).__init__(*args, **kwargs)


#############################################################################
class KivyTutorApp(App):
    """App object"""

    def __init__(self, **kwargs):
        super(KivyTutorApp, self).__init__(**kwargs)
        # chama a funcao onBackBtn sempre que qq tecla eh pressionada
        Window.bind(on_keyboard=self.onBackBtn)

    def onBackBtn(self, window, key, *args):
        """checa se tecla de voltar foi pressionada"""
        if key == 27:
            return self.root.onBackButton()

    def build(self):
        return KivyTutorRoot()

    def getText(self):
        return ("Hey there!\nThis App was built using [b][ref=kivy]kivy"
                "[/ref][/b]\nFeel free to look at the source code "
                "[b][ref=source]here[/ref][/b].\nThis app has the "
                "[b][ref=mit]MIT License[/ref][/b].\n")

    def on_ref_press(self, instace, ref):
        _dict = {
            "source": "https://github.com/amelco/kivy_test/mathtutor",
            "kivy": "http://kivy.org/#home",
            "mit": "https://opensource.org/licenses/MIT"
        }

        webbrowser.open(_dict[ref])


if __name__ == '__main__':
    KivyTutorApp().run()
