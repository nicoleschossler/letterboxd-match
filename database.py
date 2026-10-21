
# Importa o SQLite, banco de dados que já vem com o Python.
import sqlite3


# Define o nome do arquivo que armazenará nosso banco de dados.
DATABASE = "letterboxd.db"


def conectar():
    # Abre uma conexão com o banco.
    # Se o arquivo não existir, o SQLite o cria automaticamente.
    conexao = sqlite3.connect(DATABASE)

    # Permite acessar as colunas pelo nome, além do índice.
    conexao.row_factory = sqlite3.Row

    # Devolve a conexão para o restante do programa.
    return conexao


def criar_tabelas():
    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Cria as tabelas caso elas ainda não existam.
        with conexao:

            # Guarda os usuários importados do Letterboxd.
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE
                )
            """)

            # Guarda cada filme uma única vez no catálogo.
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS films (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    year INTEGER
                )
            """)

            # Relaciona cada usuário aos filmes que avaliou.
            # A combinação usuário + filme não pode se repetir.
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS ratings (
                    user_id INTEGER NOT NULL,
                    film_id INTEGER NOT NULL,
                    rating REAL NOT NULL,
                    PRIMARY KEY (user_id, film_id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (film_id) REFERENCES films(id)
                )
            """)

            # Guarda os resultados de compatibilidade calculados.
            # Cada resultado recebe um token único para o link compartilhável.
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user1_id INTEGER NOT NULL,
                    user2_id INTEGER NOT NULL,
                    score REAL NOT NULL,
                    token TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user1_id) REFERENCES users(id),
                    FOREIGN KEY (user2_id) REFERENCES users(id),
                    CHECK (user1_id != user2_id)
                )
            """)

    finally:
        # Fecha a conexão mesmo se ocorrer algum erro.
        conexao.close()


# Permite testar este arquivo executando-o diretamente.
if __name__ == "__main__":
    # Cria as tabelas que ainda não existem.
    criar_tabelas()

    # Informa que a operação terminou.
    print("Banco de dados e tabelas criados com sucesso!")
