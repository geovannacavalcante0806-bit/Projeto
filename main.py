import sqlite3
import os

#VERIFICA SE O BANCO EXISTE, SE NÃO EXISTIR ELE CRIA O BANCO E AS TABELAS
if not os.path.exists("banco.db"):
    print("Banco de dados não encontrado. Criando...")
else:
    print("Banco já existe.")


#CONECTA AO BANCO DE DADOS E CRIA AS TABELAS SE ELAS NÃO EXISTIREM  
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

#TABELA PRODUTOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_do_produto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    unidade TEXT NOT NULL,
    preco_unitario REAL NOT NULL,
    preco_total REAL NOT NULL,
    estoque_minimo INTEGER NOT NULL,
    especificacoes TEXT
)
""")

#TABELA MOVIMENTAÇÕES
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    motivo TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    data TEXT NOT NULL,
    FOREIGN KEY(produto_id) REFERENCES produtos(codigo)
)
""")

conexao.commit()
conexao.close()

print("Banco criado com sucesso!")

def cadastrar_produto():
    print("CADASTRO DE PRODUTO")
    
    nome = input("Nome do produto: ")
    categoria = input("Categoria: ")
    quantidade = int(input("Quantidade inicial: "))
    unidade = input("Unidade: ")
    preco_unitario = float(input("Preço unitário: "))
    estoque_minimo = int(input("Estoque mínimo: "))
    especificacoes = input("Especificações técnicas: ")
    
    preco_total = quantidade * preco_unitario
    
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    
    cursor.execute("""
    INSERT INTO produtos
    (nome_do_produto, categoria, quantidade, unidade, preco_unitario, preco_total, estoque_minimo, especificacoes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, categoria, quantidade, unidade, preco_unitario, preco_total, estoque_minimo, especificacoes))
    
    conexao.commit()
    conexao.close()
    
    print("Produto cadastrado com sucesso!")
    
def listar_produtos():
    print(" ESTOQUE ATUAL DOS PRODUTOS")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT codigo, nome_do_produto, categoria, quantidade, unidade, preco_unitario, preco_total, estoque_minimo
    FROM produtos
    """)

    produtos = cursor.fetchall()

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
    else:
        for produto in produtos:
            print("Código:", produto[0])
            print("Nome:", produto[1])
            print("Categoria:", produto[2])
            print("Quantidade:", produto[3], produto[4])
            print("Preço unitário: R$", produto[5])
            print("Preço total: R$", produto[6])

            if produto[3] <= produto[7]:
                print("ALERTA: estoque baixo! Precisa atualizar o estoque.")

    conexao.close()

def registrar_movimentacao():

    print("MOVIMENTAÇÃO DE ESTOQUE")
    codigo = int(input("Código do produto: "))
    tipo = input("Tipo (entrada ou saida): ")
    motivo = input("Motivo: ")
    quantidade = int(input("Quantidade movimentada: "))
    data = input("Data da movimentação: ")
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT quantidade
    FROM produtos
    WHERE codigo = ?
    """, (codigo,))

    produto = cursor.fetchone()

    if produto == None:
        print("Produto não encontrado.")
        conexao.close()
        return

    quantidade_atual = produto[0]

    if tipo == "entrada":
        nova_quantidade = quantidade_atual + quantidade
    elif tipo == "saida":

        if quantidade > quantidade_atual:
            print("Estoque insuficiente.")
            conexao.close()
            return

        nova_quantidade = quantidade_atual - quantidade

    else:
        print("Tipo inválido.")
        conexao.close()
        return

    cursor.execute("""
    UPDATE produtos
    SET quantidade = ?
    WHERE codigo = ?
    """, (nova_quantidade, codigo))

    cursor.execute("""
    INSERT INTO movimentacoes
    (
        produto_id,
        tipo,
        motivo,
        quantidade,
        data
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        codigo,
        tipo,
        motivo,
        quantidade,
        data
    ))

    conexao.commit()

    conexao.close()

    print("Movimentação registrada com sucesso!")

def mostrar_movimentacoes():

    print("HISTÓRICO DE MOVIMENTAÇÕES ")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT
    produto_id,
    tipo,
    motivo,
    quantidade,
    data
    FROM movimentacoes
    """)

    movimentacoes = cursor.fetchall()

    if movimentacoes == []:
        print("Nenhuma movimentação cadastrada.")
    else:
        for movimentacao in movimentacoes:

            print("Produto:", movimentacao[0])
            print("Tipo:", movimentacao[1])
            print("Motivo:", movimentacao[2])
            print("Quantidade:", movimentacao[3])
            print("Data:", movimentacao[4])

def relatorio_gerencial():

    print("RELATÓRIO GERENCIAL")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT quantidade, preco_unitario, estoque_minimo
    FROM produtos
    """)

    produtos = cursor.fetchall()

    total_itens = 0
    valor_total = 0
    estoque_baixo = 0

    for produto in produtos:
        quantidade = produto[0]
        preco_unitario = produto[1]
        estoque_minimo = produto[2]

        total_itens = total_itens + quantidade
        valor_total = valor_total + (quantidade * preco_unitario)

        if quantidade <= estoque_minimo:
            estoque_baixo = estoque_baixo + 1

    print("Total de itens:", total_itens)
    print("Valor total do estoque: R$", valor_total)
    print("Produtos com estoque baixo:", estoque_baixo)

    conexao.close()


def menu():

    while True:
        print("SISTEMA DE GERENCIAMENTO DE ESTOQUE ===")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Registrar movimentação de estoque")
        print("4. Mostrar histórico de movimentações")
        print("5. Alertas inteligentes")
        print("6. Relatório gerencial")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            registrar_movimentacao()
        elif opcao == "4":
            mostrar_movimentacoes()
        elif opcao == "5":
            alertas_inteligentes()
        elif opcao == "6":
            relatorio_gerencial()
        elif opcao == "7":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")


menu()