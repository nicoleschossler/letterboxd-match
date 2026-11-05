# Letterboxd Match
# Letterboxd Match 🎬

**Uma aplicação web para descobrir a compatibilidade cinematográfica entre duas pessoas a partir de suas avaliações do Letterboxd.**

## Sobre o projeto

O Letterboxd Match é um projeto em desenvolvimento que tem como objetivo importar históricos de avaliações do Letterboxd, identificar filmes avaliados por duas pessoas e calcular uma medida de compatibilidade entre suas preferências cinematográficas.

A proposta é transformar avaliações individuais em uma experiência compartilhável, com resultados persistentes e links próprios para cada combinação de usuários.

## Objetivos

- [x] Criar uma aplicação web com Flask.
- [x] Criar a estrutura inicial do banco de dados SQLite.
- [x] Armazenar usuários, filmes e avaliações.
- [x] Implementar a estrutura inicial para armazenar resultados de compatibilidade.
- [x] Criar uma interface inicial para importar históricos.
- [x] Finalizar a importação e validação de arquivos CSV.
- [ ] Implementar o algoritmo de compatibilidade.
- [ ] Criar e consultar resultados salvos.
- [ ] Gerar links compartilháveis com tokens aleatórios.
- [ ] Melhorar o tratamento de erros e os testes.
- [ ] Preparar a aplicação para implantação online.

## Tecnologias

- **Python:** linguagem principal.
- **Flask:** aplicação web e rotas HTTP.
- **SQLite:** armazenamento persistente dos dados.
- **HTML e CSS:** interface da aplicação.
- **CSV:** formato utilizado para importar avaliações exportadas do Letterboxd.
- **Git e GitHub:** versionamento e documentação do projeto.

## Como o projeto está organizado

```text
letterboxd-match/
├── app.py
├── database.py
├── letterboxd.db       # Banco local; não deve ser enviado ao GitHub
├── templates/
│   └── index.html
├── .gitignore
├── README.md
└── .venv/              # Ambiente virtual local; não deve ser versionado
```

A estrutura poderá crescer conforme novas funcionalidades forem implementadas.

## Pré-requisitos

- Python instalado.
- Git instalado para contribuir com o projeto.
- Um navegador web.
- Uma exportação de avaliações do Letterboxd em formato CSV.

## Executar localmente

No Windows, abra o PowerShell e entre na pasta do projeto:

```powershell
cd "C:\Users\seu-usuario\letterboxd-match"
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Inicie a aplicação:

```powershell
python app.py
```

Se a ativação do ambiente virtual não funcionar, execute diretamente o Python dele:

```powershell
& ".\.venv\Scripts\python.exe" ".\app.py"
```

O endereço local e as instruções para abrir a aplicação devem ser conferidos no terminal após iniciar o servidor Flask.

## Banco de dados

O arquivo `database.py` contém as funções de conexão e criação das tabelas.

O banco utiliza SQLite e possui as seguintes entidades:

- `users`: usuários identificados por nome de usuário.
- `films`: catálogo de filmes.
- `ratings`: avaliações associadas a usuários e filmes.
- `matches`: resultados de compatibilidade, pontuação, token e data de criação.

A tabela `matches` prepara o armazenamento persistente dos resultados. O cálculo e o fluxo completo de compartilhamento ainda precisam ser finalizados e testados.

## Privacidade e segurança

- O banco local contém dados pessoais de uso e avaliações.
- Arquivos CSV exportados podem conter históricos pessoais e não devem ser publicados.
- Tokens de compartilhamento devem ser aleatórios e difíceis de adivinhar.
- Chaves, senhas e variáveis de ambiente privadas não devem ser versionadas.
- O projeto deve ser revisado antes de ser publicado ou implantado online.

## Próximas etapas

1. Validar o formato e o conteúdo dos CSVs importados.
2. Garantir que a importação não duplique avaliações.
3. Implementar o cálculo de compatibilidade entre filmes avaliados em comum.
4. Persistir e recuperar os resultados pelo token.
5. Criar testes automatizados para importação, cálculo e compartilhamento.
6. Melhorar a experiência de uso e o tratamento de erros.
7. Documentar a instalação em outro computador e a implantação online.

## Status

**Em desenvolvimento.**

Este repositório documenta a implementação incremental do Letterboxd Match. As funcionalidades listadas como pendentes ainda precisam ser implementadas e verificadas.

## Licença

A licença do projeto ainda não foi definida.
