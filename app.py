
# Importa ferramentas para ler arquivos CSV.
import csv
import io

# Importa recursos do Flask para criar a API e responder em JSON.
from flask import Flask, jsonify, request, render_template

# Importa as funções que criam e acessam o banco de dados.
from database import conectar, criar_tabelas

# Cria a aplicação Flask.
app = Flask(__name__)

# Garante que as tabelas existam antes de atender às requisições.
criar_tabelas()


# Define a rota inicial para verificar se a API está funcionando.
# Exibe a página inicial do Letterboxd Match.
@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")

# Define a rota que lista os usuários cadastrados.
@app.route("/users", methods=["GET"])
def listar_usuarios():
    # Abre uma conexão com o banco.
    conexao = conectar()

    try:
        # Consulta os usuários em ordem de cadastro.
        usuarios = conexao.execute(
            "SELECT id, username FROM users ORDER BY id"
        ).fetchall()

        # Converte as linhas do banco em uma lista de dicionários.
        resultado = [
            {"id": usuario["id"], "username": usuario["username"]}
            for usuario in usuarios
        ]

        # Devolve a lista como JSON.
        return jsonify(resultado)

    finally:
        # Fecha a conexão mesmo se ocorrer algum erro.
        conexao.close()


# Define a rota para cadastrar um usuário.
@app.route("/users", methods=["POST"])
def cadastrar_usuario():
    # Lê o corpo da requisição, esperando que seja JSON.
    dados = request.get_json(silent=True)

    # Verifica se o corpo recebido é um objeto JSON.
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um objeto JSON."}), 400

    # Lê o username e remove espaços extras nas pontas.
    username = dados.get("username", "")
    if not isinstance(username, str):
        return jsonify({"erro": "O username deve ser um texto."}), 400

    username = username.strip()

    # Impede o cadastro de usernames vazios.
    if not username:
        return jsonify({"erro": "O username é obrigatório."}), 400

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Insere o usuário com parâmetros para evitar SQL injection.
        cursor = conexao.execute(
            "INSERT INTO users (username) VALUES (?)",
            (username,)
        )

        # Confirma a gravação no banco.
        conexao.commit()

        # Devolve o usuário criado com status HTTP 201.
        return jsonify({
            "id": cursor.lastrowid,
            "username": username
        }), 201

    except Exception as erro:
        # Trata a violação da restrição UNIQUE do username.
        if "UNIQUE constraint failed" in str(erro):
            return jsonify({"erro": "Esse usuário já está cadastrado."}), 409

        # Devolve um erro genérico para outras falhas no banco.
        app.logger.exception("Erro ao cadastrar usuário.")
        return jsonify({"erro": "Não foi possível cadastrar o usuário."}), 500

    finally:
        # Fecha a conexão após a operação.
        conexao.close()


# Define a rota para listar os filmes cadastrados.
@app.route("/films", methods=["GET"])
def listar_filmes():
    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Busca os filmes em ordem alfabética pelo título.
        filmes = conexao.execute(
            "SELECT id, title, year FROM films ORDER BY title"
        ).fetchall()

        # Converte cada linha do banco em um dicionário.
        resultado = [
            {
                "id": filme["id"],
                "title": filme["title"],
                "year": filme["year"]
            }
            for filme in filmes
        ]

        # Retorna a lista de filmes no formato JSON.
        return jsonify(resultado)

    finally:
        # Fecha a conexão mesmo se ocorrer algum erro.
        conexao.close()


