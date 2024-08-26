import sqlite3

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

# Chame a função para criar o banco de dados e a tabela
create_db()
