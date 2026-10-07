from fakepinterest.models import Usuario


def test_homepage_ok(client):
    resposta = client.get("/")
    assert resposta.status_code == 200


def test_criarconta_ok(client):
    resposta = client.get("/criarconta")
    assert resposta.status_code == 200


def test_feed_exige_login(client):
    resposta = client.get("/feed")
    assert resposta.status_code == 302


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

    resposta_feed = client.get("/feed")
    assert resposta_feed.status_code == 200
