# funcoes de manipulaçãode dados no BD
import sqlite3

BD_name = 'database.sqlite3'

def select_one(query, campos):
        """
            Retorna lista com os resultados da query. Se houver WHERE, campos
            é um tuple com os campos
        """
        conn = sqlite3.connect(BD_name, isolation_level=None)

        cursor = conn.cursor()
        cursor.execute(query, campos)
        res = cursor.fetchone()[0]
        conn.close()
        return res

def select_many(query):
    """
        Retorna lista contendo os resultados da query
    """
    conn = sqlite3.connect(BD_name)
    cursor = conn.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    lista = []
    for resultado in resultados:
        for nome in resultado:
            lista.append(nome)
    conn.close()
    return lista

def insert(query, campos):
    """
        Insere dados no BD.
        Retorna True ou False, caso haja sucesso ou nao.
        """
    try:
        conn = sqlite3.connect(BD_name, isolation_level=None)
        cursor = conn.cursor()
        cursor.execute(query, campos)
        conn.commit()
        conn.close()
        return True
    except:
        return False
