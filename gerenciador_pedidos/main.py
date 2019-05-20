from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.factory import Factory

import datetime
import sqlite3

BD_name = 'database.sqlite3'


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
        elif tela == "listar pedidos":
            self.ids.screen_manager.current = "listaPedidos_screen"
        elif tela == "clientes":
            self.ids.screen_manager.current = "clientes_screen"

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

        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE name = ?", (cliente,))
        id_cliente = cursor.fetchone()[0]
        conn.close()

        pedido = self.root.ids.pedidos_screen.ids.pedido.text
        data = self.root.ids.pedidos_screen.ids.data.text
        quantidade = self.root.ids.pedidos_screen.ids.quantidade.text
        obs = self.root.ids.pedidos_screen.ids.observacao.text

        conn = sqlite3.connect(BD_name, isolation_level=None)
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

    def gravarCliente(self):
        nome = self.root.ids.clientes_screen.ids.nome.text
        endereco = self.root.ids.clientes_screen.ids.endereco.text
        telefone = self.root.ids.clientes_screen.ids.telefone.text
        email = self.root.ids.clientes_screen.ids.email.text

        conn = sqlite3.connect(BD_name, isolation_level=None)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes "
                       "(name,endereco,telefone,email)"
                       "VALUES (?, ?, ?, ?)",
                       (nome, endereco, telefone, email)
                       )
        conn.commit()
        conn.close()

        # print(query)
        self.root.botaoVoltar()

    def getClientes(self):
        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM clientes")
        resultados = cursor.fetchall()
        lista_clientes = []
        for resultado in resultados:
            for nome in resultado:
                lista_clientes.append(nome)
        conn.close()
        return lista_clientes

    def getPedidos(self):
        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        cursor.execute("SELECT "
                       "clientes.name, pedidos.pedido, pedidos.quantidade,"
                       "pedidos.data_entrega, pedidos.observacoes "
                       "FROM pedidos "
                       "JOIN clientes ON clientes.id = pedidos.id_cliente")
        resultados = cursor.fetchall()

        cliente = []
        pedido = []
        qtd = []
        data = []
        obs = []
        for resultado in resultados:
                cliente.append(resultado[0])
                pedido.append(resultado[1])
                qtd.append(resultado[2])
                data.append(resultado[3])
                obs.append(resultado[4])
        conn.close()

        string = (f"[b]Cliente             Pedido         "
                  f"Qtd Data      Obs          [/b]\n\n")
        for i, v in enumerate(cliente):
            string += (f"{cliente[i]:20.18}{pedido[i]:15.13}"
                       f"{str(qtd[i]):4.2}{data[i]:10.8}{obs[i]}\n"
                       )
            print(i)

        return string


class MyWidget(FloatLayout):
    box = ObjectProperty(None)

    def on_box(self, *args):
        for i in range(5):
            self.box.add_widget(Button(text=str(i)))
            self.box.add_widget(Label(text=str(i + 1)))


Factory.register('MyWidget', cls=MyWidget)


if __name__ == '__main__':
    GerenciadorApp().run()
