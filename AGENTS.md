# AGENTS.md — FakePinterest

Clone simplificado do Pinterest em **Flask**: cadastro/login, feed de imagens e upload de fotos. Flask 3.1.1 · Flask-SQLAlchemy 3.1.1 (SQLAlchemy 2.0.41) · Flask-Login 0.6.3 · Flask-Bcrypt 1.0.1 · Flask-WTF 1.2.2 · gunicorn · python-dotenv · Python 3.12 · SQLite ou PostgreSQL · Docker (porta host 8011 → container 5000).

## Contexto em camadas
`SOUL.md` (regras globais do agente) → `AGENTS.md` da pasta da linguagem (regras comuns) → este arquivo (particularidades do projeto). Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Arquitetura

- **Sem app factory**: `fakepinterest/__init__.py` cria módulo global `app` + extensões globais (`database`, `bcrypt`, `login_manager`) — não usa padrão `create_app()`.
- **Rotas na importação**: `routes.py` registra decoradores `@app.route` no import no fim de `__init__.py` (`import fakepinterest.routes`) — novo arquivo de rotas precisa ser importado lá.
- **Entrypoint**: `main.py` chama `app.run(debug=IS_ONLINE)` — com `IS_ONLINE=true`, **debug fica ligado em produção** (sobe via gunicorn no Docker; avaliar antes de mudar).
- **Config em `__init__.py`**: `SECRET_KEY` (fallback de dev), `SQLALCHEMY_DATABASE_URI` (fallback SQLite), `UPLOAD_FOLDER = static/fotos_posts`, `EXTENSOES_PERMITIDAS` (png/jpg/jpeg/gif), `MAX_CONTENT_LENGTH` 4 MB, `ITENS_POR_PAGINA` 12.
- **Login**: `login_manager.login_view = 'homepage'` (login é a própria homepage `homepage()`; token em sessão Flask).

### Estrutura

| Arquivo/pasta | Finalidade | Particularidades |
|---|---|---|
| `main.py` | Entrypoint | `IS_ONLINE` controla `debug` |
| `cria_banco.py` | Criação de tabelas | `database.create_all()` idempotente; rodar **no start do container** antes do gunicorn |
| `fakepinterest/__init__.py` | App + config + extensões | Sem factory; global |
| `fakepinterest/models.py` | `Usuario`, `Foto` | `Usuario(UserMixin)`: username, email (unique), senha (hash bcrypt); `Foto`: imagem (nome do arquivo), `data_criacao` (timezone `America/Sao_Paulo`), FK `usuario.id` |
| `fakepinterest/forms.py` | WTForms | `FormLogin` (valida e-mail existente), `FormCriarConta` (e-mail único, senha 6-20 + EqualTo), `FormFoto` (FileField `FileAllowed` + accept image/*) |
| `fakepinterest/routes.py` | Rotas | `/` (login), `/criarconta`, `/perfil/<id>` (upload se dono), `/feed` (paginado), `/logout` |
| `fakepinterest/templates/` + `static/` | Templates e uploads | Uploads em `static/fotos_posts` (nome com `uuid4().hex` para não sobrescrever) |
| `tests/` + `pytest.ini` | pytest | `pythonpath = .`, `testpaths = tests` |

## Comportamentos não óbvios

- **Upload em `/perfil`**: só o dono do perfil vê o `FormFoto`; visão de terceiro (`perfil/<outra_id>`) renderiza sem form. Validação em duas camadas: `FileAllowed` no form + re-check de extensão na rota, com mensagens de erro exibidas no próprio form.
- **Hash de senha**: gerar com `bcrypt.generate_password_hash(...).decode('utf-8')` e conferir com `check_password_hash(usuario.senha.encode('utf-8'), ...)` (coluna guarda string; o `.encode` é obrigatório).
- **Paginação do feed**: `database.paginate(select(...) , per_page=ITENS_POR_PAGINA, error_out=False)`, ordenado por `-data_criacao`.
- **Erro 413**: handler customizado renderiza `413.html` quando o upload excede 4 MB.
- **Utilitários do curso**: `Cria_Banco_Flask.py` e `teste.py` na raiz são scripts auxiliares, não fazem parte do fluxo da aplicação.

## Testes e lint

- Suíte obrigatória antes de entregar: **`pytest -q`** (exatamente como no CI; runner é pytest, não unittest) e **`flake8 .`**.
- CI (`.github/workflows/tests.yml`): roda `flake8 .` e `pytest -q` em Python 3.12, sem `DATABASE_URL` específica (conftest sobrescreve via `os.environ` antes de importar o app). Fixtures de `tests/conftest.py`:
  - `client` — `test_client` com `WTF_CSRF_ENABLED=False`, banco de teste (`test_comunidade.db`) drop/create a cada teste.
  - `sessao` — sessão SQLAlchemy para testes de modelo.
  - `criar_usuario` / `usuario_logado` — helpers de factory/login.

## Banco de dados

`DATABASE_URL` no `.env`: `sqlite:///comunidade.db` (padrão) ou `postgresql://...:/5432/fakepinterest` (psycopg2-binary já instalado). Sem migrations — mudança de modelo = alterar + recriar tabelas.

## Variáveis de ambiente (.env.example)

`SECRET_KEY` (obrigatória para sessão/CSRF), `IS_ONLINE` (`false` dev / `true` produção), `DATABASE_URL`.

## Docker

Compose sobe `cria_banco` + gunicorn (`-w 2 -b 0.0.0.0:5000 main:app`), com porta do host **8011**.

- Compose força `SECRET_KEY`, `DATABASE_URL` → SQLite e `IS_ONLINE=false`.
- SQLite no container é gravado no sistema de arquivos do container (não montado em volume persistente).

## Convenções

- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
