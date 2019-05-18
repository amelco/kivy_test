from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

import datetime


############################################################################
class GerenciadorRoot(BoxLayout):
    """Root de todos os Widgets"""

    def __init__(self, **kwargs):
        super(GerenciadorRoot, self).__init__(**kwargs)
        self.lista_telas = []

    def getClientes(self):
        print(self.lista_clientes)
        return self.lista_clientes

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
        self.lista_clientes = "Ana Maria, Josélia, Fernanda, Carlos".split(',')
        self.lista_cardapio = "Tradicional, Ameixa, Bolo de Maçã".split(',')

    def build(self):
        gerenciador = GerenciadorRoot()
        return gerenciador

    def checaTecla(self, window, key, *args):
        if key == 27:
            return self.root.botaoVoltar()

    def getDate(self):
        now = datetime.datetime.now()
        return f'{now.day}/{now.month}/{now.year}'

    def gravarPedido(self):
        print("TODO: Gravar pedido!")
        self.root.botaoVoltar()


if __name__ == '__main__':
    GerenciadorApp().run()
