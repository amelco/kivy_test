from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

import datetime
import sqlite3


############################################################################
class GerenciadorRoot(BoxLayout):
    """Root de todos os Widgets"""

    lista_telas = []

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

    # pedidos_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GerenciadorApp, self).__init__(**kwargs)
        # chama a funcao checaTecla sempre que uma tecla eh pressionada
        Window.bind(on_keyboard=self.checaTecla)
        self.lista_cardapio = "Tradicional, Ameixa, Bolo de Maçã".split(',')

    def build(self):
        return GerenciadorRoot()

    def checaTecla(self, window, key, *args):
        if key == 27:
            return self.root.botaoVoltar()

    def getDate(self):
        now = datetime.datetime.now()
        return f'{now.day}/{now.month}/{now.year}'

    def gravarPedido(self):
        cliente = self.root.ids.pedidos_screen.ids.cliente.text

        conn = sqlite3.connect('data/database.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE name = ?", (cliente,))
        id_cliente = cursor.fetchone()[0]
        conn.close()

        pedido = self.root.ids.pedidos_screen.ids.pedido.text
        data = self.root.ids.pedidos_screen.ids.data.text
        quantidade = self.root.ids.pedidos_screen.ids.quantidade.text
        obs = self.root.ids.pedidos_screen.ids.observacao.text

        conn = sqlite3.connect('data/database.sqlite3')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos "
                       "(id_cliente,pedido,data_entrega,"
                       "quantidade,observacoes) "
                       "VALUES (?, ?, ?, ?, ?)",
                       (id_cliente, pedido, data, quantidade, obs)
                       )
        conn.commit()
        conn.close()

        # print(query)
        self.root.botaoVoltar()

    def getClientes(self):
        conn = sqlite3.connect('data/database.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM clientes")
        resultados = cursor.fetchall()
        lista_clientes = []
        for resultado in resultados:
            for nome in resultado:
                lista_clientes.append(nome)
        conn.close()
        return lista_clientes


if __name__ == '__main__':
    GerenciadorApp().run()
