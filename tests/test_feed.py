from fakepinterest import app, database
from fakepinterest.models import Foto

ITENS_POR_PAGINA = app.config["ITENS_POR_PAGINA"]


def _criar_fotos(usuario_id, quantidade):
    with app.app_context():
        for _ in range(quantidade):
            database.session.add(Foto(id_usuario=usuario_id))
        database.session.commit()


def test_feed_lista_fotos(client, usuario_logado):
    _criar_fotos(usuario_logado, 3)

    corpo = client.get("/feed").get_data(as_text=True)
    assert corpo.count("bloco-imagem") == 3


def test_feed_respeita_itens_por_pagina(client, usuario_logado):
    _criar_fotos(usuario_logado, ITENS_POR_PAGINA + 3)

    corpo = client.get("/feed").get_data(as_text=True)
    assert corpo.count("bloco-imagem") == ITENS_POR_PAGINA


def test_feed_segunda_pagina(client, usuario_logado):
    _criar_fotos(usuario_logado, ITENS_POR_PAGINA + 3)

    corpo = client.get("/feed?page=2").get_data(as_text=True)
    assert corpo.count("bloco-imagem") == 3


def test_feed_pagina_inexistente_nao_quebra(client, usuario_logado):
    _criar_fotos(usuario_logado, 3)

    assert client.get("/feed?page=99").status_code == 200
