import flet as ft
import sqlite3
from flet import ElevatedButton, Page, TextField, Text, Column

def create_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gestao_clientes (
            cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            documento TEXT NOT NULL UNIQUE,
            nr_telefone TEXT NOT NULL UNIQUE,
            tipo_usuario TEXT NOT NULL,
            instituicao TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            cep TEXT NOT NULL,
            logradouro TEXT NOT NULL,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            nr_imovel TEXT NOT NULL,
            observacao TEXT NOT NULL,
            erro_cep TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Global variable to keep track of the current record index
current_index = 0
clients = []


def load_clients():
    global clients
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gestao_clientes')
    clients = cursor.fetchall()
    conn.close()


def show_client(page, index):
    if index < 0 or index >= len(clients):
        page.add(ft.Text("Índice fora dos limites da lista."))
        page.update()
        return

    client = clients[index]
    nome_input.value = client[1]
    email_input.value = client[2]
    documento_input.value = client[3]
    nr_telefone_input.value = client[4]
    tipo_usuario_input.value = client[5]
    instituicao_input.value = client[6]
    cpf_input.value = client[7]
    cep_input.value = client[8]
    logradouro_input.value = client[9]
    bairro_input.value = client[10]
    cidade_input.value = client[11]
    estado_input.value = client[12]
    nr_imovel_input.value = client[13]
    observacao_input.value = client[14]
    erro_cep_input.value = client[15]

    page.update()

# Define um único elemento de texto global
message_text = ft.Text("", size=16)

def print_controls(page):
    for control in page.controls:
        print(f"Control: {type(control)}, Value: {getattr(control, 'value', 'N/A')}")

def add_client(page, nome, email, documento, nr_telefone, tipo_usuario, instituicao, cpf, cep, logradouro, bairro,
               cidade, estado, nr_imovel, observacao, erro_cep):
    try:
        clear_fields()  # Limpar os campos antes de adicionar um novo registro

        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Verificar se o CPF já existe
        cursor.execute("SELECT cpf FROM gestao_clientes WHERE cpf = ?", (cpf,))
        if cursor.fetchone() is not None:
            update_message(page, "Erro: CPF já cadastrado no sistema.")
            return

        # Verificar se o telefone já existe
        cursor.execute("SELECT nr_telefone FROM gestao_clientes WHERE nr_telefone = ?", (nr_telefone,))
        if cursor.fetchone() is not None:
            update_message(page, "Erro: Telefone já cadastrado no sistema.")
            return

        # Inserir novo cliente
        cursor.execute('''
            INSERT INTO gestao_clientes (nome, email, documento, nr_telefone, tipo_usuario, instituicao, cpf, cep, logradouro, bairro, cidade, estado, nr_imovel, observacao, erro_cep)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nome, email, documento, nr_telefone, tipo_usuario, instituicao, cpf, cep, logradouro, bairro, cidade,
            estado, nr_imovel, observacao, erro_cep))

        conn.commit()

        # Mostrar mensagem de sucesso
        update_message(page, "Registro adicionado com sucesso.")
    except sqlite3.IntegrityError as e:
        update_message(page, "Erro: Telefone já cadastrado no sistema.")
    except Exception as e:
        update_message(page, f"Erro inesperado: {e}")
        conn.close()

def delete_client(page, client_id):
    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Excluir cliente pelo ID
        cursor.execute("DELETE FROM gestao_clientes WHERE id = ?", (client_id,))
        conn.commit()

        # Verificar se o cliente foi realmente excluído
        if cursor.rowcount > 0:
            update_message(page, "Registro excluído com sucesso!")
        else:
            update_message(page, "Nenhum registro encontrado para exclusão.")

        load_clients()  # Recarregar os clientes após excluir

    except sqlite3.Error as e:
        update_message(page, f"Erro ao excluir cliente: {e}")
    finally:
        conn.close()

def update_message(page, message):
    # Remove controles de mensagem existentes
    page.controls = [control for control in page.controls if not (isinstance(control, ft.Text) and 'Mensagem:' in control.value)]

    # Adiciona um novo controle de mensagem
    message_control = ft.Text(f"Mensagem: {message}", size=20)
    page.controls.append(message_control)

    # Atualiza a página para refletir as mudanças
    page.update()


def search_client(page, documento):
    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        # Usar LIKE para buscar parcialmente
        cursor.execute('SELECT * FROM gestao_clientes WHERE documento LIKE ? OR nome LIKE ?',
                       ('%' + documento + '%', '%' + documento + '%'))
        client = cursor.fetchall()
        conn.close()
        if client:
            clients[:] = client  # Atualizar a lista global de clientes com o resultado da busca
            if clients:
                show_client(page, 0)  # Mostrar o primeiro cliente encontrado
            page.add(ft.Text("Clientes encontrados."))
        else:
            page.add(ft.Text("Nenhum cliente encontrado."))
    except Exception as e:
        page.add(ft.Text(f"Erro ao localizar cliente: {e}"))
    page.update()

# Armazene o controle de resultados globalmente
results_column = None

def display_results(page, results):
    print("Displaying results...")
    for control in page.controls:
        print(f"Control type: {type(control)}")
        if isinstance(control, ft.Text):
            print(f"Control value: {control.value}")

    # Remove resultados anteriores
    page.controls = [control for control in page.controls if not isinstance(control, ft.Column)]

    # Adiciona novos resultados
    for index, result in enumerate(results):
        result_control = ft.Column(
            controls=[
                ft.Text(f"Nome: {result['name']}"),
                ft.Text(f"Telefone: {result['phone']}"),
                # Adicione outros campos conforme necessário
            ],
            id=f"result_{index}"
        )
        page.controls.append(result_control)

    # Atualiza a página para refletir as mudanças
    page.update()


def clear_fields():
    nome_input.value = ""
    email_input.value = ""
    documento_input.value = ""
    nr_telefone_input.value = ""
    tipo_usuario_input.value = ""
    instituicao_input.value = ""
    cpf_input.value = ""
    cep_input.value = ""
    logradouro_input.value = ""
    bairro_input.value = ""
    cidade_input.value = ""
    estado_input.value = ""
    nr_imovel_input.value = ""
    observacao_input.value = ""
    erro_cep_input.value = ""


def main(page: ft.Page):
    create_db()
    load_clients()

    global nome_input, email_input, documento_input, nr_telefone_input, tipo_usuario_input, instituicao_input, cpf_input
    global cep_input, logradouro_input, bairro_input, cidade_input, estado_input, nr_imovel_input, observacao_input, erro_cep_input

    nome_input = ft.TextField(label="Nome")
    email_input = ft.TextField(label="Email")
    documento_input = ft.TextField(label="Documento")
    nr_telefone_input = ft.TextField(label="Número de Telefone")
    tipo_usuario_input = ft.TextField(label="Tipo de Usuário")
    instituicao_input = ft.TextField(label="Instituição")
    cpf_input = ft.TextField(label="CPF")
    cep_input = ft.TextField(label="CEP")
    logradouro_input = ft.TextField(label="Logradouro")
    bairro_input = ft.TextField(label="Bairro")
    cidade_input = ft.TextField(label="Cidade")
    estado_input = ft.TextField(label="Estado")
    nr_imovel_input = ft.TextField(label="Número do Imóvel")
    observacao_input = ft.TextField(label="Observação")
    erro_cep_input = ft.TextField(label="Erro do CEP")

    search_input = ft.TextField(label="Documento para Localizar")
    # Exemplo do botão ou elemento que chama a função de busca
    search_button = ft.ElevatedButton(
        text="Buscar",
        on_click=lambda e: search_client(page, search_input.value)
    )

    add_button = ft.ElevatedButton(
        text="Adicionar Cliente",
        on_click=lambda e: add_client(
            page,
            nome_input.value,
            email_input.value,
            documento_input.value,
            nr_telefone_input.value,
            tipo_usuario_input.value,
            instituicao_input.value,
            cpf_input.value,
            cep_input.value,
            logradouro_input.value,
            bairro_input.value,
            cidade_input.value,
            estado_input.value,
            nr_imovel_input.value,
            observacao_input.value,
            erro_cep_input.value
        )
    )

    delete_button = ft.ElevatedButton(
        text="Excluir Cliente",
        on_click=lambda e: delete_client(page, documento_input.value)
    )

    update_button = ft.ElevatedButton(
        text="Alterar Cliente",
        on_click=lambda e: update_client(
            page,
            documento_input.value,
            nome_input.value,
            email_input.value,
            nr_telefone_input.value,
            tipo_usuario_input.value,
            instituicao_input.value,
            cpf_input.value,
            cep_input.value,
            logradouro_input.value,
            bairro_input.value,
            cidade_input.value,
            estado_input.value,
            nr_imovel_input.value,
            observacao_input.value,
            erro_cep_input.value
        )
    )

    def go_next(e):
        global current_index
        if clients and current_index < len(clients) - 1:
            current_index += 1
            show_client(page, current_index)
        elif not clients:
            page.add(ft.Text("Nenhum cliente disponível."))
            page.update()

    def go_prev(e):
        global current_index
        if clients and current_index > 0:
            current_index -= 1
            show_client(page, current_index)
        elif not clients:
            page.add(ft.Text("Nenhum cliente disponível."))
            page.update()

    next_button = ft.ElevatedButton(text="Avançar Registro", on_click=go_next)
    prev_button = ft.ElevatedButton(text="Retornar Registro", on_click=go_prev)
    exit_button = ft.ElevatedButton(
        text="Sair",
        on_click=lambda e: page.window.close()
    )

    button_row_1 = ft.Row(
        [search_button, add_button, delete_button, update_button],
        alignment="center",
        spacing=5
    )
    button_row_2 = ft.Row(
        [prev_button, next_button, exit_button],
        alignment="center",
        spacing=5
    )

    # Centraliza os campos e botões na tela
    page.add(
        ft.Column(
            [
                ft.Row([nome_input, email_input], alignment="center"),
                ft.Row([documento_input, nr_telefone_input], alignment="center"),
                ft.Row([tipo_usuario_input, instituicao_input], alignment="center"),
                ft.Row([cpf_input, cep_input], alignment="center"),
                ft.Row([logradouro_input, bairro_input], alignment="center"),
                ft.Row([cidade_input, estado_input], alignment="center"),
                ft.Row([nr_imovel_input, observacao_input], alignment="center"),
                ft.Row([erro_cep_input, search_input], alignment="center"),
                button_row_1,
                button_row_2
            ],
            horizontal_alignment="center",
            alignment="center"
        )
    )

    page.update()

ft.app(target=main)