# Define a rota para cadastrar um filme.
@app.route("/films", methods=["POST"])
def cadastrar_filme():
    # Lê os dados JSON enviados na requisição.
    dados = request.get_json(silent=True)

    # Confere se recebemos um objeto JSON.
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um objeto JSON."}), 400

    # Obtém o título e verifica se ele é um texto.
    titulo = dados.get("title", "")
    if not isinstance(titulo, str):
        return jsonify({"erro": "O título deve ser um texto."}), 400

    # Remove espaços extras do título.
    titulo = titulo.strip()

    # Impede o cadastro de títulos vazios.
    if not titulo:
        return jsonify({"erro": "O título é obrigatório."}), 400

    # Obtém o ano, que pode ser informado ou deixado vazio.
    ano = dados.get("year")

    # Valida o ano caso ele tenha sido informado.
    if ano is not None:
        # Impede valores que não sejam números inteiros.
        if isinstance(ano, bool) or not isinstance(ano, int):
            return jsonify({"erro": "O ano deve ser um número inteiro."}), 400

        # Impede anos fora de uma faixa plausível.
        if ano < 1888 or ano > 2100:
            return jsonify({"erro": "Informe um ano entre 1888 e 2100."}), 400

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Insere o filme usando parâmetros para evitar SQL injection.
        cursor = conexao.execute(
            "INSERT INTO films (title, year) VALUES (?, ?)",
            (titulo, ano)
        )

        # Confirma a gravação no banco.
        conexao.commit()

        # Retorna os dados do filme criado.
        return jsonify({
            "id": cursor.lastrowid,
            "title": titulo,
            "year": ano
        }), 201

    finally:
        # Fecha a conexão após a operação.
        conexao.close()



# Define a rota para listar as avaliações cadastradas.
@app.route("/ratings", methods=["GET"])
def listar_avaliacoes():
    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Busca as avaliações junto aos nomes dos usuários e filmes.
        avaliacoes = conexao.execute("""
            SELECT
                users.username,
                films.title,
                films.year,
                ratings.rating
            FROM ratings
            JOIN users ON ratings.user_id = users.id
            JOIN films ON ratings.film_id = films.id
            ORDER BY users.username, films.title
        """).fetchall()

        # Converte os resultados em uma lista de dicionários.
        resultado = [
            {
                "username": avaliacao["username"],
                "title": avaliacao["title"],
                "year": avaliacao["year"],
                "rating": avaliacao["rating"]
            }
            for avaliacao in avaliacoes
        ]

        # Devolve as avaliações no formato JSON.
        return jsonify(resultado)

    finally:
        # Fecha a conexão com o banco.
        conexao.close()


# Define a rota para registrar uma avaliação.
@app.route("/ratings", methods=["POST"])
def cadastrar_avaliacao():
    # Lê os dados enviados no formato JSON.
    dados = request.get_json(silent=True)

    # Verifica se recebemos um objeto JSON.
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um objeto JSON."}), 400

    # Obtém o nome do usuário e valida seu tipo.
    username = dados.get("username", "")
    if not isinstance(username, str) or not username.strip():
        return jsonify({"erro": "Informe um username válido."}), 400

    # Remove espaços extras do username.
    username = username.strip()

    # Obtém o ID do filme e verifica seu tipo.
    film_id = dados.get("film_id")
    if isinstance(film_id, bool) or not isinstance(film_id, int):
        return jsonify({"erro": "O ID do filme deve ser um número inteiro."}), 400

    # Obtém a nota e aceita números inteiros ou decimais.
    nota = dados.get("rating")
    if isinstance(nota, bool) or not isinstance(nota, (int, float)):
        return jsonify({"erro": "A nota deve ser um número."}), 400

    # Verifica se a nota está na escala de 0,5 a 5.
    if not 0.5 <= nota <= 5:
        return jsonify({"erro": "A nota deve estar entre 0,5 e 5."}), 400

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Procura o usuário pelo username.
        usuario = conexao.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        # Impede avaliações de usuários inexistentes.
        if usuario is None:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        # Procura o filme pelo ID.
        filme = conexao.execute(
            "SELECT id FROM films WHERE id = ?",
            (film_id,)
        ).fetchone()

        # Impede avaliações de filmes inexistentes.
        if filme is None:
            return jsonify({"erro": "Filme não encontrado."}), 404

        # Insere a avaliação associando usuário, filme e nota.
        conexao.execute(
            "INSERT INTO ratings (user_id, film_id, rating) VALUES (?, ?, ?)",
            (usuario["id"], film_id, nota)
        )

        # Confirma a gravação no banco.
        conexao.commit()

        # Devolve os dados da avaliação criada.
        return jsonify({
            "username": username,
            "film_id": film_id,
            "rating": nota
        }), 201

    except Exception as erro:
        # Trata a tentativa de avaliar duas vezes o mesmo filme.
        if "UNIQUE constraint failed" in str(erro):
            return jsonify({
                "erro": "Esse usuário já avaliou esse filme."
            }), 409

        # Registra outros erros para facilitar a investigação.
        app.logger.exception("Erro ao cadastrar avaliação.")
        return jsonify({"erro": "Não foi possível cadastrar a avaliação."}), 500

    finally:
        # Fecha a conexão após a operação.
        conexao.close()


