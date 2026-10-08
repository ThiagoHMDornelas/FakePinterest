from fakepinterest.models import Usuario


def test_homepage_ok(client):
    assert client.get("/").status_code == 200


def test_criarconta_ok(client):
    assert client.get("/criarconta").status_code == 200


def test_feed_exige_login(client):
    assert client.get("/feed").status_code == 302


def test_perfil_exige_login(client):
    assert client.get("/perfil/1").status_code == 302


def test_logout_exige_login(client):
    assert client.get("/logout").status_code == 302


def test_registrar_usuario_e_acessar_feed(client):
    resposta = client.post(
        "/criarconta",
        data={
            "email": "teste@teste.com",
            "username": "teste",
            "senha": "123456",
            "confirmacao_senha": "123456",
        },
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert Usuario.query.filter_by(email="teste@teste.com").first() is not None
    assert client.get("/feed").status_code == 200


def test_login_com_sucesso(client, criar_usuario):
    criar_usuario(email="login@teste.com", senha="123456")

    resposta = client.post("/", data={"email": "login@teste.com", "senha": "123456"})

    assert resposta.status_code == 302
    assert "/perfil/" in resposta.headers["Location"]


def test_login_senha_incorreta(client, criar_usuario):
    criar_usuario(email="errada@teste.com", senha="123456")

    resposta = client.post("/", data={"email": "errada@teste.com", "senha": "senha-errada"})

    assert resposta.status_code == 200


def test_logout(client, usuario_logado):
    resposta = client.get("/logout")

    assert resposta.status_code == 302
