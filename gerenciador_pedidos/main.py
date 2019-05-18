from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window


############################################################################
class GerenciadorRoot(BoxLayout):
    """Root de todos os Widgets"""

    def __init__(self, **kwargs):
        super(GerenciadorRoot, self).__init__(**kwargs)
        self.lista_telas = []

    def changeScreen(self, tela):
        if self.ids.screen_manager.current not in self.lista_telas:
            self.lista_telas.append(self.ids.screen_manager.current)

        if tela == "anotar pedido":
            self.ids.screen_manager.current = "pedidos_screen"

    def botaoVoltar(self):
        if self.lista_telas:
            self.ids.screen_manager.current = self.lista_telas.pop()
            return True
        return False


############################################################################
class GerenciadorApp(App):
    """Objeto App"""

    def __init__(self, **kwargs):
        super(GerenciadorApp, self).__init__(**kwargs)
        # chama a funcao checaTecla sempre que uma tecla eh pressionada
        Window.bind(on_keyboard=self.checaTecla)

    def build(self):
        return GerenciadorRoot()

    def checaTecla(self, window, key, *args):
        if key == 27:
            return self.root.botaoVoltar()


if __name__ == '__main__':
    GerenciadorApp().run()