# Define a rota para importar as avaliações de um arquivo CSV.
@app.route("/import/ratings", methods=["POST"])
def importar_avaliacoes():
    # Obtém o nome do usuário enviado no formulário.
    username = request.form.get("username", "").strip()

    # Obtém o arquivo CSV enviado.
    arquivo = request.files.get("file")

    # Verifica se o username foi informado.
    if not username:
        return jsonify({"erro": "Informe o username."}), 400

    # Verifica se um arquivo foi enviado.
    if arquivo is None or not arquivo.filename:
        return jsonify({"erro": "Envie um arquivo CSV."}), 400

    # Aceita somente arquivos com extensão CSV.
    if not arquivo.filename.lower().endswith(".csv"):
        return jsonify({"erro": "O arquivo deve ser CSV."}), 400

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    try:
        # Procura o usuário que receberá as avaliações.
        usuario = conexao.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        # Impede a importação para usuários inexistentes.
        if usuario is None:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        # Lê o CSV como texto e remove um possível marcador UTF-8.
        texto = io.TextIOWrapper(
            arquivo.stream,
            encoding="utf-8-sig",
            newline=""
        )

        # Interpreta a primeira linha como cabeçalho.
        leitor = csv.DictReader(texto)

        # Confere se o CSV possui as colunas necessárias.
        colunas = leitor.fieldnames or []
        if not {"Name", "Year", "Rating"}.issubset(colunas):
            return jsonify({
                "erro": "CSV incompatível. São necessárias as colunas Name, Year e Rating.",
                "colunas_encontradas": colunas
            }), 400

        # Inicializa os contadores da importação.
        importadas = 0
        ignoradas = 0

        # Processa cada linha do histórico.
        for linha in leitor:
            # Obtém o título, o ano e a nota do filme.
            titulo = (linha.get("Name") or "").strip()
            ano_texto = (linha.get("Year") or "").strip()
            nota_texto = (linha.get("Rating") or "").strip()

            # Ignora registros incompletos ou sem nota.
            if not titulo or not ano_texto or not nota_texto:
                ignoradas += 1
                continue

            try:
                # Converte o ano e a nota para números.
                ano = int(ano_texto)
                nota = float(nota_texto)

                # Valida os valores antes de salvar.
                if not 1888 <= ano <= 2100 or not 0.5 <= nota <= 5:
                    ignoradas += 1
                    continue

            except ValueError:
                # Ignora linhas com números inválidos.
                ignoradas += 1
                continue

            # Procura o filme pelo título e pelo ano.
            filme = conexao.execute(
                "SELECT id FROM films WHERE title = ? AND year = ?",
                (titulo, ano)
            ).fetchone()

            # Cadastra o filme caso ele ainda não exista.
            if filme is None:
                cursor = conexao.execute(
                    "INSERT INTO films (title, year) VALUES (?, ?)",
                    (titulo, ano)
                )
                film_id = cursor.lastrowid
            else:
                # Reutiliza o ID do filme já cadastrado.
                film_id = filme["id"]

            # Insere a avaliação ou atualiza a nota existente.
            conexao.execute("""
                INSERT INTO ratings (user_id, film_id, rating)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, film_id)
                DO UPDATE SET rating = excluded.rating
            """, (usuario["id"], film_id, nota))

            # Atualiza o total de avaliações processadas.
            importadas += 1

        # Salva as alterações no banco de dados.
        conexao.commit()

        # Retorna um resumo da importação.
        return jsonify({
            "usuario": username,
            "avaliacoes_importadas": importadas,
            "linhas_ignoradas": ignoradas
        }), 200

    except Exception:
        # Desfaz alterações se ocorrer uma falha.
        conexao.rollback()

        # Registra o erro para ajudar na investigação.
        app.logger.exception("Erro ao importar avaliações.")
        return jsonify({
            "erro": "Falha ao importar o arquivo."
        }), 500

    finally:
        # Fecha a conexão com o banco de dados.
        conexao.close()


# Inicia o servidor apenas quando o arquivo é executado diretamente.
if __name__ == "__main__":
    # Executa o servidor local em modo de desenvolvimento.
    app.run(debug=True)
