# AGENTS.md — FakePinterest

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
Clone simplificado do Pinterest em **Flask**: cadastro/login, feed de imagens e persistência via SQLAlchemy.

**Stack:** Flask 3.1 · Flask-Login · Flask-Bcrypt · Flask-WTF · SQLAlchemy/Flask-SQLAlchemy · psycopg2 · python-dotenv · gunicorn · Python 3.12 · SQLite ou PostgreSQL · Docker

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `main.py` — aplicação Flask (factory/entrypoint)
- `fakepinterest/` — pacote com rotas, modelos, formulários e templates
- `cria_banco.py` — criação inicial do banco (executado no start do container)
- `tests/`, `pytest.ini`, `docs/`

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env
python cria_banco.py
python main.py            # ou: flask --app main run
```

## Testes e lint
```bash
pytest -q
flake8 .
```

## Particularidades
- Banco pela `DATABASE_URL` (padrão SQLite no `.env.example`; PostgreSQL comentado).
- `IS_ONLINE` alterna o comportamento de ambiente; `SECRET_KEY` é obrigatória para sessões/CSRF.
- Senhas via Flask-Bcrypt — nunca comparar texto puro.
- Gunicorn serve `main:app` na porta 5000.

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
