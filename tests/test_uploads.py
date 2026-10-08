import io

from fakepinterest.models import Foto


def test_upload_imagem_valida(client, usuario_logado):
    dados = {
        "foto": (io.BytesIO(b"conteudo-de-imagem"), "minha-foto.png"),
        "botao_confirmacao": "Enviar Foto",
    }

    resposta = client.post(
        f"/perfil/{usuario_logado}",
        data=dados,
        content_type="multipart/form-data",
    )

    assert resposta.status_code == 302
    foto = Foto.query.first()
    assert foto is not None
    assert foto.imagem.endswith(".png")
    assert foto.id_usuario == usuario_logado


def test_upload_extensao_invalida(client, usuario_logado):
    dados = {
        "foto": (io.BytesIO(b"conteudo"), "arquivo.exe"),
        "botao_confirmacao": "Enviar Foto",
    }

    resposta = client.post(
        f"/perfil/{usuario_logado}",
        data=dados,
        content_type="multipart/form-data",
    )

    assert resposta.status_code == 200
    assert "apenas imagens" in resposta.get_data(as_text=True)
    assert Foto.query.count() == 0


def test_upload_arquivo_muito_grande(client, usuario_logado):
    grande = io.BytesIO(b"0" * (5 * 1024 * 1024))
    dados = {"foto": (grande, "grande.png")}

    resposta = client.post(
        f"/perfil/{usuario_logado}",
        data=dados,
        content_type="multipart/form-data",
    )

    assert resposta.status_code == 413
