from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import datetime
import sqlite3
from plyer import email

# import pdb  # for debugging only

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
        elif tela == "cardápio":
            self.ids.screen_manager.current = "cardapio_screen"

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

    def gravarProduto(self):
        produto = self.root.ids.cardapio_screen.ids.produto.text

        # Resetando os text inputs
        self.root.ids.cardapio_screen.ids.produto.text = ""

        conn = sqlite3.connect(BD_name, isolation_level=None)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos "
                       "(nome) "
                       "VALUES (?)",
                       (produto,)
                       )
        conn.commit()
        conn.close()

        self.root.botaoVoltar()

    def gravarPedido(self):
        cliente = self.root.ids.pedidos_screen.ids.cliente.text
        pedido = self.root.ids.pedidos_screen.ids.pedido.text

        # Popup
        conteudo = BoxLayout(orientation='vertical')
        conteudo.add_widget(Label(text='Campos "Cliente" e "Pedido" devem '
                                       'ser preechidos',
                                  ))
        closeBtn = Button(text='Fechar')
        conteudo.add_widget(closeBtn)

        if (cliente == "---" or pedido == "---"):
            popup = Popup(title='Atenção',
                          content=conteudo,
                          size_hint=(None, None),
                          size=(400, 220))
            popup.open()
            closeBtn.bind(on_press=popup.dismiss)
            return

        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE name = ?", (cliente,))
        id_cliente = cursor.fetchone()[0]
        conn.close()
        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM produtos WHERE nome = ?", (pedido,))
        id_pedido = cursor.fetchone()[0]
        conn.close()

        data = self.root.ids.pedidos_screen.ids.data.text
        quantidade = self.root.ids.pedidos_screen.ids.quantidade.text
        obs = self.root.ids.pedidos_screen.ids.observacao.text

        # Resetando os text inputs
        self.root.ids.pedidos_screen.ids.cliente.text = "---"
        self.root.ids.pedidos_screen.ids.pedido.text = "---"
        self.root.ids.pedidos_screen.ids.data.text = self.getDate()
        self.root.ids.pedidos_screen.ids.quantidade.text = "1"
        self.root.ids.pedidos_screen.ids.observacao.text = ""

        conn = sqlite3.connect(BD_name, isolation_level=None)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos "
                       "(id_cliente,id_pedido,data_entrega,"
                       "quantidade,observacoes) "
                       "VALUES (?, ?, ?, ?, ?)",
                       (id_cliente, id_pedido, data, quantidade, obs)
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

        # Resetando os text inputs
        self.root.ids.clientes_screen.ids.nome.text = ""
        self.root.ids.clientes_screen.ids.endereco.text = ""
        self.root.ids.clientes_screen.ids.telefone.text = ""
        self.root.ids.clientes_screen.ids.email.text = ""

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

    def getProdutos(self):
        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM produtos")
        resultados = cursor.fetchall()
        lista_produtos = []
        for resultado in resultados:
            for nome in resultado:
                lista_produtos.append(nome)
        conn.close()
        return lista_produtos

    def getPedidos(self):
        conn = sqlite3.connect(BD_name)
        cursor = conn.cursor()
        query = ("SELECT "
                 "clientes.name, produtos.nome, pedidos.quantidade,"
                 "pedidos.data_entrega, pedidos.observacoes "
                 "FROM pedidos "
                 "JOIN clientes ON clientes.id = pedidos.id_cliente "
                 "JOIN produtos ON pedidos.id_pedido = produtos.id")
        cursor.execute(query)
        resultados = cursor.fetchall()

        cliente = []
        produto = []
        qtd = []
        data = []
        obs = []
        for resultado in resultados:
                cliente.append(resultado[0])
                produto.append(resultado[1])
                qtd.append(resultado[2])
                data.append(resultado[3])
                obs.append(resultado[4])
        conn.close()

        string = (f"[b]Cliente             Pedido                "
                  f"Qtd Data        Obs          [/b]\n\n")
        for i, v in enumerate(cliente):
            string += (f"{cliente[i]:20.18}{produto[i]:22.20}"
                       f"{str(qtd[i]):4.2}{data[i]:12.10}{obs[i]}\n"
                       )
        return string

    def exportDB(self):
        con = sqlite3.connect('database.sqlite3')
        dump = ""
        for line in con.iterdump():
            dump += line + "\n"
        print(dump)
        email.send(recipient="amelco.herman@gmail.com",
                   subject="GerenciadorPedidosAPP_BD_dump",
                   text=dump)


if __name__ == '__main__':
    GerenciadorApp().run()
