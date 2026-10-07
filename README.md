# FakePinterest

> Projeto desenvolvido com base no curso **Hashtag Treinamentos**.

![Testes](https://github.com/ThiagoHMDornelas/FakePinterest/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.1-000000)
![License](https://img.shields.io/badge/license-MIT-green)

Rede social de compartilhamento de imagens inspirada no Pinterest, desenvolvida com Flask. Usuários podem criar conta, fazer login, enviar fotos para o próprio perfil e visualizar as imagens de todos no feed.

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Bancos de dados](#bancos-de-dados)
- [Executar com Docker](#executar-com-docker)
- [Testes](#testes)
- [Principais rotas](#principais-rotas)
- [Licença](#licença)

## Visão geral

O **FakePinterest** é uma aplicação web de compartilhamento de imagens construída com Flask (templates Jinja2 e rotas organizadas em um pacote). O visitante cria uma conta, faz login e envia fotos para o próprio perfil; a página de feed reúne as imagens publicadas por todos os usuários. A autenticação usa Flask-Login e as senhas são armazenadas com hash (Flask-Bcrypt).

## Funcionalidades

- Cadastro de usuário (com validação de e-mail e confirmação de senha)
- Login e logout
- Upload de fotos no perfil do usuário
- Página de perfil com as fotos do usuário
- Feed com as fotos de todos os usuários (mais recentes primeiro)
- Proteção de rotas para usuários autenticados

## Tecnologias

- Python
- Flask 3.1
- Flask-SQLAlchemy (ORM)
- Flask-Login (autenticação)
- Flask-WTF (formulários e CSRF)
- Flask-Bcrypt (hash de senha)
- python-dotenv (variáveis de ambiente)
- SQLite e PostgreSQL
- Gunicorn (produção)
- Docker e Docker Compose
- flake8 e pytest (desenvolvimento)
- GitHub Actions (CI)

## Estrutura do projeto

```
FakePinterest/
├── fakepinterest/        # pacote da aplicação (app, models, forms, routes)
│   ├── static/           # css e imagens
│   └── templates/        # templates Jinja2
├── tests/                # testes automatizados (pytest)
├── .github/workflows/    # pipeline de CI (GitHub Actions)
├── cria_banco.py         # cria as tabelas do banco de dados
├── main.py               # ponto de entrada da aplicação
├── pytest.ini            # configuração do pytest
├── Dockerfile
├── docker-compose.yml
├── .env.example          # exemplo de variáveis de ambiente
├── requirements.txt
└── requirements_dev.txt
```

## Instalação e execução

Pré-requisitos:

- Python 3.11 ou superior instalado

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint e testes), instale também:

    pip install -r requirements_dev.txt

Crie o arquivo de variáveis de ambiente a partir do exemplo:

    copy .env.example .env

No Linux ou macOS:

    cp .env.example .env

Crie as tabelas do banco de dados:

    python cria_banco.py

Inicie o servidor:

    python main.py

A aplicação estará disponível em:

    http://127.0.0.1:5000/

## Variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste os valores:

    # Flask
    SECRET_KEY=troque-por-uma-chave-secreta
    IS_ONLINE=false

    # Banco de dados ativo: SQLite (padrão) ou PostgreSQL
    DATABASE_URL=sqlite:///comunidade.db
    # DATABASE_URL=postgresql://postgres:senha@localhost:5432/fakepinterest

- `SECRET_KEY` → chave usada pelo Flask para sessões e proteção CSRF.
- `IS_ONLINE` → quando `true`, sobe o servidor em modo de desenvolvimento (debug/auto-reload).
- `DATABASE_URL` → string de conexão do banco (SQLite por padrão).

## Bancos de dados

O projeto pode rodar com dois bancos, definidos pela variável `DATABASE_URL` no `.env`:

- `sqlite:///comunidade.db` → SQLite (criado em `instance/comunidade.db`)
- `postgresql://usuario:senha@host:5432/banco` → PostgreSQL

As tabelas são criadas pelo script `cria_banco.py`.

## Executar com Docker

A forma recomendada de rodar a aplicação. O Docker Compose sobe o serviço já configurado (Flask + Gunicorn + SQLite), sem precisar montar o ambiente Python manualmente.

**Pré-requisitos:**

- Docker Desktop instalado e em execução (engine)
- Docker Compose (já vem com o Docker Desktop)
- Git instalado (para clonar o repositório)
- A porta `5000` livre

> **Importante:** o Docker Desktop sozinho **não** faz o setup inicial — ele é o *engine* e o painel de gerenciamento. Clonar o repositório e rodar `docker compose up --build` são feitos pelo **terminal**; o Docker Desktop é ótimo para acompanhar logs, iniciar/parar e abrir um terminal dentro do container **depois** que a stack subiu.

> O Docker **não** precisa do arquivo `.env`: as variáveis já vêm definidas no `docker-compose.yml`. O `.env.example` é usado apenas na execução local (fora do Docker).

### Passo a passo (via shell / PowerShell)

**1. Clone o repositório**

```powershell
git clone https://github.com/ThiagoHMDornelas/FakePinterest.git
cd FakePinterest
```

> O `git clone` cria a pasta `FakePinterest` dentro da pasta atual, e o `cd` entra nela. Se você **já está dentro** da pasta do projeto, **pule o `cd`**.

**2. Suba a stack.** Na primeira execução o Docker compila a imagem do projeto — pode levar alguns minutos:

```powershell
docker compose up --build -d
```

**3. Confira os containers:**

```powershell
docker compose ps
```

Espere o serviço `web` como `Up`.

| Serviço | Porta | Acesso |
|---|---|---|
| `web` | 5000 | `http://localhost:5000` |

**4. Acesse a aplicação:**

- Aplicação: `http://localhost:5000/`

O banco e as tabelas são criados automaticamente na inicialização. Não há superusuário: crie sua conta pela tela **Criar conta**.

**5. Comandos úteis:**

```powershell
docker compose logs -f web     # logs da aplicação
docker compose restart web     # reinicia a aplicação
docker compose down            # para e remove os containers
```

> O banco SQLite é criado dentro do container, então os dados **não persistem** após um `docker compose down`.

### Usando o Docker Desktop (interface gráfica)

Depois que a stack estiver no ar (passo 2), o Docker Desktop ajuda a operar. Na aba **Containers** você verá o serviço `web`:

- **Logs**: clique no container → aba *Logs* (equivale a `docker compose logs`).
- **Start / Stop / Restart**: botões no topo do container.
- **Terminal no container**: botão *Exec* (útil para depurar dentro do container).
- **Abrir no navegador**: clique na porta publicada (`5000:5000`).

O que **não** dá para fazer pela interface gráfica: clonar o repositório e rodar `docker compose up --build` em um clone novo (isso é feito pelo terminal).

### Problemas comuns

- **A aplicação não abre**
  - Veja os logs: `docker compose logs -f web`
  - Confirme que o container está `Up`: `docker compose ps`
- **Erro de porta em uso** (`5000`) → pare o serviço que ocupa a porta ou ajuste o mapeamento no `docker-compose.yml` (ex.: `5001:5000`) e acesse em `http://localhost:5001`
- **Os dados sumiram após reiniciar** → é esperado: o SQLite fica dentro do container e não persiste após um `docker compose down`

## Testes

A suíte de testes cobre as rotas principais (homepage, cadastro, feed e proteção de acesso). Execute:

    pytest

A suíte também roda automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`, que roda flake8 + pytest), e o resultado é exibido no badge no topo deste README.

## Principais rotas

| Método | Rota | Descrição |
|---|---|---|
| GET/POST | `/` | Login (homepage) |
| GET/POST | `/criarconta` | Cadastro de usuário |
| GET/POST | `/perfil/<id_usuario>` | Perfil do usuário (upload de fotos, requer login) |
| GET | `/feed` | Feed com as fotos de todos (requer login) |
| GET | `/logout` | Logout (requer login) |

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
