from fakepinterest.models import Usuario


def test_cadastro_email_invalido_nao_cria_usuario(client):
    client.post("/criarconta", data={
        "email": "email-invalido",
        "username": "teste",
        "senha": "123456",
        "confirmacao_senha": "123456",
    })
    assert Usuario.query.first() is None


def test_cadastro_email_duplicado(client, criar_usuario):
    criar_usuario(email="dup@exemplo.com")

    resposta = client.post("/criarconta", data={
        "email": "dup@exemplo.com",
        "username": "outro",
        "senha": "123456",
        "confirmacao_senha": "123456",
    })

    assert resposta.status_code == 200
    assert "já cadastrado" in resposta.get_data(as_text=True)
    assert Usuario.query.filter_by(username="outro").first() is None


def test_cadastro_senha_curta(client):
    client.post("/criarconta", data={
        "email": "curta@exemplo.com",
        "username": "curta",
        "senha": "123",
        "confirmacao_senha": "123",
    })
    assert Usuario.query.filter_by(email="curta@exemplo.com").first() is None


def test_cadastro_confirmacao_diferente(client):
    client.post("/criarconta", data={
        "email": "diferente@exemplo.com",
        "username": "diferente",
        "senha": "123456",
        "confirmacao_senha": "654321",
    })
    assert Usuario.query.filter_by(email="diferente@exemplo.com").first() is None


def test_login_usuario_inexistente(client):
    resposta = client.post("/", data={"email": "nao@existe.com", "senha": "123456"})

    assert resposta.status_code == 200
    assert "inexistente" in resposta.get_data(as_text=True)
