from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import webbrowser


class KivyTutorRoot(BoxLayout):
    """Root of all Widgets"""

    def __init__(self, **kwargs):
        super(KivyTutorRoot, self).__init__(**kwargs)

    def changeScreen(self, next_screen):
        operations = ("addition subtraction division "
                     "multiplication division".split())
        question = None

        if next_screen == "about this app":
            self.ids.kivy_screen_manager.current = "about screen"


class KivyTutorApp(App):
    """App object"""

    def __init__(self, **kwargs):
        super(KivyTutorApp, self).__init__(**kwargs)

    def build(self):
        return KivyTutorRoot()

    def getText(self):
        return ("Hey there!\nThis App was built using [b][ref=kivy]kivy"
                "[/ref][/b]\nFeel free to look at the source code "
                "[b][ref=source]here[/ref][/b].\nThis app is under the "
                "[b][ref=mit]MIT License[/ref][/b].\n")

    def on_ref_press(self, instace, ref):
        _dict = {
            "source": "https://github.com/amelco/kivy_test",
            "kivy": "http://kivy.org/#home",
            "mit": "https://opensource.org/licenses/MIT"
        }

        webbrowser.open(_dict[ref])


if __name__ == '__main__':
    KivyTutorApp().run()
