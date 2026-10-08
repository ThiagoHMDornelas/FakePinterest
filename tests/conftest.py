import os

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "sqlite:///test_comunidade.db"

import pytest  # noqa: E402

from fakepinterest import app, bcrypt, database  # noqa: E402
from fakepinterest.models import Usuario  # noqa: E402


@pytest.fixture
def client(tmp_path):
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        UPLOAD_FOLDER=str(tmp_path / "uploads"),
    )
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        database.drop_all()
        database.create_all()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        database.drop_all()


@pytest.fixture
def sessao(tmp_path):
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        UPLOAD_FOLDER=str(tmp_path / "uploads"),
    )
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        database.drop_all()
        database.create_all()
        yield database.session
        database.session.remove()
        database.drop_all()


@pytest.fixture
def criar_usuario(client):
    def _criar(email="teste@teste.com", username="teste", senha="123456"):
        with app.app_context():
            hash_senha = bcrypt.generate_password_hash(senha).decode("utf-8")
            usuario = Usuario(username=username, email=email, senha=hash_senha)
            database.session.add(usuario)
            database.session.commit()
            return usuario.id

    return _criar


@pytest.fixture
def usuario_logado(criar_usuario, client):
    usuario_id = criar_usuario()
    client.post("/", data={"email": "teste@teste.com", "senha": "123456"})
    return usuario_id
