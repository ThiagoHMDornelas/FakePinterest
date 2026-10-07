from fakepinterest import app, database
from fakepinterest.models import Foto, Usuario  # noqa: F401 (registra os modelos)

# Cria as tabelas do banco de dados (idempotente)
with app.app_context():
    database.create_all()

print("Banco de dados criado com sucesso.")
